import json, time, base64
from pathlib import Path
import requests, websocket

PORT=9226
BASE='http://127.0.0.1:8765/'
ROOT=Path(__file__).resolve().parents[1]
SHOTS=ROOT/'tests'/'screenshots'
SHOTS.mkdir(parents=True,exist_ok=True)

class CDP:
    def __init__(self,width=1440,height=1000):
        self.target=requests.put(f'http://127.0.0.1:{PORT}/json/new?about:blank',timeout=5).json()
        self.ws=websocket.create_connection(self.target['webSocketDebuggerUrl'],timeout=15,origin=f'http://127.0.0.1:{PORT}')
        self.seq=0; self.events=[]; self.exceptions=[]
        self.send('Page.enable'); self.send('Runtime.enable')
        self.send('Emulation.setDeviceMetricsOverride',{'width':width,'height':height,'deviceScaleFactor':1,'mobile':width<=600,'screenWidth':width,'screenHeight':height})
        self.send('Emulation.setTouchEmulationEnabled',{'enabled':width<=600,'maxTouchPoints':5})
    def send(self,method,params=None,timeout=20):
        self.seq+=1; ident=self.seq
        self.ws.send(json.dumps({'id':ident,'method':method,'params':params or {}}))
        end=time.time()+timeout
        while time.time()<end:
            msg=json.loads(self.ws.recv())
            if msg.get('method')=='Runtime.exceptionThrown':
                self.exceptions.append(msg)
            elif 'method' in msg:
                self.events.append(msg)
            if msg.get('id')==ident:
                if 'error' in msg: raise RuntimeError(f'{method}: {msg["error"]}')
                return msg.get('result',{})
        raise TimeoutError(method)
    def eval(self,expression,await_promise=False):
        result=self.send('Runtime.evaluate',{'expression':expression,'returnByValue':True,'awaitPromise':await_promise})
        return result.get('result',{}).get('value')
    def goto(self,path):
        self.send('Page.navigate',{'url':BASE+path})
        for _ in range(100):
            try:
                if self.eval('document.readyState')=='complete': break
            except Exception: pass
            time.sleep(.08)
        time.sleep(.35)
    def wait(self,expr,timeout=8):
        end=time.time()+timeout
        while time.time()<end:
            try:
                value=self.eval(expr)
                if value: return value
            except Exception: pass
            time.sleep(.1)
        raise AssertionError(f'timeout waiting for {expr}')
    def screenshot(self,name):
        self.eval("document.querySelectorAll('[data-reveal]').forEach(e=>e.classList.add('is-revealed')); document.querySelectorAll('video').forEach(v=>v.pause())")
        data=self.send('Page.captureScreenshot',{'format':'png','captureBeyondViewport':False,'fromSurface':True})['data']
        (SHOTS/name).write_bytes(base64.b64decode(data))
    def close(self):
        try:self.ws.close()
        except:pass
        try:requests.get(f'http://127.0.0.1:{PORT}/json/close/'+self.target['id'],timeout=3)
        except:pass

results=[]
def ok(name,detail=''):
    results.append({'test':name,'status':'PASS','detail':detail})

def test_search_overlay():
    c=CDP();
    try:
        c.goto('index.html')
        c.eval("document.querySelector('.search-trigger').click()")
        state=c.wait("document.querySelector('[data-search-modal]').classList.contains('is-open') && document.activeElement.matches('.search-modal input')")
        assert state
        c.screenshot('search-overlay-desktop.png')
        c.eval("document.querySelector('[data-search-close]').click()")
        assert not c.eval("document.querySelector('[data-search-modal]').classList.contains('is-open')")
        assert not c.exceptions
        ok('桌面搜索弹层','打开、聚焦、关闭正常')
    finally:c.close()

def test_mobile_menu():
    c=CDP(390,844)
    try:
        c.goto('index.html')
        c.eval("document.querySelector('.menu-toggle').click()")
        assert c.wait("document.body.classList.contains('menu-open')")
        assert c.eval("document.querySelector('.mobile-menu-panel').getAttribute('aria-hidden')")=='false'
        c.screenshot('mobile-menu-open.png')
        c.eval("document.querySelector('.menu-toggle').click()")
        assert not c.eval("document.body.classList.contains('menu-open')")
        ok('手机菜单','展开与关闭正常')
    finally:c.close()

def test_navigator_flow():
    c=CDP(1280,900)
    try:
        c.goto('navigator.html')
        c.eval("document.querySelector('#challenge-knowledge').click()")
        c.eval("document.querySelector('[data-next]').click()")
        c.wait("document.querySelector('.step-panel[data-step=\"2\"]').classList.contains('is-active')")
        c.eval("document.querySelector('#goal-speed').click(); document.querySelector('#goal-quality').click(); document.querySelector('#readiness-process').click()")
        c.eval("document.querySelector('[data-next]').click()")
        c.wait("document.querySelector('.step-panel[data-step=\"3\"]').classList.contains('is-active')")
        c.eval("document.querySelector('#deployment-hybrid').click(); document.querySelector('#timeline-30').click(); document.querySelector('#constraint-sensitive').click()")
        c.eval("document.querySelector('[data-next]').click()")
        c.wait("location.pathname.endsWith('/navigator-results.html')",10)
        c.wait("document.querySelector('[data-result-challenge]')?.textContent.includes('企业知识')")
        context=c.eval("({title:document.title,challenge:document.querySelector('[data-result-challenge]').textContent,goal:document.querySelector('[data-result-goal]').textContent,deployment:document.querySelector('[data-result-deployment]').textContent,video:!!document.querySelector('video[controls]')})")
        assert context['video'] and '提高质量' in context['goal'] and '混合部署' in context['deployment']
        assert not c.exceptions
        ok('Navigator 端到端','问卷成功跳转并个性化结果；视频控件存在')
    finally:c.close()

def test_faq_and_filters():
    c=CDP(390,844)
    try:
        c.goto('service-agent-build.html')
        c.eval("document.querySelector('.faq-question').click()")
        assert c.eval("document.querySelector('.faq-item').classList.contains('is-open')")
        c.goto('category-hrms.html')
        c.eval("document.querySelector('[data-filter-open]').click()")
        assert c.wait("document.querySelector('[data-filter-panel]').classList.contains('is-open')")
        c.eval("const x=[...document.querySelectorAll('[data-category-filter]')].find(i=>i.value==='build');x.click()")
        count=int(c.eval("document.querySelector('[data-category-count]').textContent"))
        assert 0<count<6
        c.eval("document.querySelector('[data-filter-close]').click()")
        assert not c.eval("document.querySelector('[data-filter-panel]').classList.contains('is-open')")
        ok('FAQ 与手机筛选',f'FAQ 展开正常；build 筛选剩余 {count} 项')
    finally:c.close()

def test_case_and_search():
    c=CDP()
    try:
        c.goto('cases.html')
        c.eval("document.querySelector('[data-case-filter=\"education\"]').click()")
        visible=int(c.eval("[...document.querySelectorAll('[data-case-tags]')].filter(x=>!x.hidden).length"))
        assert visible==2
        c.goto('search.html?search=agent')
        counts=c.eval("({all:document.querySelector('[data-count-all]').textContent,service:document.querySelector('[data-count-service]').textContent,resource:document.querySelector('[data-count-resource]').textContent})")
        assert int(counts['all'])>=2 and int(counts['service'])>=1
        c.eval("document.querySelector('[data-search-tab=\"case\"]').click()")
        shown=c.eval("[...document.querySelectorAll('[data-result-type]')].filter(x=>!x.hidden).map(x=>x.dataset.resultType)")
        assert shown==['case']
        ok('案例与搜索筛选',f'教育案例 {visible}；agent 搜索 {counts["all"]} 条')
    finally:c.close()

for fn in [test_search_overlay,test_mobile_menu,test_navigator_flow,test_faq_and_filters,test_case_and_search]:
    fn()

out=ROOT/'tests'/'interaction-check-report.json'
out.write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False,indent=2))
