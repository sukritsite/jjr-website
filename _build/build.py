# สร้างไฟล์เว็บ jjrsolarcell.com จากต้นฉบับหน้าแรก (_build/home.src.html) + บทความเดิมจาก WordPress (_src/*.json)
# ใช้:  python _build/build.py   (รันจากโฟลเดอร์ jjr-website)
import io, sys, re, json, html, datetime, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
SITE = 'https://jjrsolarcell.com'
TODAY = datetime.date.today().isoformat()
E = html.escape

def head(title, desc, path, image=SITE + '/pf/p01/01.webp', extra=''):
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
             '<div class="done" id="qDone" hidden><span class="ms fill">check_circle</span><div><b>ได้รับข้อมูลแล้ว</b>ทีมงานจะโทรกลับภายในวันทำการ ถ้าต้องการด่วนโทร 081-429-4693</div></div>'
             '\n        <div class="done err" id="qErr" hidden><span class="ms fill">error</span><div><b>ส่งข้อมูลไม่สำเร็จ</b><span id="qErrMsg">กรุณาลองใหม่ หรือโทร 081-429-4693</span></div></div>', src, count=1, flags=re.S)
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
      .catch(function(err){ $('qErrMsg').textContent = (err && err.message) || 'กรุณาลองใหม่ หรือโทร 081-429-4693'; $('qErr').hidden = false; })
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
  *{box-sizing:border-box} body{margin:0;background:var(--bg);color:var(--body);font-family:var(--f);font-size:16px;line-height:1.8;-webkit-font-smoothing:antialiased}
  a{color:var(--accent)} img{max-width:100%;height:auto;display:block}
  .ms{font-family:"Material Symbols Rounded";font-weight:normal;font-style:normal;font-size:20px;line-height:1;display:inline-block;vertical-align:-4px;font-feature-settings:"liga"}
  .wrap{max-width:1120px;margin-inline:auto;padding-inline:20px}
  .hdr{position:sticky;top:0;z-index:10;background:var(--bg);border-bottom:1px solid var(--line)}
  .hdr .wrap{display:flex;align-items:center;gap:20px;height:64px}
  .brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--ink)}
  .brand img{height:36px;width:auto}.brand b{display:block;font-size:15px;line-height:1.1}.brand small{display:block;color:#8A93A0;font-size:11px}
  .nav{display:flex;gap:22px;margin-left:auto;font-size:14.5px}.nav a{color:var(--muted);text-decoration:none}.nav a:hover{color:var(--accent)}
  .cta{display:inline-flex;align-items:center;gap:6px;background:var(--accent);color:#fff;text-decoration:none;font-weight:600;font-size:14px;padding:9px 18px;border-radius:999px}
  main{padding-block:40px 72px}
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
  .posts{list-style:none;padding:0;margin:24px 0 0;display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}
  .posts a{display:block;text-decoration:none;color:inherit;border-radius:16px;overflow:hidden;box-shadow:var(--shadow-card);background:#fff;height:100%}
  .posts img{aspect-ratio:16/9;object-fit:cover;width:100%}.posts div{padding:16px 18px 18px}.posts h2{font-size:18px;margin:0 0 6px;color:var(--ink);line-height:1.4}.posts p{margin:0;color:var(--muted);font-size:14.5px}
  footer{background:var(--dark);color:rgba(255,255,255,.7);padding-block:32px;font-size:14px}
  footer .wrap{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap} footer a{color:#fff}
  @media (max-width:760px){ .nav{display:none} .cta{margin-left:auto} article h1{font-size:27px} }
</style>
'''
HEADER = '''<header class="hdr"><div class="wrap">
  <a class="brand" href="/"><img src="/pf/jjr.webp" alt="JJR Solar" width="54" height="36"><span><b>JJR โซล่าเซลล์</b><small>บจก. จงเจริญ โซลาร์เซลล์</small></span></a>
  <nav class="nav"><a href="/#work">ผลงาน</a><a href="/#clients">ลูกค้า</a><a href="/#calc">คำนวณ</a><a href="/blog/">บทความ</a></nav>
  <a class="cta" href="/#quote">ขอใบเสนอราคา</a>
</div></header>
'''
FOOTER = '''<footer><div class="wrap">
  <div><b style="color:#fff">บริษัท จงเจริญ โซลาร์เซลล์ จำกัด</b><br>ติดตั้งกับช่างที่ชำนาญ บริการใกล้บ้านคุณ · โทร 081-429-4693 · jjrsolarcell@gmail.com</div>
  <div><a href="/">หน้าแรก</a> · <a href="/blog/">บทความ</a> · <a href="/privacy-policy/">นโยบายความเป็นส่วนตัว</a></div>
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

def post_page(slug, title, desc, date, modified, body_html, cover):
    iso = date[:10]
    ld = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": title, "description": desc,
          "datePublished": date, "dateModified": modified, "image": SITE + cover, "inLanguage": "th",
          "mainEntityOfPage": f"{SITE}/{slug}/",
          "author": {"@type": "Organization", "name": "JJR โซล่าเซลล์", "url": SITE + "/"},
          "publisher": {"@type": "Organization", "name": "บริษัท จงเจริญ โซลาร์เซลล์ จำกัด", "logo": {"@type": "ImageObject", "url": SITE + "/icon-512.png"}}}
    th_date = f'{int(iso[8:10])} ' + ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'][int(iso[5:7]) - 1] + f' {int(iso[:4]) + 543}'
    page = head(f'{title} | JJR โซล่าเซลล์', desc, f'/{slug}/', SITE + cover,
                FONTS + PAGE_CSS + f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n') + '</head>\n<body>\n' + HEADER + f'''<main class="wrap">
<article>
  <div class="crumb"><a href="/">หน้าแรก</a> › <a href="/blog/">บทความ</a></div>
  <h1>{E(title)}</h1>
  <div class="meta"><span><span class="ms">calendar_today</span> {th_date}</span><span>JJR โซล่าเซลล์</span></div>
  <figure class="cover" style="margin:0 0 28px"><img src="{cover}" alt="{E(title)}" width="1024" height="576"></figure>
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
<li>เบอร์โทรศัพท์: 081-429-4693</li>
<li>อีเมล: jjrsolarcell@gmail.com</li>
<li>ขอใบเสนอราคาออนไลน์: <a href="/#quote">กรอกฟอร์มที่นี่</a></li>
<li>Facebook: <a href="https://facebook.com/jjr.detudom" rel="noopener">JJR โซล่าเซลล์</a></li>
</ul>
<p style="color:var(--muted);font-size:14px">jjrโซล่าเซลล์, โซล่าเซลล์อุบล, อุบลโซล่าเซลล์, ติดตั้งโซล่าเซลล์</p>'''
post_page('jjrsolarcell', t2, desc2, d['date'], d['modified'], body2, '/img/blog/jjrsolarcell.webp')
posts.append(('jjrsolarcell', t2, desc2, d['date']))

# ---------------------------------------------------------------- blog index
posts.sort(key=lambda p: p[3], reverse=True)
items = ''.join(f'<li><a href="/{s}/"><img src="/img/blog/{s}.webp" alt="{E(t)}" loading="lazy" width="1024" height="576"><div><h2>{E(t)}</h2><p>{E(ds)}</p></div></a></li>' for s, t, ds, _ in posts)
open('blog/index.html' if os.path.isdir('blog') else (os.makedirs('blog') or 'blog/index.html'), 'w', encoding='utf8').write(
    head('บทความ | JJR โซล่าเซลล์', 'บทความและความรู้เรื่องโซล่าเซลล์จาก JJR โซล่าเซลล์', '/blog/', extra=FONTS + PAGE_CSS) + '</head>\n<body>\n' + HEADER +
    f'<main class="wrap"><div class="crumb"><a href="/">หน้าแรก</a> › บทความ</div><h1 style="font-size:32px;color:var(--ink);margin:0">บทความ</h1><ul class="posts">{items}</ul></main>\n' + FOOTER + '</body>\n</html>\n')

# ---------------------------------------------------------------- privacy policy (ต้นฉบับเดิม + ข้อมูลจากฟอร์มเว็บไซต์)
d = json.load(open('_src/privacy-policy.json', encoding='utf8'))[0]
pp = clean_wp(d['content']['rendered'])
pp = re.sub(r'https?://(www\.)?jjrsolarcell\.com/wp-content/uploads/[^"]+\.pdf', '/files/privacy-policy.pdf', pp)
pp += '''
<h2>ข้อมูลที่เก็บจากแบบฟอร์มขอใบเสนอราคาบนเว็บไซต์</h2>
<p>เมื่อคุณกรอกแบบฟอร์มขอใบเสนอราคา เราเก็บชื่อ เบอร์โทรศัพท์ ประเภทสถานที่ ค่าไฟต่อเดือน พื้นที่ และรายละเอียดที่คุณกรอก เพื่อใช้ติดต่อกลับ สำรวจหน้างาน และจัดทำใบเสนอราคาเท่านั้น ข้อมูลจัดเก็บในระบบงานภายในของบริษัท และไม่ขายหรือเปิดเผยให้บุคคลภายนอก หากต้องการให้ลบหรือแก้ไขข้อมูล ติดต่อ 081-429-4693 หรือ jjrsolarcell@gmail.com</p>'''
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
