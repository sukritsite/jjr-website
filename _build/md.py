# แปลงบทความ Markdown (รูปแบบที่ทีมคอนเทนต์ส่งมา) เป็น HTML สำหรับหน้าบทความ
# รองรับ: # หัวข้อ, ย่อหน้า (ขึ้นบรรทัดใหม่ = <br>), - / 1. รายการ, | ตาราง |, > กล่องสรุป, **หนา**, *เอียง*, `code`, [ข้อความ](ลิงก์), ลิงก์/เบอร์โทรเปล่า
# กติกา README ของทีมคอนเทนต์: ข้อความใน [[รอช่างยืนยัน: …]] ห้ามขึ้นเว็บ → ตัดทิ้งทั้งแถวตาราง / รายการ / ย่อหน้า
#   และในส่วน FAQ ตัดทั้งคำถาม (คำตอบครึ่งเดียวทำให้เข้าใจผิด)
import re, html

PENDING = '[[รอช่างยืนยัน'

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?!\w)', r'<em>\1</em>', s)
    s = re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+|/[^)\s]*)\)', r'<a href="\2">\1</a>', s)
    s = re.sub(r'(?<!["=>])(https?://[^\s<]+[^\s<.,)])', r'<a href="\1" target="_blank" rel="noopener">\1</a>', s)
    s = re.sub(r'(?<![\d-])(0\d{2})-(\d{3})-(\d{4})(?![\d-])', r'<a href="tel:\1\2\3">\1-\2-\3</a>', s)
    return s

def text_of(h):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', h))).strip()

def blocks(md):
    out, cur = [], []
    for line in md.splitlines():
        if line.strip():
            cur.append(line.rstrip())
        elif cur:
            out.append(cur); cur = []
    if cur: out.append(cur)
    return out

def convert(md, hooks=None):
    """คืน (html, faq) — faq = [(คำถาม, คำตอบข้อความล้วน)] สำหรับ FAQPage schema
    hooks = {'[ข้อความในวงเล็บเหลี่ยมทั้งบรรทัด ขึ้นต้นด้วย]': html} ใช้แทนตำแหน่งวิดีโอ/แกลเลอรี"""
    hooks = hooks or {}
    bl = blocks(md)
    # ตัด H1 + บรรทัดผู้เขียนตัวเอียงถัดไป (หน้าเว็บแสดงหัวเรื่อง/วันที่เอง)
    if bl and bl[0][0].startswith('# '): bl.pop(0)
    if bl and re.fullmatch(r'\*[^*].*\*', bl[0][0]): bl.pop(0)

    # จัดกลุ่มตามหัวข้อ เพื่อทำ FAQ และตัดคำถามที่ยังรอคำตอบ
    html_out, faq, in_faq, q = [], [], False, None
    groups, g = [], None
    for b in bl:
        if b[0].startswith('#'):
            g = [b]; groups.append(g)
        else:
            if g is None: g = []; groups.append(g)
            g.append(b)
    for g in groups:
        head = g[0][0] if g and g[0][0].startswith('#') else ''
        if head.startswith('## '): in_faq = 'คำถามที่พบบ่อย' in head
        if in_faq and head.startswith('### ') and any(PENDING in l for b in g for l in b):
            continue
        body = []
        for b in g: body.append(render(b, hooks))
        chunk = '\n'.join(x for x in body if x)
        html_out.append(chunk)
        if in_faq and head.startswith('### '):
            faq.append((text_of(inline(head[4:])), text_of('\n'.join(render(b, hooks) for b in g[1:]))))
    return '\n'.join(html_out), faq

def render(b, hooks):
    first = b[0]
    m = re.match(r'(#{2,4}) (.*)', first)
    if m:
        n = len(m.group(1)); return f'<h{n}>{inline(m.group(2))}</h{n}>'
    if first.startswith('[') and first.endswith(']') and len(b) == 1:
        for k, v in hooks.items():
            if first.startswith(k): return v
        return ''
    if first.startswith('|'):
        rows = [r for r in b if not re.fullmatch(r'\|[\s:|-]+\|', r)]
        rows = [rows[0]] + [r for r in rows[1:] if PENDING not in r]
        cells = [[c.strip() for c in r.strip('|').split('|')] for r in rows]
        th = ''.join(f'<th>{inline(c)}</th>' for c in cells[0])
        tb = ''.join('<tr>' + ''.join(f'<td>{inline(c)}</td>' for c in r) + '</tr>' for r in cells[1:])
        return f'<div class="tbl"><table><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>'
    if first.startswith('>'):
        inner = [re.sub(r'^>\s?', '', l) for l in b]
        return '<aside class="tldr">' + render_lines(inner) + '</aside>'
    return render_lines(b)

def render_lines(lines):
    """ย่อหน้า/รายการ (อาจปนกันในบล็อกเดียว เช่น กล่องสรุป)"""
    out, para, lst, kind = [], [], [], None
    def flush_p():
        if para and not any(PENDING in l for l in para):
            out.append('<p>' + '<br>'.join(inline(l) for l in para) + '</p>')
        para.clear()
    def flush_l():
        nonlocal kind
        items = [i for i in lst if PENDING not in i]
        if items: out.append(f'<{kind}>' + ''.join(f'<li>{inline(i)}</li>' for i in items) + f'</{kind}>')
        lst.clear(); kind = None
    for l in lines:
        mu, mo = re.match(r'\s*[-*] (.*)', l), re.match(r'\s*\d+\. (.*)', l)
        if mu or mo:
            k = 'ul' if mu else 'ol'
            flush_p()
            if kind and kind != k: flush_l()
            kind = k; lst.append((mu or mo).group(1))
        else:
            flush_l() if lst else None
            para.append(l.strip())
    flush_p(); flush_l() if lst else None
    return '\n'.join(out)
