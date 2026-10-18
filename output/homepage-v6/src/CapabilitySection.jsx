import React, {useEffect, useRef, useState} from 'react';
import {ArrowRight, ArrowCounterClockwise, Cube, Pause} from '@phosphor-icons/react';

const layers = [
  {name: '业务上下文', description: '把合同、业务记录与专业知识关联到具体任务，明确处理所需的信息。', examples: '合同 · 数据 · 图纸 · 规则 · 知识 · 人的判断'},
  {name: '工作流', description: '将任务拆成可执行的步骤，明确每一步的输入、判断规则与处理责任。', examples: '关联依据 → 分析判断 → 复核交接'},
  {name: '能力资产', description: '保留经过审核与评测的知识、规则和流程，让后续项目有据可循。', examples: '知识 · 规则 · 工作流 · 评估样本'}
];

export function CapabilitySection() {
  const mount = useRef(null);
  const model = useRef(null);
  const [active, setActive] = useState(1);
  const [rotating, setRotating] = useState(false);
  const [interactive, setInteractive] = useState(false);
  const [status, setStatus] = useState('loading');
  const selectLayerWithKey = (event, index) => {
    const next = event.key === 'ArrowRight' ? (index + 1) % layers.length
      : event.key === 'ArrowLeft' ? (index + layers.length - 1) % layers.length
      : event.key === 'Home' ? 0 : event.key === 'End' ? layers.length - 1 : null;
    if (next === null) return;
    event.preventDefault();
    setActive(next);
    event.currentTarget.parentElement.querySelectorAll('[role="tab"]')[next]?.focus();
  };
  useEffect(() => {
    if (!interactive) return;
    setStatus('loading');
    let alive = true;
    const observer = new IntersectionObserver(async entries => {
      if (!entries.some(e => e.isIntersecting)) return;
      observer.disconnect();
      try {
        const {createCapabilityScene} = await import('./capability-scene.js');
        if (!alive) return;
        model.current = createCapabilityScene(mount.current);
        setStatus('ready');
      } catch {
        if (alive) setStatus('fallback');
      }
    }, {rootMargin: '250px'});
    observer.observe(mount.current);
    return () => {alive = false; observer.disconnect(); model.current?.dispose(); model.current = null;};
  }, [interactive]);
  useEffect(() => {model.current?.setLayer(active);}, [active, status]);
  useEffect(() => {model.current?.setRotating(rotating);}, [rotating, status]);
  return <section className="capability-section v6-container" id="capabilities">
    <div className="capability-copy">
      <span className="overline"><Cube size={14}/>企业 AI 资产</span>
      <h2>把有效方法，<br/><span>留给下一次工作。</span></h2>
      <p>管理规则、工作流和评测样本的版本、依据与适用条件。</p>
      <a className="v6-button light" href="https://forflow.ai/service-agent-build">了解企业服务<ArrowRight size={15}/></a>
      <div className="capability-description" id="capability-detail" aria-live="polite"><span>{layers[active].name}</span><p>{layers[active].description}</p></div>
    </div>
    <div className="capability-model">{interactive&&<div className="model-caption"><span>拖动查看结构</span></div>}
      <div className="capability-canvas" ref={mount} role="img" aria-label="三维能力结构：底层业务上下文连接中层工作流，上层保留知识、规则、流程和评估资产" data-render-state={status}/>
      {interactive && status === 'loading' && <span className="model-loading"><Cube size={18}/>正在呈现能力结构</span>}
      {(!interactive || status === 'fallback') && <div className="model-fallback"><img src="/assets/capability-poster.png" loading="lazy" alt="业务上下文、工作流与能力资产的三层结构"/></div>}
      <div className="model-labels">{[2,1,0].map(i => <button className={active===i?'active':''} aria-pressed={active===i} onClick={() => setActive(i)} key={i}><i/><span>{layers[i].name}</span></button>)}</div>
      <div className="model-tools">{interactive ? <><button onClick={() => {setInteractive(false);setRotating(false);}}>返回渲染图</button>{status === 'ready' && <><button aria-pressed={rotating} onClick={() => setRotating(!rotating)}>{rotating?<Pause size={13}/>:<Cube size={13}/>} {rotating?'暂停旋转':'旋转模型'}</button><button onClick={() => {setRotating(false);model.current?.reset();}} aria-label="恢复模型视角"><ArrowCounterClockwise size={14}/></button></>}</> : <button onClick={() => setInteractive(true)}><Cube size={14}/>查看立体结构</button>}</div>
    </div>
    <div className="capability-steps" role="tablist" aria-label="能力形成的三个层次">{layers.map((layer, i) => <button key={layer.name} role="tab" aria-selected={active===i} aria-controls="capability-detail" tabIndex={active===i?0:-1} onKeyDown={event => selectLayerWithKey(event, i)} onClick={() => setActive(i)}><strong>{layer.name}</strong></button>)}</div>

  </section>;
}
