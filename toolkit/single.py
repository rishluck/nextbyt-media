# Alternative single-image layouts (1080x1350) so weeks don't repeat build.py's list card.
# Usage: python3 single.py file.json   (replace TOOLKIT_DIR first, as with build.py)
# Layouts: "date" (big framed date + headline), "dm" (headline + DM chat mockup lead driver)
import json, sys, asyncio, re
from playwright.async_api import async_playwright
D='TOOLKIT_DIR'
MARK=re.search(r"MARK = '''(.*?)'''",open(D+'/build.py').read(),re.S).group(1)
CSS='''@font-face{font-family:'Cormorant';src:url(cormorant-garamond-latin-500-italic.woff2);font-style:italic;font-weight:500}
@font-face{font-family:'Josefin';src:url(josefin-sans-latin-300-normal.woff2);font-weight:300}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#0d0a09;color:#f5f0ea;font-family:'DM Sans';position:relative;overflow:hidden}
.glow{position:absolute;width:1100px;height:1100px;border-radius:50%;background:radial-gradient(circle,rgba(207,100,41,.22),rgba(0,0,0,0) 62%)}
.wrap{position:absolute;inset:96px;display:flex;flex-direction:column}
.top{display:flex;align-items:center;justify-content:space-between}
.brand{display:flex;align-items:center;gap:24px}.brand svg{width:56px;height:56px}
.word{font-family:'Josefin';font-weight:300;letter-spacing:8px;font-size:28px;color:#fff}.word span{color:#d4a070}
.tag{font-family:'Josefin';font-weight:300;letter-spacing:7px;font-size:24px;text-transform:uppercase;color:#f0a46e}
h1{font-weight:500;font-size:96px;line-height:1.02;letter-spacing:-3.5px}
h1 em{font-family:'Cormorant';font-style:italic;font-weight:500;color:#d4a070;font-size:1.1em;letter-spacing:-1px}
.body{font-weight:300;font-size:34px;line-height:1.45;color:#9a8a82}
.foot{margin-top:auto;display:flex;align-items:center;justify-content:space-between}
.btn{display:flex;align-items:center;gap:22px;background:linear-gradient(#ee8a4c,#cf6429);border-radius:999px;padding:14px 14px 14px 40px;font-size:30px;font-weight:500;color:#0d0a09;box-shadow:0 18px 50px rgba(207,100,41,.35)}
.chip{width:58px;height:58px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;font-size:30px}
.url{font-family:'Josefin';letter-spacing:5px;font-size:24px;color:#9a8a82}
/* date layout */
.dwrap{margin-top:100px;display:flex;gap:56px;align-items:center}
.frame{position:relative;width:340px;height:340px;flex:none;display:flex;flex-direction:column;align-items:center;justify-content:center}
.frame i{position:absolute;width:54px;height:54px;border-color:#cf6429;border-style:solid;border-width:0}
.frame .a{left:0;top:0;border-left-width:3px;border-top-width:3px}.frame .b{right:0;top:0;border-right-width:3px;border-top-width:3px}
.frame .c{left:0;bottom:0;border-left-width:3px;border-bottom-width:3px}.frame .d{right:0;bottom:0;border-right-width:3px;border-bottom-width:3px}
.dn{font-family:'Cormorant';font-style:italic;font-weight:500;font-size:190px;line-height:.85;color:#d4a070}
.dm{font-family:'Josefin';letter-spacing:8px;font-size:24px;color:#f0a46e;text-transform:uppercase;margin-top:34px}
.dside .tag{margin-bottom:18px}.dside .big{font-size:44px;font-weight:300;line-height:1.25;color:#f5f0ea}
.dh{margin-top:96px}
.dbody{margin-top:40px;max-width:860px}
/* dm layout */
.phone{margin-top:64px;background:#141010;border:1px solid #2a2018;border-radius:28px;padding:40px 44px;display:flex;flex-direction:column;gap:26px}
.ph{display:flex;align-items:center;gap:20px;padding-bottom:26px;border-bottom:1px solid #2a2018}
.av{width:64px;height:64px;border-radius:50%;background:#0d0a09;border:1px solid #2a2018;display:flex;align-items:center;justify-content:center}.av svg{width:38px;height:38px}
.pn{font-size:28px;font-weight:500}.ps{font-size:22px;font-weight:300;color:#9a8a82;margin-top:2px}
.me{align-self:flex-end;background:linear-gradient(#ee8a4c,#cf6429);color:#0d0a09;border-radius:30px 30px 8px 30px;padding:20px 36px;font-size:40px;font-weight:500;letter-spacing:4px}
.them{align-self:flex-start;max-width:720px;background:#1c1614;border:1px solid #2a2018;border-radius:30px 30px 30px 8px;padding:24px 32px;font-size:29px;font-weight:300;line-height:1.4;color:#f5f0ea}
.them b{font-weight:500;color:#d4a070}
'''
def top(right=''):
    return f'<div class="top"><div class="brand">{MARK}<div class="word">NEXT<span>BYT</span></div></div>{right}</div>'
def foot(cta):
    return f'<div class="foot"><div class="btn">{cta}<div class="chip">&rarr;</div></div><div class="url">NEXTBYT.UK</div></div>'
def page(p):
    if p['layout']=='date':
        glow='<div class="glow" style="left:-420px;top:-380px"></div>'
        mid=f'''<div class="dwrap"><div class="frame"><i class="a"></i><i class="b"></i><i class="c"></i><i class="d"></i><div class="dn">{p["day"]}</div><div class="dm">{p["month"]}</div></div>
<div class="dside"><div class="tag">{p["tag"]}</div><div class="big">{p["side"]}</div></div></div>
<h1 class="dh">{p["h1"]}</h1><div class="body dbody">{p["body"]}</div>'''
    else:
        glow='<div class="glow" style="right:-420px;bottom:-420px"></div>'
        msgs=''.join(f'<div class="{w}">{t}</div>' for w,t in p['chat'])
        mid=f'''<div class="tag" style="margin-top:72px">{p["tag"]}</div><h1 style="margin-top:24px">{p["h1"]}</h1>
<div class="phone"><div class="ph"><div class="av">{MARK}</div><div><div class="pn">nextbyt_web</div><div class="ps">Direct message</div></div></div>{msgs}</div>'''
    return f'<html><head><style>{CSS}</style></head><body>{glow}<div class="wrap">{top()}{mid}{foot(p["cta"])}</div></body></html>'
async def main(spec):
    posts=json.load(open(spec))
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1080,'height':1350})
        for p in posts:
            h=f"{D}/{p['slug']}.html"; open(h,'w').write(page(p))
            await pg.goto('file://'+h); await pg.wait_for_timeout(400); await pg.screenshot(path=f"{D}/{p['slug']}.png"); print('ok',p['slug'])
        await b.close()
asyncio.run(main(sys.argv[1]))
