import json, os, sys, time, base64
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.python-deps'))

import requests, websocket

PORT=int(os.environ.get('CDP_PORT','9226'))
BASE=os.environ.get('BASE_URL','http://127.0.0.1:8765/').rstrip('/') + '/'
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
        placeholder_free=c.eval("!['原型说明','内容映射占位','内容占位说明','DETAIL / CMS SLOT','正式上线时可接','响应式企业网站原型'].some((phrase)=>document.body.textContent.includes(phrase))")
        assert placeholder_free
        assert c.eval("document.querySelector('[data-next]').disabled")
        c.eval("document.querySelector('#challenge-knowledge').click()")
        assert not c.eval("document.querySelector('[data-next]').disabled")
        c.eval("document.querySelector('[data-next]').click()")
        c.wait("document.querySelector('.step-panel[data-step=\"2\"]').classList.contains('is-active')")
        c.eval("document.querySelector('#goal-speed').click(); document.querySelector('#goal-quality').click(); document.querySelector('#readiness-process').click()")
        c.eval("document.querySelector('[data-next]').click()")
        c.wait("document.querySelector('.step-panel[data-step=\"3\"]').classList.contains('is-active')")
        c.eval("document.querySelector('[data-progress-step=\"2\"]').click()")
        c.wait("document.querySelector('.step-panel[data-step=\"2\"]').classList.contains('is-active')")
        c.eval("document.querySelector('[data-next]').click()")
        c.wait("document.querySelector('.step-panel[data-step=\"3\"]').classList.contains('is-active')")
        c.eval("document.querySelector('#deployment-hybrid').click(); document.querySelector('#timeline-30').click(); document.querySelector('#constraint-sensitive').click()")
        c.eval("document.querySelector('[data-next]').click()")
        c.wait("location.pathname.endsWith('/navigator-results.html')",10)
        c.wait("document.querySelector('[data-result-challenge]')?.textContent.includes('企业知识')")
        context=c.eval("({title:document.title,challenge:document.querySelector('[data-result-challenge]').textContent,goal:document.querySelector('[data-result-goal]').textContent,deployment:document.querySelector('[data-result-deployment]').textContent,video:!!document.querySelector('video[controls]')})")
        assert context['video'] and '提高质量' in context['goal'] and '混合部署' in context['deployment']
        result_placeholder_free=c.eval("!['原型说明','内容映射占位','内容占位说明','DETAIL / CMS SLOT','正式上线时可接','响应式企业网站原型'].some((phrase)=>document.body.textContent.includes(phrase))")
        assert result_placeholder_free
        assert not c.exceptions
        ok('Navigator 端到端','问卷可回退修改、成功跳转并个性化结果；视频控件存在')
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
        linked=c.eval("({pid:!!document.querySelector('#pid[href=\"case-manufacturing-pid-intelligence.html\"]'),healthcare:!!document.querySelector('#healthcare-agent-roi[href=\"case-healthcare-agent-roi.html\"]'),automotive:!!document.querySelector('#automotive-dfmea-ontology-agent[href=\"case-automotive-dfmea-ontology-agent.html\"]'),supply:!!document.querySelector('#supply-chain-agentic-decision[href=\"case-supply-chain-agentic-decision.html\"]'),financial:!!document.querySelector('#financial-bda-document-automation[href=\"case-financial-bda-document-automation.html\"]'),vanguard:!!document.querySelector('#vanguard-virtual-analyst[href=\"case-vanguard-virtual-analyst.html\"]'),agentEval:!!document.querySelector('#agent-evaluation-first[href=\"case-agent-evaluation-first.html\"]'),total:document.querySelectorAll('[data-case-tags]').length})")
        assert linked['pid'] and linked['healthcare'] and linked['automotive'] and linked['supply'] and linked['financial'] and linked['vanguard'] and linked['agentEval'] and linked['total']>=14
        c.eval("document.querySelector('[data-case-filter=\"education\"]').click()")
        visible=int(c.eval("[...document.querySelectorAll('[data-case-tags]')].filter(x=>!x.hidden).length"))
        assert visible==2
        c.eval("document.querySelector('[data-case-filter=\"service\"]').click()")
        healthcare_visible=c.eval("!document.querySelector('#healthcare-agent-roi').hidden")
        assert healthcare_visible
        c.goto('search.html?search=Agent')
        c.wait("document.querySelector('.search-page')?.dataset.searchSource === 'json-index'")
        counts=c.eval("({all:document.querySelector('[data-count-all]').textContent,service:document.querySelector('[data-count-service]').textContent,resource:document.querySelector('[data-count-resource]').textContent})")
        assert int(counts['all'])>=2 and int(counts['service'])>=1
        c.goto('search.html?search=医疗')
        c.wait("document.querySelector('.search-page')?.dataset.searchSource === 'json-index'")
        medical_case=c.eval("({caseCount:document.querySelector('[data-count-case]').textContent,healthcare:!!document.querySelector('a[href=\"case-healthcare-agent-roi.html\"]:not([hidden])')})")
        assert int(medical_case['caseCount'])>=1 and medical_case['healthcare']
        c.goto('search.html?search=DFMEA')
        c.wait("document.querySelector('.search-page')?.dataset.searchSource === 'json-index'")
        automotive_case=c.eval("({caseCount:document.querySelector('[data-count-case]').textContent,automotive:!!document.querySelector('a[href=\"case-automotive-dfmea-ontology-agent.html\"]:not([hidden])')})")
        assert int(automotive_case['caseCount'])>=1 and automotive_case['automotive']
        c.goto('search.html?search=B柱')
        c.wait("document.querySelector('.search-page')?.dataset.searchSource === 'json-index'")
        b_pillar_case=c.eval("({caseCount:document.querySelector('[data-count-case]').textContent,automotive:!!document.querySelector('a[href=\"case-automotive-dfmea-ontology-agent.html\"]:not([hidden])'),summary:document.querySelector('[data-search-summary]').textContent,marks:document.querySelectorAll('.search-mark').length})")
        assert int(b_pillar_case['caseCount'])>=1 and b_pillar_case['automotive'] and 'B柱' in b_pillar_case['summary'] and b_pillar_case['marks']>=1
        c.goto('search.html?search=AgentCore')
        c.wait("document.querySelector('.search-page')?.dataset.searchSource === 'json-index'")
        agentcore_case=c.eval("({caseCount:document.querySelector('[data-count-case]').textContent,automotive:!!document.querySelector('a[href=\"case-automotive-dfmea-ontology-agent.html\"]:not([hidden])')})")
        assert int(agentcore_case['caseCount'])>=1 and agentcore_case['automotive']
        c.goto('search.html?search=知识流失')
        c.wait("document.querySelector('.search-page')?.dataset.searchSource === 'json-index'")
        knowledge_loss_case=c.eval("({caseCount:document.querySelector('[data-count-case]').textContent,automotive:!!document.querySelector('a[href=\"case-automotive-dfmea-ontology-agent.html\"]:not([hidden])')})")
        assert int(knowledge_loss_case['caseCount'])>=1 and knowledge_loss_case['automotive']
        c.goto('search.html?search=供应链')
        c.wait("document.querySelector('.search-page')?.dataset.searchSource === 'json-index'")
        supply_chain_case=c.eval("({caseCount:document.querySelector('[data-count-case]').textContent,supply:!!document.querySelector('a[href=\"case-supply-chain-agentic-decision.html\"]:not([hidden])')})")
        assert int(supply_chain_case['caseCount'])>=1 and supply_chain_case['supply']
        c.goto('search.html?search=BDA')
        c.wait("document.querySelector('.search-page')?.dataset.searchSource === 'json-index'")
        financial_case=c.eval("({caseCount:document.querySelector('[data-count-case]').textContent,financial:!!document.querySelector('a[href=\"case-financial-bda-document-automation.html\"]:not([hidden])')})")
        assert int(financial_case['caseCount'])>=1 and financial_case['financial']
        c.goto('search.html?search=金融文档')
        c.wait("document.querySelector('.search-page')?.dataset.searchSource === 'json-index'")
        financial_doc_case=c.eval("({caseCount:document.querySelector('[data-count-case]').textContent,financial:!!document.querySelector('a[href=\"case-financial-bda-document-automation.html\"]:not([hidden])')})")
        assert int(financial_doc_case['caseCount'])>=1 and financial_doc_case['financial']
        c.goto('search.html?search=虚拟分析师')
        c.wait("document.querySelector('.search-page')?.dataset.searchSource === 'json-index'")
        vanguard_case=c.eval("({caseCount:document.querySelector('[data-count-case]').textContent,vanguard:!!document.querySelector('a[href=\"case-vanguard-virtual-analyst.html\"]:not([hidden])')})")
        assert int(vanguard_case['caseCount'])>=1 and vanguard_case['vanguard']
        c.goto('search.html?search=AI-ready')
        c.wait("document.querySelector('.search-page')?.dataset.searchSource === 'json-index'")
        ai_ready_case=c.eval("({caseCount:document.querySelector('[data-count-case]').textContent,vanguard:!!document.querySelector('a[href=\"case-vanguard-virtual-analyst.html\"]:not([hidden])')})")
        assert int(ai_ready_case['caseCount'])>=1 and ai_ready_case['vanguard']
        c.goto('search.html?search=Evaluation')
        c.wait("document.querySelector('.search-page')?.dataset.searchSource === 'json-index'")
        evaluation_case=c.eval("({caseCount:document.querySelector('[data-count-case]').textContent,agentEval:!!document.querySelector('a[href=\"case-agent-evaluation-first.html\"]:not([hidden])')})")
        assert int(evaluation_case['caseCount'])>=1 and evaluation_case['agentEval']
        c.goto('search.html?search=ADLC')
        c.wait("document.querySelector('.search-page')?.dataset.searchSource === 'json-index'")
        adlc_case=c.eval("({caseCount:document.querySelector('[data-count-case]').textContent,agentEval:!!document.querySelector('a[href=\"case-agent-evaluation-first.html\"]:not([hidden])')})")
        assert int(adlc_case['caseCount'])>=1 and adlc_case['agentEval']
        c.goto('search.html?search=P%26ID')
        c.wait("document.querySelector('.search-page')?.dataset.searchSource === 'json-index'")
        pid_case=c.eval("({caseCount:document.querySelector('[data-count-case]').textContent,pid:!!document.querySelector('a[href=\"case-manufacturing-pid-intelligence.html\"]:not([hidden])')})")
        assert int(pid_case['caseCount'])>=1 and pid_case['pid']
        c.eval("document.querySelector('[data-search-tab=\"case\"]').click()")
        shown=c.eval("[...document.querySelectorAll('[data-result-type]')].filter(x=>!x.hidden).map(x=>x.dataset.resultType)")
        assert shown==['case']
        c.goto('search.html')
        c.wait("document.querySelector('.search-page')?.dataset.searchSource === 'json-index'")
        c.eval("const input=document.querySelector('[data-search-page-input]'); input.value='RFLP'; input.dispatchEvent(new Event('input',{bubbles:true}))")
        c.wait("document.querySelector('[data-count-case]').textContent !== '0' && decodeURIComponent(location.search).includes('RFLP')")
        live_search=c.eval("({source:document.querySelector('.search-page').dataset.searchSource,version:document.querySelector('.search-page').dataset.searchVersion,caseCount:document.querySelector('[data-count-case]').textContent,automotive:!!document.querySelector('a[href=\"case-automotive-dfmea-ontology-agent.html\"]:not([hidden])')})")
        assert live_search['source']=='json-index' and live_search['version'] and int(live_search['caseCount'])>=1 and live_search['automotive']
        ok('案例与搜索筛选',f'案例卡 {linked["total"]}；教育案例 {visible}；医疗搜索案例 {medical_case["caseCount"]} 条；JSON 索引 {live_search["version"]}；DFMEA/B柱/AgentCore/知识流失/供应链/BDA/金融文档/虚拟分析师/AI-ready/Evaluation/ADLC/P&ID/RFLP 均命中')
    finally:c.close()

for fn in [test_search_overlay,test_mobile_menu,test_navigator_flow,test_faq_and_filters,test_case_and_search]:
    fn()

out=ROOT/'tests'/'interaction-check-report.json'
out.write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False,indent=2))
