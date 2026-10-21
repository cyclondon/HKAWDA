# Split each bilingual source page into a Chinese page (site root) and an English page (site/en/),
# then add SEO tags: titles, descriptions, canonical, hreflang, Open Graph, JSON-LD, sitemap.
import re, os, glob, json, copy
from bs4 import BeautifulSoup, Comment
BASE='https://hkawda.org/'
CJK = re.compile(r'[㐀-鿿＀-￯　-〿《》「」]')
SEP=' ·|/:：-–—'
def sp(t, lang):
    if not t or not CJK.search(t) or not re.search('[A-Za-z]{2,}', t): return t
    if t.strip().endswith(('LE-RELAX','HKAWDA')): return t
    idx=[i for i,ch in enumerate(t) if CJK.match(ch)]; i=idx[-1]
    rest=t[i+1:]
    if re.match(r'^[\s·|/:：\-–—]*[A-Za-z]', rest) and re.search('[A-Za-z]{2,}', rest):
        head=t[:i+1]
        prefix=re.match(r'^[0-9\s\-·./:]*', head).group(0)
        if lang=='zh': return head.rstrip(SEP)
        lead=re.match(r'^\s*',t).group(0); trail=re.search(r'\s*$',t).group(0)
        return lead+prefix+rest.strip().lstrip(SEP).strip()+trail
    return t

ORG = {"@context":"https://schema.org","@type":"Organization","@id":BASE+"#org",
 "name":"香港鋁門窗同業聯會有限公司","alternateName":["Hong Kong Aluminium Windows & Doors Association","HKAWDA"],
 "url":BASE,"logo":BASE+"assets/img/logo.png","foundingDate":"2015-11-30","email":"info@hkawda.org","telephone":"+852 2381 4161",
 "areaServed":{"@type":"Place","name":"Hong Kong"},
 "sameAs":["https://www.facebook.com/profile.php?id=61580456752522","https://www.linkedin.com/company/hong-kong-aluminum-window-and-doors-association"]}

TITLES={
 'find-installer.html':('搵鋁窗工程公司｜全港會員名錄｜香港鋁門窗同業聯會','Find an Aluminium Window Installer in Hong Kong | HKAWDA'),
 'homeowners.html':('更換鋁窗指南：小型工程、強制驗窗及報價須知｜香港鋁門窗同業聯會','How to Replace Aluminium Windows in Hong Kong: Minor Works & MWIS | HKAWDA'),
 'about.html':('關於香港鋁門窗同業聯會｜宗旨、成果及架構','About the Hong Kong Aluminium Windows & Doors Association | HKAWDA'),
 'membership.html':('申請入會｜會員類別、會費及福利｜香港鋁門窗同業聯會','Join HKAWDA: Membership Categories, Fees & Benefits'),
 'courses.html':('鋁窗行業課程｜窗戶安裝、維修及驗窗｜香港鋁門窗同業聯會','Window Installation & Inspection Courses | HKAWDA'),
 'news.html':('消息及活動｜香港鋁門窗同業聯會','News & Events | HKAWDA Hong Kong'),
 'contact.html':('聯絡我們｜香港鋁門窗同業聯會','Contact HKAWDA | Hong Kong Aluminium Windows & Doors Association'),
 'installers-hong-kong-island.html':('香港島鋁窗工程公司名單｜港島換鋁窗｜HKAWDA','Aluminium Window Installers on Hong Kong Island | HKAWDA'),
 'installers-kowloon.html':('九龍鋁窗工程公司名單｜九龍換鋁窗｜HKAWDA','Aluminium Window Installers in Kowloon | HKAWDA'),
 'installers-new-territories.html':('新界鋁窗工程公司名單｜新界換鋁窗｜HKAWDA','Aluminium Window Installers in the New Territories | HKAWDA'),
}
pages=sorted(os.path.basename(f) for f in glob.glob('./*.html'))
SRC={p:open('./'+p).read() for p in pages}
os.makedirs('./en',exist_ok=True)
titles={}
for p in pages:
    for lang in ('zh','en'):
        s=BeautifulSoup(SRC[p],'html.parser')
        drop,keep=('en','zh') if lang=='zh' else ('zh','en')
        for el in s.select('.'+drop): el.decompose()
        for el in s.select('.'+keep):
            cls=[c for c in el.get('class',[]) if c!=keep]
            if el.name=='span' and not cls: el.unwrap(); continue
            if cls: el['class']=cls
            else: del el['class']
            if el.has_attr('lang'): del el['lang']
        if lang=='en':
            for t in s.select('svg text.lbl'): t.decompose()
            for t in s.select('svg text.dim'):
                if CJK.search(t.get_text()): t.string='UNIT: mm · ILLUSTRATIVE'
        for t in list(s.find_all(string=True)):
            if isinstance(t,Comment) or t.parent.name in ('script','style','title') or t.find_parent('svg'): continue
            n=sp(str(t),lang)
            if n!=str(t): t.replace_with(n)
        for tag in s.find_all(True):
            for a in ('placeholder','alt','aria-label','title','content'):
                if isinstance(tag.get(a),str): tag[a]=sp(tag[a],lang)
        # titles
        raw=s.title.string
        x=raw.split(' | ')[0]
        xt=s.select_one('meta[name=x-title]')
        if xt:
            T=xt['data-zh'] if lang=='zh' else xt['data-en']; xt.decompose()
        elif p in TITLES:
            T=TITLES[p][0 if lang=='zh' else 1]
        elif p=='index.html':
            T={'zh':'香港鋁門窗同業聯會 HKAWDA｜搵鋁窗工程公司・更換鋁窗指南','en':'Hong Kong Aluminium Windows & Doors Association (HKAWDA) | Find a window installer'}[lang]
        else:
            T=(sp(x,'zh')+'｜香港鋁門窗同業聯會 HKAWDA') if lang=='zh' else (sp(x,'en')+' | HKAWDA Hong Kong')
        s.title.string=T
        titles[(p,lang)]=T
        head=s.head
        url=BASE+('' if lang=='zh' else 'en/')+('' if p=='index.html' else p)
        s.html['lang']='zh-Hant-HK' if lang=='zh' else 'en'
        for m in s.select('meta[property="og:title"]'): m['content']=T
        desc=s.select_one('meta[name=description]')['content']
        s.select_one('link[rel=canonical]')['href']=url
        def tag(tname,**kw):
            t=s.new_tag(tname,attrs=kw); head.append(t); head.append('\n')
        zurl=BASE+('' if p=='index.html' else p); eurl=BASE+'en/'+('' if p=='index.html' else p)
        if p!='404.html':
            tag('link',rel='alternate',hreflang='zh-Hant-HK',href=zurl)
            tag('link',rel='alternate',hreflang='en',href=eurl)
            tag('link',rel='alternate',hreflang='x-default',href=zurl)
        else:
            tag('meta',name='robots',content='noindex')
        tag('meta',property='og:url',content=url)
        tag('meta',property='og:locale',content='zh_HK' if lang=='zh' else 'en_HK')
        tag('meta',property='og:site_name',content='香港鋁門窗同業聯會 HKAWDA')
        t=s.new_tag('meta'); t['name']='twitter:card'; t['content']='summary_large_image'; head.append(t)
        t=s.new_tag('meta'); t['name']='theme-color'; t['content']='#c42a31'; head.append(t)
        # JSON-LD
        ld=[]
        if p=='index.html':
            o=dict(ORG); 
            o['description']=desc
            ld.append(o)
            ld.append({"@context":"https://schema.org","@type":"WebSite","url":url,"name":T,"inLanguage":s.html['lang'],"publisher":{"@id":BASE+"#org"},
              "potentialAction":{"@type":"SearchAction","target":url+"find-installer.html?q={search_term_string}","query-input":"required name=search_term_string"}})
        elif p!='404.html':
            h1=s.h1.get_text(' ',strip=True)
            ld.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
              {"@type":"ListItem","position":1,"name":"首頁" if lang=='zh' else "Home","item":BASE+('' if lang=='zh' else 'en/')},
              {"@type":"ListItem","position":2,"name":h1,"item":url}]})
        if s.select('details'):
            qa=[{"@type":"Question","name":d.summary.get_text(' ',strip=True),"acceptedAnswer":{"@type":"Answer","text":d.select_one('.ans').get_text(' ',strip=True)}} for d in s.select('details')]
            ld.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":qa})
        for j in ld:
            sc=s.new_tag('script',type='application/ld+json'); sc.string=json.dumps(j,ensure_ascii=False); head.append(sc); head.append('\n')
        out=str(s)
        # language switch
        if lang=='zh':
            sw=f'<a class="lang-link" href="en/{p}" hreflang="en" lang="en">EN</a>'
        else:
            sw=f'<a class="lang-link" href="../{p}" hreflang="zh-Hant-HK" lang="zh-Hant-HK">中文</a>'
        out=out.replace('<!--LANGSWITCH-->',sw)
        if lang=='en':
            out=re.sub(r'(href|src)="(assets/|docs/)',r'\1="../\2',out)
            out=out.replace('og:image" content="'+BASE,'og:image" content="'+BASE)
        open(('./' if lang=='zh' else './en/')+p,'w').write(out)
# sitemap with hreflang alternates
items=''
for p in pages:
    if p=='404.html': continue
    z=BASE+('' if p=='index.html' else p); e=BASE+'en/'+('' if p=='index.html' else p)
    alt=f'<xhtml:link rel="alternate" hreflang="zh-Hant-HK" href="{z}"/><xhtml:link rel="alternate" hreflang="en" href="{e}"/>'
    pr='1.0' if p=='index.html' else ('0.9' if p.startswith(('find','installers','homeowners','district','housing','window','soundproof','typhoon')) else '0.6')
    items+=f'  <url><loc>{z}</loc>{alt}<priority>{pr}</priority></url>\n  <url><loc>{e}</loc>{alt}<priority>{pr}</priority></url>\n'
open('./sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'+items+'</urlset>\n')
for k,v in titles.items(): print(k,v)
