/* HKAWDA site script: language switch + mobile menu + small helpers */
(function () {
  var root = document.documentElement;
  // larger text toggle (remembered on this device)
  function st(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  var ts = document.querySelector('.text-size');
  function setBig(on) { root.classList.toggle('big', on); if (ts) ts.setAttribute('aria-pressed', String(on)); st('hkawda-big', on ? '1' : '0'); }
  setBig(st('hkawda-big') === '1');
  if (ts) ts.addEventListener('click', function () { setBig(!root.classList.contains('big')); });
  var btn = document.querySelector('.menu-btn'), nav = document.getElementById('nav');
  if (btn && nav) btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open'); btn.setAttribute('aria-expanded', String(open));
  });

  // contact form → opens the visitor's email app with a prefilled message
  var f = document.getElementById('contact-form');
  if (f) f.addEventListener('submit', function (e) {
    e.preventDefault();
    var d = new FormData(f), to = f.dataset.to;
    var body = '姓名 Name: ' + d.get('name') + '\n電話 Phone: ' + d.get('phone') + '\n電郵 Email: ' + d.get('email') + '\n\n' + d.get('message');
    var url = 'mailto:' + to + '?subject=' + encodeURIComponent('[HKAWDA 網站查詢] ' + d.get('topic')) + '&body=' + encodeURIComponent(body);
    document.getElementById('form-msg').hidden = false;
    window.location.href = url;
  });

  var y = document.getElementById('year'); if (y) y.textContent = new Date().getFullYear();
})();
