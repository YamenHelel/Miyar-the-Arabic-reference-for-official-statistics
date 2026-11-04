* =============================================================================
* Miʿyar code library — labour indicators from LFS microdata (ICLS-19), Stata version
* STATUS: NOT EXECUTED. Written to mirror code/python/miyar_lfs.py and reviewed by reading;
*         the Python and R versions are tested. Please report any problem (GitHub issue).
* Standards: ILO 19th ICLS resolution (2013, amended 2023) §27, §47, §73. Licence: MIT.
* Standard errors: svyset psu [pw=weight], strata(stratum)  -> Taylor linearisation, PSUs with replacement.
* =============================================================================
version 15
clear all
set more off

* ---- parameters: replace with the values of your country (see code/presets/countries.json) ----
local age_min            15      // minimum age of the working-age population
local search_days        28      // job search in the last N days (ICLS-19 §47(b))
local availability_days  14      // available within N days after the reference week (§47(d)(i))
local future_starters    1       // 1 = available future starters count as unemployed
local hours_threshold    35      // time-related underemployment threshold (national choice)
local youth_min          15
local youth_max          24

* ---- data: the CSV starts with one comment line, so variable names are on line 2 ----
import delimited "code/data/synthetic_lfs.csv", varnames(2) rowrange(3) clear
destring searched_days available_days hours_usual, replace force

* ---- ICLS-19 labour force status ----
gen byte wap        = age >= `age_min'
gen byte employed   = wap & (worked_1h == 1 | temp_absent == 1)
gen byte searched   = !missing(searched_days) & searched_days <= `search_days'
gen byte available  = !missing(available_days) & available_days <= `availability_days'
gen byte future     = (`future_starters' == 1) & future_starter == 1
gen byte unemployed = wap & !employed & available & (searched | future)
gen byte lf         = employed | unemployed
gen byte plf        = wap & !employed & !unemployed & ((searched & !available) | (!searched & available & wants_work == 1))
gen byte tru        = employed & !missing(hours_usual) & hours_usual < `hours_threshold' & wants_more_hours == 1 & available_more_hours == 1
gen byte youth      = inrange(age, `youth_min', `youth_max')
gen byte neet       = youth & !employed & in_education != 1 & in_training != 1
gen byte youth_lf   = youth & lf
gen byte youth_unemployed = youth & unemployed
gen byte tru_or_u   = tru | unemployed
gen byte u_or_plf   = unemployed | plf
gen byte elf        = lf | plf
gen byte tru_u_plf  = tru | unemployed | plf

* ---- design and indicators (ratios x 100) ----
svyset psu [pweight = weight], strata(stratum) singleunit(certainty)
svy: ratio (lfpr: lf/wap) (epr: employed/wap) (lu1: unemployed/lf) (lu2: tru_or_u/lf) ///
           (lu3: u_or_plf/elf) (lu4: tru_u_plf/elf) (yur: youth_unemployed/youth_lf) (neet: neet/youth)
* multiply estimates and SEs by 100 to read them as percentages; disaggregate with: svy, over(sex): ratio ...
