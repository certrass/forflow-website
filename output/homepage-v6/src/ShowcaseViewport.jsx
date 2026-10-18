import React, {useEffect, useLayoutEffect, useRef, useState} from 'react';
import {ArrowsOut, ArrowsIn, ArrowLeft, ArrowRight, X} from '@phosphor-icons/react';

// Product demonstrations keep their spatial grammar at every viewport size.
export function ShowcaseViewport({children, label, width = 970, extraControls, focusTarget, focusVersion, detailSections, onExpand, chrome = false}) {
  const viewport = useRef(null);
  const native = useRef(null);
  const opener = useRef(null);
  const restingHeight = useRef(0);
  const pagePosition = useRef({left:0,top:0});
  const [size, setSize] = useState({width, height: 620});
  const [expanded, setExpanded] = useState(false);
  const [detail, setDetail] = useState(true);
  const [detailFocus, setDetailFocus] = useState(null);
  const activeTarget = detailFocus && detailFocus.version === focusVersion ? detailFocus.target : focusTarget;
  const [edges,setEdges] = useState({left:false,right:false});
  useLayoutEffect(() => {
    const measure = () => setSize({width: viewport.current.clientWidth, height: native.current.offsetHeight});
    const observer = new ResizeObserver(measure);
    observer.observe(viewport.current);
    observer.observe(native.current);
    measure();
    return () => observer.disconnect();
  }, []);
  useEffect(() => {
    if (!expanded) return;
    const previous = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    const close = e => { if(e.key === 'Escape'&&!document.querySelector('[data-case-dialog]')) setExpanded(false); };
    window.addEventListener('keydown', close);
    const controls = viewport.current.parentElement.querySelectorAll('.showcase-controls button');
    controls[0]?.focus();
    return () => {
      document.body.style.overflow = previous;
      window.removeEventListener('keydown', close);
      // The canvas refits through ResizeObserver after leaving fixed layout.
      // Restore reading position after that measurement, as well as focus.
      const position={...pagePosition.current};
      requestAnimationFrame(()=>requestAnimationFrame(()=>{
        window.scrollTo({...position,behavior:'instant'});
        opener.current?.focus({preventScroll:true});
      }));
    };
  }, [expanded]);
  const fit = Math.min(1, size.width / width);
  const scale = expanded && detail ? Math.max(fit, .92) : fit;
  const updateEdges=()=>{
    const el=viewport.current;if(!el)return;
    const next={left:el.scrollLeft>2,right:el.scrollLeft+el.clientWidth<el.scrollWidth-2};
    setEdges(prev=>prev.left===next.left&&prev.right===next.right?prev:next);
  };
  useLayoutEffect(updateEdges,[expanded,detail,scale,size.width,size.height]);
  useEffect(() => {
    const canvasElement = native.current;
    const viewportElement = viewport.current;
    if (!expanded || !detail || !canvasElement || !viewportElement) return;
    const reveal = () => {
      const action = activeTarget && native.current?.querySelector(activeTarget);
      if (action) {
        const context = action.closest('.wq-source-sheet,.wq-inspector,.story-source,.story-team,.cli-result');
        const contextBounds = context?.getBoundingClientRect();
        const actionBounds = contextBounds && contextBounds.width <= size.width ? contextBounds : action.getBoundingClientRect();
        const canvasBounds = native.current.getBoundingClientRect();
        viewport.current.scrollTo({left: actionBounds.left - canvasBounds.left + actionBounds.width / 2 - size.width / 2, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'});
        return;
      }
      const drawer = native.current?.querySelector('[aria-modal="true"]') || native.current?.querySelector('.task-detail');
      if (!drawer) return;
      const drawerBounds = drawer.getBoundingClientRect();
      const canvasBounds = native.current.getBoundingClientRect();
      const target = drawerBounds.left - canvasBounds.left - Math.max(0, (size.width - drawerBounds.width) / 2);
      viewport.current.scrollTo({left: target, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'});
    };
    const observer = new MutationObserver(reveal);
    observer.observe(canvasElement, {childList:true, subtree:true});
    reveal();
    return () => observer.disconnect();
  }, [expanded, detail, scale, size.width, activeTarget, focusVersion]);
  const move = direction => viewport.current.scrollBy({left: direction * size.width * .75, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'});
  const trap = e => {
    if (!expanded || e.key !== 'Tab') return;
    const nodes = [...e.currentTarget.querySelectorAll('button,a,input,textarea,select,[tabindex="0"]')].filter(n => !n.disabled && n.getClientRects().length);
    if (e.shiftKey && document.activeElement === nodes[0]) { e.preventDefault(); nodes.at(-1)?.focus(); }
    else if (!e.shiftKey && document.activeElement === nodes.at(-1)) { e.preventDefault(); nodes[0]?.focus(); }
  };
  return <>{expanded && <div aria-hidden="true" className="showcase-placeholder" style={{height:restingHeight.current}}/>}<div className={`showcase-viewer ${expanded ? 'is-expanded' : ''}`} role={expanded ? 'dialog' : undefined} aria-modal={expanded || undefined} aria-label={expanded ? label : undefined} onKeyDown={trap}>
    <div className={`showcase-controls${chrome ? ' window-chrome' : ''}`}>
      {chrome && <span className="window-dots" aria-hidden="true"><i/><i/><i/></span>}
      <span>{label}</span>
      {expanded ? <div>
        {extraControls}
        <button onClick={() => { setDetail(!detail); viewport.current.scrollTo({left: 0, top: 0}); }}>{detail ? <ArrowsIn size={15}/> : <ArrowsOut size={15}/>} {detail ? '查看全貌' : '查看细节'}</button>
        {width*scale>size.width+2&&<><button disabled={!edges.left} onClick={() => move(-1)} aria-label="向左浏览展示" title="向左浏览"><ArrowLeft size={16}/></button>
        <button disabled={!edges.right} onClick={() => move(1)} aria-label="向右浏览展示" title="向右浏览"><ArrowRight size={16}/></button></>}
        <button onClick={() => setExpanded(false)} aria-label="关闭放大展示" title="关闭 · Esc" aria-keyshortcuts="Escape"><X size={19}/></button>
      </div> : <button ref={opener} onClick={() => { restingHeight.current=viewport.current.parentElement.getBoundingClientRect().height;pagePosition.current={left:window.scrollX,top:window.scrollY};setDetailFocus(null);setDetail(true);setExpanded(true);onExpand?.(); }}><ArrowsOut size={14}/>查看细节</button>}
    </div>
    <div ref={viewport} className="showcase-viewport" onScroll={updateEdges} tabIndex={expanded ? 0 : undefined} aria-label={`${label}，放大后可左右浏览`}>
      <div className="showcase-size" style={{width: width * scale, height: size.height * scale}}>
        <div className="showcase-native" style={{width, transform: `scale(${scale})`}} ref={native}>{children}</div>
      </div>
    </div>
    {expanded && detailSections && size.width < width * .92 && <div className="showcase-detail-nav" role="group" aria-label="快速定位展示内容">{detailSections.map(section=><button key={section.target} aria-pressed={detail && activeTarget===section.target} onClick={()=>{setDetail(true);setDetailFocus({target:section.target,version:focusVersion});}}>{section.label}<ArrowRight size={13}/></button>)}</div>}
    {expanded && <div className="showcase-viewer-help">{width*scale>size.width+2?'左右滑动查看完整界面':'当前显示完整界面'}<span>Esc 关闭</span></div>}
  </div></>;
}
