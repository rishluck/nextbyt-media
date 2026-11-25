import json, sys, asyncio
from playwright.async_api import async_playwright

MARK = '''<svg viewBox="0 0 100 100" width="64" height="64" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#eacca8"/><stop offset="50%" stop-color="#d4a070"/><stop offset="100%" stop-color="#a86030"/></linearGradient></defs><path d="M4 22 L4 4 L22 4" fill="none" stroke="url(#g)" stroke-width="2.2"/><path d="M78 4 L96 4 L96 22" fill="none" stroke="url(#g)" stroke-width="2.2"/><path d="M4 78 L4 96 L22 96" fill="none" stroke="url(#g)" stroke-width="2.2"/><path d="M78 96 L96 96 L96 78" fill="none" stroke="url(#g)" stroke-width="2.2"/><line x1="27" y1="21" x2="27" y2="79" stroke="url(#g)" stroke-width="10"/><line x1="73" y1="21" x2="73" y2="79" stroke="url(#g)" stroke-width="10"/><line x1="27" y1="21" x2="73" y2="79" stroke="url(#g)" stroke-width="10"/><rect x="42" y="42" width="12" height="12" fill="#0d0a09"/></svg>'''

CSS = '''
@font-face{font-family:'Cormorant';src:url(cormorant-garamond-latin-500-italic.woff2);font-style:italic;font-weight:500}
@font-face{font-family:'Josefin';src:url(josefin-sans-latin-300-normal.woff2);font-weight:300}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#0d0a09;color:#f5f0ea;font-family:'DM Sans';position:relative;overflow:hidden}
.glow{position:absolute;width:900px;height:900px;border-radius:50%;background:radial-gradient(circle,rgba(207,100,41,.22),rgba(207,100,41,0) 65%);right:-320px;top:-300px}
.glow2{position:absolute;width:700px;height:700px;border-radius:50%;background:radial-gradient(circle,rgba(212,160,112,.10),rgba(0,0,0,0) 65%);left:-300px;bottom:-260px}
.wrap{position:absolute;inset:96px;display:flex;flex-direction:column}
.top{display:flex;align-items:center;gap:32px}
.word{font-family:'Josefin';font-weight:300;letter-spacing:9px;font-size:30px;color:#fff}
.word span{color:#d4a070}
.tag{margin-top:72px;font-family:'Josefin';font-weight:300;letter-spacing:7px;font-size:24px;text-transform:uppercase;color:#f0a46e}
h1{margin-top:28px;font-weight:500;font-size:100px;line-height:1.02;letter-spacing:-3.5px}
h1 em{font-family:'Cormorant';font-style:italic;font-weight:500;color:#d4a070;font-size:1.1em;letter-spacing:-1px}
.body{margin-top:44px;font-weight:300;font-size:36px;line-height:1.45;color:#9a8a82;max-width:840px}
ol{margin-top:48px;list-style:none;display:flex;flex-direction:column;gap:22px}
li{display:flex;gap:28px;align-items:baseline;background:#141010;border:1px solid #2a2018;border-radius:28px;padding:26px 36px;font-size:34px;font-weight:300;line-height:1.3}
li b{font-family:'Cormorant';font-style:italic;font-weight:500;color:#d4a070;font-size:46px;min-width:44px}
li strong{font-weight:500;color:#f5f0ea}
.price{margin-top:56px;display:flex;gap:22px}
.pcard{flex:1;background:#141010;border:1px solid #2a2018;border-radius:28px;padding:36px}
.pcard .n{font-family:'Josefin';letter-spacing:5px;font-size:22px;color:#f0a46e;text-transform:uppercase}
.pcard .p{margin-top:16px;font-family:'Cormorant';font-style:italic;font-weight:500;font-size:84px;color:#d4a070}
.pcard .d{margin-top:8px;font-size:26px;font-weight:300;color:#9a8a82;line-height:1.35}
.foot{margin-top:auto;padding-top:48px;display:flex;align-items:center;justify-content:space-between}
.btn{display:flex;align-items:center;gap:22px;background:linear-gradient(#ee8a4c,#cf6429);border-radius:999px;padding:14px 14px 14px 40px;font-size:30px;font-weight:500;color:#0d0a09;box-shadow:0 18px 50px rgba(207,100,41,.35)}
.chip{width:58px;height:58px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;font-size:30px;color:#0d0a09}
.url{font-family:'Josefin';letter-spacing:5px;font-size:24px;color:#9a8a82}
'''

def page(p):
    inner = p['html']
    return f'''<html><head><style>{CSS}</style></head><body><div class="glow"></div><div class="glow2"></div><div class="wrap">
<div class="top">{MARK}<div class="word">NEXT<span>BYT</span></div></div>
<div class="tag">{p['tag']}</div><h1>{p['h1']}</h1>{inner}
<div class="foot"><div class="btn">{p['cta']}<div class="chip">&rarr;</div></div><div class="url">NEXTBYT.UK</div></div>
</div></body></html>'''

async def main(spec):
    posts = json.load(open(spec))
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg = await b.new_page(viewport={'width':1080,'height':1350})
        for p in posts:
            html = f"TOOLKIT_DIR/{p['slug']}.html"
            open(html,'w').write(page(p))
            await pg.goto('file://'+html); await pg.wait_for_timeout(400)
            await pg.screenshot(path=f"TOOLKIT_DIR/{p['slug']}.png")
            print('ok', p['slug'])
        await b.close()
asyncio.run(main(sys.argv[1]))
