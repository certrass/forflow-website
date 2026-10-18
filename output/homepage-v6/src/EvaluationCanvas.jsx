import React from 'react';
import {ArrowRight, Check, FileText, ShieldCheck} from '@phosphor-icons/react';
import {ShowcaseViewport} from './ShowcaseViewport.jsx';
import {governanceModules} from './governance-content.js';

// These are visual encodings of the existing, authored governance walkthroughs.
// They are not aggregate evaluation scores or customer performance claims.
const stories = [
  {question:'这份回答，和采购制度一致吗？', title:'审批金额，回到原文核对。', metric:'审批阈值', unit:'万元', labels:['AI 回答', '制度原文'], before:[100,50], after:[50,50], max:100, ticks:[0,25,50,75,100], beforeLabel:'相差 50 万元', afterLabel:'金额与原文一致', sample:governanceModules[0].samples[0]},
  {question:'只换一个名字，评价会改变吗？', title:'业务条件相同，评分应有同一依据。', metric:'供应商初评得分', unit:'分', labels:['供应商 A', '供应商 B'], before:[82,74], after:[80,80], max:100, ticks:[0,25,50,75,100], beforeLabel:'相差 8 分', afterLabel:'同组复测 · 80 / 80', sample:governanceModules[1].samples[0]},
  {question:'同一份材料，为什么审核结论不同？', title:'固定条件，观察每一次判断。', metric:'重复核验结果', unit:'', beforeLabel:'3 次运行出现 2 种结论', afterLabel:'3 次复测均定位到缺失证据', sample:governanceModules[2].stabilitySamples[0]},
];

function ComparisonChart({story, corrected, onInspect}) {
  const values = corrected ? story.after : story.before;
  return <div className="evaluation-chart" role="group" aria-label={`${story.metric}，${corrected?'整改复测':'修订前'}`}>
    <div className="evaluation-chart-scale" aria-hidden="true">{story.ticks.map(tick=><span key={tick}>{tick}</span>)}</div>
    <div className="evaluation-chart-grid" aria-hidden="true">{story.ticks.map(tick=><i key={tick}/>)}</div>
    <div className="evaluation-bars">{values.map((value,i)=><button className={`evaluation-bar-group bar-${i}`} key={story.labels[i]} onClick={onInspect} aria-label={`${story.labels[i]}：${value}${story.unit}，查看核验依据`}>
      <span className="evaluation-bar" style={{'--bar-height':`${value/story.max*100}%`}}><strong>{value}<small>{story.unit}</small></strong></span><span className="evaluation-bar-label">{story.labels[i]}</span>
    </button>)}</div>
  </div>;
}

function StabilityChart({corrected, onInspect}) {
  return <div className="evaluation-runs" role="group" aria-label="三次重复核验结果">{[0,1,2].map(i=>{
    const missing=corrected||i===1;
    return <button key={i} onClick={onInspect} className={missing?'needs-evidence':'passed'} aria-label={`运行 ${i+1}：${missing?'需补证':'通过'}，查看核验依据`}><small>运行 0{i+1}</small><span>{missing?<FileText size={23}/>:<Check size={23}/>}</span><strong>{missing?'需补证':'通过'}</strong><p>{missing?'必要证据缺失':'已给出通过结论'}</p></button>;
  })}</div>;
}

const detailSections = [{label:'对比图表',target:'.evaluation-chart, .evaluation-runs'}, {label:'核验依据',target:'.evaluation-note'}];

export function EvaluationCanvas({moduleIndex, view, corrected, revision, inspect, pause, openWorkspace}) {
  const story=stories[moduleIndex];
  return <div className="evaluation-showcase">
    <ShowcaseViewport label="Q2Q · 交互概览" width={1080} focusTarget={detailSections[view==='evidence'?1:0].target} focusVersion={`${moduleIndex}-${view}-${revision}`} detailSections={detailSections} onExpand={pause}>
      <div className="evaluation-canvas" data-view={view}>
        <header className="evaluation-appbar"><span><ShieldCheck size={16}/><strong>Q2Q</strong><i/>评估记录</span><span><i className="evaluation-live-dot"/>依据已关联</span></header>
        <div className="evaluation-conversation"><div className="evaluation-question" key={moduleIndex}>{story.question}</div><div className="evaluation-response"><span className="evaluation-agent"><ShieldCheck size={15}/></span><p>对照业务规则，找出差异，再用同一组材料复测。</p></div></div>
        <div className="evaluation-result">
          <div className="evaluation-visual"><header><span>{story.metric}</span><div className="evaluation-version" aria-label="比较版本"><button aria-pressed={!corrected} onClick={()=>inspect('finding')}>修订前</button><button aria-pressed={corrected} onClick={()=>inspect('retest')}>整改复测</button></div></header><h3>{story.title}</h3>
            {moduleIndex===2?<StabilityChart corrected={corrected} onInspect={()=>inspect('evidence')}/>:<ComparisonChart story={story} corrected={corrected} onInspect={()=>inspect('evidence')}/>}
            <div className="evaluation-conclusion" aria-live="polite"><span className={corrected?'is-corrected':''}/>{corrected?story.afterLabel:story.beforeLabel}<button onClick={()=>inspect('evidence')}>查看依据<ArrowRight size={13}/></button></div>
          </div>
          <aside className="evaluation-note" data-emphasis={view==='evidence'}><header><FileText size={16}/><span>核验依据</span></header><h4>{story.sample.source}</h4><span className="evaluation-location">{story.sample.location}</span><blockquote>{story.sample.excerpt}</blockquote><div className="evaluation-note-divider"/><span className="evaluation-note-label">{corrected?'复测记录':'核验结论'}</span><p key={`${moduleIndex}-${corrected}`}>{corrected?story.sample.after:story.sample.finding}</p><button className="evaluation-workspace-link" onClick={openWorkspace}>在工作台查看完整记录<ArrowRight size={14}/></button></aside>
        </div>
      </div>
    </ShowcaseViewport>
  </div>;
}
