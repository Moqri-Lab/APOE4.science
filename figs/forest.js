/* Interactive forest plot: odds of Alzheimer's by APOE genotype, by group and sex.
   Data: window.FOREST = {rows: [{sex, genotype, group, carriers, or, lo, hi}], ...}
   Built without libraries; all labels are inserted with textContent. */
(function () {
  "use strict";
  var D = window.FOREST;
  var root = document.getElementById(D.id);
  if (!root) return;

  var SVGNS = "http://www.w3.org/2000/svg";
  var GENOTYPES = D.genotypes;          // top to bottom
  var GROUPS = D.groups;                // fixed order -> fixed colour slot
  var SHAPES = ["circle", "square", "diamond"];
  var state = { sex: "All", hidden: {} };

  function el(tag, attrs, parent, ns) {
    var n = ns ? document.createElementNS(SVGNS, tag) : document.createElement(tag);
    for (var k in attrs) if (Object.prototype.hasOwnProperty.call(attrs, k)) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  }
  function fmt(x) { return x.toFixed(2); }
  function rowsFor(sex) { return D.rows.filter(function (r) { return r.sex === sex; }); }

  // ---------- controls ----------
  var controls = el("div", { "class": "fp-controls" }, root);
  var sexGroup = el("div", { "class": "fp-seg", role: "group", "aria-label": "Sex" }, controls);
  ["All", "Women", "Men"].forEach(function (s) {
    var b = el("button", { type: "button", "aria-pressed": String(s === state.sex) }, sexGroup);
    b.textContent = s === "All" ? "Everyone" : s;
    b.addEventListener("click", function () {
      state.sex = s;
      Array.prototype.forEach.call(sexGroup.children, function (c) { c.setAttribute("aria-pressed", "false"); });
      b.setAttribute("aria-pressed", "true");
      render();
    });
  });
  var viewGroup = el("div", { "class": "fp-seg", role: "group", "aria-label": "View" }, controls);
  var showChart = el("button", { type: "button", "aria-pressed": "true" }, viewGroup); showChart.textContent = "Chart";
  var showTable = el("button", { type: "button", "aria-pressed": "false" }, viewGroup); showTable.textContent = "Table";
  var dl = el("a", { "class": "fp-dl", href: D.csv, download: D.csv.split("/").pop() }, controls);
  dl.textContent = "Download data (CSV)";

  // ---------- legend (toggles groups) ----------
  var legend = el("div", { "class": "fp-legend", role: "group", "aria-label": "Groups shown" }, root);
  GROUPS.forEach(function (g, i) {
    var b = el("button", { type: "button", "aria-pressed": "true", "class": "fp-key" }, legend);
    var sw = el("svg", { width: "14", height: "14", viewBox: "-7 -7 14 14", "aria-hidden": "true" }, b, true);
    mark(sw, 0, 0, i, 5);
    b.appendChild(document.createTextNode(g));
    b.addEventListener("click", function () {
      var shown = GROUPS.filter(function (x) { return !state.hidden[x]; }).length;
      if (!state.hidden[g] && shown === 1) return; // keep at least one group
      state.hidden[g] = !state.hidden[g];
      b.setAttribute("aria-pressed", String(!state.hidden[g]));
      render();
    });
  });

  var figure = el("div", { "class": "fp-figure" }, root);
  var tableWrap = el("div", { "class": "fp-table alleles", hidden: "", role: "region", "aria-label": D.title + ", table", tabindex: "0" }, root);
  var tip = el("div", { "class": "fp-tip", role: "status", "aria-live": "polite", hidden: "" }, root);

  showChart.addEventListener("click", function () {
    showChart.setAttribute("aria-pressed", "true"); showTable.setAttribute("aria-pressed", "false");
    figure.hidden = false; legend.hidden = false; tableWrap.hidden = true;
  });
  showTable.addEventListener("click", function () {
    showTable.setAttribute("aria-pressed", "true"); showChart.setAttribute("aria-pressed", "false");
    figure.hidden = true; legend.hidden = true; tableWrap.hidden = false;
  });

  // ---------- marks ----------
  function mark(parent, x, y, i, r) {
    var cls = "fp-m fp-s" + (i + 1);
    if (SHAPES[i] === "circle") return el("circle", { cx: x, cy: y, r: r, "class": cls }, parent, true);
    if (SHAPES[i] === "square") return el("rect", { x: x - r * 0.9, y: y - r * 0.9, width: r * 1.8, height: r * 1.8, rx: 1.5, "class": cls }, parent, true);
    return el("path", { d: "M" + x + "," + (y - r * 1.2) + "L" + (x + r * 1.2) + "," + y + "L" + x + "," + (y + r * 1.2) + "L" + (x - r * 1.2) + "," + y + "Z", "class": cls }, parent, true);
  }

  // ---------- render ----------
  function render() {
    var rows = rowsFor(state.sex);
    var groups = GROUPS.filter(function (g) { return !state.hidden[g]; });
    var W = Math.max(300, figure.clientWidth || 640);
    var narrow = W < 520;
    var left = narrow ? 58 : 76, right = 16, top = 26, bottom = 40;
    var band = narrow ? 50 : 46;
    var H = top + band * GENOTYPES.length + bottom;
    // Fit the axis to the rows on screen, so one wide interval does not squeeze the rest
    var shown = rows.filter(function (r) { return r.genotype !== D.reference && groups.indexOf(r.group) >= 0; });
    var lowest = Math.min.apply(null, shown.map(function (r) { return r.lo; }));
    var highest = Math.max.apply(null, shown.map(function (r) { return r.hi; }));
    var d0 = Math.min(0.8, lowest / 1.25), d1 = Math.max(1.25, highest * 1.6);
    var x0 = Math.log(d0), x1 = Math.log(d1);
    function X(v) { return left + (Math.log(v) - x0) / (x1 - x0) * (W - left - right); }

    figure.textContent = "";
    var svg = el("svg", { width: W, height: H, viewBox: "0 0 " + W + " " + H, role: "img", "aria-label": D.title + ". " + D.summary }, figure, true);

    // grid + axis
    var ticks = (narrow ? D.ticksNarrow : D.ticks).filter(function (t) { return t >= d0 && t <= d1; });
    ticks.forEach(function (t) {
      var x = X(t);
      el("line", { x1: x, x2: x, y1: top - 6, y2: H - bottom, "class": t === 1 ? "fp-ref" : "fp-grid" }, svg, true);
      var lab = el("text", { x: x, y: H - bottom + 18, "class": "fp-tick", "text-anchor": "middle" }, svg, true);
      lab.textContent = (t < 1 ? String(t).replace(/^0/, "") : String(t)) + (t === 1 ? "" : "");
    });
    var ax = el("text", { x: X(1), y: H - 6, "class": "fp-axis", "text-anchor": "middle" }, svg, true);
    ax.textContent = "Odds ratio vs ε3/ε3 (log scale)";
    var lo = el("text", { x: X(1) - 8, y: top - 12, "class": "fp-dir", "text-anchor": "end" }, svg, true); lo.textContent = "← lower risk";
    var hi = el("text", { x: X(1) + 8, y: top - 12, "class": "fp-dir", "text-anchor": "start" }, svg, true); hi.textContent = "higher risk →";

    GENOTYPES.forEach(function (gt, gi) {
      var yc = top + band * gi + band / 2;
      if (gi % 2 === 0) el("rect", { x: 0, y: top + band * gi, width: W, height: band, "class": "fp-band" }, svg, true);
      var lab = el("text", { x: 4, y: yc + 4, "class": "fp-row" + (gt === "ε4/ε4" ? " fp-row-key" : "") }, svg, true);
      lab.textContent = gt;
      if (gt === D.reference) {
        var rf = el("text", { x: X(1) + 8, y: yc + 4, "class": "fp-dir" }, svg, true);
        rf.textContent = "reference";
        return;
      }
      groups.forEach(function (g, k) {
        var r = rows.filter(function (d) { return d.genotype === gt && d.group === g; })[0];
        if (!r) return;
        var i = GROUPS.indexOf(g);
        var off = (k - (groups.length - 1) / 2) * (narrow ? 12 : 11);
        var y = yc + off;
        var gEl = el("g", { "class": "fp-pt", tabindex: "0", role: "img",
          "aria-label": g + ", " + gt + ": odds ratio " + fmt(r.or) + ", 95% CI " + fmt(r.lo) + " to " + fmt(r.hi) + ", " + r.carriers.toLocaleString() + " carriers" }, svg, true);
        el("line", { x1: X(r.lo), x2: X(r.hi), y1: y, y2: y, "class": "fp-ci fp-c" + (i + 1) }, gEl, true);
        mark(gEl, X(r.or), y, i, 4.5);
        el("rect", { x: X(r.lo) - 6, y: y - 6, width: Math.max(24, X(r.hi) - X(r.lo) + 12), height: 12, "class": "fp-hit" }, gEl, true);
        if (gt === "ε4/ε4" && !narrow) { // selective direct labels on the headline row
          var v = el("text", { x: X(r.hi) + 6, y: y + 4, "class": "fp-val" }, gEl, true);
          v.textContent = fmt(r.or);
        }
        function show(ev) {
          tip.textContent = "";
          var s = el("strong", {}, tip); s.textContent = fmt(r.or) + " (" + fmt(r.lo) + "–" + fmt(r.hi) + ")";
          var line = el("span", {}, tip);
          var key = el("i", { "class": "fp-tk fp-c" + (i + 1) }, line);
          line.appendChild(document.createTextNode(g + " · " + gt + " · " + r.carriers.toLocaleString() + " carriers"));
          tip.hidden = false;
          var box = root.getBoundingClientRect(), fb = figure.getBoundingClientRect();
          var px = X(r.or) + (fb.left - box.left), py = y + (fb.top - box.top);
          tip.style.left = Math.min(Math.max(px - tip.offsetWidth / 2, 0), box.width - tip.offsetWidth) + "px";
          tip.style.top = (py - tip.offsetHeight - 14) + "px";
          gEl.classList.add("is-on");
        }
        function hide() { tip.hidden = true; gEl.classList.remove("is-on"); }
        gEl.addEventListener("pointerenter", show);
        gEl.addEventListener("pointerleave", hide);
        gEl.addEventListener("focus", show);
        gEl.addEventListener("blur", hide);
      });
    });

    // table view (always current with the sex filter)
    tableWrap.textContent = "";
    var tb = el("table", { "class": "data" }, tableWrap);
    var hr = el("tr", {}, el("thead", {}, tb));
    ["Genotype"].concat(GROUPS).forEach(function (h) { el("th", {}, hr).textContent = h; });
    var body = el("tbody", {}, tb);
    GENOTYPES.forEach(function (gt) {
      var tr = el("tr", {}, body);
      el("td", {}, tr).textContent = gt;
      GROUPS.forEach(function (g) {
        var r = rows.filter(function (d) { return d.genotype === gt && d.group === g; })[0];
        el("td", { "class": "num" }, tr).textContent = gt === D.reference ? "1 (reference)" :
          fmt(r.or) + " (" + fmt(r.lo) + "–" + fmt(r.hi) + ")";
      });
    });
  }

  render();
  var rt;
  window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(render, 120); });
})();
