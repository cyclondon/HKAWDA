# 香港鋁門窗同業聯會 HKAWDA 網站

Static website for the Hong Kong Aluminium Windows & Doors Association. Plain HTML/CSS/JS, works on GitHub Pages.

- **Chinese (default):** site root, e.g. `https://hkawda.org/homeowners.html`
- **English:** `/en/`, e.g. `https://hkawda.org/en/homeowners.html`
- Every page has a 中文 / EN button that jumps to the same page in the other language.

## Pages
All pages sit in the top folder (Chinese) and in `en/` (English) — no deeper folders, so GitHub Pages serves them as-is.

| Files | What |
|---|---|
| `index.html` | Home |
| `find-installer.html` | Searchable member directory |
| `installers-*.html` (3) | Region pages: 香港島 / 九龍 / 新界 |
| `district-*.html` (17) | One page per district, e.g. `district-yuen-long.html` |
| `homeowners.html` | Homeowner guide hub + FAQ |
| `housing-*.html` (5) | 私人住宅, 唐樓, 居屋, 公屋, 村屋 |
| `window-*.html`, `soundproof-windows.html`, `typhoon-window-check.html` (6) | Common problems: leaks, rusty hinges, latches, inspection notices, soundproofing, typhoon check |
| `member-m001.html` … `member-m152.html` | One profile page per member firm (name, district, address, phone, map, trade, verified badge, Google business data) |
| `about.html`, `membership.html`, `courses.html`, `news.html`, `contact.html`, `404.html` | Association pages |

## SEO built in
- Separate Chinese and English pages with their own `<title>` and meta description (keywords such as 換鋁窗、鋁窗工程公司、強制驗窗).
- `hreflang` links between the two languages, canonical URLs, Open Graph / social-share tags.
- Structured data (JSON-LD): Organization + site search on the home page, FAQ on the homeowner guide, breadcrumbs on inner pages.
- Founding member LE-RELAX is linked from the footer, About page, homeowner guide and news (supply-only wording).
- Member listings are in the HTML itself (not only loaded by script), so Google can index every company name and district.
- `sitemap.xml` (both languages) and `robots.txt`.
- After going live: add the site to **Google Search Console**, submit `https://hkawda.org/sitemap.xml`, and create/claim a **Google Business Profile** for the association.

## Performance (Lighthouse, mobile)
Tested locally: Performance 98–100, Accessibility 98–100, Best Practices 100, SEO 100. Images are WebP with fixed dimensions; the home photo has a smaller version for phones. (GitHub Pages adds compression and caching automatically.)

## Mobile
Mobile-first layout, 44px+ tap targets, fixed bottom bar with "搵會員工程公司" and WhatsApp buttons, phone numbers are tap-to-call, addresses open Google Maps.

## Partner logos (optional)
The recognition strip on the home page shows text badges for IVE, 大公報 and 屋宇署. To show official logos instead, save them as square PNGs named `ive-logo.png`, `takungpao-logo.png` or `bd-logo.png` in `assets/img/` and rebuild. Only use logos you have written permission to use.

## Editing
The pages are generated from two small Python scripts in `tools/` so both languages stay in sync.

1. Install once: `pip install beautifulsoup4`
2. Edit content in `tools/gen.py` (text is written as pairs: Chinese, English) or members in `tools/members.json`. Contact details are at the top of `tools/gen.py`.
3. From this folder run:
   ```
   python3 tools/gen.py && python3 tools/post.py
   ```
   Always run both, in that order.

Member fields in `members.json` — `id` is the permanent page name (e.g. `m001` → `member-m001.html`); give new members the next unused number and never reuse one: `n` name, `a` address, `t` phones, `r` region (`hki`/`kln`/`nt`), `d`/`de` district (中/EN), `c` true = 會長單位, `s` trade tags (`alu`,`glass`,`gate`,`steel`,`reno`).

## Publish on GitHub Pages
1. Create a repository and upload the contents of this folder to the root.
2. Settings → Pages → Deploy from a branch → `main` / `(root)`.
3. Custom domain: the `CNAME` file says `hkawda.org`. In GoDaddy DNS, set:
   - `A` records for `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `CNAME` for `www` → `<your-github-username>.github.io`
4. Tick **Enforce HTTPS** in Settings → Pages once available.
5. Leave the email (MX) records unchanged so info@hkawda.org keeps working.
