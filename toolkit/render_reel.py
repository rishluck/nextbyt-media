import asyncio, subprocess
from playwright.async_api import async_playwright
FPS=30; DUR=12.0
async def main():
    ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate',str(FPS),'-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart','reel.mp4'],stdin=subprocess.PIPE)
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page(viewport={'width':1080,'height':1920})
        await pg.goto('file://TOOLKIT_DIR/reel.html'); await pg.wait_for_timeout(500)
        for f in range(int(FPS*DUR)):
            t=f/FPS
            await pg.evaluate(f'renderFrame({t})')
            png=await pg.screenshot(type='jpeg',quality=95)
            ff.stdin.write(png)
            if f in (15,45,110,200,240,300): open(f'/tmp/f{f}.jpg','wb').write(png)
        await b.close()
    ff.stdin.close(); ff.wait()
asyncio.run(main())
