# Miʿyar code library — labour indicators from LFS microdata (ICLS-19), R version
# Same derivations as code/python/miyar_lfs.py; standard errors with the `survey` package
# (svydesign(ids = ~psu, strata = ~stratum, weights = ~weight): PSUs with replacement, Taylor linearisation).
#
# Usage:  Rscript code/r/miyar_lfs.R DATA.csv [country] [out.json]
#   country = a Miʿyar preset (jor, sau, mar, are, aus, usa, ilo) or "none" for ILO defaults.
# Standards: ILO 19th ICLS resolution (2013, amended 2023) §27, §47, §73. Licence: MIT.
# Packages: install.packages(c("survey", "jsonlite"))

suppressPackageStartupMessages({ library(survey); library(jsonlite) })
options(survey.lonely.psu = "certainty")

presets_path <- function() {
  args <- commandArgs(trailingOnly = FALSE)
  me <- sub("^--file=", "", args[grep("^--file=", args)])
  base <- if (length(me)) dirname(normalizePath(me)) else "code/r"
  file.path(base, "..", "presets", "countries.json")
}

params_for <- function(iso = NULL) {
  pr <- fromJSON(presets_path(), simplifyVector = FALSE)
  d <- pr[["_default_ilo"]]
  p <- list(age_min = d$age_min, search_days = d$search_days, availability_days = d$availability_days,
            future_starters = d$future_starters, hours_threshold = d$hours_threshold, youth = c(15, 24))
  if (!is.null(iso) && iso != "none") {
    c <- pr[[iso]]
    if (is.null(c)) stop("No Miʿyar preset for ", iso)
    for (k in c("age_min", "search_days", "availability_days")) if (!is.null(c[[k]])) p[[k]] <- c[[k]]
  }
  p
}

flag <- function(v) { v <- suppressWarnings(as.numeric(v)); !is.na(v) & v == 1 }

derive <- function(d, p) {
  age <- as.numeric(d$age)
  wap <- age >= p$age_min
  employed <- wap & (flag(d$worked_1h) | flag(d$temp_absent))
  sd <- suppressWarnings(as.numeric(d$searched_days)); av <- suppressWarnings(as.numeric(d$available_days))
  searched <- !is.na(sd) & sd <= p$search_days
  available <- !is.na(av) & av <= p$availability_days
  future <- if (isTRUE(p$future_starters)) flag(d$future_starter) else rep(FALSE, nrow(d))
  unemployed <- wap & !employed & available & (searched | future)
  plf <- wap & !employed & !unemployed & ((searched & !available) | (!searched & available & flag(d$wants_work)))
  hours <- suppressWarnings(as.numeric(d$hours_usual))
  tru <- employed & !is.na(hours) & hours < p$hours_threshold & flag(d$wants_more_hours) & flag(d$available_more_hours)
  youth <- age >= p$youth[1] & age <= p$youth[2]
  neet <- youth & !employed & !flag(d$in_education) & !flag(d$in_training)
  lf <- employed | unemployed
  new <- list(wap = wap, employed = employed, unemployed = unemployed, lf = lf, plf = plf, tru = tru,
              youth = youth & wap, neet = neet, youth_lf = youth & lf, youth_unemployed = youth & unemployed,
              tru_or_u = tru | unemployed, u_or_plf = unemployed | plf, elf = lf | plf, tru_u_plf = tru | unemployed | plf)
  for (k in names(new)) d[[k]] <- as.integer(new[[k]])
  d
}

INDICATORS <- list(lfpr = c("lf", "wap"), epr = c("employed", "wap"), lu1 = c("unemployed", "lf"),
                   lu2 = c("tru_or_u", "lf"), lu3 = c("u_or_plf", "elf"), lu4 = c("tru_u_plf", "elf"),
                   yur = c("youth_unemployed", "youth_lf"), neet = c("neet", "youth"))

one <- function(des, num, den) {
  r <- svyratio(as.formula(paste0("~", num)), as.formula(paste0("~", den)), des)
  est <- as.numeric(coef(r)); se <- as.numeric(SE(r))
  list(estimate = round(100 * est, 4), se = round(100 * se, 4),
       ci95 = round(100 * c(est - qnorm(0.975) * se, est + qnorm(0.975) * se), 4))
}

indicators <- function(d, by = NULL) {
  des <- svydesign(ids = ~psu, strata = ~stratum, weights = ~weight, data = d)
  out <- list(total = lapply(INDICATORS, function(x) one(des, x[1], x[2])))
  if (!is.null(by)) for (g in sort(unique(d[[by]]))) {
    sub <- subset(des, d[[by]] == g)
    out[[paste0(by, "=", g)]] <- lapply(INDICATORS, function(x) one(sub, x[1], x[2]))
  }
  out
}

main <- function() {
  a <- commandArgs(trailingOnly = TRUE)
  data <- if (length(a) >= 1) a[1] else "code/data/synthetic_lfs.csv"
  iso <- if (length(a) >= 2) a[2] else "none"
  out <- if (length(a) >= 3) a[3] else NULL
  raw <- read.csv(data, comment.char = "#")
  res <- list(
    ilo_default = indicators(derive(raw, params_for("none")))$total,
    jor = indicators(derive(raw, params_for("jor")), by = "sex"))
  if (iso != "none") res$requested <- indicators(derive(raw, params_for(iso)))
  for (k in names(res$ilo_default)) cat(sprintf("%-6s %8.2f  SE %6.2f\n", k, res$ilo_default[[k]]$estimate, res$ilo_default[[k]]$se))
  if (!is.null(out)) write_json(res, out, auto_unbox = TRUE, digits = 10, pretty = TRUE)
}

if (sys.nframe() == 0) main()
