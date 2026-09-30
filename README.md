# jjrsolarcell.com

เว็บไซต์หลักของ บริษัท จงเจริญ โซลาร์เซลล์ จำกัด (JJR โซล่าเซลล์) — เว็บ static (HTML ล้วน) โฮสต์บน Plesk เครื่องเดียวกับ workspace

## โครงสร้าง
- `index.html` — หน้าแรก (ฉาก 3D โรงงาน, ผลงาน, ลูกค้า/พาร์ทเนอร์, คำนวณ, ฟอร์มขอใบเสนอราคา)
- `benefits-of-solar-cells/`, `jjrsolarcell/` — บทความเดิมจาก WordPress (URL เดิม)
- `blog/`, `privacy-policy/`, `404.html`, `sitemap.xml`, `robots.txt`
- `pf/` — รูปผลงาน (ใส่ลายน้ำแล้ว) และโลโก้ลูกค้า/พาร์ทเนอร์
- `.htaccess` — redirect URL เดิมของ WordPress, https, cache, noindex สำหรับ new.jjrsolarcell.com
- `_build/` — ต้นฉบับ + สคริปต์ build (ถูกบล็อกไม่ให้เข้าจากเว็บ)

## แก้เว็บ
1. แก้ `_build/home.src.html` (หน้าแรก) หรือ `_build/build.py` (บทความ/หน้าอื่น)
2. `python _build/build.py`
3. commit + push → Plesk deploy ให้อัตโนมัติ

⚠️ อย่าแก้ไฟล์ตรงใน Plesk File Manager — จะถูก deploy ทับ

## ฟอร์มขอใบเสนอราคา
ส่งไป Cloud Function `submitLead` (project `jjr-workspaces`, repo jjr-workspace) → สร้างงาน "ลูกค้าขอใบเสนอราคา (เว็บไซต์)" ใน `tasks.html`

## กติกาเนื้อหา
- ตัวเลขผลงานใช้ตามไฟล์ข้อมูลของบริษัทเท่านั้น ห้ามเติม MW รวม / จำนวนปี / % ประหยัด / คืนทุน
- โลโก้ลูกค้า/พาร์ทเนอร์ห้ามดัดแปลงสีหรือรูปทรง
- ลูกค้าเอกชนห้ามใส่ชื่อ
