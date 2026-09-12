import React, {useEffect, useRef, useState} from 'react';
import {ArrowRight, Pause, Play} from '@phosphor-icons/react';
import './hero-headline.css';

const tasks = ['业务跟进', '合同复核', '知识查询'];
const hold = 4200;

export function HeroHeadline() {
  const root = useRef(null);
  const [index, setIndex] = useState(0);
  const [previous, setPrevious] = useState(null);
  const [playing, setPlaying] = useState(true);
  const [visible, setVisible] = useState(false);
  const [pageVisible, setPageVisible] = useState(!document.hidden);
  const [reduced, setReduced] = useState(() => matchMedia('(prefers-reduced-motion: reduce)').matches);
  const [interacting, setInteracting] = useState(false);
  const running = playing && visible && pageVisible && !reduced && !interacting;

  useEffect(() => {
    const media = matchMedia('(prefers-reduced-motion: reduce)');
    const preference = () => setReduced(media.matches);
    const visibility = () => setPageVisible(!document.hidden);
    const observer = new IntersectionObserver(([entry]) => setVisible(entry.isIntersecting && entry.intersectionRatio >= .2), {threshold: .2});
    observer.observe(root.current.querySelector('h1'));
    media.addEventListener('change', preference);
    document.addEventListener('visibilitychange', visibility);
    return () => {
      observer.disconnect();
      media.removeEventListener('change', preference);
      document.removeEventListener('visibilitychange', visibility);
    };
  }, []);

  useEffect(() => {
    if (!running) return;
    const timer = setTimeout(() => {
      setPrevious(index);
      setIndex((index + 1) % tasks.length);
    }, hold);
    return () => clearTimeout(timer);
  }, [running, index]);

  useEffect(() => {
    if (previous === null) return;
    const timer = setTimeout(() => setPrevious(null), 520);
    return () => clearTimeout(timer);
  }, [previous, index]);

  function select(next) {
    setPlaying(false);
    if (next === index) return;
    setPrevious(index);
    setIndex(next);
  }

  return <div className="hero-headline rotating-hero" ref={root} data-task={index} data-running={running}>
    <div className="hero-brand-line">让 AI 真正流入业务</div>
    <h1 aria-label="与 AI 一起完成业务跟进、合同复核、知识查询。">
      <span className="hero-task-anchor" aria-hidden="true">与 AI 一起完成</span>
      <span className="hero-task-window" aria-hidden="true">
        {tasks.map((task, i) => <span key={task} className={`hero-task-word${i === index ? ' is-current' : i === previous ? ' is-leaving' : ''}${previous === null ? '' : ' is-transitioning'}`}>{task}</span>)}
      </span>
    </h1>
    <p>ForFlow 帮助企业把 AI 用进业务流程，<br/>解决具体问题，并把有效方法沉淀为可复用的能力。</p>
    <div className="v6-actions">
      <a className="v6-button dark" href="https://forflow.ai/contact">预约产品演示<ArrowRight size={15}/></a>
      <a className="v6-button light" href="#platform"><Play size={13}/>查看工作台</a>
    </div>
    <div className="hero-task-controls" role="group" aria-label="首屏工作场景"
      onPointerEnter={() => setInteracting(true)} onPointerLeave={() => setInteracting(false)}
      onFocus={() => setInteracting(true)} onBlur={e => {if (!e.currentTarget.contains(e.relatedTarget)) setInteracting(false)}}>
      {tasks.map((task, i) => <button key={task} className="hero-task-choice" aria-label={`查看${task}`} title={task} aria-pressed={i === index} onClick={() => select(i)}><span/></button>)}
      {!reduced && <button className="hero-task-pause" aria-label={playing ? '暂停标题轮换' : '播放标题轮换'} title={playing ? '暂停' : '播放'} onClick={() => setPlaying(value => !value)}>{playing ? <Pause size={12}/> : <Play size={12}/>}</button>}
    </div>
  </div>;
}
