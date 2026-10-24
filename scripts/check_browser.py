"""Local browser integration and responsive-layout checks on the authored site."""
from pathlib import Path
import json, threading, functools
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"build/browser-review";OUT.mkdir(parents=True,exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
    def copyfile(self,source,output):
        try:super().copyfile(source,output)
        except (ConnectionAbortedError,ConnectionResetError,BrokenPipeError):pass
server=ThreadingHTTPServer(("127.0.0.1",0),functools.partial(Quiet,directory=str(ROOT/"docs")))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f"http://127.0.0.1:{server.server_port}"
errors=[];results=[]
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={"width":1360,"height":1000},device_scale_factor=1)
    page.route("https://www.youtube-nocookie.com/**",
               lambda route:route.fulfill(status=200,content_type="text/html",
                                          body="<p>External player URL test only.</p>"))
    page.on("pageerror",lambda e:errors.append(str(e)))
    page.goto(base+"/index.html")
    assert page.locator(".course li").count()==67
    page.screenshot(path=str(OUT/"index.png"),full_page=True)
    for slug in ["linear","derivative","integral","gradient","attention","heat","complex","entropy","taylor"]:
        page.goto(base+"/lab.html#"+slug)
        page.wait_for_selector("#controls input")
        initial=page.locator("#readout").inner_text()
        control=page.locator("#controls input").first
        control.evaluate("(el)=>{el.value=el.max;el.dispatchEvent(new Event('input',{bubbles:true}));}")
        changed=page.locator("#readout").inner_text()
        assert initial!=changed,slug
        page.locator("#reset").click()
        assert page.locator("#readout").inner_text()==initial,slug
        page.locator("#play").click()
        page.wait_for_timeout(220)
        assert page.locator("#play").get_attribute("aria-pressed")=="true"
        page.locator("#play").click()
        assert page.locator("#play").get_attribute("aria-pressed")=="false"
        page.locator("#reset").click()
        page.wait_for_function("document.querySelector('#movie').readyState>=1")
        assert page.locator("#movie").evaluate("(v)=>v.duration")>5
        page.screenshot(path=str(OUT/(slug+".png")),full_page=True)
        results.append({"experiment":slug,"controls":True,"play_pause":True,"reset":True,"mp4_metadata":True})
    page.goto(base+"/lab.html#derivative")
    page.locator("#control-h").evaluate("(el)=>{el.value=0;el.dispatchEvent(new Event('input',{bubbles:true}));}")
    assert "未定义" in page.locator("#readout").inner_text()
    page.goto(base+"/lab.html#entropy")
    page.locator("#control-q").evaluate("(el)=>{el.value=.5;el.dispatchEvent(new Event('input',{bubbles:true}));}")
    assert "KL(p∥q) = 0 bit" in page.locator("#readout").inner_text()
    page.goto(base+"/lessons/linear-transformations.html")
    assert page.locator("math").count()>5
    page.locator(".load-video").click()
    assert "kYB8IZa5AuE" in page.locator("iframe").get_attribute("src")
    page.screenshot(path=str(OUT/"lesson-desktop.png"),full_page=True)
    page.set_viewport_size({"width":390,"height":844})
    for suffix in ["/index.html","/lab.html#attention","/lessons/cross-entropy.html"]:
        page.goto(base+suffix)
        assert page.evaluate("document.documentElement.scrollWidth<=innerWidth+1"),suffix
        name="mobile-"+suffix.split("/")[-1].replace(".html","").replace("#","-")+".png"
        page.screenshot(path=str(OUT/name),full_page=True)
    browser.close()
server.shutdown()
assert not errors,errors
report={"experiments":results,"responsive_width":390,"javascript_errors":errors,
        "official_embed_url_checked":True,"external_youtube_playback_verified":False,
        "note":"External playback depends on network/YouTube policy; original links remain available."}
(ROOT/"validation/browser.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"experiments_passed":len(results),"javascript_errors":len(errors),"mobile_overflow":False}))
