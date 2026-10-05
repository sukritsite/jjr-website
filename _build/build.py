# สร้างไฟล์เว็บ jjrsolarcell.com จากต้นฉบับหน้าแรก (_build/home.src.html) + บทความเดิมจาก WordPress (_src/*.json)
# ใช้:  python _build/build.py   (รันจากโฟลเดอร์ jjr-website)
import io, sys, re, json, html, datetime, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
SITE = 'https://jjrsolarcell.com'
TODAY = datetime.date.today().isoformat()
E = html.escape
sys.path.insert(0, os.path.join(ROOT, '_build'))
import contact as C
import md as MD

def head(title, desc, path, image=SITE + '/pf/p01/02.webp', extra=''):
    return f'''<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{SITE}{path}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#0A9447">
<meta property="og:type" content="website">
<meta property="og:locale" content="th_TH">
<meta property="og:site_name" content="JJR โซล่าเซลล์">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
{extra}'''

# ---------------------------------------------------------------- home
src = open('_build/home.src.html', encoding='utf8').read()
# ตัด head ส่วนที่ต้นฉบับ (artifact) ใส่ไว้เอง แล้วใส่ head ของ production แทน
src = re.sub(r'^<title>.*?</title>\n', '', src, count=1)
for pat in [r'<meta name="description"[^>]*>\n', r'<meta name="robots"[^>]*>\n', r'<link rel="canonical"[^>]*>\n',
            r'<meta name="theme-color"[^>]*>\n', r'<meta property="og:[^"]*"[^>]*>\n', r'<meta name="twitter:card"[^>]*>\n',
            r'<link rel="icon"[^>]*>\n']:
    src = re.sub(pat, '', src)
home_desc = ('JJR โซล่าเซลล์ ติดตั้งกับช่างที่ชำนาญ บริการใกล้บ้านคุณ ออกแบบและติดตั้งโซล่าเซลล์สำหรับโรงงาน อาคารพาณิชย์ '
             'หน่วยงาน และบ้านพักอาศัย ในอุบลราชธานี ศรีสะเกษ ยโสธร สุรินทร์ สำรวจหน้างานฟรี ยื่นขออนุญาตการไฟฟ้าให้')
src = src.replace('/*SITE*/', SITE)
src = re.sub(r'"description": "[^"]*"', '"description": ' + json.dumps(home_desc, ensure_ascii=False), src, count=1)
src = src.replace('"logo": "https://jjrsolarcell.com/pf/jjr.webp"', '"logo": "https://jjrsolarcell.com/icon-512.png"')

# ฟอร์มจริง: ส่งไป Cloud Function submitLead แทนข้อความตัวอย่าง
src = src.replace('<form id="qForm" novalidate>', '<form id="qForm" novalidate>\n        <input type="text" name="website" id="qWeb" tabindex="-1" autocomplete="off" aria-hidden="true" style="position:absolute;left:-9999px;width:1px;height:1px;opacity:0">', 1)
src = re.sub(r'<div class="done" id="qDone" hidden>.*?</div></div>',
             '<div class="done" id="qDone" hidden><span class="ms fill">check_circle</span><div><b>ได้รับข้อมูลแล้ว</b>ทีมงานจะโทรกลับภายในวันทำการ ถ้าต้องการด่วนโทร 094-264-6142</div></div>'
             '\n        <div class="done err" id="qErr" hidden><span class="ms fill">error</span><div><b>ส่งข้อมูลไม่สำเร็จ</b><span id="qErrMsg">กรุณาลองใหม่ หรือโทร 094-264-6142</span></div></div>', src, count=1, flags=re.S)
old_submit = re.search(r"  // Draft only: validates.*?\n  \}\);\n", src, re.S)
assert old_submit, 'form handler'
src = src[:old_submit.start()] + r'''  // ส่งฟอร์มขอใบเสนอราคา → Cloud Function submitLead → งานโทรกลับในศูนย์งาน (tasks)
  var LEAD_URL = 'https://asia-southeast1-jjr-workspaces.cloudfunctions.net/submitLead';
  $('qForm').addEventListener('submit', function(e){
    e.preventDefault();
    var name = $('qName').value.trim(), tel = $('qTel').value.replace(/[^\d]/g, '');
    $('fName').classList.toggle('bad', !name);
    $('fTel').classList.toggle('bad', !/^0\d{8,9}$/.test(tel));
    if (!name) { $('qName').focus(); return; }
    if (!/^0\d{8,9}$/.test(tel)) { $('qTel').focus(); return; }
    if (!$('qOk').checked) { $('qOk').focus(); return; }
    var typeEl = document.querySelector('input[name="type"]:checked');
    var btn = $('qSend'); btn.disabled = true; $('qDone').hidden = $('qErr').hidden = true;
    fetch(LEAD_URL, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({
      name: name, tel: tel, type: typeEl ? typeEl.value : 'อื่นๆ', bill: $('qBill').value.trim(), area: $('qArea').value.trim(),
      msg: $('qMsg').value.trim(), consent: true, website: $('qWeb').value, page: location.href.slice(0, 200) }) })
      .then(function(r){ return r.json().catch(function(){ return {}; }).then(function(j){ if (!r.ok || !j.ok) throw new Error(j.error || 'ส่งไม่สำเร็จ'); }); })
      .then(function(){ $('qForm').reset(); $('qDone').hidden = false; if (window.gtag) gtag('event', 'generate_lead'); })
      .catch(function(err){ $('qErrMsg').textContent = (err && err.message) || 'กรุณาลองใหม่ หรือโทร 094-264-6142'; $('qErr').hidden = false; })
      .then(function(){ btn.disabled = false; });
  });
''' + src[old_submit.end():]
src = src.replace('  .done .ms{color:var(--accent);font-size:26px}',
                  '  .done .ms{color:var(--accent);font-size:26px}\n  .done.err{background:#FEF2F2;border-color:#FECACA}\n  .done.err .ms{color:#DC2626}\n  #qSend[disabled]{opacity:.6;cursor:wait}')
src = src.replace('ยินยอมให้ บจก. จงเจริญ โซลาร์เซลล์ ใช้ข้อมูลนี้เพื่อติดต่อกลับเรื่องใบเสนอราคาเท่านั้น',
                  'ยินยอมให้ บจก. จงเจริญ โซลาร์เซลล์ ใช้ข้อมูลนี้เพื่อติดต่อกลับเรื่องใบเสนอราคาเท่านั้น (<a href="/privacy-policy/" style="color:var(--accent)">นโยบายความเป็นส่วนตัว</a>)')
src = src.replace('<a href="/blog/"><span class="ms">article</span>บทความ</a>',
                  '<a href="/blog/"><span class="ms">article</span>บทความ</a>\n        <a href="/privacy-policy/"><span class="ms">shield</span>นโยบายความเป็นส่วนตัว</a>')
# ไอคอนที่เพิ่มในหน้านี้ต้องอยู่ใน subset ของ Material Symbols ด้วย
m = re.search(r'icon_names=([a-z0-9_,]+)', src)
icons = sorted(set(m.group(1).split(',')) | {'check_circle', 'error', 'shield', 'arrow_back', 'calendar_today'})
src = src[:m.start(1)] + ','.join(icons) + src[m.end(1):]
ICON_Q = ','.join(icons)

title = 'JJR โซล่าเซลล์ | ติดตั้งโซล่าเซลล์โรงงาน ธุรกิจ อุบลราชธานี ภาคอีสาน'
open('index.html', 'w', encoding='utf8').write(head(title, home_desc, '/') + src.replace('\n<link rel="preconnect" href="https://fonts.googleapis.com">', '<link rel="preconnect" href="https://fonts.googleapis.com">', 1) + '\n</html>\n')

# ---------------------------------------------------------------- shared page shell (บทความ / นโยบาย / 404)
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600;700&display=swap">\n'
         f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,400,0..1,0&icon_names={ICON_Q}&display=block">\n')
PAGE_CSS = '''<style>
  :root{--accent:#0A9447;--accent-soft:#EAF6EF;--ink:#16202A;--body:#2B3440;--muted:#5B6573;--line:#E4E8EC;--bg:#FFFFFF;--band:#F6F8F7;--dark:#0F1A14;
    --f:"IBM Plex Sans Thai",system-ui,sans-serif;--shadow-card:0 1px 4px 0 rgba(12,12,13,.05),0 1px 4px 0 rgba(12,12,13,.10)}
  *{box-sizing:border-box} html,body{height:100%} body{display:flex;flex-direction:column;min-height:100vh;margin:0;background:var(--bg);color:var(--body);font-family:var(--f);font-size:16px;line-height:1.8;-webkit-font-smoothing:antialiased}
  a{color:var(--accent)} img{max-width:100%;height:auto;display:block}
  .ms{font-family:"Material Symbols Rounded";font-weight:normal;font-style:normal;font-size:20px;line-height:1;display:inline-block;vertical-align:-4px;font-feature-settings:"liga"}
  .wrap{max-width:1120px;margin-inline:auto;padding-inline:20px}
  .hdr{position:sticky;top:0;z-index:10;background:var(--bg);border-bottom:1px solid var(--line)}
  .hdr .wrap{display:flex;align-items:center;gap:20px;height:64px}
  .brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--ink)}
  .brand img{height:36px;width:auto}.brand b{display:block;font-size:15px;line-height:1.1}.brand small{display:block;color:#8A93A0;font-size:11px}
  .nav{display:flex;gap:22px;margin-left:auto;font-size:14.5px}.nav a{color:var(--muted);text-decoration:none}.nav a:hover{color:var(--accent)}
  .cta{display:inline-flex;align-items:center;gap:6px;background:var(--accent);color:#fff;text-decoration:none;font-weight:600;font-size:14px;padding:9px 18px;border-radius:999px}
  main{padding-block:40px 72px;flex:1 0 auto;width:100%}
  .band{background:linear-gradient(180deg,#EAF6EF,#F6F8F7);border-bottom:1px solid var(--line)}
  .band .wrap{padding-block:44px 38px}
  .band h1{font-size:36px;color:var(--ink);margin:6px 0 8px;line-height:1.25}
  .band p{margin:0;color:var(--muted);max-width:60ch}
  .band .crumb{margin:0}
  .hdr-tel{display:inline-flex;align-items:center;gap:6px;font-weight:600;font-size:14.5px;color:var(--ink);text-decoration:none;white-space:nowrap}
  .hdr-tel .ms{color:var(--accent)}
  .posts .d{display:flex;align-items:center;gap:6px;font-size:13px;color:var(--muted);margin-bottom:6px}
  .posts .more{display:inline-flex;align-items:center;gap:4px;margin-top:12px;color:var(--accent);font-weight:600;font-size:14.5px}
  .posts a:hover img{transform:scale(1.04)} .posts img{transition:transform .5s ease}
  .posts .ph{overflow:hidden}
  .crumb{font-size:13.5px;color:var(--muted);margin-bottom:14px}.crumb a{color:var(--muted);text-decoration:none}
  article{max-width:760px;margin-inline:auto}
  article h1{font-size:34px;line-height:1.3;color:var(--ink);margin:0 0 10px;text-wrap:balance}
  article h2{font-size:24px;line-height:1.35;color:var(--ink);margin:36px 0 10px}
  article h3{font-size:19px;color:var(--ink);margin:28px 0 8px}
  article p,article li{color:var(--body)} article ul,article ol{padding-left:22px}
  .meta{display:flex;gap:16px;color:var(--muted);font-size:14px;margin-bottom:24px}
  .cover{border-radius:16px;overflow:hidden;box-shadow:var(--shadow-card);margin:0 0 28px}
  .box{margin-top:40px;padding:22px 24px;border-radius:16px;background:var(--accent-soft);display:flex;gap:16px;align-items:center;flex-wrap:wrap}
  .box b{display:block;color:var(--ink);font-size:18px}.box span{color:var(--muted);font-size:14.5px}.box div{flex:1;min-width:220px}
  .posts{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px}
  .posts a{display:block;text-decoration:none;color:inherit;border-radius:16px;overflow:hidden;box-shadow:var(--shadow-card);background:#fff;height:100%}
  .posts img{aspect-ratio:16/9;object-fit:cover;width:100%}.posts .tx{padding:18px 22px 22px}.posts h2{font-size:20px;margin:0 0 8px;color:var(--ink);line-height:1.4}.posts p{margin:0;color:var(--muted);font-size:14.5px}
  .tbl{overflow-x:auto;margin:18px 0 22px;border-radius:12px;border:1px solid var(--line)}
  .tbl table{border-collapse:collapse;width:100%;min-width:520px;font-size:15px;line-height:1.6}
  .tbl th,.tbl td{padding:10px 14px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}
  .tbl thead th{background:var(--band);color:var(--ink);font-weight:600} .tbl tbody tr:last-child td{border-bottom:0}
  .tbl td:first-child{color:var(--ink);font-weight:500}
  .tldr{margin:22px 0;padding:16px 20px;border-radius:14px;background:var(--accent-soft);border-left:4px solid var(--accent)}
  .tldr p{margin:0 0 6px;color:var(--ink)} .tldr ul{margin:0}
  .vid{margin:18px auto 22px;max-width:340px} .vid video{width:100%;height:auto;border-radius:16px;background:#000;box-shadow:var(--shadow-card);display:block}
  .vid figcaption,.gal figcaption{font-size:13.5px;color:var(--muted);margin-top:8px;text-align:center}
  .gal{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:20px 0 8px} .gal figure{margin:0;min-width:0}
  .gal figure:first-child{grid-column:1/-1} .gal img{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:12px}
  article h1 .nb{display:inline-block} article a[href^="tel:"]{white-space:nowrap}
  article code{background:var(--band);padding:1px 6px;border-radius:6px;font-size:.92em}
  footer{background:var(--dark);color:rgba(255,255,255,.72);padding-block:44px 24px;font-size:14px;flex-shrink:0}
  .ft{display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:28px}
  .ft h4{margin:0 0 10px;color:#fff;font-size:15px}
  .ft a,.ft .r{display:flex;align-items:center;gap:8px;padding-block:3px;color:rgba(255,255,255,.72);text-decoration:none}
  .ft a:hover{color:#fff} .ft .ms{font-size:18px;color:#5BE092}
  .ft .co{color:#fff;font-weight:600;font-size:16px;margin-bottom:6px}
  .soc{display:flex;gap:10px;margin:4px 0 10px} .soc a{width:40px;height:40px;border-radius:12px;background:rgba(255,255,255,.08);display:grid;place-items:center;padding:0}
  .soc svg{width:20px;height:20px}
  .copy{border-top:1px solid rgba(255,255,255,.12);margin-top:28px;padding-top:16px;font-size:13px}
  @media (max-width:760px){ .ft{grid-template-columns:1fr} .band h1{font-size:28px} .hdr-tel{display:none} }
  @media (max-width:520px){ .gal{grid-template-columns:1fr} .tbl table{min-width:0;font-size:14px} .tbl th,.tbl td{padding:9px 10px} }
  @media (max-width:760px){ .nav{display:none} .cta{margin-left:auto} article h1{font-size:27px} }
</style>
'''
HEADER = f'''<header class="hdr"><div class="wrap">
  <a class="brand" href="/"><img src="/pf/jjr.webp" alt="JJR Solar" width="54" height="36"><span><b>JJR โซล่าเซลล์</b><small>บจก. จงเจริญ โซลาร์เซลล์</small></span></a>
  <nav class="nav"><a href="/#work">ผลงาน</a><a href="/#clients">ลูกค้า</a><a href="/#calc">คำนวณ</a><a href="/blog/">บทความ</a></nav>
  <a class="hdr-tel" href="tel:{C.PHONE_TEL}"><span class="ms">call</span>{C.PHONE}</a>
  <a class="cta" href="/#quote">ขอใบเสนอราคา</a>
</div></header>
'''
FOOTER = f'''<footer><div class="wrap">
  <div class="ft">
    <div><div class="co">JJR โซล่าเซลล์</div>บริษัท จงเจริญ โซลาร์เซลล์ จำกัด<br>ติดตั้งกับช่างที่ชำนาญ บริการใกล้บ้านคุณ · ให้บริการติดตั้งทั่วภาคอีสาน
      <div class="r" style="margin-top:12px;align-items:flex-start"><span class="ms">location_on</span><span>{C.ADDRESS}<br>({C.ADDRESS_NOTE}) · <a href="{C.MAP_URL}" target="_blank" rel="noopener" style="display:inline;color:#fff">แผนที่</a></span></div>
      <div class="r"><span class="ms">schedule</span>{C.HOURS}</div></div>
    <div><h4>ติดต่อ</h4><a href="tel:{C.PHONE_TEL}"><span class="ms">call</span>{C.PHONE}</a><a href="{C.LINE_URL}" target="_blank" rel="noopener"><span class="ms">chat</span>LINE {C.LINE_ID}</a><div class="r"><span class="ms">mail</span>{C.EMAIL}</div><a href="/#quote"><span class="ms">request_quote</span>ขอใบเสนอราคา</a></div>
    <div><h4>ติดตามเรา</h4>
      <div class="soc"><a href="{C.LINE_URL}" target="_blank" rel="noopener" aria-label="LINE">{C.SVG_LINE}</a><a href="{C.TIKTOK_URL}" target="_blank" rel="noopener" aria-label="TikTok">{C.SVG_TIKTOK}</a><a href="{C.YOUTUBE_URL}" target="_blank" rel="noopener" aria-label="YouTube">{C.SVG_YOUTUBE}</a></div>
      <a href="/blog/"><span class="ms">article</span>บทความ</a><a href="/privacy-policy/"><span class="ms">shield</span>นโยบายความเป็นส่วนตัว</a></div>
  </div>
  <div class="copy">© 2569 บริษัท จงเจริญ โซลาร์เซลล์ จำกัด</div>
</div></footer>
'''
CTA = '''<div class="box"><div><b>อยากรู้ว่าโรงงานหรือบ้านของคุณควรติดกี่ kW</b><span>ส่งข้อมูลให้ทีม JJR สำรวจหน้างานฟรี ไม่มีข้อผูกมัด</span></div>
<a class="cta" href="/#quote">ขอใบเสนอราคาฟรี <span class="ms">arrow_forward</span></a></div>'''

def clean_wp(c):
    c = re.sub(r'<(script|style|noscript)[^>]*>.*?</\1>', '', c, flags=re.S)
    c = re.sub(r'<!--.*?-->', '', c, flags=re.S)
    c = re.sub(r'<figure[^>]*>.*?</figure>', '', c, flags=re.S)
    c = re.sub(r'<img[^>]*>', '', c)
    c = re.sub(r'\s(class|style|id|data-[a-z-]+|srcset|sizes|decoding|loading|width|height|fetchpriority)="[^"]*"', '', c)
    c = re.sub(r'<(/?)(div|span|section)[^>]*>', '', c)
    c = re.sub(r'<p>\s*(&nbsp;)?\s*</p>', '', c)
    return c.strip()

def post_page(slug, title, desc, date, modified, body_html, cover, cover_wh=(1024, 576), og=None, ld_type='BlogPosting', extra_ld=(), seo_title=None, cover_alt=None):
    iso = date[:10]
    ld = {"@context": "https://schema.org", "@type": ld_type, "headline": title, "description": desc,
          "datePublished": date, "dateModified": modified, "image": SITE + (og or cover), "inLanguage": "th",
          "mainEntityOfPage": f"{SITE}/{slug}/",
          "author": {"@type": "Organization", "name": "JJR โซล่าเซลล์", "url": SITE + "/"},
          "publisher": {"@type": "Organization", "name": "บริษัท จงเจริญ โซลาร์เซลล์ จำกัด", "logo": {"@type": "ImageObject", "url": SITE + "/icon-512.png"}}}
    th_date = f'{int(iso[8:10])} ' + ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'][int(iso[5:7]) - 1] + f' {int(iso[:4]) + 543}'
    h1_html = ' '.join(f'<span class="nb">{E(x)}</span>' for x in re.split(r'(?<=[?:]) ', title))
    lds = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in (ld, *extra_ld))
    page = head(f'{seo_title or title} | JJR โซล่าเซลล์', desc, f'/{slug}/', SITE + (og or cover), FONTS + PAGE_CSS + lds).replace(
        '<meta property="og:type" content="website">', '<meta property="og:type" content="article">') + '</head>\n<body>\n' + HEADER + f'''<main class="wrap">
<article>
  <div class="crumb"><a href="/">หน้าแรก</a> › <a href="/blog/">บทความ</a></div>
  <h1>{h1_html}</h1>
  <div class="meta"><span><span class="ms">calendar_today</span> {th_date}</span><span>JJR โซล่าเซลล์</span></div>
  <figure class="cover" style="margin:0 0 28px"><img src="{cover}" alt="{E(cover_alt or title)}" width="{cover_wh[0]}" height="{cover_wh[1]}"></figure>
{body_html}
{CTA}
</article>
</main>
''' + FOOTER + '</body>\n</html>\n'
    os.makedirs(slug, exist_ok=True)
    open(f'{slug}/index.html', 'w', encoding='utf8').write(page)

posts = []
# บทความ 1: ประโยชน์ของโซล่าเซลล์ — ย้ายตามต้นฉบับ
d = json.load(open('_src/benefits-of-solar-cells.json', encoding='utf8'))[0]
desc1 = 'เรียนรู้เกี่ยวกับประโยชน์หลัก ๆ ของโซล่าเซลล์ และทำไมคุณควรเริ่มใช้พลังงานจากแสงอาทิตย์'
post_page('benefits-of-solar-cells', html.unescape(d['title']['rendered']), desc1, d['date'], d['modified'],
          clean_wp(d['content']['rendered']), '/img/blog/benefits-of-solar-cells.webp')
posts.append(('benefits-of-solar-cells', html.unescape(d['title']['rendered']), desc1, d['date']))

# บทความ 2: JJR โซล่าเซลล์ บริการครบวงจร — คงหัวข้อ/บริการ/คีย์เวิร์ด ตัดตัวเลขที่บริษัทไม่ให้ใช้ (% ลดค่าไฟ คืนทุน รับประกันกี่ปี) + LINE
d = json.load(open('_src/jjrsolarcell.json', encoding='utf8'))[0]
t2 = html.unescape(d['title']['rendered'])
desc2 = 'JJR โซล่าเซลล์ พลังงานสะอาดเพื่ออนาคต บริการติดตั้งโซล่าเซลล์ครบวงจร ตั้งแต่ออกแบบ ติดตั้ง ตรวจสอบ จนถึงดูแลรักษา โดยทีมช่างผู้ชำนาญ'
body2 = '''<h2>JJR โซล่าเซลล์ พลังงานสะอาดเพื่ออนาคต</h2>
<p>เบื่อหน่ายหรือไม่ กับค่าไฟที่พุ่งสูงขึ้นทุกเดือน JJR โซล่าเซลล์ พร้อมตอบโจทย์ทุกความต้องการของคุณ</p>
<p>โซล่าเซลล์ เปลี่ยนแสงอาทิตย์เป็นพลังงานไฟฟ้า โดยไม่ต้องพึ่งพาเชื้อเพลิงฟอสซิล ช่วยลดการปล่อยก๊าซคาร์บอนไดออกไซด์ เป็นมิตรต่อสิ่งแวดล้อม และช่วยลดค่าไฟฟ้าในระยะยาว การติดตั้งโซล่าเซลล์ยังเป็นการเพิ่มมูลค่าและฟังก์ชันให้กับบ้านหรืออาคารของคุณ</p>
<h2>บริการครบวงจร มั่นใจได้</h2>
<p>ดูแลตั้งแต่การออกแบบ ติดตั้ง ตรวจสอบ และดูแลรักษา</p>
<ul>
<li>ติดตั้งระบบโซล่าเซลล์อย่างมืออาชีพ</li>
<li>ตรวจสอบระบบโซล่าเซลล์เป็นประจำ</li>
<li>ดูแลรักษาระบบโซล่าเซลล์ให้มีประสิทธิภาพ</li>
</ul>
<h2>ทีมงานมืออาชีพ</h2>
<ul>
<li>วิศวกรและช่างผู้ชำนาญ</li>
<li>ช่างผ่านการอบรมจากผู้ผลิตอุปกรณ์โซล่าเซลล์</li>
</ul>
<h2>อุปกรณ์มาตรฐาน มั่นใจในคุณภาพ</h2>
<ul>
<li>แผงโซล่าเซลล์จากผู้ผลิตชั้นนำ</li>
<li>อินเวอร์เตอร์ประสิทธิภาพสูง</li>
<li>อุปกรณ์ไฟฟ้าได้มาตรฐาน</li>
<li>รับประกันตามเงื่อนไขของผู้ผลิตแต่ละแบรนด์ รายละเอียดระบุในใบเสนอราคา</li>
</ul>
<h2>ผลงานการติดตั้ง</h2>
<p>ดูผลงานติดตั้งจริงของ JJR ทั้งโรงงาน อาคารพาณิชย์ หน่วยงาน และบ้านพักอาศัย ในอุบลราชธานี ศรีสะเกษ ยโสธร และสุรินทร์ ได้ที่ <a href="/#work">หน้าผลงาน</a></p>
<h2>ช่องทางการติดต่อ</h2>
<ul>
<li>เบอร์โทรศัพท์: <a href="tel:''' + C.PHONE_TEL + '''">''' + C.PHONE + '''</a></li>
<li>LINE OA: <a href="''' + C.LINE_URL + '''" rel="noopener">''' + C.LINE_ID + '''</a></li>
<li>อีเมล: ''' + C.EMAIL + '''</li>
<li>ขอใบเสนอราคาออนไลน์: <a href="/#quote">กรอกฟอร์มที่นี่</a></li>
<li>สำนักงานใหญ่: ''' + C.ADDRESS + ' (' + C.ADDRESS_NOTE + ''') <a href="''' + C.MAP_URL + '''" rel="noopener">ดูแผนที่</a></li>
<li>เวลาทำการ: ''' + C.HOURS + '''</li>
<li>TikTok: <a href="''' + C.TIKTOK_URL + '''" rel="noopener">JJR Solar Rooftop</a> · YouTube: <a href="''' + C.YOUTUBE_URL + '''" rel="noopener">JJR Solar</a></li>
</ul>
<p style="color:var(--muted);font-size:14px">jjrโซล่าเซลล์, โซล่าเซลล์อุบล, อุบลโซล่าเซลล์, ติดตั้งโซล่าเซลล์</p>'''
post_page('jjrsolarcell', t2, desc2, d['date'], d['modified'], body2, '/img/blog/jjrsolarcell.webp')
posts.append(('jjrsolarcell', t2, desc2, d['date']))

# บทความ 3: On-Grid กับ Hybrid (ทีมคอนเทนต์ส่งมาเป็น .md · ส่วน [[รอช่างยืนยัน]] ถูกซ่อนอัตโนมัติจนกว่าจะเติมคำตอบใน _build/posts/*.md)
slug3 = 'on-grid-vs-hybrid-solar-home'
A3 = '/img/blog/on-grid-vs-hybrid/'
md3 = open(f'_build/posts/{slug3}.md', encoding='utf8').read()
GAL3 = [('01', 1200, 676, 'งานติดตั้งโซลาร์เซลล์บ้านพักอาศัย ระบบ On-Grid 5 kW · อุบลราชธานี', 'On-Grid 5 kW · ไม่มีแบตเตอรี่'),
        ('02', 887, 665, 'อินเวอร์เตอร์และแบตเตอรี่ระบบ Hybrid ติดตั้งผนังในบ้านลูกค้า', 'Hybrid · อินเวอร์เตอร์ + แบตเตอรี่'),
        ('03', 1200, 676, 'งานติดตั้งโซลาร์เซลล์ระบบ Hybrid และ On-Grid ภาพมุมสูง', 'งานติดตั้งจริงของทีม JJR'),
        ('04', 1200, 676, 'งานติดตั้งโซลาร์เซลล์บ้านพักอาศัย ภาพมุมสูง', 'บ้านพักอาศัย'),
        ('05', 1200, 676, 'งานติดตั้งโซลาร์เซลล์บ้านพักอาศัยในหมู่บ้าน ภาพมุมสูง', 'บ้านในหมู่บ้าน')]
gal3 = '<div class="gal">' + ''.join(
    f'<figure><a href="{A3}g{n}-{w}.webp" target="_blank" rel="noopener"><img src="{A3}g{n}-640.webp" srcset="{A3}g{n}-640.webp 640w, {A3}g{n}-{w}.webp {w}w" '
    f'sizes="(max-width:760px) 100vw, 380px" alt="{E(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async"></a><figcaption>{E(cap)}</figcaption></figure>'
    for n, w, h, alt, cap in GAL3) + '</div>'
vid3 = (f'<figure class="vid"><video controls playsinline preload="none" poster="{A3}hybrid-38s.webp" width="720" height="1280">'
        f'<source src="{A3}hybrid-38s.mp4" type="video/mp4"></video><figcaption>คลิป 38 วินาที · ระบบไฮบริดใช้ไฟจากไหนก่อน (เปิดเสียงได้)</figcaption></figure>')
body3, faq3 = MD.convert(md3, {'[วิดีโอ': vid3, '[แกลเลอรี': gal3})
assert MD.PENDING not in body3
t3 = 'On-Grid กับ Hybrid ต่างกันยังไง? เลือกโซลาร์เซลล์บ้านแบบไหนดี'
desc3 = 'ออนกริดกับไฮบริดต่างกันตรงไหน แบตเตอรี่จำเป็นไหม ไฟดับใช้ได้ไหม บ้านแบบไหนเหมาะกับระบบไหน พร้อมตัวเลขจริงจากบ้าน 84 หลังที่ JJR ติดตั้งในอีสาน'
date3 = '2026-09-30T09:00:00+07:00'
ld_faq = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq3]}
ld_vid = {"@context": "https://schema.org", "@type": "VideoObject", "name": "ระบบไฮบริด ใช้ไฟจากไหนก่อน",
          "description": "ลำดับการใช้ไฟของโซลาร์เซลล์ระบบไฮบริด: แดดก่อน แบตเป็นลำดับที่สอง การไฟฟ้าเป็นลำดับสุดท้าย",
          "thumbnailUrl": SITE + A3 + 'hybrid-38s.webp', "contentUrl": SITE + A3 + 'hybrid-38s.mp4', "uploadDate": date3, "duration": "PT38S"}
post_page(slug3, t3, desc3, date3, date3, body3, '/img/blog/on-grid-vs-hybrid-solar-home.webp', (1200, 630), og=A3 + 'cover.jpg',
          ld_type='Article', extra_ld=[x for x in (ld_faq if faq3 else None, ld_vid) if x],
          seo_title='On-Grid กับ Hybrid ต่างกันยังไง? โซลาร์เซลล์บ้านแบบไหนดี', cover_alt='เทียบระบบโซลาร์เซลล์ On-Grid (ไม่มีแบตเตอรี่) กับ Hybrid (มีแบตเตอรี่) จากงานติดตั้งจริงของ JJR')
posts.append((slug3, t3, desc3, date3))

# บทความ 4: เงินอุดหนุนโซลาร์ 50,000 บาท (ทีมคอนเทนต์ 5 ต.ค. 69) — ข่าวเปลี่ยนเร็ว: ถ้ามีมติ ครม./หลักเกณฑ์ ให้แก้ _build/posts/*.md
# ช่วง [[รอยืนยัน e-Tax]] … [[/รอยืนยัน]] (สิทธิ์ลดหย่อนภาษี) ซ่อนจนกว่าโป้งยืนยันว่า JJR ออก e-Tax Invoice ได้ → ใส่ 'e-Tax' ใน CONFIRMED4
slug4 = 'solar-subsidy-50000-baht-update'
CONFIRMED4 = ()
md4 = open(f'_build/posts/{slug4}.md', encoding='utf8').read()
body4, faq4 = MD.convert(md4, confirmed=CONFIRMED4)
assert '[[รอ' not in body4 and '[[/รอ' not in body4
t4 = 'เงินอุดหนุนโซลาร์เซลล์ 50,000 บาท สรุปล่าสุด: ข้อเสนอขยายให้ติดบนดิน-ลอยน้ำ ลงทะเบียนได้เมื่อไหร่'
desc4 = 'สรุปข้อเสนอเงินอุดหนุนโซลาร์เซลล์ 50,000 บาท 1.5 ล้านหลัง ขยายให้ติดบนพื้นดินและโซลาร์ลอยน้ำได้ สถานะยังรอ ครม. คาดว่าเปิดลงทะเบียน 1 พ.ย. 69 ควรเตรียมอะไร'
date4 = '2026-10-05T09:00:00+07:00'
ld_faq4 = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq4]}
post_page(slug4, t4, desc4, date4, date4, body4, f'/img/blog/{slug4}.webp', (1200, 630), og=f'/img/blog/{slug4}/cover.jpg',
          ld_type='Article', extra_ld=[ld_faq4] if faq4 else [],
          seo_title='เงินอุดหนุนโซลาร์เซลล์ 50,000 บาท ล่าสุด ลงทะเบียนเมื่อไหร่',
          cover_alt='ข่าว มท. ลงนามขอใช้เงินกู้ 7.5 หมื่นล้าน ขยายกลุ่มอุดหนุนติดโซลาร์เซลล์บนดิน-ลอยน้ำ')
posts.append((slug4, t4, desc4, date4))

# ---------------------------------------------------------------- blog index
posts.sort(key=lambda p: p[3], reverse=True)
TH_M = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']
def th_date(iso): return f'{int(iso[8:10])} {TH_M[int(iso[5:7]) - 1]} {int(iso[:4]) + 543}'
items = ''.join(f'<li><a href="/{s}/"><div class="ph"><img src="/img/blog/{s}.webp" alt="{E(t)}" loading="lazy" width="1024" height="576"></div><div class="tx"><div class="d"><span class="ms">calendar_today</span>{th_date(dt)}</div><h2>{E(t)}</h2><p>{E(ds)}</p><span class="more">อ่านต่อ <span class="ms">arrow_forward</span></span></div></a></li>' for s, t, ds, dt in posts)
os.makedirs('blog', exist_ok=True)
open('blog/index.html', 'w', encoding='utf8').write(
    head('บทความ | JJR โซล่าเซลล์', 'บทความและความรู้เรื่องโซล่าเซลล์จาก JJR โซล่าเซลล์', '/blog/', extra=FONTS + PAGE_CSS) + '</head>\n<body>\n' + HEADER +
    '<section class="band"><div class="wrap"><div class="crumb"><a href="/">หน้าแรก</a> › บทความ</div><h1>บทความ</h1><p>ความรู้เรื่องโซล่าเซลล์ การเลือกขนาดระบบ และเรื่องน่ารู้ก่อนติดตั้ง จากทีม JJR โซล่าเซลล์</p></div></section>\n'
    f'<main class="wrap"><ul class="posts">{items}</ul>{CTA}</main>\n' + FOOTER + '</body>\n</html>\n')

# ---------------------------------------------------------------- privacy policy (ต้นฉบับเดิม + ข้อมูลจากฟอร์มเว็บไซต์)
d = json.load(open('_src/privacy-policy.json', encoding='utf8'))[0]
pp = clean_wp(d['content']['rendered'])
pp = re.sub(r'https?://(www\.)?jjrsolarcell\.com/wp-content/uploads/[^"]+\.pdf', '/files/privacy-policy.pdf', pp)
pp = re.sub(r'^\s*<h[1-3][^>]*>\s*นโยบายคุ้มครองข้อมูลส่วนบุคคล\s*</h[1-3]>', '', pp)  # ต้นฉบับซ้ำกับ h1
pp = pp.replace('081-429-4693', C.PHONE).replace('0814294693', C.PHONE_TEL)
pp += '''
<h2>ข้อมูลที่เก็บจากแบบฟอร์มขอใบเสนอราคาบนเว็บไซต์</h2>
<p>เมื่อคุณกรอกแบบฟอร์มขอใบเสนอราคา เราเก็บชื่อ เบอร์โทรศัพท์ ประเภทสถานที่ ค่าไฟต่อเดือน พื้นที่ และรายละเอียดที่คุณกรอก เพื่อใช้ติดต่อกลับ สำรวจหน้างาน และจัดทำใบเสนอราคาเท่านั้น ข้อมูลจัดเก็บในระบบงานภายในของบริษัท และไม่ขายหรือเปิดเผยให้บุคคลภายนอก หากต้องการให้ลบหรือแก้ไขข้อมูล ติดต่อ 094-264-6142 หรือ jjrsolarcell@gmail.com</p>'''
os.makedirs('privacy-policy', exist_ok=True)
open('privacy-policy/index.html', 'w', encoding='utf8').write(
    head('นโยบายคุ้มครองข้อมูลส่วนบุคคล | JJR โซล่าเซลล์', 'นโยบายคุ้มครองข้อมูลส่วนบุคคลของ บริษัท จงเจริญ โซลาร์เซลล์ จำกัด ตาม พ.ร.บ.คุ้มครองข้อมูลส่วนบุคคล พ.ศ. 2562', '/privacy-policy/', extra=FONTS + PAGE_CSS)
    + '</head>\n<body>\n' + HEADER + f'<main class="wrap"><article><div class="crumb"><a href="/">หน้าแรก</a> › นโยบายความเป็นส่วนตัว</div><h1>นโยบายคุ้มครองข้อมูลส่วนบุคคล</h1>\n{pp}\n</article></main>\n' + FOOTER + '</body>\n</html>\n')

# ---------------------------------------------------------------- 404
open('404.html', 'w', encoding='utf8').write(
    head('ไม่พบหน้านี้ | JJR โซล่าเซลล์', 'ไม่พบหน้าที่คุณต้องการ', '/404.html', extra=FONTS + PAGE_CSS).replace('index,follow,max-image-preview:large', 'noindex') + '</head>\n<body>\n' + HEADER +
    '<main class="wrap" style="text-align:center;padding-block:90px"><h1 style="font-size:64px;color:var(--accent);margin:0">404</h1><p style="font-size:18px;color:var(--ink)">ไม่พบหน้าที่คุณต้องการ</p><p><a class="cta" href="/"><span class="ms">arrow_back</span> กลับหน้าแรก</a></p></main>\n' + FOOTER + '</body>\n</html>\n')

# ---------------------------------------------------------------- sitemap + robots
urls = [('/', TODAY, '1.0'), ('/blog/', TODAY, '0.6')] + [(f'/{s}/', dt[:10], '0.5') for s, _, _, dt in posts] + [('/privacy-policy/', TODAY, '0.2')]
open('sitemap.xml', 'w', encoding='utf8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    ''.join(f'  <url><loc>{SITE}{u}</loc><lastmod>{lm}</lastmod><priority>{p}</priority></url>\n' for u, lm, p in urls) + '</urlset>\n')
open('robots.txt', 'w', encoding='utf8').write(f'User-agent: *\nAllow: /\nDisallow: /_build/\nDisallow: /_src/\n\nSitemap: {SITE}/sitemap.xml\n')
print('built:', ', '.join(['index.html', 'blog/', *[s + '/' for s, *_ in posts], 'privacy-policy/', '404.html', 'sitemap.xml', 'robots.txt']))
