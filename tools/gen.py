# Generates the static HKAWDA site (plain HTML, no build step needed afterwards).
import json, collections, html as H
OUT = './'
M = json.load(open('tools/members.json'))
REGION_COUNT = collections.Counter(m['r'] for m in M)
RSLUG = {'hki':'installers-hong-kong-island.html','kln':'installers-kowloon.html','nt':'installers-new-territories.html'}
DIST_BY_REGION = collections.defaultdict(list)
DIST_EN = {}
for m in M:
    if m['d'] and m['d'] not in DIST_BY_REGION[m['r']]: DIST_BY_REGION[m['r']].append(m['d'])
    if m['d']: DIST_EN[m['d']] = m['de']

# ---- contact details: edit here, then re-run ----
C = dict(email='info@hkawda.org', tel='2381 4161', whatsapp='6915 6828',
         fb='https://www.facebook.com/profile.php?id=61580456752522',
         li='https://www.linkedin.com/company/hong-kong-aluminum-window-and-doors-association')
BASE = 'https://hkawda.org/'
LR = 'https://www.le-relax.co'

def b(zh, en, tag='span', cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<{tag}{c}><span class="zh">{zh}</span><span class="en" lang="en">{en}</span></{tag}>' if tag != 'span' or cls else f'<span class="zh">{zh}</span><span class="en" lang="en">{en}</span>'
def p(zh, en, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<p{c}><span class="zh">{zh}</span></p><p class="en{(" "+cls) if cls else ""}" lang="en">{en}</p>'

NAV = [('index.html','首頁','Home'),('find-installer.html','搵會員工程公司','Find an installer'),('homeowners.html','業主指南','Homeowner guide'),
       ('about.html','關於聯會','About'),('news.html','消息及活動','News & events'),('courses.html','行業課程','Courses'),('contact.html','聯絡我們','Contact')]

def head(title_zh, title_en, desc, path, title=None):
    xt = f'<meta name="x-title" data-zh="{H.escape(title[0])}" data-en="{H.escape(title[1])}">' if title else ''
    return f'''<!doctype html>
<html lang="zh-Hant-HK">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{'香港鋁門窗同業聯會 HKAWDA | 搵鋁窗工程公司 Find an installer' if path=='index.html' else title_zh+' '+title_en+' | 香港鋁門窗同業聯會 HKAWDA'}</title>
<meta name="claude:viewport-fit-sides" content="cover">{xt}
<meta name="description" content="{H.escape(desc)}">
<link rel="canonical" href="{BASE}{'' if path=='index.html' else path}">
<meta property="og:title" content="{title_zh} | 香港鋁門窗同業聯會 HKAWDA">
<meta property="og:description" content="{H.escape(desc)}">
<meta property="og:image" content="{BASE}assets/img/founding-2015-b.jpg">
<meta property="og:type" content="website">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<a class="skip" href="#main">跳至內容 Skip to content</a>
<header class="site-head">
 <div class="wrap head-row">
  <a class="brand" href="index.html" aria-label="香港鋁門窗同業聯會首頁 HKAWDA home">
   <span class="brand-chip"><img src="assets/img/logo.png" alt="HKAWDA 標誌" width="64" height="40"></span>
   <span class="brand-name"><span class="zh">香港鋁門窗同業聯會</span><span class="en" lang="en">Hong Kong Aluminium Windows &amp; Doors Association</span></span>
  </a>
  <nav class="nav" id="nav" aria-label="主選單 Main">
   {''.join(f'<a href="{h}"{" aria-current=page" if h==path else ""}>{b(z,e)}</a>' for h,z,e in NAV[1:])}
   <a class="nav-cta" href="membership.html"{" aria-current=page" if path=="membership.html" else ""}>{b("申請入會","Join")}</a>
  </nav>
  <div class="head-tools"><button class="text-size" type="button" aria-pressed="false" aria-label="放大字體 Larger text">A+</button><!--LANGSWITCH--><button class="menu-btn" aria-expanded="false" aria-controls="nav">選單 Menu</button></div>
 </div>
</header>
<main id="main">
'''

def foot(extra_js=''):
    return f'''</main>
<footer class="site-foot">
 <div class="wrap">
  <div class="foot-grid">
   <div class="foot-brand">
    <span class="brand-chip"><img src="assets/img/logo.png" alt="HKAWDA" width="84" height="52"></span>
    <div><strong>{b("香港鋁門窗同業聯會有限公司","Hong Kong Aluminium Windows &amp; Doors Association Co., Ltd.")}</strong></div>
    {p("團結業界 · 提升專業 · 為市民服務","Uniting the trade, raising standards, serving the public.")}
    <p class="foot-founder">{b("創會成員：","Founding member: ")}<a href="{LR}" target="_blank" rel="noopener">{b("升威 LE-RELAX 鋁門窗製造及批發","LE-RELAX aluminium windows &amp; doors (manufacturer &amp; wholesaler)")} ↗</a></p>
   </div>
   <div><h4>業主 FOR HOMEOWNERS</h4><ul>
    <li><a href="find-installer.html">{b("搵會員工程公司","Find an installer")}</a></li>
    <li><a href="homeowners.html">{b("更換鋁窗指南","Window replacement guide")}</a></li>
    <li><a href="homeowners.html#housing">{b("按住宅類型","By type of home")}</a></li>
    <li><a href="homeowners.html#problems">{b("常見窗戶問題","Common window problems")}</a></li>
    <li><a href="window-inspection-notice.html">{b("收到驗窗通知","Window inspection notice")}</a></li></ul></div>
   <div><h4>業界 FOR THE TRADE</h4><ul>
    <li><a href="membership.html">{b("會員福利及入會","Membership")}</a></li>
    <li><a href="courses.html">{b("行業課程","Courses")}</a></li>
    <li><a href="news.html">{b("消息及活動","News & events")}</a></li></ul></div>
   <div><h4>聯絡 CONTACT</h4><ul>
    <li class="mono">{C['email']}</li>
    <li class="mono">Tel {C['tel']}</li>
    <li class="mono">WhatsApp {C['whatsapp']}</li>
    <li><a href="{C['fb']}" target="_blank" rel="noopener">Facebook ↗</a> · <a href="{C['li']}" target="_blank" rel="noopener">LinkedIn ↗</a></li></ul></div>
  </div>
  <div class="foot-meta"><span>© 2015–<span id="year">2026</span> Hong Kong Aluminium Windows &amp; Doors Association Co., Ltd.</span><span>九龍總商會附屬團體 · Affiliated association of the Kowloon Chamber of Commerce</span></div>
 </div>
</footer>
<nav class="mbar" aria-label="快捷 Quick actions"><a href="find-installer.html">{b("搵會員工程公司","Find an installer")}</a><a class="wa" href="https://wa.me/852{C['whatsapp'].replace(' ','')}" target="_blank" rel="noopener">WhatsApp</a></nav>
<script src="assets/js/main.js"></script>
{extra_js}
</body>
</html>
'''

def page_title(path, crumb_zh, crumb_en, h_zh, h_en, lede_zh, lede_en):
    return f'''<div class="page-title"><div class="wrap">
 <div class="crumb"><a href="index.html">首頁 Home</a> / {crumb_zh} {crumb_en}</div>
 <h1><span class="zh">{h_zh}</span><span class="en" lang="en">{h_en}</span></h1>
 {p(lede_zh, lede_en, 'lede')}
</div></div>'''

def write(path, body, tz, te, desc, js='', title=None):
    open(OUT+path,'w').write(head(tz,te,desc,path,title)+body+foot(js))

def region_opts():
    return ''.join(f'<option value="{k}">{z} {e}</option>' for k,z,e in [('all','全港','All Hong Kong'),('hki','香港島','HK Island'),('kln','九龍','Kowloon'),('nt','新界','New Territories')])

HERO_SVG = '''<svg viewBox="0 0 400 470" role="img" aria-label="鋁窗立面圖 Elevation of an aluminium window">
 <g fill="none" stroke="currentColor">
  <rect x="70" y="50" width="270" height="360" stroke-width="2.2"/>
  <rect x="80" y="60" width="250" height="340" stroke-width="1"/>
  <rect class="glass" x="80" y="60" width="250" height="96" stroke-width="1"/>
  <line x1="70" y1="160" x2="340" y2="160" stroke-width="2.2"/>
  <line x1="205" y1="160" x2="205" y2="410" stroke-width="2.2"/>
  <rect class="glass" x="88" y="170" width="109" height="232" stroke-width="1.2"/>
  <rect class="glass" x="213" y="170" width="109" height="232" stroke-width="1.2"/>
  <polyline points="88,170 197,286 88,402" stroke-dasharray="5 4" stroke-width=".9"/>
  <polyline points="322,170 213,286 322,402" stroke-dasharray="5 4" stroke-width=".9"/>
  <line x1="88" y1="410" x2="322" y2="410" stroke-width=".6"/>
  <!-- dimension lines -->
  <g stroke-width=".7" opacity=".75">
   <line x1="70" y1="28" x2="340" y2="28"/><line x1="70" y1="22" x2="70" y2="44"/><line x1="340" y1="22" x2="340" y2="44"/>
   <line x1="364" y1="50" x2="364" y2="410"/><line x1="356" y1="50" x2="372" y2="50"/><line x1="356" y1="410" x2="372" y2="410"/><line x1="356" y1="160" x2="372" y2="160"/>
   <line x1="70" y1="432" x2="205" y2="432"/><line x1="70" y1="426" x2="70" y2="438"/><line x1="205" y1="426" x2="205" y2="438"/>
  </g>
 </g>
 <text class="dim" x="205" y="20" text-anchor="middle">1200</text>
 <text class="dim" x="384" y="108" text-anchor="middle" transform="rotate(90 384 108)">400</text>
 <text class="dim" x="384" y="288" text-anchor="middle" transform="rotate(90 384 288)">1100</text>
 <text class="dim" x="138" y="452" text-anchor="middle">600</text>
 <text class="lbl" x="205" y="104" text-anchor="middle">固定窗</text>
 <text class="lbl-en" x="205" y="120" text-anchor="middle">FIXED LIGHT</text>
 <text class="lbl" x="142" y="300" text-anchor="middle">平開窗</text>
 <text class="lbl-en" x="142" y="316" text-anchor="middle">CASEMENT</text>
 <text class="lbl" x="268" y="300" text-anchor="middle">平開窗</text>
 <text class="lbl-en" x="268" y="316" text-anchor="middle">CASEMENT</text>
 <g><circle class="callout" cx="88" cy="196" r="4"/><line x1="88" y1="196" x2="30" y2="196" stroke="currentColor" stroke-width=".7"/>
 <text class="lbl-en" x="2" y="186">HINGE</text><text class="lbl" x="2" y="212" style="font-size:10px">鉸位</text></g>
 <g><circle class="callout" cx="88" cy="380" r="4"/><line x1="88" y1="380" x2="30" y2="380" stroke="currentColor" stroke-width=".7"/>
 <text class="lbl-en" x="2" y="370">RIVETS</text><text class="lbl" x="2" y="396" style="font-size:10px">鉚釘</text></g>
 <text class="dim" x="70" y="466">單位 UNIT: mm · 示意圖 ILLUSTRATIVE</text>
</svg>'''

# ================= HOME =================
home = f'''
<section class="hero"><div class="wrap hero-grid">
 <div class="hero-copy">
  <div class="eyebrow">{b("香港鋁門窗同業聯會 · 2015 年成立","EST. 2015")}</div>
  <h1><span class="zh">更換鋁窗，<br><span class="accent">先搵聯會會員。</span></span><span class="en" lang="en">Replacing aluminium windows? Start with an HKAWDA member.</span></h1>
  {p("香港鋁門窗同業聯會匯聚全港鋁窗、鋁門及玻璃工程公司，為業主提供可信的會員名錄、更換鋁窗指南，並與政府部門溝通，推動行業規範化。","HKAWDA brings together aluminium window, door and glazing contractors across Hong Kong. We publish a trusted member directory and a homeowner guide, and work with government on clear standards for the trade.","lede")}
  <form class="finder" action="find-installer.html" method="get">
   <div class="finder-label">{b("按地區搵會員工程公司","Find a member firm near you")}</div>
   <div class="finder-row">
    <div class="field"><label for="h-region">地區 REGION</label><select id="h-region" name="region">{region_opts()}</select></div>
    <div class="field"><label for="h-q">關鍵字 KEYWORD</label><input id="h-q" name="q" type="search" placeholder="例如：旺角、元朗、公司名稱 e.g. Mong Kok"></div>
    <button class="btn red" type="submit">{b("搜尋","Search")}</button>
   </div>
  </form>
  <div class="facts">
   <div class="fact"><b>{len(M)}</b><span>{b("會員公司","member firms")}</span></div>
   <div class="fact"><b>{len({m['d'] for m in M if m['d']})}</b><span>{b("個地區","districts covered")}</span></div>
   <div class="fact"><b>2015</b><span>{b("成立","founded")}</span></div>
  </div>
 </div>
 <div class="hero-art" aria-hidden="false">{HERO_SVG}</div>
</div></section>

<section><div class="wrap">
 <div class="sec-head"><div class="eyebrow">業主指南 HOMEOWNERS</div>
  <h2><span class="zh">更換鋁窗三步走</span><span class="en" lang="en">Three steps to replacing your windows</span></h2></div>
 <div class="steps">
  <div class="step"><div class="step-no">STEP 01</div><h3>{b("了解規定","Know the rules")}</h3>
   {p("在香港更換窗戶一般屬「小型工程」，須由屋宇署註冊的合資格承建商進行；收到「強制驗窗」通知的大廈另有要求。","In Hong Kong, replacing a window is usually a 'minor works' item that must be carried out by a contractor registered with the Buildings Department. Buildings served a Mandatory Window Inspection notice have extra steps.")}
   <a class="more" href="homeowners.html#rules">{b("了解小型工程及驗窗 →","Minor works & MWIS →")}</a></div>
  <div class="step"><div class="step-no">STEP 02</div><h3>{b("揀選聯會會員","Choose a member")}</h3>
   {p("在會員名錄按地區搜尋，比較最少兩至三份書面報價，並留意店舖的聯會會員貼紙。","Search the directory by district, compare at least two or three written quotations, and look for the HKAWDA member sticker at the shop.")}
   <a class="more" href="find-installer.html">{b("瀏覽會員名錄 →","Browse the directory →")}</a></div>
  <div class="step"><div class="step-no">STEP 03</div><h3>{b("驗收及保養","Check and maintain")}</h3>
   {p("完工後核對報價項目、索取保養單據及屋宇署提交文件副本，並定期檢查鉸位、鉚釘及窗扣。","On completion, check the work against the quotation, keep the warranty and copies of Buildings Department submissions, and inspect hinges, rivets and latches regularly.")}
   <a class="more" href="homeowners.html#checklist">{b("驗收清單 →","Handover checklist →")}</a></div>
 </div>
</div></section>

<section class="band"><div class="wrap trust">
 <div style="display:grid;gap:24px">
  <div class="sec-head" style="margin:0"><div class="eyebrow">為何選擇會員 WHY A MEMBER</div>
   <h2><span class="zh">認住聯會標誌，安心之選</span><span class="en" lang="en">Look for the HKAWDA mark</span></h2></div>
  <ul class="checklist">
   <li><span class="tick">✓</span><div><strong>{b("店舖貼有聯會認證貼紙","Certified sticker on the shopfront")}</strong>{p("每間會員公司均獲發專業認證玻璃貼紙及獨立編號會員卡。","Every member firm receives a certified glass sticker and a numbered membership card.")}</div></li>
   <li><span class="tick">✓</span><div><strong>{b("行業代表，與政府溝通","A voice for the trade with government")}</strong>{p("聯會曾向屋宇署反映改善收表時間，屋宇署其後增設驗窗卡以識別鋁窗專業人士。","The Association raised processing times with the Buildings Department, which later introduced a window-inspection card to identify qualified window professionals.")}</div></li>
   <li><span class="tick">✓</span><div><strong>{b("持續培訓，提升工藝","Ongoing training")}</strong>{p("與職業訓練局 IVE 合辦窗戶安裝及維修、強制驗窗相關課程。","Courses with IVE (VTC) on window installation, maintenance and inspection schemes.")}</div></li>
   <li><span class="tick">✓</span><div><strong>{b("法律及專業支援","Legal and professional support")}</strong>{p("會員遇上牌照問題，可獲聯會顧問律師提供意見。","Members facing licensing issues can get advice from the Association's legal adviser.")}</div></li>
  </ul>
 </div>
 <div class="sticker">
  <div class="sticker-mock" role="img" aria-label="聯會會員貼紙示意 Member sticker (illustration)">
   <img src="assets/img/logo.png" alt="">
   <div><div class="s1">香港鋁門窗同業聯會<br>認可會員</div><div class="s2">HKAWDA CERTIFIED MEMBER</div><div class="s3">www.hkawda.org</div></div>
  </div>
  {p("看到這個標誌，可在本網站會員名錄核實公司名稱。","Seen this mark? Check the company name in our member directory.")}
  <a class="btn ghost" href="find-installer.html">{b("核實會員","Verify a member")}</a>
 </div>
</div></section>

<section class="alt"><div class="wrap">
 <div class="sec-head"><div class="eyebrow">會員分佈 BY REGION</div>
  <h2><span class="zh">會員遍佈港九新界</span><span class="en" lang="en">Members across Hong Kong</span></h2></div>
 <div class="regions">
  {''.join(f"""<a class="region" href="{RSLUG[k]}"><div class="count">{REGION_COUNT[k]}<small>{b("間","firms")}</small></div><h3>{b(z,e)}</h3><div class="districts">{b('、'.join(DIST_BY_REGION[k]), ', '.join(DIST_EN[d] for d in DIST_BY_REGION[k]))}</div><div class="go">{b("查看名單 →","View list →")}</div></a>""" for k,z,e in [('hki','香港島','Hong Kong Island'),('kln','九龍','Kowloon'),('nt','新界','New Territories')])}
 </div>
</div></section>

<section><div class="wrap">
 <div class="sec-head"><div class="eyebrow">消息及活動 NEWS &amp; EVENTS</div>
  <h2><span class="zh">聯會近況</span><span class="en" lang="en">Latest from the Association</span></h2></div>
 <div class="news-grid">
  <a class="news-card" href="news.html#2025-zhongshan"><div class="ph"><img src="assets/img/zhongshan-2025-factory.jpg" alt="會員參觀中山鋁門窗廠生產線" loading="lazy"></div><div class="bd"><div class="date">2025-11-29</div><h3>{b("鋁門窗及玻璃廠中山考察團","Aluminium window & glass factory tour")}</h3>{p("實地考察鋁門窗廠及玻璃廠，交流行業最新趨勢與加工技術。","Site visits to window and glass factories to share the latest trends and processing techniques.")}</div></a>
  <a class="news-card" href="news.html#2023-zhongshan"><div class="ph"><img src="assets/img/zhongshan-2023-glass.jpg" alt="會員參觀中山玻璃加工車間" loading="lazy"></div><div class="bd"><div class="date">2023-12-09</div><h3>{b("中山廠房參觀團","Zhongshan factory visit")}</h3>{p("近五十位會長及會員參觀中山鋁窗及玻璃生產線。","Nearly fifty members toured aluminium window and glass production lines.")}</div></a>
  <a class="news-card" href="news.html#2015-founding"><div class="ph"><img src="assets/img/founding-2015-c.jpg" alt="2015 年成立典禮全體合照" loading="lazy"></div><div class="bd"><div class="date">2015-11-30</div><h3>{b("聯會成立典禮","Founding ceremony")}</h3>{p("近百位嘉賓及同業見證聯會成立，《大公報》專題報道。","Close to a hundred guests marked the Association's founding, covered by Ta Kung Pao.")}</div></a>
 </div>
</div></section>

<section class="band"><div class="wrap recog">
 <img src="assets/img/kcc-logo.jpg" alt="九龍總商會標誌" width="110" height="100">
 <div style="display:grid;gap:8px"><h3>{b("九龍總商會附屬團體","Affiliated association of the Kowloon Chamber of Commerce")}</h3>{p("聯會獲九龍總商會認可為附屬團體，與商界共同推動行業發展。","HKAWDA is recognised by the Kowloon Chamber of Commerce as an affiliated association.")}</div>
 <a class="btn red" href="membership.html">{b("業界同行：申請入會","In the trade? Join us")}</a>
</div></section>
'''
write('index.html', home, '香港鋁門窗同業聯會', 'HKAWDA',
      '香港鋁門窗同業聯會（HKAWDA）：按地區搜尋鋁窗、鋁門及玻璃工程會員公司，了解在香港更換鋁窗的規定。Find vetted aluminium window and door installers in Hong Kong.')

# ================= DIRECTORY =================
SV = {'alu':('鋁窗鋁門','Aluminium'),'glass':('玻璃 / 鏡','Glass'),'gate':('鋼閘鐵閘','Gates'),'steel':('不銹鋼','Stainless steel'),'reno':('裝修工程','Renovation')}
RN = {'hki':('香港島','HK Island'),'kln':('九龍','Kowloon'),'nt':('新界','New Territories')}
def dslug(de): return 'district-' + de.lower().replace(' & ', '-').replace(' ', '-') + '.html'
def card(m):
    import urllib.parse as up
    tel=(m['t'] or [])
    mp='https://www.google.com/maps/search/?api=1&query='+up.quote(m['a']+' 香港')
    tags=f'<span class="tag d">{b(m["d"] or RN[m["r"]][0], m["de"] or RN[m["r"]][1])}</span>'+''.join(f'<span class="tag">{b(*SV[s])}</span>' for s in m['s'])
    acts=''.join(f'<a class="{"call" if i==0 else ""}" href="tel:+852{t.replace(" ","")}">☎ {t}</a>' for i,t in enumerate(tel))
    if m['a']: acts+=f'<a href="{mp}" target="_blank" rel="noopener">{b("地圖","Map")} ↗</a>'
    badge=f'<span class="badge">{b("會長單位","Council")}</span>' if m['c'] else ''
    return f'<article class="m-card"><div class="m-top"><h3 class="m-name">{H.escape(m["n"])}</h3>{badge}</div><div class="m-meta">{tags}</div>'+(f'<div class="m-addr">{H.escape(m["a"])}</div>' if m['a'] else '')+f'<div class="m-actions">{acts}</div></article>'
def sorted_members(lst):
    return sorted(lst,key=lambda m:(not m['c'],m['de'] or 'zz',m['n']))

members_js = 'window.HKAWDA_MEMBERS = ' + json.dumps(M, ensure_ascii=False, indent=0) + ';\n'
open(OUT+'assets/js/members-data.js','w').write('/* 會員名錄資料 Member directory data.\n   n=公司名 a=地址 t=電話 f=傳真 r=區域(hki/kln/nt) d/de=地區 c=會長單位 s=業務(alu/glass/gate/steel/reno) */\n'+members_js)
dirpage = page_title('find-installer.html','搵會員工程公司','Find an installer','搵會員工程公司','Find an HKAWDA member firm',
  f'按地區、業務或公司名稱搜尋 {len(M)} 間聯會會員公司。致電前可先比較地點，並向最少兩至三間公司索取書面報價。',
  f'Search {len(M)} member firms by area, trade or name. We suggest getting written quotations from at least two or three firms.') + f'''
<section style="padding-top:36px"><div class="wrap dir-layout">
 <aside class="filters" aria-label="篩選 Filters">
  <div class="field"><label for="f-q">關鍵字 KEYWORD</label><input id="f-q" type="search" placeholder="公司名、街道、電話 Name, street, phone"></div>
  <div style="display:grid;gap:8px"><h3>{b("區域","Region")}</h3><div class="seg" id="f-region"></div></div>
  <div class="field"><label for="f-district">地區 DISTRICT</label><select id="f-district"></select></div>
  <div style="display:grid;gap:8px"><h3>{b("業務","Trade")}</h3><div class="chips" id="f-svc"></div></div>
  <label class="toggle" for="f-council"><input type="checkbox" id="f-council"><span>{b("只顯示會長單位","Council member firms only")}</span></label>
  <button class="btn ghost" type="button" id="f-reset">{b("重設","Reset filters")}</button>
 </aside>
 <div style="min-width:0">
  <div class="dir-bar"><div class="dir-count" id="count" aria-live="polite"></div></div>
  <div class="results" id="results">{"".join(card(m) for m in sorted_members(M))}</div>
  <div style="display:grid;gap:10px;margin-top:28px"><h2 class="dist-h">{b("按地區瀏覽","Browse by district")}</h2><div class="chips">{''.join(f'<a class="chip" href="{dslug(e)}">{b(z,e)}</a>' for z,e in sorted({(m['d'],m['de']) for m in M if m['d']}, key=lambda x:x[1]))}</div></div>
  <div class="note" style="margin-top:24px">{p("名錄資料由會員提供，聯會會定期更新。業務分類按公司名稱整理，僅供參考。聯會不就個別工程的質素、價格或合約作出保證，業主應自行比較報價並簽訂書面合約。資料有誤或需更新，請電郵 "+C['email']+"。",
  "Listings are supplied by members and updated regularly. Trade tags are based on company names and are for reference only. The Association does not guarantee the quality, price or contract terms of any individual job; please compare quotations and sign a written contract. To correct a listing, email "+C['email']+".")}</div>
 </div>
</div></section>'''
write('find-installer.html', dirpage, '搵會員工程公司', 'Find an installer',
      '按地區搜尋香港鋁門窗同業聯會會員：鋁窗、鋁門、玻璃及鋼閘工程公司。Search HKAWDA member installers by district.',
      '<script src="assets/js/members-data.js"></script>\n<script src="assets/js/directory.js"></script>')

# ================= REGION LANDING PAGES (SEO) =================
for k,(rz,re_) in RN.items():
    lst=[m for m in M if m['r']==k]
    byd=collections.OrderedDict()
    for m in sorted(lst,key=lambda m:(m['de'] or 'zz')):
        byd.setdefault((m['d'] or rz, m['de'] or re_),[]).append(m)
    toc=''.join(f'<a class="chip" href="{dslug(de)}">{b(dz,de)} <span class="mono">{len(v)}</span></a>' for (dz,de),v in byd.items())
    secs=''.join(f'''<div class="dist-block" id="d-{de.replace(" ","-").replace("&","and").lower()}"><h2 class="dist-h"><a href="{dslug(de)}">{b(dz+"鋁窗工程公司",de+" installers")}</a> <span class="mono">{len(v)}</span></h2><div class="results">{"".join(card(m) for m in sorted_members(v))}</div></div>''' for (dz,de),v in byd.items())
    body=page_title(RSLUG[k],rz+'會員',re_+' members',f'{rz}鋁窗、鋁門工程公司',f'Aluminium window &amp; door installers in {re_}',
      f'{rz}共有 {len(lst)} 間香港鋁門窗同業聯會會員公司，按地區列出地址及電話，方便業主更換或維修鋁窗時查詢。',
      f'{len(lst)} HKAWDA member firms in {re_}, listed by district with address and phone, for homeowners replacing or repairing aluminium windows.')+f'''
<section style="padding-top:28px"><div class="wrap" style="display:grid;gap:28px">
 <nav class="chips" aria-label="{rz}">{toc}</nav>
 {secs}
 <div class="btn-row"><a class="btn red" href="find-installer.html">{b("進階搜尋全港會員","Search all members")}</a><a class="btn ghost" href="homeowners.html">{b("更換鋁窗指南","Homeowner guide")}</a></div>
 <div class="note">{p("名錄資料由會員提供，聯會不就個別工程的質素、價格或合約作出保證。","Listings are supplied by members. The Association does not guarantee the quality, price or terms of any individual job.")}</div>
</div></section>'''
    write(RSLUG[k], body, f'{rz}鋁窗工程公司', f'{re_} window installers',
          f'{rz}鋁窗、鋁門及玻璃工程公司名單（{"、".join(d for d,_ in byd.keys())}）：香港鋁門窗同業聯會會員地址及電話。Aluminium window installers in {re_}, Hong Kong: HKAWDA member firms by district.')

BD_WIN = 'https://www.bd.gov.hk/en/building-works/minor-works/minor-works-related-to-windows/index.html'
BD_MWIS = 'https://www.bd.gov.hk/en/safety-inspection/mwis/index.html'
# ================= SEO CONTENT PAGES: housing types, problems, districts =================
BD_NTEH = 'https://www.bd.gov.hk/en/safety-inspection/ubw/UBW-in-new-territories-exempted-houses/index_ubw_nteh_intro.html'
HA_TTP = 'https://www.housingauthority.gov.hk/common/pdf/public-housing/estate-maintenance-and-improvement/tenant-to-pay-ttp-repair-items/Tenant-to-pay-TTP-Repairs-Items-TC.pdf'
SRC = {
 'win': (BD_WIN, '屋宇署：與窗戶相關的小型工程', 'Buildings Department: minor works related to windows'),
 'mwis': (BD_MWIS, '屋宇署：強制驗窗計劃', 'Buildings Department: Mandatory Window Inspection Scheme'),
 'nteh': (BD_NTEH, '屋宇署：新界豁免管制屋宇', 'Buildings Department: New Territories Exempted Houses'),
 'ttp': (HA_TTP, '房屋委員會：租戶自費維修項目（PDF）', 'Housing Authority: tenant-to-pay repair items (PDF)'),
}

HOUSING = [
 ('housing-private.html','私人住宅','Private flats','私人住宅更換鋁窗指南','Replacing windows in a private flat',
  '私人樓宇業主更換鋁窗前要知道的責任、規定及大廈管理安排。','What private flat owners need to know about responsibility, rules and building management before replacing windows.',
  [('誰負責','Who is responsible',[('單位內的窗戶一般由業主負責保養、維修及更換。外牆或公用部分的窗戶，責任一般按大廈公契由業主立案法團或管理公司處理。','Windows inside your flat are generally the owner\'s responsibility to maintain, repair and replace. Windows on common parts are usually handled by the owners\' corporation or management company under the deed of mutual covenant (DMC).')],None),
   ('要遵守的規定','The rules',[('更換窗戶一般屬屋宇署「小型工程」，須由已註冊並具相關資格的承建商進行及提交文件。','Replacing a window is usually a Buildings Department "minor works" item, carried out and submitted by a suitably registered contractor.'),
     ('樓齡十年或以上的大廈（三層或以下的住用建築物除外）屬強制驗窗計劃範圍，收到法定通知的業主須委任合資格人士檢驗。','Buildings aged ten years or more (except domestic buildings of three storeys or fewer) fall under the Mandatory Window Inspection Scheme; owners served a notice must appoint a qualified person.')],None),
   ('動工前','Before work starts',None,[('通知管理處，了解施工時間、搬運路線、升降機保護及工程按金安排。','Tell the management office and check working hours, delivery routes, lift protection and any works deposit.'),
     ('查閱大廈公契或管理規則，部分大廈對外牆窗戶的顏色及款式有統一要求。','Check the DMC or house rules: some buildings require a uniform window colour and style on the façade.'),
     ('向最少兩至三間會員公司索取書面報價。','Get written quotations from at least two or three member firms.')])],
  ['win','mwis']),
 ('housing-tong-lau.html','唐樓','Tong lau (walk-ups)','唐樓更換窗戶指南','Replacing windows in a tong lau',
  '舊式唐樓的窗戶較易出現鏽蝕及鬆脫，更換前要留意驗窗規定及搬運安排。','Windows in older walk-up buildings are prone to rust and loosening. Here is what to check before replacing them.',
  [('唐樓窗戶常見問題','Common problems',[('唐樓樓齡普遍較高，部分仍使用舊式鐵窗或早期鋁窗，鉸位、鉚釘及窗框較易鏽蝕或鬆脫，須特別留意安全。','Tong lau are generally old, and some still have steel or early aluminium windows. Hinges, rivets and frames are prone to rust and loosening, so safety needs extra attention.')],None),
   ('驗窗及規定','Inspection and rules',[('超過三層的唐樓如樓齡達十年或以上，屬強制驗窗計劃範圍。收到通知後，須委任合資格人士檢驗，所需修葺由註冊承建商在其監督下進行。','Tong lau of more than three storeys and aged ten years or more fall under the Mandatory Window Inspection Scheme. After a notice, appoint a qualified person to inspect; any repairs are carried out by a registered contractor under their supervision.'),
     ('由舊式鐵窗改為鋁窗屬更換窗戶，同樣受小型工程制度規管。','Changing old steel windows to aluminium is a window replacement and is covered by the minor works system in the same way.')],None),
   ('施工安排','Practical arrangements',None,[('很多唐樓沒有管理公司，動工前宜先通知鄰居，協調施工時間。','Many tong lau have no management company, so let neighbours know and agree working hours.'),
     ('樓梯較窄，大型窗框可能需要分件運送或吊運，報價時要問清楚。','Staircases are narrow; large frames may need to be split or hoisted, so ask about this when getting quotes.'),
     ('同一幢大廈多戶一齊更換，可方便協調及驗窗安排。','If several flats in the building replace windows together, coordination and inspection are simpler.')])],
  ['mwis','win']),
 ('housing-hos.html','居屋','HOS flats','居屋更換鋁窗指南','Replacing windows in a HOS flat',
  '居屋業主更換鋁窗前要知道的責任、驗窗及屋苑管理要求。','What Home Ownership Scheme owners need to know before replacing windows.',
  [('誰負責','Who is responsible',[('購買居屋後，單位內窗戶的保養及更換一般由業主自行負責，屋苑公用部分則由業主立案法團或管理公司處理。','Once you own a HOS flat, maintaining and replacing the windows inside it is generally your responsibility; common parts are handled by the owners\' corporation or management company.')],None),
   ('驗窗及規定','Inspection and rules',[('樓齡十年或以上的居屋大廈同樣可能收到強制驗窗通知。更換窗戶一般屬小型工程，須由合資格的註冊承建商進行。','HOS blocks aged ten years or more may also be served Mandatory Window Inspection notices. Replacing windows is usually minor works and must be done by a suitably registered contractor.')],None),
   ('動工前','Before work starts',None,[('聯絡屋苑管理處，了解裝修申請、施工時間及外觀要求。','Contact the estate management office about renovation applications, working hours and appearance requirements.'),
     ('屋苑內同款單位眾多，可向管理處或鄰居了解原裝窗戶型號及尺寸。','Many flats share the same layout; the office or neighbours may know the original window type and sizes.'),
     ('索取書面報價時，列明型材系列、玻璃種類及五金物料。','Ask for written quotes that list the profile series, glass type and hardware.')])],
  ['mwis','win']),
 ('housing-public-rental.html','公屋','Public rental housing','公屋窗戶維修須知','Window repairs in public rental housing',
  '公屋單位屬房屋委員會物業。窗戶有問題，先聯絡屋邨辦事處。','Public rental flats belong to the Housing Authority. If a window has a problem, contact your estate office first.',
  [('先聯絡屋邨辦事處','Contact the estate office first',[('公屋單位屬房屋委員會物業。房委會負責單位內固定裝置的正常損耗維修，但窗門玻璃除外。窗戶有問題，應先向屋邨辦事處報修，不宜自行聘請承辦商拆換窗戶。','Public rental flats are Housing Authority property. The Authority repairs normal wear and tear of fixtures in the flat, except window and door glass. Report window problems to your estate office rather than hiring a contractor to remove or replace windows yourself.')],None),
   ('租戶自費項目','Tenant-to-pay items',[('部分維修項目屬「租戶自費維修項目」，例如供應及安裝窗門玻璃、更換窗門抽手或鉸。收費由房屋署公布，並每年檢討，詳情可向屋邨辦事處查詢。','Some repairs are "tenant-to-pay" items, such as supplying and fitting window or door glass, or replacing window handles or hinges. Charges are set by the Housing Department and reviewed annually; ask your estate office for details.')],None),
   ('日常安全','Everyday safety',None,[('定期檢查窗鉸、窗扣有沒有鬆脫或生鏽，發現問題盡快報修。','Check hinges and latches regularly for looseness or rust, and report problems promptly.'),
     ('颱風前關好所有窗戶並扣緊。','Close and latch every window before a typhoon.'),
     ('如你住在私人樓宇或居屋，可在會員名錄搵會員工程公司。','If you live in a private or HOS flat, you can find a member firm in the directory.')])],
  ['ttp']),
 ('housing-village-house.html','村屋','Village houses','村屋更換鋁窗及趟門指南','Windows and sliding doors for village houses',
  '新界村屋的規管與市區樓宇不同。更換窗戶、加建玻璃屋前要知道的事。','Village houses in the New Territories are regulated differently from urban flats. What to know before replacing windows or adding a glass room.',
  [('村屋的規管','How village houses are regulated',[('新界豁免管制屋宇（村屋）獲豁免《建築物條例》部分條文，一般毋須事先取得屋宇署批准才動工。但如工程令屋宇超出豁免準則（例如不超過三層、高度不超過 8.23 米、上蓋面積不超過 65.03 平方米），豁免可能失效。','New Territories Exempted Houses (village houses) are exempt from parts of the Buildings Ordinance and generally do not need prior Buildings Department approval to start works. But if works take the house beyond the exemption criteria (such as no more than three storeys, 8.23 m high and a 65.03 m² roofed-over area), the exemption may be lost.'),
     ('樓高不超過三層的住用建築物不在強制驗窗計劃範圍內，大部分村屋屬此類，但窗戶仍需業主定期檢查保養。','Domestic buildings of three storeys or fewer are outside the Mandatory Window Inspection Scheme, which covers most village houses, but owners should still inspect and maintain their windows.')],None),
   ('村屋常見工程','Common village house jobs',None,[('大面積落地趟門、摺門及露台門。','Large sliding, folding and balcony doors.'),
     ('近海或空曠地方風壓較大，要選用合適的型材及玻璃厚度。','Open and coastal sites face stronger wind, so choose suitable profiles and glass thickness.'),
     ('天台玻璃屋、簷篷等加建可能屬違例建築工程，動工前應先查詢。','Rooftop glass rooms and canopies may count as unauthorised building works; check before building.')])],
  ['nteh']),
]

PROBLEMS = [
 ('window-leak.html','鋁窗漏水','Leaking windows','鋁窗漏水點算好？','Why is my aluminium window leaking?',
  '落雨時窗邊滲水，常見原因及處理方法。','Common causes of water coming in around a window, and what to do.',
  [('常見原因','Common causes',None,[('窗框與牆身之間的防水膠老化或開裂。','Sealant between the frame and the wall has aged or cracked.'),
     ('窗台或趟窗路軌的去水孔被塵埃堵塞。','Drain holes in the sill or sliding track are blocked with dirt.'),
     ('窗扇膠條老化變硬，關窗後仍有縫隙。','Sash gaskets have hardened and no longer seal.'),
     ('窗扇變形或鉸位下墮，窗扇未能貼合窗框。','A warped sash or sagging hinge stops the sash sitting flush.')]),
   ('自己可以做的','What you can do yourself',None,[('清理路軌及去水孔的塵埃和雜物。','Clear dust and debris from tracks and drain holes.'),
     ('記錄漏水位置及天氣情況，方便師傅判斷。','Note where and in what weather it leaks, to help the contractor diagnose it.'),
     ('切勿自行攀出窗外或在高處外牆施工。','Never climb outside or work on the external wall at height yourself.')]),
   ('需要師傅處理','When to call a member firm',[('重新打防水膠、更換膠條，或調整、更換窗鉸，一般可解決大部分漏水問題；窗框嚴重損壞則需要更換窗戶。如漏水涉及外牆或大廈公用部分，應同時通知管理處。','Resealing, replacing gaskets or adjusting the hinges fixes most leaks; a badly damaged frame means replacing the window. If the leak involves the external wall or common parts, also tell the management office.')],None)],
  ['win']),
 ('window-hinge-rust.html','窗鉸生鏽','Rusty hinges','窗鉸生鏽、窗扇下墮要點處理？','Rusty hinges and sagging windows',
  '窗鉸及鉚釘是窗戶安全的關鍵。出現這些情況，應盡快處理。','Hinges and rivets are what keep a window safely in place. If you see these signs, act quickly.',
  [('危險訊號','Warning signs',None,[('窗鉸或鉚釘生鏽、鬆脫或缺失。','Hinges or rivets are rusty, loose or missing.'),
     ('窗扇下墮、搖晃，或開關時有異聲。','The sash sags, wobbles or makes noise when opened.'),
     ('窗扇難以關上或扣緊。','The sash is hard to close or latch.')]),
   ('發現問題時','What to do',[('停止開啟有問題的窗扇，並盡快聯絡會員公司檢查。窗扇從高處墮下可造成嚴重傷亡。','Stop opening the affected sash and have a member firm inspect it promptly. A sash falling from height can cause serious injury.')],None),
   ('更換窗鉸','Replacing hinges',[('更換時宜選用不銹鋼摩擦鉸及鉚釘，並按窗扇尺寸及重量選擇合適規格。報價時要求列明物料。','Use stainless-steel friction stays and rivets sized for the sash dimensions and weight, and ask for materials to be listed in the quotation.')],None)],
  ['mwis']),
 ('window-latch.html','窗關唔埋','Windows that won\'t close','窗扣壞、窗關唔埋點算？','Broken latch or a window that won\'t close',
  '窗戶關不緊，颱風時有機會被吹開。常見原因及處理。','A window that won\'t close properly can blow open in a typhoon. Causes and fixes.',
  [('常見原因','Common causes',None,[('窗扣損壞或鬆脫。','The latch is broken or loose.'),
     ('窗鉸磨損，令窗扇下墮對唔準。','Worn hinges make the sash drop out of line.'),
     ('膠條變形或窗扇變形。','Deformed gaskets or a warped sash.')]),
   ('處理方法','Fixes',[('更換窗扣或調整、更換窗鉸，一般可以解決。窗扇或窗框變形嚴重，則要考慮更換窗戶。在修好之前，颱風期間要特別留意。','Replacing the latch or adjusting or replacing the hinges usually solves it. If the sash or frame is badly warped, consider replacing the window. Until it is fixed, take extra care in typhoons.')],None)],
  ['win']),
 ('window-inspection-notice.html','收到驗窗通知','Window inspection notice','收到強制驗窗通知，要做甚麼？','Served a Mandatory Window Inspection notice?',
  '屋宇署強制驗窗計劃的步驟，一頁看清。','The steps of the Buildings Department\'s Mandatory Window Inspection Scheme, on one page.',
  [('計劃範圍','Who is covered',[('強制驗窗計劃涵蓋樓齡十年或以上的樓宇，三層或以下的住用建築物除外。','The scheme covers buildings aged ten years or more, except domestic buildings of three storeys or fewer.')],None),
   ('處理步驟','Steps',None,[('細閱通知，留意遵辦期限。','Read the notice carefully and note the deadline.'),
     ('委任合資格人士（QP），檢驗單位內所有窗戶。','Appoint a qualified person (QP) to inspect all the windows in your flat.'),
     ('如需修葺，由註冊承建商在合資格人士監督下進行。','If repairs are needed, a registered contractor carries them out under the QP\'s supervision.'),
     ('完成後由合資格人士向屋宇署提交所需文件。','The QP then submits the required documents to the Buildings Department.')]),
   ('實用提示','Tips',[('同一大廈多戶同時收到通知，可透過法團或管理處一齊安排，較易協調。如有疑問，請以屋宇署的資料為準。','When many flats in a building receive notices, arranging inspection together through the owners\' corporation or management office is easier. If in doubt, follow the Buildings Department\'s guidance.')],None)],
  ['mwis','win']),
 ('soundproof-windows.html','隔音窗','Soundproof windows','想裝隔音窗？要知道的事','Thinking about soundproof windows?',
  '近馬路、天橋或工地，隔音窗可以改善生活質素。揀選時的重點。','Near a road, flyover or building site, soundproof windows can make a big difference. What to look for.',
  [('隔音效果取決於','What makes a window quiet',None,[('密封：窗扇與窗框之間的膠條及窗框四周的密封，往往比玻璃本身更重要。','Sealing: gaskets and the seal around the frame often matter more than the glass itself.'),
     ('玻璃：夾層玻璃或中空玻璃，一般較單層玻璃隔音。','Glass: laminated or insulated glazing generally blocks more noise than a single pane.'),
     ('開啟方式：平開窗關閉後一般較推拉窗密封。','Opening type: a closed casement usually seals better than a sliding window.')]),
   ('揀選建議','Advice',[('向會員公司說明噪音來源及時段，請對方建議合適的玻璃及窗型，並在報價中列明玻璃結構及厚度。更換外牆窗戶一般屬小型工程，須由合資格承建商進行。','Tell the member firm where and when the noise comes from, ask for a suitable glass and window type, and get the glass make-up and thickness written into the quotation. Replacing external windows is usually minor works and must be done by a qualified contractor.')],None)],
  ['win']),
 ('typhoon-window-check.html','颱風前檢查','Typhoon check','颱風前窗戶檢查清單','Typhoon window checklist',
  '颱風來臨前，花十分鐘檢查窗戶，減少意外。','Ten minutes checking your windows before a typhoon can prevent accidents.',
  [('颱風前','Before the typhoon',None,[('關好所有窗戶並扣緊窗扣。','Close every window and lock the latches.'),
     ('檢查窗鉸、鉚釘有沒有鬆脫或生鏽。','Check hinges and rivets for looseness or rust.'),
     ('移走窗台及露台上的花盆、雜物。','Remove flowerpots and loose items from sills and balconies.'),
     ('拉上窗簾，減少玻璃破裂時碎片飛散。','Draw the curtains to reduce flying glass if a pane breaks.')]),
   ('颱風後','After the typhoon',None,[('檢查窗扇是否鬆脫、變形或關不緊。','Check whether any sash is loose, bent or won\'t close.'),
     ('如有損壞，避免開啟該窗扇，並盡快聯絡會員公司檢查。','If anything is damaged, keep that sash shut and have a member firm inspect it promptly.')])],
  ['mwis']),
]

def section_html(eyz, eye, items_p, items_l, alt=False):
    body = ''.join(p(z, e) for z, e in (items_p or []))
    if items_l:
        body += '<ol class="olist">' + ''.join(f'<li><div>{p(z,e)}</div></li>' for z, e in items_l) + '</ol>'
    return f'<div class="guide-sec"><h2>{b(eyz, eye)}</h2>{body}</div>'

def related_html(current):
    hz = ''.join(f'<a class="chip" href="{s}">{b(z,e)}</a>' for s,z,e,*_ in HOUSING if s != current)
    pz = ''.join(f'<a class="chip" href="{s}">{b(z,e)}</a>' for s,z,e,*_ in PROBLEMS if s != current)
    return f'''<aside class="related">
  <div style="display:grid;gap:10px"><h3>{b("按住宅類型","By type of home")}</h3><div class="chips">{hz}</div></div>
  <div style="display:grid;gap:10px"><h3>{b("常見窗戶問題","Common window problems")}</h3><div class="chips">{pz}</div></div>
 </aside>'''

def guide_page(slug, kz, ke, hz, he, lz, le, secs, srcs, kind):
    secs_html = ''.join(section_html(a, c, d, e) for a, c, d, e in secs)
    src_html = ''.join(f'<li><a class="ext" href="{SRC[s][0]}" target="_blank" rel="noopener">{b(SRC[s][1], SRC[s][2])} ↗</a></li>' for s in srcs)
    crumb = ('業主指南', 'Homeowner guide')
    body = page_title(slug, crumb[0], crumb[1], hz, he, lz, le) + f'''
<section><div class="wrap guide-layout">
 <article class="guide-body">
  {secs_html}
  <div class="guide-sec"><h2>{b("官方資料","Official sources")}</h2><ul class="src-list">{src_html}</ul>
   {p("本頁只供一般參考，並非法律意見；規定如有更新，以政府部門公布為準。","This page is general guidance, not legal advice. If rules change, the government department's information prevails.","note")}</div>
 </article>
 <aside class="guide-side">
  <div class="cta-card"><h3>{b("搵會員工程公司","Find a member firm")}</h3>{p("按地區搵聯會會員，索取書面報價。","Find HKAWDA members by district and get written quotes.")}
   <a class="btn red" href="find-installer.html">{b("搵會員工程公司","Find an installer")}</a>
   <div class="chips">{''.join(f'<a class="chip" href="{RSLUG[k]}">{b(*RN[k])}</a>' for k in RN)}</div></div>
 </aside>
</div></section>
<section class="alt"><div class="wrap">{related_html(slug)}</div></section>'''
    title = (f'{hz}｜香港鋁門窗同業聯會', f'{he} | HKAWDA Hong Kong')
    write(slug, body, kz, ke, f'{lz}{le}', title=title)

for (slug, kz, ke, hz, he, lz, le, secs, srcs) in HOUSING:
    guide_page(slug, kz, ke, hz, he, lz, le, secs, srcs, 'housing')
for (slug, kz, ke, hz, he, lz, le, secs, srcs) in PROBLEMS:
    guide_page(slug, kz, ke, hz, he, lz, le, secs, srcs, 'problem')

# ---- district pages ----
def dslug(de): return 'district-' + de.lower().replace(' & ', '-').replace(' ', '-') + '.html'
DISTRICTS = collections.OrderedDict()
for m in sorted(M, key=lambda m: m['de'] or 'zz'):
    if m['d']: DISTRICTS.setdefault((m['d'], m['de'], m['r']), []).append(m)
for (dz, de, r), lst in DISTRICTS.items():
    nearby = ''.join(f'<a class="chip" href="{dslug(e2)}">{b(z2,e2)} <span class="mono">{len(l2)}</span></a>' for (z2, e2, r2), l2 in DISTRICTS.items() if r2 == r and e2 != de)
    body = page_title(dslug(de), dz, de, f'{dz}鋁窗工程公司', f'Aluminium window &amp; door installers in {de}',
        f'{dz}區共有 {len(lst)} 間香港鋁門窗同業聯會會員公司。更換或維修鋁窗、鋁門及玻璃，可直接致電查詢及索取書面報價。',
        f'{len(lst)} HKAWDA member firm{"s" if len(lst)>1 else ""} in {de}. Call them directly about replacing or repairing aluminium windows, doors and glass, and ask for a written quotation.') + f'''
<section style="padding-top:28px"><div class="wrap" style="display:grid;gap:28px">
 <div class="results">{"".join(card(m) for m in sorted_members(lst))}</div>
 <div style="display:grid;gap:10px"><h2 class="dist-h">{b(RN[r][0]+"其他地區","Other districts in "+RN[r][1])}</h2><div class="chips">{nearby}</div></div>
 <div class="btn-row"><a class="btn red" href="find-installer.html">{b("搜尋全港會員","Search all members")}</a><a class="btn ghost" href="homeowners.html">{b("更換鋁窗指南","Homeowner guide")}</a></div>
 <div class="note">{p("名錄資料由會員提供，聯會不就個別工程的質素、價格或合約作出保證。","Listings are supplied by members. The Association does not guarantee the quality, price or terms of any individual job.")}</div>
</div></section>
<section class="alt"><div class="wrap">{related_html('')}</div></section>'''
    write(dslug(de), body, f'{dz}鋁窗', f'{de} windows',
          f'{dz}鋁窗、鋁門及玻璃工程公司：{len(lst)} 間香港鋁門窗同業聯會會員的地址及電話，換鋁窗、鋁窗維修可直接查詢。Aluminium window installers in {de}, Hong Kong: HKAWDA member firms with address and phone.',
          title=(f'{dz}鋁窗工程公司｜{dz}換鋁窗、鋁窗維修｜HKAWDA', f'Aluminium Window Installers in {de}, Hong Kong | HKAWDA'))

# ================= HOMEOWNER GUIDE =================
guide = page_title('homeowners.html','業主指南','Homeowner guide','更換鋁窗業主指南','Replacing aluminium windows in Hong Kong: a homeowner guide',
 '由規定、報價到驗收，一頁看清更換鋁窗要注意的事項。','What to check before, during and after replacing your windows, on one page.') + f'''
<section id="rules"><div class="wrap two">
 <div style="display:grid;gap:18px">
  <div class="eyebrow">規定 THE RULES</div>
  <h2><span class="zh">更換窗戶屬「小型工程」</span><span class="en" lang="en">Window replacement is "minor works"</span></h2>
  <div class="prose">
  {p("根據屋宇署的小型工程監管制度，修葺或更換窗戶一般屬第 I、II 或 III 級小型工程，視乎窗戶離地高度、窗框大小及是否涉及主窗框而定。例如離地 3.5 米以下的窗戶工程，一般屬第 III 級項目 3.6。","Under the Buildings Department's Minor Works Control System, repairing or replacing a window is usually a Class I, II or III minor works item, depending on height above ground, frame size and whether the main frame is involved. Works no more than 3.5 m above ground, for example, generally fall under Class III item 3.6.")}
  {p("這類工程須由已在屋宇署註冊、具相關級別及類型資格的承建商進行，並按規定向屋宇署提交文件。簽約前，請要求承建商說明工程屬哪一級別及項目，以及由誰負責提交。","The work must be carried out by a contractor registered with the Buildings Department for the relevant class and type, with the required documents submitted to the Department. Before signing, ask the contractor which class and item applies and who will make the submission.")}
  </div>
  <a class="ext" href="{BD_WIN}" target="_blank" rel="noopener">屋宇署：與窗戶相關的小型工程 Buildings Department: minor works related to windows ↗</a>
 </div>
 <div style="display:grid;gap:18px">
  <div class="eyebrow">強制驗窗 MWIS</div>
  <h2><span class="zh">收到驗窗通知怎麼辦？</span><span class="en" lang="en">Served a window inspection notice?</span></h2>
  <div class="prose">
  {p("屋宇署的強制驗窗計劃涵蓋樓齡十年或以上的私人樓宇。收到法定通知的業主，須委任合資格人士檢驗窗戶，並由註冊承建商進行所需的修葺或更換。","The Buildings Department's Mandatory Window Inspection Scheme covers private buildings aged ten years or more. Owners served a statutory notice must appoint a qualified person to inspect their windows, with any repair or replacement carried out by a registered contractor.")}
  {p("不少聯會會員熟悉驗窗及維修流程，可在報價時一併查詢。","Many members are familiar with the inspection and repair process; ask about it when you request a quotation.")}
  </div>
  <a class="ext" href="{BD_MWIS}" target="_blank" rel="noopener">屋宇署：強制驗窗計劃 Buildings Department: MWIS ↗</a>
 </div>
</div></section>

<section class="alt" id="quote"><div class="wrap">
 <div class="sec-head"><div class="eyebrow">報價 QUOTATIONS</div>
  <h2><span class="zh">書面報價應列明的項目</span><span class="en" lang="en">What a written quotation should include</span></h2>
  {p("比較報價時，價錢以外更要比較用料及責任範圍。","When comparing quotes, compare materials and responsibilities, not only price.","lede")}</div>
 <div class="cards">
  <div class="card"><div class="k">01 窗框 FRAME</div><h3>{b("鋁型材系列及厚度","Profile series and wall thickness")}</h3>{p("例如 50 系列、70 系列，以及鋁材壁厚和表面處理（粉末噴塗、陽極氧化）。","e.g. 50 or 70 series, wall thickness and finish (powder-coated or anodised).")}</div>
  <div class="card"><div class="k">02 玻璃 GLASS</div><h3>{b("玻璃種類及厚度","Glass type and thickness")}</h3>{p("強化、夾層或中空玻璃，以及厚度（mm）。","Tempered, laminated or insulated glazing, and thickness in mm.")}</div>
  <div class="card"><div class="k">03 五金 HARDWARE</div><h3>{b("鉸、窗扣及鉚釘","Hinges, latches and rivets")}</h3>{p("列明不銹鋼摩擦鉸、窗扣及鉚釘的物料及品牌。","Material and brand of stainless-steel friction stays, latches and rivets.")}</div>
  <div class="card"><div class="k">04 工序 SCOPE</div><h3>{b("拆舊、防水及清理","Removal, sealing and clean-up")}</h3>{p("是否包括拆除舊窗、填補防水膠、運走廢料及修補批盪。","Whether it covers removing the old window, sealing, debris disposal and making good.")}</div>
  <div class="card"><div class="k">05 法規 COMPLIANCE</div><h3>{b("小型工程提交","Minor works submission")}</h3>{p("工程級別及項目、負責提交的註冊承建商名稱及註冊編號。","Class and item, and the name and registration number of the registered contractor making the submission.")}</div>
  <div class="card"><div class="k">06 保養 WARRANTY</div><h3>{b("保養期及付款安排","Warranty and payment terms")}</h3>{p("保養年期、範圍，以及按進度分期付款，避免一次過全數預付。","Warranty period and scope, and stage payments rather than full payment upfront.")}</div>
 </div>
</div></section>

<section id="checklist"><div class="wrap two">
 <div style="display:grid;gap:18px">
  <div class="eyebrow">驗收 HANDOVER</div>
  <h2><span class="zh">完工驗收清單</span><span class="en" lang="en">Handover checklist</span></h2>
  <ol class="olist">
   <li><div>{p("開關每扇窗數次，確認順暢、扣緊時密合。","Open and close every sash several times; it should run smoothly and seal when latched.")}</div></li>
   <li><div>{p("檢查窗框四周防水膠是否連續，沒有裂縫或空隙。","Check the sealant around the frame is continuous with no gaps or cracks.")}</div></li>
   <li><div>{p("核對玻璃、五金及型材是否與報價一致。","Confirm glass, hardware and profiles match the quotation.")}</div></li>
   <li><div>{p("索取保養單據，以及屋宇署小型工程提交文件副本。","Collect the warranty and copies of the minor works submission documents.")}</div></li>
   <li><div>{p("確認工地清理妥當，廢料已運走。","Make sure the site is cleaned and debris removed.")}</div></li>
  </ol>
 </div>
 <div style="display:grid;gap:18px">
  <div class="eyebrow">保養 MAINTENANCE</div>
  <h2><span class="zh">日常窗戶安全</span><span class="en" lang="en">Everyday window safety</span></h2>
  <ol class="olist">
   <li><div>{p("定期檢查鉸位及鉚釘有沒有生鏽、鬆脫或缺失。","Regularly check hinges and rivets for rust, looseness or missing parts.")}</div></li>
   <li><div>{p("窗扣應能扣緊；颱風前確保所有窗戶關好扣緊。","Latches should lock firmly; close and latch every window before a typhoon.")}</div></li>
   <li><div>{p("不要在窗外晾掛重物，亦不要用力推拉窗扇。","Don't hang heavy items outside windows or force the sashes.")}</div></li>
   <li><div>{p("發現窗扇下墮、搖晃或難以關上，應停止使用並盡快聯絡會員公司檢查。","If a sash sags, wobbles or won't close, stop using it and have a member firm inspect it promptly.")}</div></li>
  </ol>
 </div>
</div></section>

<section id="housing"><div class="wrap">
 <div class="sec-head"><div class="eyebrow">住宅類型 BY TYPE OF HOME</div><h2>{b("按住宅類型","Guides by type of home")}</h2>{p("責任誰屬、要守甚麼規定，視乎你住的是哪類樓宇。","Who is responsible and which rules apply depend on the type of building you live in.","lede")}</div>
 <div class="cards three">{''.join(f'<a class="card link-card" href="{s}"><h3>{b(z,e)}</h3>{p(lz,le)}<span class="go">{b("閱讀指南 →","Read guide →")}</span></a>' for s,z,e,hz,he,lz,le,*_ in HOUSING)}</div>
</div></section>

<section class="alt" id="problems"><div class="wrap">
 <div class="sec-head"><div class="eyebrow">窗戶問題 COMMON PROBLEMS</div><h2>{b("常見窗戶問題","Common window problems")}</h2></div>
 <div class="cards three">{''.join(f'<a class="card link-card" href="{s}"><h3>{b(z,e)}</h3>{p(lz,le)}<span class="go">{b("點樣處理 →","What to do →")}</span></a>' for s,z,e,hz,he,lz,le,*_ in PROBLEMS)}</div>
</div></section>

<section><div class="wrap supplier">
 <div style="display:grid;gap:10px;min-width:0"><div class="eyebrow">{b("指定用料","SPECIFYING MATERIALS")}</div>
  <h2>{b("想指定窗框及玻璃用料？","Want to choose the frame and glass?")}</h2>
  {p("你可以要求會員師傅使用指定廠商的產品，並在報價中列明。聯會創會成員升威 LE-RELAX 是本地鋁門窗及玻璃製造及批發商，自設中山廠房，只供應、不安裝：業主可向師傅指定使用升威。","You can ask your member contractor to use a named manufacturer's products and list them in the quotation. HKAWDA founding member LE-RELAX manufactures and wholesales aluminium windows, doors and glass from its own Zhongshan factory. It supplies only and does not install, so ask your contractor to specify LE-RELAX.")}</div>
 <a class="btn ghost" href="{LR}" target="_blank" rel="noopener">{b("升威 LE-RELAX","LE-RELAX")} ↗</a>
</div></section>

<section class="alt" id="faq"><div class="wrap">
 <div class="sec-head"><div class="eyebrow">常見問題 FAQ</div><h2><span class="zh">常見問題</span><span class="en" lang="en">Frequently asked questions</span></h2></div>
 <div style="max-width:860px">
  <details><summary>{b("聯會會直接承接工程嗎？","Does the Association carry out work itself?")}</summary><div class="ans">{p("不會。聯會是行業組織，工程由會員公司直接向業主報價及承接。你可在會員名錄按地區搜尋。","No. HKAWDA is a trade association; member firms quote for and carry out the work directly. Use the member directory to search by district.")}</div></details>
  <details><summary>{b("如何確認一間公司是聯會會員？","How do I confirm a firm is a member?")}</summary><div class="ans">{p("會員店舖一般貼有聯會認證貼紙，並持有獨立編號會員卡。你可在會員名錄搜尋公司名稱，或電郵 "+C['email']+" 查詢。","Members usually display the HKAWDA sticker and hold a numbered membership card. Search the company name in the directory, or email "+C['email']+".")}</div></details>
  <details><summary>{b("更換一隻窗需要多久？","How long does a window replacement take?")}</summary><div class="ans">{p("視乎窗戶數目、尺寸及訂造時間而定。請向會員公司查詢度尺、訂料及安裝所需時間，並在合約中列明。","It depends on the number and size of windows and fabrication lead time. Ask the firm for measuring, ordering and installation timings and put them in the contract.")}</div></details>
  <details><summary>{b("對會員的工程有意見，可以找聯會嗎？","Can I raise a concern about a member's work?")}</summary><div class="ans">{p("可以。請先與該公司溝通；如未能解決，可電郵聯會反映，我們會跟進了解。聯會並非仲裁機構，合約爭議可尋求消費者委員會或法律意見。","Yes. Please raise it with the firm first; if unresolved, email us and we will follow up. The Association is not an arbitrator; for contract disputes, consider the Consumer Council or legal advice.")}</div></details>
 </div>
</div></section>

<section class="band"><div class="wrap recog" style="grid-template-columns:minmax(0,1fr) auto">
 <div style="display:grid;gap:8px"><h2><span class="zh">準備好了？</span><span class="en" lang="en">Ready to start?</span></h2>{p("按地區搵會員工程公司，索取書面報價。","Find member firms in your district and ask for written quotations.","lede")}</div>
 <a class="btn red" href="find-installer.html">{b("搵會員工程公司","Find an installer")}</a>
</div></section>'''
write('homeowners.html', guide, '業主指南', 'Homeowner guide',
      '在香港更換鋁窗須知：小型工程監管制度、強制驗窗計劃、書面報價要點及驗收清單。How to replace aluminium windows in Hong Kong.')

# ================= ABOUT =================
COUNCIL = ['王志達','張文輝','葉效洪','林榮文','姚卓恩','廖俊杰','劉建枝','劉溪湖','龐道穗','周淩','夏敏','陳海錫','賴飛鴻','何鎮添','彭聲雄','葛國海','謝錦添','吳杏山','梁文超','曾德魚','盧家幟','吳冠偉','林劍偉','郭賢招','盧家鎌','姚雄','梁賀宏','李計德','陳西慶','黃永健','潘偉能','蘇捷']
AIMS = [('推廣發展','Promote','維護業界利益','Protect the interests of the trade'),('互傳資訊','Inform','與政府部門溝通','Liaise with government departments'),
        ('團結業界','Unite','提高業界經營能力','Strengthen members\' businesses'),('加強聯繫','Train','提供業界安裝技術課程','Provide installation skills courses'),
        ('平衡同業','Standardise','訂立業界合理工資及認可資格','Set fair wages and recognised qualifications'),('互動平台','Connect','推廣有意成為鋁門窗工程師之人才，提升產品認知質素及專業資格','Bring new talent into the trade and raise product knowledge and professional standards')]
about = page_title('about.html','關於聯會','About','關於香港鋁門窗同業聯會','About HKAWDA',
 '聯會於 2015 年 11 月 30 日成立，由一眾從事鋁門窗相關業務的同業組成，是業界與政府、與市民之間的溝通橋樑。',
 'Founded on 30 November 2015 by people working in the aluminium window and door trade, HKAWDA is a bridge between the industry, government and the public.') + f'''
<section><div class="wrap two">
 <div class="prose">
  <div class="eyebrow">緣起 OUR STORY</div>
  <h2><span class="zh">為業界發聲，為市民服務</span><span class="en" lang="en">A voice for the trade, a service to the public</span></h2>
  {p("聯會成立前，香港沒有一個正式平台讓市民找到合資格的鋁門窗同業。聯會的首要工作，是編製一份公開的會員名冊，方便市民找到專業師傅進行相關工程。","Before HKAWDA, there was no formal place for the public to find qualified aluminium window firms. Our first task was a public member register so residents could find professionals for their work.")}
  {p("長遠而言，聯會希望為工人提供專業課程、推動設立鋁窗師傅牌照制度，並促請政府為窗戶安裝及維修訂立清晰的標準指引，提高窗戶裝拆的安全性。","Longer term, we aim to provide professional courses for workers, push for a licensing system for window fitters, and urge government to set clear standards for window installation and repair, making installation and removal safer.")}
  {p("聯會亦致力促進同業良性競爭，協助同業拓展市場、培育人才，提升行業的持續發展。","We also encourage healthy competition, help members grow their markets and train new talent for the long-term health of the trade.")}
 </div>
 <figure class="figure-frame" style="margin:0;display:grid;gap:8px"><img src="assets/img/press-takungpao-2015.jpg" alt="《大公報》報道：香港鋁門窗同業聯會成立" loading="lazy"><figcaption class="mono" style="font-size:.78rem;color:var(--muted)">《大公報》社團新訊：香港鋁門窗同業聯會成立 · Ta Kung Pao, 2015</figcaption></figure>
</div></section>

<section class="band" id="founding-member"><div class="wrap two">
 <div class="prose">
  <div class="eyebrow">{b("創會成員","FOUNDING MEMBER")}</div>
  <h2><span class="zh">升威 LE-RELAX</span><span class="en" lang="en">LE-RELAX</span></h2>
  {p("聯會由升威 LE-RELAX 牽頭，聯同一眾業界同行於 2015 年成立，為全港鋁門窗業界而設。升威於 1986 年在香港創立，是本地鋁門窗、浴屏及玻璃製造及批發商，於中山設有自家廠房，由玻璃加工、窗鉸到成品組裝均自家製造，並列入房屋委員會認可供應商名單。","HKAWDA was set up in 2015 on the initiative of LE-RELAX, together with fellow firms, for the whole aluminium window and door trade. Founded in Hong Kong in 1986, LE-RELAX manufactures and wholesales aluminium windows and doors, shower screens and glass from its own factory in Zhongshan, handling glass processing, hinges and final assembly in-house, and is on the Housing Authority's approved supplier list.")}
  {p("升威只做供應，不做安裝。它的客戶是工程公司及師傅，包括不少聯會會員。業主可向會員師傅指定用料。","LE-RELAX supplies only and never installs. Its customers are contractors and fitters, including many HKAWDA members. Homeowners can ask their member contractor to specify its products.")}
  <div class="btn-row"><a class="btn red" href="{LR}" target="_blank" rel="noopener">{b("瀏覽升威 LE-RELAX 網站","Visit LE-RELAX")} ↗</a></div>
 </div>
 <figure class="figure-frame" style="margin:0"><img src="assets/img/zhongshan-2025-factory.jpg" alt="升威 LE-RELAX 中山廠房生產線 LE-RELAX Zhongshan factory" loading="lazy"></figure>
</div></section>

<section class="alt"><div class="wrap">
 <div class="sec-head"><div class="eyebrow">宗旨 OUR AIMS</div><h2><span class="zh">團結業界 · 提升專業</span><span class="en" lang="en">Uniting the trade, raising standards</span></h2></div>
 <div class="aims">{''.join(f'<div class="aim"><b><span class="zh">{a}</span><span class="en" lang="en">{ae}</span></b>{p(c,ce)}</div>' for a,ae,c,ce in AIMS)}</div>
</div></section>

<section><div class="wrap">
 <div class="sec-head"><div class="eyebrow">成果 WHAT WE HAVE DONE</div><h2><span class="zh">聯會的工作</span><span class="en" lang="en">Our track record</span></h2></div>
 <div class="cards">
  <div class="card"><div class="k">屋宇署 BUILDINGS DEPT</div>{p("向屋宇署反映改善收表時間，屋宇署同意改善並重新調配人手。","Raised form-processing times with the Buildings Department, which agreed to improve and redeploy staff.")}</div>
  <div class="card"><div class="k">驗窗卡 INSPECTION CARD</div>{p("聯會獲 TVB 邀請講解業界問題，屋宇署其後新增驗窗卡以識別鋁窗專業人士。","Invited by TVB to explain the trade's concerns; the Buildings Department then introduced a window-inspection card for qualified professionals.")}</div>
  <div class="card"><div class="k">培訓 TRAINING</div>{p("成功爭取職業訓練局開辦鋁窗檢驗相關課程，並與 IVE 合辦行業課程。","Secured VTC agreement to run window-inspection courses, and runs industry courses with IVE.")}</div>
  <div class="card"><div class="k">法律支援 LEGAL</div>{p("會員因牌照問題遭法律起訴時，由聯會顧問律師協助並提供法律意見。","When members faced prosecution over licensing, the Association's legal adviser assisted and gave advice.")}</div>
  <div class="card"><div class="k">考察 FACTORY VISITS</div>{p("舉辦參觀鋁型材廠、玻璃廠及鋁門窗廠，讓會員了解生產過程。","Organised visits to extrusion, glass and window factories so members understand production.")}</div>
 </div>
</div></section>

<section class="alt" id="structure"><div class="wrap" style="display:grid;gap:32px">
 <div class="sec-head" style="margin:0"><div class="eyebrow">組織架構 ORGANISATION</div><h2><span class="zh">聯會架構</span><span class="en" lang="en">Our people</span></h2></div>
 <div class="officers">
  <div class="officer"><div class="role">創會會長 FOUNDING PRESIDENT</div><div class="nm">李少波先生</div></div>
  <div class="officer"><div class="role">理事會長 CHAIRMAN OF THE COUNCIL</div><div class="nm">陳雨冰先生</div></div>
  <div class="officer"><div class="role">秘書長 SECRETARY-GENERAL</div><div class="nm">郭俊浩先生</div></div>
  <div class="officer"><div class="role">總幹事 GENERAL MANAGER</div><div class="nm">曾美雲小姐</div></div>
 </div>
 <div style="display:grid;gap:14px"><h3>{b("會長","Council members")}</h3><ul class="people">{''.join(f'<li>{n}</li>' for n in COUNCIL)}</ul></div>
 <div style="display:grid;gap:14px"><h3>{b("第一屆常務理事會","First Standing Committee")}</h3>
  <div class="tbl"><table><thead><tr><th>部門 DEPARTMENT</th><th>負責人 IN CHARGE</th></tr></thead><tbody>
   <tr><td>{b("國內總務部","Mainland Affairs")}</td><td>黃永健先生</td></tr>
   <tr><td>{b("財務部","Finance")}</td><td>林瀛杰先生</td></tr>
   <tr><td>{b("會員聯絡部","Member Liaison")}</td><td>鄭凱程小姐、劉家麗小姐</td></tr>
  </tbody></table></div></div>
</div></section>

<section class="band"><div class="wrap recog">
 <img src="assets/img/kcc-logo.jpg" alt="九龍總商會標誌" width="110" height="100">
 <div style="display:grid;gap:8px"><h3>{b("九龍總商會附屬團體","Affiliated association of the Kowloon Chamber of Commerce")}</h3>{p("聯會獲九龍總商會認可為附屬團體。","HKAWDA is recognised by the Kowloon Chamber of Commerce as an affiliated association.")}</div>
 <a class="btn ghost" href="contact.html">{b("聯絡我們","Contact us")}</a>
</div></section>'''
write('about.html', about, '關於聯會', 'About', '香港鋁門窗同業聯會於2015年成立：宗旨、工作成果及組織架構。About the Hong Kong Aluminium Windows & Doors Association.')

# ================= MEMBERSHIP =================
mem = page_title('membership.html','會員福利及入會','Membership','加入聯會','Join HKAWDA',
 '歡迎同行業界積極申請入會，集合大眾力量向政府爭取業界福利，攜手共創將來。所有會籍均為永久制。',
 'We welcome everyone in the trade. Together we can speak to government for the industry and build its future. All memberships are lifetime.') + f'''
<section><div class="wrap two">
 <div style="display:grid;gap:20px">
  <div class="eyebrow">會籍 CATEGORIES</div>
  <h2><span class="zh">會員類別及會費</span><span class="en" lang="en">Categories and fees</span></h2>
  <div class="tbl"><table><thead><tr><th>類別 CATEGORY</th><th>對象 FOR</th><th>會費 FEE (HKD)</th></tr></thead><tbody>
   <tr><td><strong>{b("會長","Council member")}</strong></td><td>{b("有意參與理事工作的公司","Firms joining the council")}</td><td class="num">$5,000</td></tr>
   <tr><td><strong>{b("公司會員","Company member")}</strong></td><td>{b("鋁門窗、玻璃及相關工程公司","Window, door, glass and related firms")}</td><td class="num">$300</td></tr>
   <tr><td><strong>{b("個人會員","Individual member")}</strong></td><td>{b("從業員及師傅","Workers and tradespeople")}</td><td class="num">$300</td></tr>
  </tbody></table></div>
  {p("所有會籍均為永久制，毋須續會。會費以 2024 年版申請表為準。","All memberships are lifetime with no renewal. Fees follow the 2024 application form.",'note')}
 </div>
 <div style="display:grid;gap:20px">
  <div class="eyebrow">福利 BENEFITS</div>
  <h2><span class="zh">會員可獲得</span><span class="en" lang="en">What members receive</span></h2>
  <ul class="checklist">
   <li><span class="tick">✓</span><div><strong>{b("專業認證貼紙及會員證書","Certified sticker and certificate")}</strong>{p("貼於店舖玻璃位置，讓公眾知道你是聯會會員。","For your shopfront glass, so the public knows you are a member.")}</div></li>
   <li><span class="tick">✓</span><div><strong>{b("會員卡（實體及電子）","Membership card (physical and digital)")}</strong>{p("均有獨立編號。","Each with its own number.")}</div></li>
   <li><span class="tick">✓</span><div><strong>{b("刊登於網上會員名錄","Listing in the online directory")}</strong>{p("業主可按地區搜尋到你的公司。","Homeowners can find your firm by district.")}</div></li>
   <li><span class="tick">✓</span><div><strong>{b("會員優惠","Member discounts")}</strong>{p("油咭回扣、餐廳、印刷及車房等商戶優惠。","Fuel card rebates and discounts at restaurants, printers and garages.")}</div></li>
   <li><span class="tick">✓</span><div><strong>{b("活動及課程","Events and courses")}</strong>{p("廠房考察、聚餐交流，並優先報名聯會活動及課程。","Factory tours, dinners and priority registration for events and courses.")}</div></li>
   <li><span class="tick">✓</span><div><strong>{b("使用聯會標誌","Use of the HKAWDA logo")}</strong>{p("可於網站及宣傳品上使用聯會標誌。","On your website and promotional materials.")}</div></li>
  </ul>
 </div>
</div></section>

<section class="alt"><div class="wrap two">
 <div style="display:grid;gap:20px">
  <div class="eyebrow">申請 HOW TO APPLY</div>
  <h2><span class="zh">入會步驟</span><span class="en" lang="en">How to apply</span></h2>
  <ol class="olist">
   <li><div><strong>{b("下載並填妥申請表","Download and complete the form")}</strong>{p("填寫公司資料及申請類別，並簽名蓋印。","Fill in company details and category, then sign and stamp.")}</div></li>
   <li><div><strong>{b("連同文件遞交","Send it with documents")}</strong>{p("將申請表、商業登記證副本及名片電郵至 "+C['email']+"，或 WhatsApp 至 "+C['whatsapp']+"。","Email the form with a copy of your Business Registration and a business card to "+C['email']+", or WhatsApp "+C['whatsapp']+".")}</div></li>
   <li><div><strong>{b("繳交會費","Pay the fee")}</strong>{p("以現金、支票或銀行轉帳繳付；付款詳情列於申請表。支票抬頭：香港鋁門窗同業聯會有限公司。","Pay by cash, cheque or bank transfer; details are on the form. Cheques payable to Hong Kong Aluminium Windows & Doors Association Company Limited.")}</div></li>
   <li><div><strong>{b("審核及發出會員資料","Approval and welcome pack")}</strong>{p("審核通過後，聯會發出會員卡、證書及貼紙，並把公司加入網上名錄。","Once approved, you receive your card, certificate and sticker, and your firm is added to the directory.")}</div></li>
  </ol>
  <div class="btn-row"><a class="btn red" href="docs/hkawda-application-form-2024.pdf" target="_blank" rel="noopener">{b("下載申請表 (PDF)","Application form (PDF)")}</a><a class="btn ghost" href="contact.html">{b("查詢","Ask a question")}</a></div>
 </div>
 <figure class="figure-frame" style="margin:0;max-width:420px;justify-self:center"><img src="assets/img/recruitment-leaflet.jpg" alt="聯會會員招募單張" loading="lazy"></figure>
</div></section>'''
write('membership.html', mem, '申請入會', 'Membership', '加入香港鋁門窗同業聯會：會員類別、會費、福利及申請步驟。Join HKAWDA: categories, fees and benefits.')

# ================= COURSES =================
courses = page_title('courses.html','行業課程','Courses','行業課程','Industry courses',
 '聯會與香港專業教育學院（IVE）工程學科合作，為鋁門窗業界提供專業課程。',
 'We partner with the Engineering Discipline of the Hong Kong Institute of Vocational Education (IVE) to offer courses for the window and door trade.') + f'''
<section><div class="wrap">
 <div class="cards">
  <div class="card"><div class="k">IVE ENGINEERING</div><h3>{b("窗戶安裝及維修專業發展課程","Professional Development Course on Windows Installation and Maintenance")}</h3>{p("涵蓋窗戶安裝、維修及安全要求。","Covers window installation, maintenance and safety requirements.")}</div>
  <div class="card"><div class="k">MBIS / MWIS</div><h3>{b("強制驗樓及強制驗窗計劃增補課程","MBIS & MWIS top-up courses")}</h3>{p("適用於 Level 2 Representative、TCP-T1 及 Authorised Signatory。","For Level 2 Representatives, TCP-T1 and Authorised Signatories.")}</div>
  <div class="card"><div class="k">GLASS &amp; FAÇADE</div><h3>{b("玻璃及幕牆工程測試與檢驗","Testing and Inspection of Glass and Façade Works")}</h3>{p("認識玻璃及外牆工程的測試標準與檢驗方法。","Testing standards and inspection methods for glass and façade works.")}</div>
  <div class="card"><div class="k">CLASS III MINOR WORKS</div><h3>{b("三級小型工程課程（三仔牌）","Class III minor works course")}</h3>{p("聯會與 IVE 合作籌辦，會員一律可報讀（收費課程）。","Arranged with IVE and open to all members (fee-paying).")}</div>
 </div>
 <div class="two" style="margin-top:48px">
  <div class="prose"><div class="eyebrow">爭取 ADVOCACY</div><h2><span class="zh">為年輕一代爭取培訓</span><span class="en" lang="en">Training for the next generation</span></h2>
  {p("聯會正向政府爭取復辦二級小型工程短期課程，讓更多年輕人入行，並推動鋁窗師傅專業資格。","We are asking government to bring back short courses for Class II minor works, so more young people can enter the trade, and to recognise window fitters' qualifications.")}</div>
  <div class="prose"><div class="eyebrow">報名 ENROL</div><h2><span class="zh">課程查詢</span><span class="en" lang="en">Course enquiries</span></h2>
  {p("開課日期及費用會經會員通告公佈。如有興趣，請聯絡會員聯絡部。","Dates and fees are announced to members. To register interest, contact Member Liaison.")}
  <div class="btn-row"><a class="btn" href="contact.html">{b("聯絡我們","Contact us")}</a></div></div>
 </div>
</div></section>'''
write('courses.html', courses, '行業課程', 'Courses', '香港鋁門窗同業聯會與IVE合辦的窗戶安裝、維修及驗窗課程。Industry courses with IVE.')

# ================= NEWS =================
news = page_title('news.html','消息及活動','News & events','消息及活動','News & events',
 '聯會舉辦廠房考察、會長會議及交流活動，讓會員掌握行業最新發展。','Factory tours, council meetings and gatherings that keep members up to date.') + f'''
<section><div class="wrap" style="max-width:900px">
 <ol class="timeline">
  <li id="2025-zhongshan"><div class="date">2025-11-29 · 星期六 SAT</div>
   <h2><span class="zh">鋁門窗及玻璃廠中山考察團</span><span class="en" lang="en">Zhongshan aluminium window &amp; glass factory tour</span></h2>
   <div class="gallery"><img src="assets/img/zhongshan-2025-factory.jpg" alt="會員參觀鋁門窗生產線" loading="lazy"><img src="assets/img/zhongshan-2025-group.jpg" alt="考察團成員在廠房外聽取介紹" loading="lazy"><img src="assets/img/zhongshan-2025-arrival.jpg" alt="考察團旅遊巴抵達中山" loading="lazy"></div>
   {p("聯會安排跨境旅遊巴，由旺角及屯門出發前往中山，參觀創會成員升威 LE-RELAX 的中山生產基地（鎮威鋁門窗廠）、鎮升玻璃廠及信義玻璃廠，並設午宴交流。活動旨在讓會員深入了解行業最新趨勢及生產加工技術，並與業內專業人士分享經驗。","Cross-border coaches from Mong Kok and Tuen Mun took members to Zhongshan to visit founding member LE-RELAX's Zhongshan production base (Zhen Wei aluminium window factory), Zhen Sheng glass factory and Xinyi Glass, with a lunch gathering. The tour helped members see the latest trends and production techniques and share experience with industry professionals.")}
  </li>
  <li id="2023-zhongshan"><div class="date">2023-12-09</div>
   <h2><span class="zh">中山廠房參觀團</span><span class="en" lang="en">Zhongshan factory visit</span></h2>
   {p("近五十位會長及會員參加，參觀創會成員升威 LE-RELAX 的中山廠房，包括鋁窗生產車間及玻璃加工部，並與供應商共晉午宴。","Nearly fifty council members and members toured founding member LE-RELAX's Zhongshan factory, including its aluminium window lines and glass processing, followed by lunch with suppliers.")}
   <div class="gallery"><img src="assets/img/zhongshan-2023-group.jpg" alt="參觀團全體合照" loading="lazy"><img src="assets/img/zhongshan-2023-glass.jpg" alt="參觀玻璃加工車間" loading="lazy"><img src="assets/img/zhongshan-2023-production.jpg" alt="參觀鋁窗生產設備" loading="lazy"></div>
  </li>
  <li id="2023-council"><div class="date">2023-10-16</div>
   <h2><span class="zh">2023 年第一次會長會議</span><span class="en" lang="en">First council meeting of 2023</span></h2>
   {p("疫情後首次會長聚會。會上討論舉辦內地廠房考察、與 IVE 合辦三級小型工程課程，以及以聯會名義向政府爭取復辦二級小型工程短期課程。","The first council gathering since the pandemic. Members discussed mainland factory tours, a Class III minor works course with IVE, and asking government to restore short courses for Class II minor works.")}
   <figure><img src="assets/img/council-meeting-2023.jpg" alt="2023 年會長會議合照" loading="lazy"><figcaption>{b("會長會議合照","Council meeting group photo")}</figcaption></figure>
  </li>
  <li id="2015-founding"><div class="date">2015-11-30</div>
   <h2><span class="zh">聯會成立典禮暨 2015 年會員聯歡晚宴</span><span class="en" lang="en">Founding ceremony and 2015 members' dinner</span></h2>
   {p("近百位嘉賓及同業到賀。創會會長李少波表示，聯會成立目的是團結鋁門窗同業力量，一齊為業界發聲，並更好地為市民大眾提供優質服務。理事會長陳雨冰指出，聯會首要工作是編製會員名冊，方便市民找到專業師傅。","Close to a hundred guests attended. Founding President Lee Siu-po said the Association would unite the trade to speak with one voice and serve the public better. Council Chairman Chan Yu-bing said the first priority was a member register so residents could find qualified professionals.")}
   <div class="gallery">
    <img src="assets/img/founding-2015-c.jpg" alt="成立典禮全體祝酒" loading="lazy">
    <img src="assets/img/founding-2015-b.jpg" alt="成立典禮嘉賓合照" loading="lazy">
    <img src="assets/img/founding-2015-a.jpg" alt="成立典禮義工團隊" loading="lazy">
   </div>
  </li>
 </ol>
 <div class="note">{p("想收到最新活動通知？請以 WhatsApp "+C['whatsapp']+" 或電郵 "+C['email']+" 登記。","Want event updates? Register by WhatsApp "+C['whatsapp']+" or email "+C['email']+".")}</div>
</div></section>'''
write('news.html', news, '消息及活動', 'News & events', '香港鋁門窗同業聯會最新消息：廠房考察團、會長會議及成立典禮。HKAWDA news and events.')

# ================= CONTACT =================
contact = page_title('contact.html','聯絡我們','Contact','聯絡我們','Contact us',
 '業主查詢會員資料、同業查詢入會，歡迎聯絡我們。','Homeowners checking a member, or firms asking about membership: we are happy to help.') + f'''
<section><div class="wrap two">
 <div style="display:grid;gap:24px">
  <dl class="contact-list" style="margin:0">
   <div><dt>{b("電郵","Email")}</dt><dd>{C['email']}</dd></div>
   <div><dt>{b("電話","Phone")}</dt><dd>{C['tel']}</dd></div>
   <div><dt>WhatsApp</dt><dd>{C['whatsapp']}</dd></div>
   <div><dt>{b("社交媒體","Social")}</dt><dd><a href="{C['fb']}" target="_blank" rel="noopener">Facebook ↗</a> · <a href="{C['li']}" target="_blank" rel="noopener">LinkedIn ↗</a></dd></div>
  </dl>
  <div style="display:flex;gap:16px;align-items:center;flex-wrap:wrap"><img src="assets/img/qr.png" alt="聯會 QR code" width="120" height="120" style="background:#fff;padding:6px;border-radius:4px">{p("掃描 QR code 瀏覽聯會網站","Scan to open the HKAWDA website")}</div>
 </div>
 <form class="form" id="contact-form" data-to="{C['email']}">
  <h2><span class="zh">發送查詢</span><span class="en" lang="en">Send an enquiry</span></h2>
  <div class="row">
   <div class="field"><label for="c-name">姓名 NAME</label><input id="c-name" name="name" type="text" required autocomplete="name"></div>
   <div class="field"><label for="c-phone">電話 PHONE</label><input id="c-phone" name="phone" type="text" autocomplete="tel"></div>
  </div>
  <div class="field"><label for="c-email">電郵 EMAIL</label><input id="c-email" name="email" type="email" required autocomplete="email"></div>
  <div class="field"><label for="c-topic">查詢類別 TOPIC</label><select id="c-topic" name="topic">
   <option>業主查詢 Homeowner enquiry</option><option>核實會員 Verify a member</option><option>申請入會 Membership</option><option>課程 Courses</option><option>傳媒 Media</option><option>其他 Other</option></select></div>
  <div class="field"><label for="c-msg">內容 MESSAGE</label><textarea id="c-msg" name="message" required></textarea></div>
  <button class="btn red" type="submit" style="justify-self:start">{b("用電郵發送","Send by email")}</button>
  <p class="form-msg" id="form-msg" hidden>{b("正在開啟你的電郵程式。如沒有反應，請直接電郵 "+C['email']+"。","Opening your email app. If nothing happens, email "+C['email']+" directly.")}</p>
 </form>
</div></section>'''
write('contact.html', contact, '聯絡我們', 'Contact', '聯絡香港鋁門窗同業聯會：電郵、電話及WhatsApp。Contact HKAWDA.')

# 404, sitemap, robots, favicon
write('404.html', page_title('404.html','找不到頁面','Not found','找不到此頁面','Page not found','頁面可能已搬遷。','This page may have moved.')+f'<section><div class="wrap btn-row"><a class="btn red" href="index.html">{b("返回首頁","Back to home")}</a><a class="btn ghost" href="find-installer.html">{b("搵會員工程公司","Find an installer")}</a></div></section>','找不到頁面','Not found','Page not found')
pages = ['','find-installer.html']+list(RSLUG.values())+['homeowners.html','about.html','membership.html','courses.html','news.html','contact.html']
open(OUT+'sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{BASE}{x}</loc></url>\n' for x in pages)+'</urlset>\n')
open(OUT+'robots.txt','w').write(f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n')
open(OUT+'assets/img/favicon.svg','w').write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="10" fill="#fff"/><rect x="9" y="10" width="20" height="44" fill="none" stroke="#5a6168" stroke-width="4"/><line x1="9" y1="32" x2="29" y2="32" stroke="#5a6168" stroke-width="4"/><rect x="6" y="8" width="3" height="48" fill="#c42a31"/><path d="M36 26l12-7 12 7-12 7z" fill="#e8525a"/><path d="M36 26v14l12 7V33z" fill="#c42a31"/><path d="M60 26v14l-12 7V33z" fill="#8f1d22"/></svg>')
open(OUT+'CNAME','w').write('hkawda.org\n')
open(OUT+'.nojekyll','w').write('')
print('ok', len(M), dict(REGION_COUNT))
