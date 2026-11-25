import json, sys, asyncio, re
from playwright.async_api import async_playwright
D='TOOLKIT_DIR'
MARK=re.search(r"MARK = '''(.*?)'''",open(D+'/build.py').read(),re.S).group(1)
CSS='''@font-face{font-family:'Cormorant';src:url(cormorant-garamond-latin-500-italic.woff2);font-style:italic;font-weight:500}
@font-face{font-family:'Josefin';src:url(josefin-sans-latin-300-normal.woff2);font-weight:300}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#0d0a09;color:#f5f0ea;font-family:'DM Sans';position:relative;overflow:hidden}
.glow{position:absolute;width:1000px;height:1000px;border-radius:50%;background:radial-gradient(circle,rgba(207,100,41,.2),rgba(0,0,0,0) 65%);right:-380px;bottom:-380px}
.wrap{position:absolute;inset:96px;display:flex;flex-direction:column}
.top{display:flex;align-items:center;justify-content:space-between}
.brand{display:flex;align-items:center;gap:24px}.brand svg{width:52px;height:52px}
.word{font-family:'Josefin';font-weight:300;letter-spacing:8px;font-size:26px;color:#fff}.word span{color:#d4a070}
.num{font-family:'Josefin';letter-spacing:5px;font-size:24px;color:#5a4a42}
.mid{margin:auto 0;display:flex;flex-direction:column}
.tag{font-family:'Josefin';font-weight:300;letter-spacing:7px;font-size:24px;text-transform:uppercase;color:#f0a46e}
h1{margin-top:28px;font-weight:500;font-size:120px;line-height:1;letter-spacing:-4px}
h1 em,h2 em{font-family:'Cormorant';font-style:italic;font-weight:500;color:#d4a070;font-size:1.1em;letter-spacing:-1px}
.sub{margin-top:40px;font-size:36px;font-weight:300;color:#9a8a82;line-height:1.4;max-width:820px}
.myth{font-family:'Josefin';letter-spacing:7px;font-size:24px;color:#5a4a42;text-transform:uppercase}
.mq{margin-top:22px;font-size:58px;font-weight:300;line-height:1.15;color:#9a8a82;text-decoration:line-through;text-decoration-color:#cf6429;text-decoration-thickness:4px;letter-spacing:-1.5px}
.rule{margin:64px 0;width:120px;height:2px;background:linear-gradient(90deg,#cf6429,#d4a070)}
.fact{font-family:'Josefin';letter-spacing:7px;font-size:24px;color:#f0a46e;text-transform:uppercase}
h2{margin-top:22px;font-weight:500;font-size:78px;line-height:1.05;letter-spacing:-2.5px}
.fx{margin-top:32px;font-size:34px;font-weight:300;color:#9a8a82;line-height:1.45;max-width:860px}
.foot{display:flex;align-items:center;justify-content:space-between}
.swipe{font-family:'Josefin';letter-spacing:6px;font-size:22px;color:#9a8a82;text-transform:uppercase}
.btn{display:flex;align-items:center;gap:22px;background:linear-gradient(#ee8a4c,#cf6429);border-radius:999px;padding:14px 14px 14px 40px;font-size:30px;font-weight:500;color:#0d0a09;box-shadow:0 18px 50px rgba(207,100,41,.35)}
.chip{width:58px;height:58px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;font-size:30px}
.cn{font-family:'Cormorant';font-style:italic;font-weight:500;font-size:220px;line-height:1;color:#d4a070}
.cl{margin-top:36px;font-family:'Josefin';letter-spacing:7px;font-size:24px;color:#f0a46e;text-transform:uppercase}
.box{display:inline-flex;width:46px;height:46px;border:2px solid #cf6429;border-radius:12px;align-items:center;justify-content:center;margin-right:22px;vertical-align:middle;font-size:28px;color:#d4a070}
.url{font-family:'Josefin';letter-spacing:5px;font-size:24px;color:#9a8a82}'''
def slide(s,i,n):
    top=f'<div class="top"><div class="brand">{MARK}<div class="word">NEXT<span>BYT</span></div></div><div class="num">{i:02d} / {n:02d}</div></div>'
    if s['kind']=='cover':
        mid=f'<div class="mid"><div class="tag">{s["tag"]}</div><h1>{s["h1"]}</h1><div class="sub">{s["sub"]}</div></div>'
        foot='<div class="foot"><div class="swipe">Swipe &rarr;</div><div class="url">NEXTBYT.UK</div></div>'
    elif s['kind']=='myth':
        mid=f'<div class="mid"><div class="myth">Myth</div><div class="mq">{s["myth"]}</div><div class="rule"></div><div class="fact">Fact</div><h2>{s["h2"]}</h2><div class="fx">{s["fx"]}</div></div>'
        foot='<div class="foot"><div class="swipe">Swipe &rarr;</div><div class="url">NEXTBYT.UK</div></div>'
    elif s['kind']=='check':
        mid=f'<div class="mid"><div class="cn">{s["n"]}</div><div class="cl"><span class="box">&#10003;</span>{s.get("label","Check")}</div><h2>{s["h2"]}</h2><div class="fx">{s["fx"]}</div></div>'
        foot='<div class="foot"><div class="swipe">Swipe &rarr;</div><div class="url">NEXTBYT.UK</div></div>'
    else:
        mid=f'<div class="mid"><div class="tag">{s["tag"]}</div><h1 style="font-size:104px">{s["h1"]}</h1><div class="sub">{s["sub"]}</div></div>'
        foot=f'<div class="foot"><div class="btn">{s["cta"]}<div class="chip">&rarr;</div></div><div class="url">NEXTBYT.UK</div></div>'
    return f'<html><head><style>{CSS}</style></head><body><div class="glow"></div><div class="wrap">{top}{mid}{foot}</div></body></html>'
async def main(spec):
    c=json.load(open(spec)); n=len(c['slides'])
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path='/usr/bin/google-chrome'); pg=await b.new_page(viewport={'width':1080,'height':1350})
        for i,s in enumerate(c['slides'],1):
            h=f"{D}/{c['slug']}-{i}.html"; open(h,'w').write(slide(s,i,n))
            await pg.goto('file://'+h); await pg.wait_for_timeout(300); await pg.screenshot(path=f"{D}/{c['slug']}-{i}.png"); print('ok',i)
        await b.close()
asyncio.run(main(sys.argv[1]))
