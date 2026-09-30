# ช่องทางติดต่อหลัก (JJR Solar Rooftop) — ใช้ร่วมกันทุกหน้า
PHONE = '094-264-6142'
PHONE_TEL = '0942646142'
PHONE_INTL = '+66942646142'
EMAIL = 'jjrsolarcell@gmail.com'
LINE_ID = '@jjrsolarrooftop'
LINE_URL = 'https://s.jjrsolarcell.com/lr'
MAP_URL = 'https://s.jjrsolarcell.com/mr'
TIKTOK_URL = 'https://s.jjrsolarcell.com/tr'
YOUTUBE_URL = 'https://s.jjrsolarcell.com/yt'
ADDRESS = '71/36 ถ.เลี่ยงเมือง ต.ในเมือง อ.เมืองอุบลราชธานี จ.อุบลราชธานี 34000'
ADDRESS_NOTE = 'ตรงข้ามแม็คโครอุบลฯ'
HOURS = 'เปิดทำการทุกวัน 08.00–17.00 น.'
GEO = (15.2686084, 104.8354157)
SAME_AS = ['https://lin.ee/O4JiyJR', 'https://www.tiktok.com/@jjrsolarcell', 'https://www.youtube.com/@JJR.solarcell']

# โลโก้ทางการ (Simple Icons v13, ไฟล์ใน _build/icons) — TikTok ใช้แบบขาวล้วนบนพื้นเข้ม (monochrome ทางการ)
import os as _os, re as _re
def _svg(name, fill):
    raw = open(_os.path.join(_os.path.dirname(__file__), 'icons', name + '.svg'), encoding='utf8').read()
    d = _re.search(r'<path d="([^"]+)"', raw).group(1)
    return f'<svg viewBox="0 0 24 24" fill="{fill}" aria-hidden="true"><path d="{d}"/></svg>'
SVG_LINE = _svg('line', '#06C755')
SVG_TIKTOK = _svg('tiktok', '#FFFFFF')
SVG_YOUTUBE = _svg('youtube', '#FF0000')
