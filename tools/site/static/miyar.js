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
