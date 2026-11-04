/* Miʿyar — site behaviour. Everything works without this file; it only adds motion and tools. */
(function () {
  document.documentElement.classList.add("js");
  var root = document.documentElement.getAttribute("data-root") || "./";
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- entrances: each [data-in] group rises once, children staggered ---- */
  var groups = document.querySelectorAll("[data-in]");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -10% 0px" });
    groups.forEach(function (g) { io.observe(g); });
  } else { groups.forEach(function (g) { g.classList.add("in"); }); }

  /* ---- Arabic-aware search over search.json ---- */
  function norm(s) {
    return (s || "").toLowerCase()
      .replace(/[ً-ْٰـ]/g, "")      // harakat, dagger alef, tatweel
      .replace(/[إأآٱ]/g, "ا").replace(/ى/g, "ي").replace(/ة/g, "ه").replace(/ؤ/g, "و").replace(/ئ/g, "ي")
      .replace(/[«»"'()،,.:؛]/g, " ").replace(/\s+/g, " ").trim();
  }
  var input = document.getElementById("q"), list = document.getElementById("q-results"), index = null;
  function load() {
    if (index) return Promise.resolve(index);
    return fetch(root + "search.json").then(function (r) { return r.json(); }).then(function (d) {
      index = d.map(function (x) { x.n = norm(x.t + " " + (x.k || "")); return x; }); return index;
    });
  }
  function show(items) {
    list.innerHTML = "";
    if (!items.length) { list.hidden = true; return; }
    items.slice(0, 8).forEach(function (x) {
      var li = document.createElement("li"), a = document.createElement("a"), s = document.createElement("small");
      a.href = root + x.u; a.textContent = x.t; s.textContent = x.c; a.appendChild(s); li.appendChild(a); list.appendChild(li);
    });
    list.hidden = false;
  }
  if (input && list) {
    input.addEventListener("focus", load);
    input.addEventListener("input", function () {
      var q = norm(input.value);
      if (q.length < 2) { show([]); return; }
      load().then(function (ix) {
        var words = q.split(" ");
        show(ix.filter(function (x) { return words.every(function (w) { return x.n.indexOf(w) > -1; }); }));
      }).catch(function () { show([]); });
    });
    input.addEventListener("keydown", function (e) { if (e.key === "Escape") { input.value = ""; show([]); } });
    document.addEventListener("click", function (e) { if (!e.target.closest(".search")) list.hidden = true; });
  }

  /* ---- the ruler: one criterion, ten countries, numbers from verified texts ---- */
  var rul = document.getElementById("ruler");
  if (rul) {
    var data = JSON.parse(document.getElementById("ruler-data").textContent);
    var marks = rul.querySelector(".ruler-marks"), track = rul.querySelector(".ruler-track"),
        ticks = rul.querySelector(".ruler-ticks"), note = rul.querySelector(".ruler-note");
    function draw(key) {
      var c = data.criteria[key], span = c.max - c.min;
      track.innerHTML = ""; ticks.innerHTML = ""; marks.innerHTML = "";
      for (var v = c.min; v <= c.max; v += c.step) {
        var i = document.createElement("i"); if ((v - c.min) % c.major === 0) i.className = "major"; track.appendChild(i);
        if ((v - c.min) % c.major === 0) { var t = document.createElement("span"); t.textContent = v; ticks.appendChild(t); }
      }
      var at = {};
      data.countries.forEach(function (k) {
        var val = k[key];
        if (val === null || val === undefined) return;
        (at[val] = at[val] || []).push(k.name);
      });
      Object.keys(at).map(Number).sort(function (x, y) { return x - y; }).forEach(function (val, k) {
        var m = document.createElement("div"); m.className = "ruler-mark";
        var pos = (val - c.min) / span * 100;
        m.style.right = pos + "%";
        var lab = document.createElement("span"); lab.textContent = at[val].join("، ");
        var bar = document.createElement("i"); bar.style.height = (18 + (k % 3) * 46) + "px";
        var num = document.createElement("b"); num.textContent = val + " " + c.unit;
        m.appendChild(lab); m.appendChild(num); m.appendChild(bar); marks.appendChild(m);
      });
      var missing = data.countries.filter(function (k) { return k[key] === null || k[key] === undefined; }).map(function (k) { return k.name; });
      note.textContent = c.note + (missing.length ? " لم يُذكر الرقم في النص المنسوخ لـ: " + missing.join("، ") + "." : "");
    }
    rul.querySelectorAll(".ruler-ctl button").forEach(function (b) {
      b.addEventListener("click", function () {
        rul.querySelectorAll(".ruler-ctl button").forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
        draw(b.dataset.k);
      });
    });
    draw(rul.querySelector('.ruler-ctl button[aria-pressed="true"]').dataset.k);
  }

  /* ---- drag row: arrows + progress ---- */
  document.querySelectorAll("[data-row]").forEach(function (sec) {
    var row = sec.querySelector(".moments"), bar = sec.querySelector(".progress i");
    function upd() { var max = row.scrollWidth - row.clientWidth; var p = max > 0 ? Math.abs(row.scrollLeft) / max : 1; bar.style.width = Math.max(12, p * 100) + "%"; }
    row.addEventListener("scroll", upd, { passive: true }); upd();
    sec.querySelectorAll("[data-dir]").forEach(function (b) {
      b.addEventListener("click", function () { row.scrollBy({ left: Number(b.dataset.dir) * 332, behavior: reduce ? "auto" : "smooth" }); });
    });
  });

  /* ---- index with preview (glossary sheet): pointing at a term shows its definition in one frame ---- */
  var frame = document.querySelector(".preview-frame");
  if (frame && window.matchMedia("(hover: hover)").matches) {
    document.querySelectorAll("[data-preview]").forEach(function (a) {
      a.addEventListener("mouseenter", function () {
        frame.querySelector("b").textContent = a.dataset.name; frame.querySelector("p").textContent = a.dataset.preview; frame.classList.add("on");
      });
      a.addEventListener("mouseleave", function () { frame.classList.remove("on"); });
    });
  }


  /* ---- «احسب بنفسك»: descriptive statistics calculator (deterministic, shows formulas) ---- */
  var calc = document.getElementById("calc-form");
  if (calc) {
    var toNum = function (s) {
      return (s || "").replace(/[٠-٩]/g, function (d) { return "٠١٢٣٤٥٦٧٨٩".indexOf(d); })
        .replace(/٫/g, ".").split(/[\s,،;؛]+/).filter(function (x) { return x !== ""; }).map(Number);
    };
    var fmt = function (v) { return isFinite(v) ? (Math.round(v * 1000) / 1000).toLocaleString("en-US", { maximumFractionDigits: 3 }) : "—"; };
    var quant = function (s, p) { var h = (s.length - 1) * p, lo = Math.floor(h), hi = Math.ceil(h); return s[lo] + (s[hi] - s[lo]) * (h - lo); };
    window.miyarStats = function (x, w) {
      var n = x.length, s = x.slice().sort(function (a, b) { return a - b; });
      var sum = x.reduce(function (a, b) { return a + b; }, 0), mean = sum / n;
      var ss = x.reduce(function (a, b) { return a + (b - mean) * (b - mean); }, 0);
      var freq = {}, best = 0; x.forEach(function (v) { freq[v] = (freq[v] || 0) + 1; best = Math.max(best, freq[v]); });
      var modes = best > 1 ? Object.keys(freq).filter(function (k) { return freq[k] === best; }).map(Number).sort(function (a, b) { return a - b; }) : [];
      var q1 = quant(s, .25), q3 = quant(s, .75), iqr = q3 - q1;
      var wm = null;
      if (w && w.length === n) { var sw = w.reduce(function (a, b) { return a + b; }, 0); wm = x.reduce(function (a, v, i) { return a + v * w[i]; }, 0) / sw; }
      return { n: n, sum: sum, mean: mean, wmean: wm, median: quant(s, .5), modes: modes, min: s[0], max: s[n - 1], range: s[n - 1] - s[0],
               varp: ss / n, vars: n > 1 ? ss / (n - 1) : NaN, sdp: Math.sqrt(ss / n), sds: n > 1 ? Math.sqrt(ss / (n - 1)) : NaN,
               cv: n > 1 ? Math.sqrt(ss / (n - 1)) / mean * 100 : NaN, q1: q1, q3: q3, iqr: iqr,
               outliers: x.filter(function (v) { return v < q1 - 1.5 * iqr || v > q3 + 1.5 * iqr; }) };
    };
    var out = document.getElementById("calc-out"), focus = calc.dataset.focus;
    var rows = [
      ["n", "عدد القيم", "n"], ["mean", "المتوسط الحسابي", "Σx / n", "con-mean"], ["wmean", "المتوسط المرجّح", "Σwx / Σw", "con-weighted-mean"],
      ["median", "الوسيط", "القيمة الوسطى بعد الترتيب", "con-median"], ["modes", "المنوال", "الأكثر تكراراً", "con-mode"],
      ["range", "المدى", "max − min", "con-range"], ["varp", "التباين (مجتمع)", "Σ(x−x̄)² / n", "con-variance"],
      ["vars", "التباين (عينة)", "Σ(x−x̄)² / (n−1)", "con-variance"], ["sdp", "الانحراف المعياري (مجتمع)", "√التباين", "con-standard-deviation"],
      ["sds", "الانحراف المعياري (عينة)", "√التباين", "con-standard-deviation"], ["cv", "معامل الاختلاف %", "s / x̄ × 100", "con-coefficient-of-variation"],
      ["q1", "الربيع الأول Q1", "المئين 25", "con-percentile"], ["q3", "الربيع الثالث Q3", "المئين 75", "con-percentile"],
      ["iqr", "المدى الربيعي", "Q3 − Q1", "con-interquartile-range"], ["outliers", "قيم شاذة", "خارج Q1−1.5·IQR و Q3+1.5·IQR", "con-outlier"]];
    calc.addEventListener("submit", function (e) {
      e.preventDefault();
      var x = toNum(document.getElementById("calc-x").value), wv = toNum(document.getElementById("calc-w").value);
      var msg = document.getElementById("calc-msg");
      if (x.some(isNaN) || x.length < 2) { msg.textContent = "أدخل قيمتين على الأقل، مفصولة بمسافة أو فاصلة (تُقبل الأرقام العربية ٠–٩ والفاصلة العشرية ٫)."; out.hidden = true; return; }
      if (wv.length && (wv.some(isNaN) || wv.length !== x.length)) { msg.textContent = "عدد الأوزان يجب أن يساوي عدد القيم، أو اترك خانة الأوزان فارغة."; out.hidden = true; return; }
      msg.textContent = "";
      var r = window.miyarStats(x, wv.length ? wv : null), tb = out.querySelector("tbody"); tb.innerHTML = "";
      rows.forEach(function (row) {
        var v = r[row[0]]; if (row[0] === "wmean" && v === null) return;
        var txt = Array.isArray(v) ? (v.length ? v.map(fmt).join("، ") : "لا يوجد") : fmt(v);
        var tr = document.createElement("tr"); if (row[3] === focus) tr.className = "focus";
        [row[1], txt, row[2]].forEach(function (c, k) { var td = document.createElement(k ? "td" : "th"); td.textContent = c; if (k === 2) td.dir = "auto"; tr.appendChild(td); });
        tb.appendChild(tr);
      });
      out.hidden = false;
    });
    calc.dispatchEvent(new Event("submit", { cancelable: true }));
  }

  /* ---- code tabs ---- */
  document.querySelectorAll(".tabs").forEach(function (tl) {
    var btns = tl.querySelectorAll("[data-tab]");
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        btns.forEach(function (x) {
          var on = x === b; x.setAttribute("aria-selected", String(on));
          var pane = document.getElementById("pane-" + x.dataset.tab);
          if (on) pane.removeAttribute("data-hidden"); else pane.setAttribute("data-hidden", "");
        });
      });
    });
  });

  /* ---- Arabic / English view on national definitions, country cards and official text sheets (one choice, remembered across pages) ---- */
  var views = document.querySelectorAll(".nat[data-view], .card-view[data-view], .sheet-view[data-view]");
  if (views.length) {
    var setView = function (v) {
      views.forEach(function (c) {
        c.setAttribute("data-view", v);
        c.querySelectorAll(".lang-switch button").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.view === v)); });
      });
      try { localStorage.setItem("miyar-def-view", v); } catch (e) {}
    };
    var saved = null;
    try { saved = localStorage.getItem("miyar-def-view"); } catch (e) {}
    if (saved === "en" || saved === "ar") setView(saved);
    views.forEach(function (c) {
      c.querySelectorAll(".lang-switch button").forEach(function (b) {
        b.addEventListener("click", function () { setView(b.dataset.view); });
      });
    });
  }

  /* ---- copy citation ---- */
  document.querySelectorAll("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      var el = document.getElementById(b.dataset.copy), txt = el.textContent, old = b.textContent;
      function done() { b.textContent = "نُسخ"; setTimeout(function () { b.textContent = old; }, 1800); }
      function sel() { var r = document.createRange(); r.selectNodeContents(el); var s = getSelection(); s.removeAllRanges(); s.addRange(r); }
      if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(txt).then(done, sel); } else { sel(); }
    });
  });

  /* ---- registry filters ---- */
  var reg = document.getElementById("registry");
  if (reg) {
    var btns = document.querySelectorAll("[data-filter]");
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        btns.forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); });
        var f = b.dataset.filter;
        reg.querySelectorAll("tbody tr").forEach(function (tr) { tr.hidden = !(f === "all" || tr.dataset.status === f || tr.dataset.scope === f); });
      });
    });
  }
})();
