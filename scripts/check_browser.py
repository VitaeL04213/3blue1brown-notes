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
    assert page.locator(".chapter-list li").count()==6
    assert page.locator(".toc-chapter").count()==6
    page.screenshot(path=str(OUT/"index.png"),full_page=True)
    search=page.locator("#book-search")
    search.fill("行列式")
    page.wait_for_function("document.querySelector('#search-results').textContent.includes('行列式')")
    assert page.locator("#search-results a[href$='determinant.html']").count()==1
    search.fill("平移")
    page.wait_for_function("[...document.querySelectorAll('#search-results mark')].some(el=>el.textContent==='平移')")
    assert page.locator("#search-results a[href$='linear-transformations.html']").count()==1
    search.fill("Backpropagation calculus")
    page.wait_for_function("document.querySelectorAll('#search-results a').length===1 && document.querySelector('#search-results a')?.getAttribute('href').includes('backpropagation-calculus')")
    page.locator("#search-results a").first.click()
    assert page.url.endswith("backpropagation-calculus.html")
    page.goto(base+"/lessons/linear-transformations.html")
    assert "1.3" in page.locator("h1").inner_text()
    assert page.locator(".book-sidebar a[aria-current=page]").get_attribute("href").endswith("linear-transformations.html")
    assert not page.locator("#example").evaluate("el=>el.open")
    page.locator("#example summary").click()
    assert page.locator("#example").evaluate("el=>el.open")
    page.locator(".expand-knowl").click()
    assert page.locator("details[data-print-open]:not([open])").count()==0
    page.locator(".expand-knowl").click()
    assert page.locator("details[data-print-open][open]").count()==0
    page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
    assert page.locator("details[data-print-open]:not([open])").count()==0
    page.evaluate("window.dispatchEvent(new Event('afterprint'))")
    assert page.locator("details[data-print-open][open]").count()==0
    page.goto(base+"/index.html")
    assert page.locator("#resume-reading").get_attribute("href")=="lessons/linear-transformations.html"
    page.goto(base+"/chapters/linear-algebra.html")
    assert page.locator(".section-list li").count()==16
    page.locator(".page-turn.bottom [rel=next]").click()
    assert "1.1" in page.locator("h1").inner_text()
    page.locator(".page-turn.top [rel=next]").click()
    assert "1.2" in page.locator("h1").inner_text()
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
    page.locator("#original summary").click()
    page.locator(".load-video").click()
    assert "kYB8IZa5AuE" in page.locator(".embed-slot iframe").get_attribute("src")
    page.locator("#original summary").click()
    page.evaluate("window.scrollTo({top:0,behavior:'instant'})")
    page.screenshot(path=str(OUT/"lesson-desktop.png"),full_page=True)
    inline_lessons=["linear-transformations","derivatives","integration","gradient-descent","attention","heat-equation","eulers-formula-dynamically","cross-entropy","taylor-series"]
    inline_results=[]
    for lesson in inline_lessons:
        page.goto(base+"/lessons/"+lesson+".html")
        page.locator(".interactive-controls summary").click()
        frame=page.frame_locator("iframe.inline-lab")
        frame.locator("#controls input").first.wait_for()
        original=frame.locator("#readout").inner_text()
        frame.locator("#controls input").first.evaluate("el=>{el.value=el.max;el.dispatchEvent(new Event('input',{bubbles:true}));}")
        assert frame.locator("#readout").inner_text()!=original,lesson
        frame.locator("#reset").click()
        assert frame.locator("#readout").inner_text()==original,lesson
        assert not frame.locator(".book-header").is_visible()
        page.wait_for_function("(()=>{const f=document.querySelector('.inline-lab');return f.clientHeight>=f.contentDocument.querySelector('main').getBoundingClientRect().height})()")
        assert frame.locator("html").evaluate("el=>el.scrollWidth<=innerWidth+1"),lesson
        inline_results.append(lesson)
    page.goto(base+"/lessons/linear-transformations.html#proof")
    assert page.locator("#proof").evaluate("el=>el.open")
    assert "theorem linear_combination" in page.locator("#proof pre").inner_text()
    page.goto(base+"/lessons/linear-transformations.html")
    page.locator(".interactive-controls summary").click()
    page.frame_locator("iframe.inline-lab").locator("#controls input").first.wait_for()
    page.locator("#interactive").screenshot(path=str(OUT/"inline-figure.png"))
    page.set_viewport_size({"width":390,"height":844})
    for suffix in ["/index.html","/chapters/linear-algebra.html","/lab.html#attention","/lessons/cross-entropy.html"]:
        page.goto(base+suffix)
        assert page.evaluate("document.documentElement.scrollWidth<=innerWidth+1"),suffix
        name="mobile-"+suffix.split("/")[-1].replace(".html","").replace("#","-")+".png"
        page.screenshot(path=str(OUT/name),full_page=True)
    assert not page.locator("#book-sidebar").is_visible()
    page.locator("#toggle-contents").click()
    assert page.locator("#book-sidebar").is_visible()
    assert page.locator("#book-search").evaluate("el=>el===document.activeElement")
    page.locator("#book-search").fill("注意力")
    page.wait_for_function("document.querySelector('#search-results').textContent.includes('注意力')")
    page.screenshot(path=str(OUT/"mobile-navigation.png"))
    page.keyboard.press("Escape")
    assert not page.locator("#book-sidebar").is_visible()
    assert page.locator("#toggle-contents").get_attribute("aria-expanded")=="false"
    page.locator(".interactive-controls summary").click()
    frame=page.frame_locator("iframe.inline-lab")
    frame.locator("#control-q").wait_for()
    assert frame.locator("html").evaluate("el=>el.scrollWidth<=innerWidth+1")
    page.wait_for_function("(()=>{const f=document.querySelector('.inline-lab');return f.clientHeight>=f.contentDocument.querySelector('main').getBoundingClientRect().height})()")
    page.locator("#interactive").screenshot(path=str(OUT/"mobile-inline.png"))
    page.set_viewport_size({"width":320,"height":720})
    page.goto(base+"/lessons/linear-transformations.html")
    assert page.evaluate("document.documentElement.scrollWidth<=innerWidth+1")
    browser.close()
server.shutdown()
assert not errors,errors
report={"experiments":results,"responsive_width":390,"javascript_errors":errors,
        "inline_experiments_checked":inline_results,"chapter_navigation":True,
        "full_text_and_english_search":True,"collapsible_examples_and_proofs":True,
        "print_expansion_and_restore":True,"mobile_navigation_keyboard":True,
        "narrow_viewport_width":320,
        "official_embed_url_checked":True,"external_youtube_playback_verified":False,
        "note":"External playback depends on network/YouTube policy; original links remain available."}
(ROOT/"validation/browser.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"experiments_passed":len(results),"javascript_errors":len(errors),"mobile_overflow":False}))
