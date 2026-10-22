/* Home page: instant member verification by company name or phone */
(function () {
  var q = document.getElementById('v-q'), out = document.getElementById('v-out');
  if (!q || !out) return;
  var EN = (document.documentElement.lang || '').indexOf('en') === 0;
  var initial = out.innerHTML;
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  q.addEventListener('input', function () {
    var k = q.value.trim().toLowerCase().replace(/\s/g, '');
    if (k.length < 2) { out.innerHTML = initial; return; }
    var hits = (window.HKAWDA_MEMBERS || []).filter(function (m) {
      return (m.n + (m.t || []).join('')).toLowerCase().replace(/\s/g, '').indexOf(k) >= 0;
    }).slice(0, 5);
    if (!hits.length) {
      out.innerHTML = '<p class="v-none">' + (EN ? 'Not found in the member directory. Check the spelling, or email info@hkawda.org to confirm.' : '名錄中找不到這間公司。請檢查名稱，或電郵 info@hkawda.org 查詢。') + '</p>';
      return;
    }
    out.innerHTML = '<ul class="v-list">' + hits.map(function (m) {
      return '<li><span class="v-ok">✓</span><a href="member-' + m.id + '.html">' + esc(m.n) + '</a><span class="v-d">' + esc(EN ? (m.de || '') : (m.d || '')) + '</span></li>';
    }).join('') + '</ul><p class="v-note">' + (EN ? 'Listed as an HKAWDA member.' : '以上公司為聯會會員。') + '</p>';
  });
})();
