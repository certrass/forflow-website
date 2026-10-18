import React, {useEffect, useRef, useState} from 'react';
import {ArrowRight, ArrowUpRight, Check, CheckCircle, FileText, FunnelSimple, GitBranch, LinkSimple, ListChecks, ShieldCheck, SlidersHorizontal, WarningCircle} from '@phosphor-icons/react';
import {ShowcaseViewport} from './ShowcaseViewport.jsx';
import {FilmControls, FilmCursor} from './ShowcaseFilmUI.jsx';
import {useShowcaseFilm} from './useShowcaseFilm.js';
import {useFilmPointer} from './useFilmPointer.js';
import {governanceModules} from './governance-content.js';
import {bookingUrl} from './contact-config.js';
import {EvaluationCanvas} from './EvaluationCanvas.jsx';
import {Q2QAssetCanvas, assetChapters} from './Q2QAssetCanvas.jsx';

const chapters = [['定位问题', 0], ['核对依据', 5400], ['整改复测', 11400]];
const icons = [FileText, SlidersHorizontal, GitBranch];
const views = [['finding','问题详情'], ['evidence','核验依据'], ['retest','整改复测']];

function moveTab(event, index, count, select) {
  const next = event.key === 'ArrowRight' ? (index + 1) % count : event.key === 'ArrowLeft' ? (index + count - 1) % count : event.key === 'Home' ? 0 : event.key === 'End' ? count - 1 : null;
  if (next === null) return;
  event.preventDefault(); select(next);
  event.currentTarget.parentElement.querySelectorAll('[role="tab"]')[next]?.focus();
}

export function GovernanceSection({standalone = false}) {
  const root = useRef(null);
  const Heading = standalone ? 'h1' : 'h2';
  const [displayMode, setDisplayMode] = useState(standalone?'overview':'assets');
  const [assetThreshold, setAssetThreshold] = useState(100);
  const [assetPolicyChanged, setAssetPolicyChanged] = useState(false);
  const lastDisplayMode = useRef(displayMode);
  const duration = displayMode==='assets'?24000:18000;
  const film = useShowcaseFilm(root, duration, true, displayMode);
  const [moduleIndex, setModuleIndex] = useState(0);
  const [noiseType, setNoiseType] = useState('data');
  const [row, setRow] = useState(0);
  const [onlyProblems, setOnlyProblems] = useState(false);
  const [manualView, setManualView] = useState(null);
  const [comparisonCorrected, setComparisonCorrected] = useState(false);
  const overviewPosition = useRef(null);
  const chapter = film.time >= 11400 ? 2 : film.time >= 5400 ? 1 : 0;
  const assetStep = Math.min(3, Math.floor(film.time / 6000));
  const module = governanceModules[moduleIndex];
  const samples = moduleIndex === 2 && noiseType === 'stability' ? module.stabilitySamples : module.samples;
  const sample = samples[row];
  const view = manualView || views[chapter][0];
  const pointer = useFilmPointer(root, view === 'retest' ? '.gov-secondary-action' : '.gov-primary-action', `${moduleIndex}-${noiseType}-${row}-${view}`, '.gov-workspace');
  const visibleSamples = onlyProblems ? samples.filter(s => s.problem) : samples;
  useEffect(() => {if (film.playing) setManualView(null);}, [film.playing]);
  useEffect(() => {
    if (lastDisplayMode.current === displayMode) return;
    lastDisplayMode.current = displayMode;
    root.current?.querySelector('.gov-display-switch [aria-pressed="true"]')?.focus({preventScroll:true});
  }, [displayMode]);
  useEffect(() => {
    if (displayMode === 'overview' && view !== 'evidence') setComparisonCorrected(view === 'retest');
  }, [displayMode, view, moduleIndex]);
  const selectModule = index => {overviewPosition.current=null;setComparisonCorrected(false);film.seek(0,false);setModuleIndex(index);setRow(0);setOnlyProblems(false);setManualView('finding');};
  const inspect = value => {film.seek(chapters[views.findIndex(([id])=>id===value)][1],false);setManualView(value);};
  const selectSample = index => {film.seek(0,false);setRow(index);setManualView('finding');};
  const selectNoise = value => {film.seek(0,false);setNoiseType(value);setRow(0);setOnlyProblems(false);setManualView('finding');};
  const problemCount = samples.filter(s => s.problem).length;
  const openWorkspace = (nextView = 'evidence') => {
    overviewPosition.current = {view, time:film.time, corrected:comparisonCorrected, displayMode};
    const targetView = displayMode==='assets'?'evidence':nextView;
    film.seek(chapters[views.findIndex(([id])=>id===targetView)][1],false);
    if(displayMode==='assets')setModuleIndex(0);
    setNoiseType(displayMode!=='assets'&&moduleIndex===2?'stability':'data');setRow(0);setOnlyProblems(false);
    setManualView(targetView);setDisplayMode('workspace');
  };
  const returnOverview = () => {
    const previous = overviewPosition.current;
    const restore = previous?.displayMode==='overview';
    film.seek(restore?previous.time:0,false);
    setManualView(restore?previous.view:'finding');
    setComparisonCorrected(restore?previous.corrected:false);
    setDisplayMode('overview');
  };
  const returnAssets = () => {
    const previous = overviewPosition.current;
    film.seek(previous?.displayMode==='assets'?previous.time:0,false);
    setManualView(null);setDisplayMode('assets');
  };
  const controlsFilm = {...film, seek:(at, autoplay)=>{setManualView(null);film.seek(at,autoplay);}, replay:()=>{setManualView(null);film.replay();}};
  const focusTarget = '.gov-inspector';
  return <section className={`governance-section v6-container${standalone?' governance-standalone':''}`} id="governance" ref={root} data-playing={film.playing} data-chapter={chapter} data-display={displayMode}>
    <div className="gov-heading"><span className="overline"><ShieldCheck size={14}/>{standalone?'Q2Q · AI 评估与治理':'Q2Q · 企业 AI 资产'}</span><Heading>{standalone?'查清问题，':'让业务经验，'}<br/><span>{standalone?'验证改进。':'成为可验证的资产。'}</span></Heading><div><p>{standalone?'检查幻觉、偏差和判断波动，保留原文依据与复测结果。':'把业务判断与专家纠正，转化为有依据的规则和评测样本。换人、换模型，经验仍有据可查。'}</p><a href={standalone?'#delivery':'/ai-governance.html'}>了解评估与治理方案<ArrowUpRight size={14}/></a></div></div>
    {displayMode!=='assets'&&<div className="gov-module-tabs" role="tablist" aria-label="AI 治理三类能力">{governanceModules.map((item, i) => {const Icon = icons[i];return <button key={item.id} id={`gov-tab-${item.id}`} role="tab" aria-selected={moduleIndex===i} aria-controls="gov-panel" tabIndex={moduleIndex===i?0:-1} onClick={() => selectModule(i)} onKeyDown={event => moveTab(event, i, 3, selectModule)}><span className="gov-tab-number">0{i+1}</span><Icon size={18}/><span><strong>{item.label}</strong><small>{item.short}</small></span><ArrowRight size={13}/></button>;})}</div>}
    <div className="gov-product-panel" role={displayMode==='assets'?'region':'tabpanel'} id="gov-panel" aria-label={displayMode==='assets'?'从判断到资产':undefined} aria-labelledby={displayMode==='assets'?undefined:`gov-tab-${module.id}`}>
      <div className="gov-panel-caption"><p>{displayMode==='assets'?'一次纠正，成为下一次工作的依据。':module.description}</p><div className="gov-display-switch" aria-label="展示方式"><button aria-pressed={displayMode==='assets'} onClick={()=>{if(displayMode!=='assets')returnAssets();}}>资产沉淀</button><button aria-pressed={displayMode==='overview'} onClick={()=>{if(displayMode!=='overview')returnOverview();}}>评估能力</button><button aria-pressed={displayMode==='workspace'} onClick={()=>{if(displayMode!=='workspace')openWorkspace(view);}}>评估工作台</button></div></div>
      {displayMode==='assets'?<Q2QAssetCanvas step={assetStep} threshold={assetThreshold} changed={assetPolicyChanged} onThreshold={value=>{film.pause();setAssetThreshold(value);}} onChanged={value=>{film.pause();setAssetPolicyChanged(value);}} pause={film.pause} openWorkspace={()=>{setModuleIndex(0);openWorkspace('evidence');}}/>:displayMode==='overview'?<EvaluationCanvas moduleIndex={moduleIndex} view={view} corrected={comparisonCorrected} revision={film.revision} inspect={inspect} pause={film.pause} openWorkspace={()=>openWorkspace()}/>:<>
      <ShowcaseViewport label="Q2Q · AI 应用评估" width={1280} focusTarget={focusTarget} focusVersion={`${moduleIndex}-${noiseType}-${row}-${view}`} extraControls={<button onClick={film.toggle}>{film.playing?'暂停流程':'播放流程'}</button>}>
        <div className="gov-workspace">
          <header className="gov-window-bar"><span className="gov-app-icon"><ShieldCheck size={16} weight="fill"/></span><strong>Q2Q</strong><span className="gov-divider">/</span><span>AI 应用评估</span><div className="gov-window-right"><span className="gov-avatars" aria-label="业务与质量复核角色"><i>业</i><i>质</i></span></div></header>
          <aside className="gov-workspace-rail"><span className="gov-rail-label">评估范围</span>{governanceModules.map((item,i)=>{const Icon=icons[i];return <button key={item.id} className={moduleIndex===i?'selected':''} aria-pressed={moduleIndex===i} onClick={()=>selectModule(i)}><Icon size={15}/>{['可信输出','公平评价','噪音与稳定性'][i]}</button>;})}<div className="gov-rail-bottom"><ShieldCheck size={17}/><strong>Q2Q 证据链</strong><span>任务 · 版本 · 规则<br/>依据 · 判断 · 复测</span></div></aside>
          <div className="gov-samples"><div className="gov-scene-path"><ListChecks size={13}/>评估任务<span>/</span>当前检查</div><h3>{module.scene}</h3><p className="gov-scene-description">{moduleIndex===2?(noiseType==='data'?'从来源、版本和适用范围检查输入材料。':'固定业务条件，定位重复与跨版本判断中的分歧。'):'从具体业务样本出发，逐项回看判断与依据。'}</p>
            <div className="gov-summary"><div><span>检查样本</span><strong>{String(samples.length).padStart(2,'0')}</strong></div><div><span>待复核</span><strong>{String(problemCount).padStart(2,'0')}<i/></strong></div><div><span>保留对照</span><strong>{String(samples.length-problemCount).padStart(2,'0')}</strong></div></div>
            <div className="gov-list-tools">{moduleIndex===2?<div className="gov-noise-switch" aria-label="噪音检测范围"><button aria-pressed={noiseType==='data'} onClick={()=>selectNoise('data')}>资料质量</button><button aria-pressed={noiseType==='stability'} onClick={()=>selectNoise('stability')}>判断稳定性</button></div>:<strong>业务样本<span>{samples.length}</span></strong>}<button className={onlyProblems?'active':''} aria-pressed={onlyProblems} onClick={()=>{film.pause();setOnlyProblems(!onlyProblems);if(!onlyProblems&&!sample.problem)setRow(samples.findIndex(s=>s.problem));}}><FunnelSimple size={12}/>{onlyProblems?'仅看问题':'全部样本'}</button></div>
            <div className="gov-sample-table" role="table" aria-label="业务检查样本"><div className="gov-table-head" role="row"><span role="columnheader">检查对象</span><span role="columnheader">检查类型</span><span role="columnheader">当前判断</span></div>{visibleSamples.map(item=><div role="row" key={item.id} className={`gov-sample-row ${sample.id===item.id?'selected':''}`} onClick={()=>selectSample(samples.indexOf(item))}><span role="cell"><button className="gov-sample-open" aria-label={`查看${item.name}`} aria-pressed={sample.id===item.id}><strong>{item.name}</strong></button></span><span role="cell">{item.category}</span><span role="cell" className={`gov-state ${item.problem?'attention':'supported'}`}><i/>{item.status}</span></div>)}</div>
            <div className="gov-list-note"><LinkSimple size={13}/><span>每项判断保留输入、规则与来源版本</span><span>{visibleSamples.length} 项</span></div>
          </div>
          <aside className="gov-inspector" aria-label="核验详情"><header><span className={`gov-state ${sample.problem?'attention':'supported'}`}>{sample.status}</span></header><h4>{sample.name}</h4><div className="gov-detail-tabs" role="tablist" aria-label="核验详情视图">{views.map(([id,label],i)=><button key={id} role="tab" id={`gov-detail-${id}`} aria-controls="gov-detail-body" aria-selected={view===id} tabIndex={view===id?0:-1} onClick={()=>inspect(id)} onKeyDown={event=>moveTab(event,i,views.length,n=>inspect(views[n][0]))}>{label}</button>)}</div>
            <div className="gov-detail-body" id="gov-detail-body" role="tabpanel" aria-labelledby={`gov-detail-${view}`} key={`${sample.id}-${view}`}>
              {view==='finding'?<><span className="gov-field-label">待核对内容</span><p className="gov-claim">{sample.claim}</p><div className="gov-compare"><div>{module.columns.map(label=><span key={label}>{label}</span>)}</div>{sample.comparison.map(([label,before,expected],i)=><div key={label}><span>{label}</span><span className={sample.problem&&i===0?'flagged':''}>{before}</span><span>{expected}</span></div>)}</div><div className="gov-finding"><WarningCircle size={15}/><p>{sample.finding}</p></div><button className="gov-primary-action" onClick={()=>inspect('evidence')}>定位核验依据<ArrowRight size={14}/></button></>:view==='evidence'?<><span className="gov-field-label">关联来源</span><div className="gov-source-sheet"><div><FileText size={24}/><span><strong>{sample.source}</strong><small>{sample.location}</small></span></div><span className="gov-source-rule"/><p>{sample.excerpt}</p><footer><LinkSimple size={12}/>已关联当前检查项</footer></div><p className="gov-evidence-note">{sample.finding}</p><button className="gov-primary-action" onClick={()=>inspect('retest')}>查看整改与复测<ArrowRight size={14}/></button></>:<><span className="gov-field-label">处理建议</span><p className="gov-remediation">{sample.fix}</p><div className="gov-retest-record"><span><i/>修订前</span><p>{sample.claim}</p><span><CheckCircle size={12}/>修订后 · 同组样本复测</span><p>{sample.after}</p></div><div className="gov-trace-note"><GitBranch size={14}/><span>保留前后版本与对应依据<br/><small>复测范围：当前检查项</small></span></div><button className="gov-secondary-action" onClick={()=>inspect('evidence')}>回看原文依据<LinkSimple size={13}/></button></>}
            </div>
          </aside>
          <footer className="gov-workspace-footer"><span><i/>当前检查项已关联证据</span><span>样本定位<ArrowRight size={10}/>依据复核<ArrowRight size={10}/>整改复测</span></footer>
          <FilmCursor visible={film.playing&&!film.reduced&&film.time>3900&&chapter<2} x={pointer.x} y={pointer.y} click={film.time>5000&&film.time<5400||film.time>11000&&film.time<11400} name="质量复核"/>
        </div>
      </ShowcaseViewport>
      </>}
    </div>
    <FilmControls film={controlsFilm} chapter={displayMode==='assets'?assetStep:views.findIndex(([id])=>id===view)} chapters={displayMode==='assets'?assetChapters:chapters} duration={duration} name={displayMode==='assets'?'AI 资产形成过程':'AI 治理流程'}></FilmControls>

  </section>;
}

export function GovernancePage() {
  useEffect(() => {document.title = 'AI 评估与治理 — ForFlow 萬維流形';}, []);
  return <div className="v6 governance-page"><a className="skip-link" href="#governance">跳到主要内容</a><header className="gov-page-nav"><a href="/" aria-label="返回 ForFlow 首页"><img src="/assets/forflow.png" alt="ForFlow 萬維流形"/></a><nav aria-label="方案导航"><a href="/#capabilities">企业 AI 资产</a><a href="#governance" aria-current="page">AI 评估与治理</a><a href="#delivery">服务与交付</a></nav><a className="v6-button dark" href={bookingUrl} target="_blank" rel="noreferrer">讨论评测需求<ArrowUpRight size={13}/></a></header><main>
    <div className="gov-page-intro v6-container"><a href="/">首页</a><span>/</span><span>AI 评估与治理</span><p>面向企业 AI 应用的评测、证据复核与持续改进方案</p></div>
    <GovernanceSection standalone/>
    <section className="gov-service-section v6-container" id="delivery"><div className="gov-service-heading"><span className="overline">服务与交付</span><h2>带着一个业务问题，<br/><span>一起看怎么做。</span></h2><p>可以检查现有应用，也可以配合正在建设的 AI 项目。<br/>从业务场景、已有材料和希望改进的问题开始，确定合作范围。</p></div><div className="gov-scope-list">{governanceModules.map((item,i)=><article key={item.id}><span>0{i+1}</span><div><h3>{item.label}</h3><p>{item.description}</p><small>适合的业务场景</small><strong>{item.target}</strong></div><div><h4>交付内容</h4><ul>{item.deliverables.map(d=><li key={d}><Check size={13}/>{d}</li>)}</ul><p className="gov-metrics">验收关注：{item.metrics}</p></div></article>)}</div><div className="gov-noise-explainer"><GitBranch size={19}/><div><h3>噪音检测，分开看两件事。</h3><p><strong>资料质量：</strong>重复、冲突、过期和不适用内容。<br/><strong>判断稳定性：</strong>固定条件下重复运行、材料扰动与版本变化带来的结论分歧。</p></div></div></section>
    <section className="gov-engagement v6-container"><div><span className="overline">按需组合</span><h2>适合当前阶段的交付方式。</h2></div><div className="gov-engagement-grid">{[['专项评测','围绕一个具体应用，约定测试范围、样本、指标与复测，交付逐项可查的问题依据。','适合已有应用的质量检查'],['平台组件','将测试任务、指标配置、证据与复测接入企业现有 AI 平台，形成可复用的评测流程。','适合平台建设与系统集成'],['持续复测','在知识库、模型或业务规则变化后运行回归，跟进问题修复与版本影响。','适合长期运行的 AI 应用']].map(([title,body,hint],i)=><article key={title}><span>0{i+1}</span><h3>{title}</h3><p>{body}</p><small>{hint}</small></article>)}</div><div className="gov-acceptance"><ShieldCheck size={20}/><p><strong>验收前，先约定共同的判断标准。</strong><br/>明确业务范围、样本版本、标注方式、误报与漏报、通过条件及整改责任。需要境内部署或信创适配时，逐项确认数据流向与适配清单。</p></div></section>
    <section className="gov-page-cta v6-container"><div><span className="overline">从一项应用开始</span><h2>把一个具体的质量问题，<br/>变成可检查的改进。</h2><p>带上一个应用、一组材料，或一个希望改进的问题。</p></div><div className="gov-cta-actions"><a className="v6-button dark" href={bookingUrl} target="_blank" rel="noreferrer">填写需求，预约沟通<ArrowUpRight size={15}/></a><a className="gov-template-link" href="/ai-governance-brief.html">准备一份交流稿<ArrowRight size={13}/></a></div></section>
  </main><footer className="gov-page-footer v6-container"><span>© 2026 ForFlow 萬維流形</span><a href="/">返回首页<ArrowRight size={13}/></a></footer></div>;
}
