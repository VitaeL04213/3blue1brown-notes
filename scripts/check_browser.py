"""Exercise the actual reading UI, 198 linked states, geometry and responsive spreads."""
from pathlib import Path
import json, threading, functools, math
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
from walkthroughs import STEPS, EXPERIMENTS

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
errors=[];results=[];linked=0;movies=[]
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={"width":1440,"height":1000},device_scale_factor=1)
    page.route("https://www.youtube-nocookie.com/**",lambda route:route.fulfill(status=200,content_type="text/html",body="<p>URL test only.</p>"))
    page.on("pageerror",lambda e:errors.append(str(e)))
    def visit(path):
        page.goto(base+path)
        if "lessons/" in path or "lab.html" in path:page.wait_for_function("!!window.BookExperiment")
    def state():return page.evaluate("BookExperiment.snapshot()")
    def set_control(key,value):
        page.locator("#control-"+key).evaluate("(el,v)=>{el.value=v;el.dispatchEvent(new Event('input',{bubbles:true}));}",value)
    def preset(name):page.evaluate("(name)=>BookExperiment.applyPreset(name)",name)
    def read():return page.locator("#readout").inner_text()
    visit("/index.html")
    assert page.locator(".chapter-list li").count()==6
    search=page.locator("#book-search")
    search.fill("行列式")
    page.wait_for_function("document.querySelector('#search-results').textContent.includes('行列式')")
    assert page.locator("#search-results a[href$='determinant.html']").count()==1
    search.fill("Backpropagation calculus")
    page.wait_for_function("document.querySelectorAll('#search-results a').length===1 && document.querySelector('#search-results a')?.href.includes('backpropagation-calculus')")
    page.locator("#search-results a").click()
    assert page.url.endswith("backpropagation-calculus.html")
    visit("/lessons/linear-transformations.html")
    assert "1.3" in page.locator("h1").inner_text()
    assert page.locator(".book-sidebar a[aria-current=page]").get_attribute("href").endswith("linear-transformations.html")
    page.locator(".expand-knowl").click()
    assert page.locator("details[data-print-open]:not([open])").count()==0
    page.locator(".expand-knowl").click()
    assert page.locator("details[data-print-open][open]").count()==0
    page.evaluate("window.dispatchEvent(new Event('beforeprint'))")
    assert page.locator("details[data-print-open]:not([open])").count()==0
    page.evaluate("window.dispatchEvent(new Event('afterprint'))")
    assert page.locator("details[data-print-open][open]").count()==0
    visit("/index.html")
    assert page.locator("#resume-reading").get_attribute("href")=="lessons/linear-transformations.html"
    visit("/chapters/linear-algebra.html")
    assert page.locator(".section-list li").count()==16
    page.locator(".page-turn.bottom [rel=next]").click()
    assert "1.1" in page.locator("h1").inner_text()
    page.locator(".page-turn.top [rel=next]").click()
    assert "1.2" in page.locator("h1").inner_text()

    # Every lesson's controls must select a deterministic, complete state, even after edits.
    for slug,data in STEPS.items():
        visit("/lessons/"+slug+".html")
        assert state()["demo"]==data["demo"]
        for i,name in enumerate(data["presets"]):
            c=EXPERIMENTS[data["demo"]]["controls"][0]
            set_control(c[0],c[3])
            page.locator(".step-play").nth(i).click()
            expected={c[0]:c[5] for c in EXPERIMENTS[data["demo"]]["controls"]}
            expected.update(EXPERIMENTS[data["demo"]]["presets"][name])
            actual=state()["values"]
            assert all(math.isclose(actual[k],v,abs_tol=1e-9) for k,v in expected.items()),(slug,i,actual,expected)
            assert page.locator(".step-play[aria-pressed=true]").count()==1
            assert page.locator(".return-step").get_attribute("href")==f"#step-{i+1}"
            linked+=1

    for name,d in EXPERIMENTS.items():
        visit("/lab.html#"+name)
        before=state()["values"]
        c=d["controls"][0];set_control(c[0],c[3])
        assert state()["values"]!=before,name
        page.locator("#reset").click()
        assert state()["values"]==before,name
        page.locator("#play").click();page.wait_for_timeout(100)
        assert state()["playing"]
        page.locator("#play").click()
        assert not state()["playing"]
        # Camera updates must not alter mathematical data.
        page.locator("#zoom-in").click()
        assert state()["camera"]["zoom"]>1
        values=state()["values"]
        page.locator("#reset-view").click()
        assert state()["values"]==values and state()["camera"]["zoom"]==1
        if d.get("scene"):
            page.locator("#movie-area summary").click()
            page.locator("#movie").evaluate("(v)=>{v.preload='metadata';v.load();}")
            page.wait_for_function("document.querySelector('#movie').readyState>=1")
            assert page.locator("#movie").evaluate("v=>v.duration")>5
            movies.append(d["scene"])
        results.append(name)

    # Independently known numerical examples, domain limits and actual endpoint manipulation.
    visit("/lab.html#linear");preset("solve")
    assert "A x = (4, 7)" in read() and "det A = 5" in read()
    preset("collapse");assert "det A = 0" in read()
    preset("reflect");assert "det A = -1" in read()
    preset("shear")
    handle=state()["handles"][0];box=page.locator("#plot").bounding_box()
    old=state()["values"]
    page.mouse.move(box["x"]+handle["x"],box["y"]+handle["y"]);page.mouse.down()
    page.mouse.move(box["x"]+handle["x"]+20,box["y"]+handle["y"]-12,steps=5);page.mouse.up()
    assert state()["values"]["x"]!=old["x"] and state()["values"]["y"]!=old["y"]
    old=state()["values"];page.locator("#plot").focus();page.keyboard.press("ArrowRight")
    assert state()["values"]["x"]!=old["x"]
    visit("/lab.html#compose");preset("ab");a=read();preset("ba");assert read()!=a
    visit("/lab.html#spatial");preset("cross")
    assert "u × v = (0, 0, 1)" in read() and "底面面积 = 1" in read()
    values=state()["values"];camera=state()["camera"];box=page.locator("#plot").bounding_box()
    page.mouse.move(box["x"]+25,box["y"]+70);page.mouse.down()
    page.mouse.move(box["x"]+75,box["y"]+90,steps=5);page.mouse.up()
    assert state()["camera"]["yaw"]!=camera["yaw"] and state()["values"]==values
    visit("/lab.html#projection");set_control("ux",0);set_control("uy",0);assert "未定义" in read()
    visit("/lab.html#eigen");preset("large");assert "λ₁ = 3" in read() and "det[v,Av] = 0" in read()
    visit("/lab.html#derivative");preset("zero");assert "差商 = 未定义" in read() and "导数 = 0" in read()
    preset("log");set_control("a",-1);assert "导数 = 未定义" in read()
    visit("/lab.html#gradient");preset("small");assert "wₖ = 0.2592" in read()
    visit("/lab.html#network");preset("active");assert "∂L/∂w₁ = -2" in read()
    preset("off");assert "∂L/∂w₁ = 0" in read()
    set_control("x1",1.5);assert "折点" in read()
    visit("/lab.html#attention");preset("equal");assert "加权输出 = 6" in read()
    visit("/lab.html#noise");preset("known");assert "重建误差 = 0" in read()
    preset("noisy");assert "重建误差 = -1.5" in read()
    visit("/lab.html#phase");preset("rotate");assert "散度 = 0" in read() and "旋度 = 2" in read()
    visit("/lab.html#entropy");preset("match");assert "KL(p∥q) = 0 bit" in read()
    set_control("q",.8);assert "0.321928" in read()
    visit("/lab.html#iteration");preset("escape");set_control("base",1.6);set_control("k",12);assert "超过可显示范围" in read()

    widths=[1920,1440,1280]
    for width in widths:
        page.set_viewport_size({"width":width,"height":1000})
        visit("/lessons/linear-transformations.html")
        page.locator(".step-play").nth(1).click()
        left=page.locator(".reading-column").bounding_box();right=page.locator(".experiment-pane").bounding_box()
        assert right["x"]>=left["x"]+left["width"],(width,left,right)
        assert right["width"]>=350 and left["width"]>=340,(width,left,right)
        assert page.evaluate("document.documentElement.scrollWidth<=innerWidth+1"),width
        page.evaluate("window.scrollTo({top:420,behavior:'instant'})");page.wait_for_timeout(80)
        r=page.locator(".experiment-pane").bounding_box()
        assert r["y"]>=124 and r["y"]<180,(width,r)
        page.screenshot(path=str(OUT/f"spread-{width}.png"))
    for slug in ["cross-products","attention","derivatives","diffusion-models","eigenvalues"]:
        visit("/lessons/"+slug+".html")
        page.locator(".step-play").nth(1).click()
        page.evaluate("window.scrollTo({top:420,behavior:'instant'})");page.wait_for_timeout(60)
        page.screenshot(path=str(OUT/f"spread-{slug}.png"))
    visit("/lessons/linear-transformations.html#proof")
    assert page.locator("#proof").evaluate("el=>el.open")
    assert "theorem linear_combination" in page.locator("#proof pre").inner_text()
    page.locator("#original summary").click();page.locator(".load-video").click()
    assert "kYB8IZa5AuE" in page.locator(".embed-slot iframe").get_attribute("src")
    for width in [390,320]:
        page.set_viewport_size({"width":width,"height":844})
        for path in ["/index.html","/chapters/linear-algebra.html","/lab.html#spatial","/lessons/linear-transformations.html","/lessons/cross-entropy.html"]:
            visit(path)
            assert page.evaluate("document.documentElement.scrollWidth<=innerWidth+1"),(width,path)
        page.locator(".step-play").nth(1).click()
        page.wait_for_timeout(600)
        assert page.locator("#step-status").inner_text().startswith("02")
        page.locator(".return-step").click();page.wait_for_timeout(600)
        assert page.url.endswith("#step-2")
        page.screenshot(path=str(OUT/f"mobile-step-{width}.png"))
    for slug in STEPS:
        visit('/lessons/'+slug+'.html')
        assert page.evaluate("document.documentElement.scrollWidth<=innerWidth+1"),('narrow lesson',slug)
    page.locator("#toggle-contents").click()
    assert page.locator("#book-sidebar").is_visible()
    assert page.locator("#book-search").evaluate("el=>el===document.activeElement")
    page.locator("#book-search").fill("注意力")
    page.wait_for_function("document.querySelector('#search-results').textContent.includes('注意力')")
    page.keyboard.press("Escape")
    assert not page.locator("#book-sidebar").is_visible()
    assert page.locator("#toggle-contents").get_attribute("aria-expanded")=="false"
    browser.close()
server.shutdown()
assert not errors,errors
report={"experiments_checked":results,"linked_lesson_states_checked":linked,"manim_metadata_checked":movies,
        "desktop_widths_checked":widths,"mobile_widths_checked":[390,320],"javascript_errors":errors,
        "endpoint_drag_mouse_and_keyboard":True,"spatial_orbit_preserves_values":True,
        "known_numeric_examples_and_domain_limits":True,"step_reset_after_manual_edits":True,
        "full_text_english_search_and_resume":True,"chapter_navigation":True,
        "print_expansion_and_restore":True,"mobile_step_return_and_menu_keyboard":True,
        "official_embed_url_checked":True,"external_youtube_playback_verified":False}
(ROOT/"validation/browser.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"experiments_passed":len(results),"linked_steps":linked,"javascript_errors":len(errors),"overflow":False}))
