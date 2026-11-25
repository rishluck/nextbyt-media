import asyncio, subprocess, sys
# Usage: python3 render_reel.py [reel.html] [out.mp4] [seconds]
from playwright.async_api import async_playwright
FPS=30
SRC=sys.argv[1] if len(sys.argv)>1 else 'reel.html'
OUT=sys.argv[2] if len(sys.argv)>2 else 'reel.mp4'
DUR=float(sys.argv[3]) if len(sys.argv)>3 else 12.0
async def main():
    ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',OUT],stdin=subprocess.PIPE)
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1080,'height':1920})
        await pg.goto('file://TOOLKIT_DIR/'+SRC); await pg.wait_for_timeout(500)
        for f in range(int(FPS*DUR)):
            t=f/FPS
            await pg.evaluate(f'renderFrame({t})')
            png=await pg.screenshot(type='jpeg',quality=95)
            ff.stdin.write(png)
            if f%30==0: open(f'/tmp/f{f:04d}.jpg','wb').write(png)
        await b.close()
    ff.stdin.close(); ff.wait()
asyncio.run(main())
