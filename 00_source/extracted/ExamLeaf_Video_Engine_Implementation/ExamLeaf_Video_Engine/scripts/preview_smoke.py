"""Smoke-test the LOCAL preview page; no external browser or service access."""
from pathlib import Path
import json,threading,http.server,socketserver,functools,shutil
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
handler=functools.partial(Quiet,directory=str(ROOT))
with socketserver.TCPServer(('127.0.0.1',0),handler) as server:
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path=shutil.which('chromium'),headless=True,args=['--no-sandbox'])
        # --no-sandbox is necessary in this isolated container, not recommended for a production host.
        page=browser.new_page(viewport={'width':1440,'height':1000})
        errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        try:
            page.goto(f'http://127.0.0.1:{server.server_address[1]}/preview.html')
        except Exception as exc:
            (ROOT/'outputs/browser_smoke.json').write_text(json.dumps({'status':'blocked_or_failed','error':str(exc),'passed_browser_tests':0},indent=2))
            browser.close()
            raise SystemExit(2)
        page.wait_for_function('Array.from(document.querySelectorAll("video")).length===8 && Array.from(document.querySelectorAll("video")).every(v=>v.readyState>=1)',timeout=20000)
        metadata=page.locator('video').evaluate_all('(vs)=>vs.map(v=>({duration:v.duration,width:v.videoWidth,height:v.videoHeight,captionTracks:v.querySelectorAll("track").length}))')
        assert len(metadata)==8 and all(x['duration']==30 for x in metadata)
        assert all(x['captionTracks']==1 for x in metadata)
        assert not errors,errors
        page.screenshot(path=str(ROOT/'outputs/preview_browser.png'),full_page=True)
        # Layout smoke test at phone width; not a real student readability test.
        page.set_viewport_size({'width':390,'height':844})
        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth+1')
        (ROOT/'outputs/browser_smoke.json').write_text(json.dumps({'status':'passed','videos':metadata,'script_errors':errors,'phone_horizontal_overflow':False,'boundary':'Playback metadata and page layout only; not voice, learning or physical-device usability validation.'},indent=2))
        browser.close()
    server.shutdown()
print('Browser smoke: 8 local MP4s loaded with 30-second metadata; no script errors; no horizontal page overflow at 390px.')
