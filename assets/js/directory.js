/* Member directory: filter by region, district, trade and keyword.
   Data lives in members-data.js (window.HKAWDA_MEMBERS). Edit that file to add or remove members. */
(function () {
  var DATA = window.HKAWDA_MEMBERS || [];
  var EN = (document.documentElement.lang || '').indexOf('en') === 0;
  var REGIONS = { all: ['全港', 'All HK'], hki: ['香港島', 'HK Island'], kln: ['九龍', 'Kowloon'], nt: ['新界', 'New Territories'] };
  var SERVICES = { alu: ['鋁窗鋁門', 'Aluminium'], glass: ['玻璃 / 鏡', 'Glass'], gate: ['鋼閘鐵閘', 'Gates'], steel: ['不銹鋼', 'Stainless steel'], reno: ['裝修工程', 'Renovation'] };
  var state = { region: 'all', district: '', svc: '', q: '', council: false };

  var params = new URLSearchParams(location.search);
  if (REGIONS[params.get('region')]) state.region = params.get('region');
  if (params.get('district')) state.district = params.get('district');
  if (params.get('q')) state.q = params.get('q');

  var $ = function (s) { return document.querySelector(s); };
  var q = $('#f-q'), dsel = $('#f-district'), out = $('#results'), cnt = $('#count'), council = $('#f-council');
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function bi(p) { return EN ? p[1] : p[0]; }

  // region buttons
  var seg = $('#f-region');
  Object.keys(REGIONS).forEach(function (k) {
    var b = document.createElement('button'); b.type = 'button'; b.className = 'chip'; b.dataset.v = k; b.innerHTML = bi(REGIONS[k]);
    b.addEventListener('click', function () { state.region = k; state.district = ''; fillDistricts(); render(); });
    seg.appendChild(b);
  });
  // service chips
  var sc = $('#f-svc');
  Object.keys(SERVICES).forEach(function (k) {
    var b = document.createElement('button'); b.type = 'button'; b.className = 'chip'; b.dataset.v = k; b.innerHTML = bi(SERVICES[k]);
    b.addEventListener('click', function () { state.svc = state.svc === k ? '' : k; render(); });
    sc.appendChild(b);
  });

  function fillDistricts() {
    var seen = {}, opts = '<option value="">' + bi(['全部地區', 'All districts']) + '</option>';
    DATA.forEach(function (m) {
      if ((state.region === 'all' || m.r === state.region) && m.d && !seen[m.d]) { seen[m.d] = m.de; }
    });
    Object.keys(seen).sort(function (a, b) { return seen[a].localeCompare(seen[b]); }).forEach(function (d) {
      opts += '<option value="' + esc(d) + '"' + (d === state.district ? ' selected' : '') + '>' + esc(EN ? seen[d] : d) + '</option>';
    });
    dsel.innerHTML = opts;
  }

  function card(m) {
    var tel = (m.t || [])[0];
    var map = 'https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent(m.a + ' 香港');
    var tags = '<span class="tag d">' + esc(EN ? (m.de || REGIONS[m.r][1]) : (m.d || REGIONS[m.r][0])) + '</span>';
    (m.s || []).forEach(function (s) { tags += '<span class="tag">' + bi(SERVICES[s]) + '</span>'; });
    return '<article class="m-card">' +
      '<div class="m-top"><h3 class="m-name">' + esc(m.n) + '</h3>' + (m.c ? '<span class="badge">' + bi(['會長單位', 'Council']) + '</span>' : '') + '</div>' +
      '<div class="m-meta">' + tags + '</div>' +
      (m.a ? '<div class="m-addr">' + esc(m.a) + '</div>' : '') +
      '<div class="m-actions">' +
      (tel ? '<a class="call" href="tel:+852' + tel.replace(/\s/g, '') + '">☎ ' + esc(tel) + '</a>' : '') +
      ((m.t || []).slice(1).map(function (t) { return '<a href="tel:+852' + t.replace(/\s/g, '') + '">☎ ' + esc(t) + '</a>'; }).join('')) +
      (m.a ? '<a href="' + map + '" target="_blank" rel="noopener">' + bi(['地圖', 'Map']) + ' ↗</a>' : '') +
      '</div></article>';
  }

  function render() {
    document.querySelectorAll('#f-region .chip').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.v === state.region)); });
    document.querySelectorAll('#f-svc .chip').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.v === state.svc)); });
    state.district = dsel.value; state.q = q.value.trim(); state.council = council.checked;
    var k = state.q.toLowerCase();
    var list = DATA.filter(function (m) {
      if (state.region !== 'all' && m.r !== state.region) return false;
      if (state.district && m.d !== state.district) return false;
      if (state.svc && (m.s || []).indexOf(state.svc) < 0) return false;
      if (state.council && !m.c) return false;
      if (k) {
        var hay = (m.n + ' ' + m.a + ' ' + m.d + ' ' + m.de + ' ' + (m.t || []).join(' ')).toLowerCase();
        if (hay.indexOf(k) < 0 && hay.replace(/\s/g, '').indexOf(k.replace(/\s/g, '')) < 0) return false;
      }
      return true;
    });
    list.sort(function (a, b) { return (b.c - a.c) || (a.de || 'zz').localeCompare(b.de || 'zz') || (a.n < b.n ? -1 : a.n > b.n ? 1 : 0); });
    cnt.innerHTML = '<b>' + list.length + '</b> / ' + DATA.length + ' ' + bi(['間會員公司', 'member firms']);
    out.innerHTML = list.length ? list.map(card).join('') :
      '<div class="empty">' + bi(['沒有符合條件的會員。請放寬地區或關鍵字。', 'No members match. Try a wider area or a shorter keyword.']) + '</div>';
  }

  fillDistricts();
  q.value = state.q;
  q.addEventListener('input', render);
  dsel.addEventListener('change', render);
  council.addEventListener('change', render);
  $('#f-reset').addEventListener('click', function () { state = { region: 'all', district: '', svc: '', q: '', council: false }; q.value = ''; council.checked = false; fillDistricts(); render(); });
  render();
})();
