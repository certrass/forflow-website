import React, {useRef, useState} from 'react';
import {ArrowRight, BookOpen, Check, CheckCircle, Database, FileText, FlowArrow, GitBranch, LinkSimple, MagnifyingGlass, Pause, Play, ShieldCheck, Stack} from '@phosphor-icons/react';
import {ShowcaseViewport} from './ShowcaseViewport.jsx';
import {useAmbientSequence} from './useAmbientSequence.js';

const sourceDurations = [2500, 2500, 2500, 3800];
const evaluationDurations = [2800, 2800, 2800, 4000];
const assetDurations = [1800, 2400, 2400, 800, 3800];
const sources = [
  {Icon:FileText, title:'供应商合同', detail:'合同原文', field:'待核对内容', value:'终止与续约条款'},
  {Icon:Database, title:'业务记录', detail:'ERP · 供应商档案', field:'负责团队', value:'采购团队'},
  {Icon:BookOpen, title:'续约规则', detail:'业务知识库 · 已审核', field:'适用规则', value:'到期前 30 天发起复核'},
];
const evaluationSteps = [
  {Icon:MagnifyingGlass, label:'关联依据', status:'正在关联判断依据', result:'合同、记录与规则已对应', subtitle:'3 类来源 · 同一业务对象'},
  {Icon:FlowArrow, label:'规则核验', status:'正在核对适用规则', result:'发现需人工确认的事项', subtitle:'续约条件 · 保留原文依据'},
  {Icon:ShieldCheck, label:'业务复核', status:'交给业务负责人复核', result:'判断与依据，一起交接', subtitle:'负责人 · 复核意见 · 处理记录'},
  {Icon:Check, label:'记录结果', status:'评估记录已保留', result:'为下一次评估留下依据', subtitle:'输入版本 · 判断规则 · 复核记录'},
];

function DemoPointer({label}) {
  return <div className="method-pointer" aria-hidden="true"><svg width="22" height="26" viewBox="0 0 22 26"><path d="M3 2 19 15 11 16 7 23Z" fill="currentColor" stroke="white" strokeWidth="2" strokeLinejoin="round"/></svg><span>{label}</span></div>;
}

function SourcesScene({enabled, onTakeover}) {
  const root = useRef(null);
  const {phase, running, select} = useAmbientSequence(root, sourceDurations, enabled);
  const selected = Math.min(2, phase);
  return <div className="method-scene source-sequence" ref={root} data-phase={phase} data-running={running}>
    <div className="method-windowbar"><span><LinkSimple size={13}/>关联业务资料</span></div>
    <div className="method-source-list" role="group" aria-label="查看关联来源">
      <i className="method-selection" style={{transform:`translateY(${selected * 56}px)`}} aria-hidden="true"/>
      {sources.map(({Icon,title,detail}, i) => <button key={title} aria-pressed={i === selected} onClick={() => {onTakeover();select(i);}}><span className="method-file-icon"><Icon size={18}/></span><span><strong>{title}</strong><small>{detail}</small></span><CheckCircle size={16} weight={i <= phase ? 'fill' : 'regular'}/></button>)}
    </div>
    <div className="method-source-detail"><span>{sources[selected].field}</span><strong key={selected}>{sources[selected].value}</strong><LinkSimple size={13}/></div>
    <div className="method-source-status"><span className={phase === 3 ? 'is-complete' : ''}><Check size={12}/>{phase === 3 ? '已关联到同一项工作' : `${phase + 1} / 3 类来源已关联`}</span></div>
    <DemoPointer label="关联资料"/>
  </div>;
}

function EvaluationScene({enabled, onTakeover}) {
  const root = useRef(null);
  const {phase, running, select} = useAmbientSequence(root, evaluationDurations, enabled);
  return <div className="method-scene evaluation-sequence" ref={root} data-phase={phase} data-running={running}>
    <div className="method-windowbar"><span><ShieldCheck size={13}/>Q2Q 评估</span><span>持续复评</span></div>
    <div className="method-agent-stage"><div className="method-agent-track" role="group" aria-label="查看评估步骤">
      {evaluationSteps.map(({Icon,label,status}, i) => <button key={label} className={`method-agent${i === phase ? ' is-active' : ''}`} aria-label={label} aria-pressed={i === phase} onClick={() => {onTakeover();select(i);}}><span className="method-agent-symbol"><Icon size={17}/></span><span className="method-agent-status">{status}</span></button>)}
    </div></div>
    <div className="method-evaluation-result"><div className="method-result-symbol"><ShieldCheck size={22} weight="light"/></div><div className="method-result-window">{evaluationSteps.map((step,i) => <div key={step.label} className={i === phase ? 'is-current' : ''} aria-hidden={i !== phase}><strong>{step.result}</strong><small>{step.subtitle}</small></div>)}</div></div>
    <div className="method-evaluation-steps" aria-hidden="true">{evaluationSteps.map((step,i) => <span key={step.label} data-complete={i < phase} data-active={i === phase}><i>{i < phase ? <Check size={9}/> : `0${i+1}`}</i>{step.label}</span>)}</div>
    <div className="method-evaluation-foot"><GitBranch size={13}/>模型、数据或规则变化时，重新评估。</div>
  </div>;
}

function AssetsScene({enabled, onTakeover}) {
  const root = useRef(null);
  const {phase, running, select} = useAmbientSequence(root, assetDurations, enabled);
  return <div className="method-scene asset-sequence" ref={root} data-phase={phase} data-running={running}>
    <div className="method-windowbar"><span><Stack size={13}/>企业能力库</span><span>规则 / 续约管理</span></div>
    <div className="method-rule-document"><div><FileText size={15}/><span>供应商续约规则</span></div><p>合同到期前 30 天，发起续约复核。</p><p><span className="method-rule-mark">核对履约记录，关联合同原文。</span></p><p><span className="method-rule-mark second">由业务负责人确认下一步。</span></p><div className="method-rule-citation"><LinkSimple size={11}/>原文依据 · 第 4.2 条</div></div>
    <button className="method-save-rule" onClick={() => {onTakeover();select(phase === 4 ? 0 : 4);}}><span>{phase === 4 ? <Check size={13}/> : <Stack size={13}/>}</span>{phase === 4 ? '已保留为业务规则' : '保存到能力库'}</button>
    <div className="method-rule-foot"><span className="method-review-avatar">陈</span><span>业务负责人已复核</span><span className="method-rule-stamp" data-visible={phase === 4}><Check size={11}/>已入库</span></div>
    <DemoPointer label="保留规则"/>
  </div>;
}

const cards = [
  {tag:'业务上下文',title:'关联资料',body:'合同、业务记录与规则，对应到同一项任务。',Scene:SourcesScene,link:'#connectors',cta:'查看连接方式'},
  {tag:'评估与复评',title:'核验结果',body:'按业务规则检查结果，将例外交给负责人。',Scene:EvaluationScene,link:'#governance',cta:'了解评估服务'},
  {tag:'能力积累',title:'保存规则',body:'审核后保留为业务规则，供后续任务使用。',Scene:AssetsScene,link:'#capabilities',cta:'探索 AI 资产'},
];

export function Advantages() {
  const [playing, setPlaying] = useState(true);
  return <section className="advantages-section v6-container" id="advantages">
    <div className="advantages-heading"><span className="overline"><ShieldCheck size={14}/>工作依据</span><h2>每个判断，<br/><span>都有依据。</span></h2></div>
    <div className="method-motion-toolbar"><button aria-label={playing ? '暂停能力演示' : '继续能力演示'} onClick={() => setPlaying(value => !value)}>{playing ? <Pause size={12} weight="fill"/> : <Play size={12} weight="fill"/>}{playing ? '暂停' : '继续播放'}</button></div>
    <div className="method-grid">{cards.map(({tag,title,body,Scene,link,cta},i) => <article className={`method-card method-card-${i}`} key={tag}>
      <header><h3>{title}</h3><p>{body}</p></header>
      <ShowcaseViewport width={320} label={tag}><Scene enabled={playing} onTakeover={() => setPlaying(false)}/></ShowcaseViewport>
      <a className="method-card-link" href={link}>{cta}<ArrowRight size={13}/></a>
    </article>)}</div>

  </section>;
}
