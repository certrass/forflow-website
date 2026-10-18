import React, {useMemo, useRef, useState} from 'react';
import {ArrowRight, ArrowUpRight, MagnifyingGlass, X} from '@phosphor-icons/react';
import catalog from './case-catalog.json';

const filters=[['all','全部'],['manufacturing','制造与工程'],['finance','金融与文档'],['service','运营与服务'],['education','教育']];
const featured=['automotive-dfmea-ontology-agent','energy-optimization-agent','healthcare-agent-roi','agent-evaluation-first'];
export const bPillarCase={id:'bpillar',name:'汽车工程',title:'让 B 柱 DFMEA 的工程经验可追溯。',tag:'工程方法',sources:['历史 DFMEA 与 ECO','材料与工艺资料','试验与质量记录']};

export function CaseLibrary({onRead, scenes}) {
  const [filter,setFilter]=useState('all'),[query,setQuery]=useState(''),[expanded,setExpanded]=useState(false);
  const search = useRef(null), heading = useRef(null);
  const hasQuery = Boolean(query.trim());
  const filtered=useMemo(()=>catalog.filter(c=>(filter==='all'||c.tags.includes(filter))&&`${c.title} ${c.description} ${c.search}`.toLowerCase().includes(query.trim().toLowerCase())),[filter,query]);
  const showingFeatured=filter==='all'&&!hasQuery&&!expanded;
  const items=showingFeatured?featured.map(id=>catalog.find(c=>c.id===id)).filter(Boolean):filtered;
  const counts=useMemo(()=>Object.fromEntries(filters.map(([id])=>[id,id==='all'?catalog.length:catalog.filter(item=>item.tags.includes(id)).length])),[]);
  const resultSummary=showingFeatured?`精选 ${items.length} 条 · 共 ${catalog.length} 条案例`:hasQuery||filter!=='all'?`${filtered.length} 条匹配结果`:`全部 ${catalog.length} 条案例`;
  const clearSearch = () => {setQuery('');search.current?.focus({preventScroll:true});};
  const toggleExpanded = () => {
    setExpanded(!expanded);
    if (expanded) requestAnimationFrame(()=>{
      heading.current?.focus({preventScroll:true});
      heading.current?.closest('.case-library').scrollIntoView({block:'start',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
    });
  };
  function openCase(event,item){
    if(event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
    const scene=scenes.find(s=>item.source===`${s.link}.html`);
    if(item.id==='automotive-dfmea-ontology-agent'||scene){event.preventDefault();onRead(scene||bPillarCase);}
  }
  return <div className="case-library" id="case-library">
    <div className="case-library-heading">
      <div><h3 ref={heading} tabIndex={-1}>更多案例</h3></div>
      <label className="case-search"><MagnifyingGlass size={18}/><input
        ref={search} value={query} onChange={event=>setQuery(event.target.value)}
        onKeyDown={event=>{if(event.key==='Escape'&&query){event.preventDefault();clearSearch();}}}
        placeholder="搜索 B 柱、合同、能效…" aria-label="搜索案例" type="search"
        aria-controls="case-library-results"
      />{query&&<button onClick={clearSearch} aria-label="清空案例搜索"><X size={16}/></button>}</label>
    </div>
    <div className="case-library-controls">
      <div className="case-filters" role="group" aria-label="按业务筛选案例">
        {filters.map(([id,label])=><button key={id} onClick={()=>setFilter(id)} aria-pressed={filter===id} aria-controls="case-library-results">{label}<span className="case-filter-count" aria-hidden="true">{counts[id]}</span></button>)}
      </div>
      <p className="case-result-summary" role="status">{resultSummary}</p>
    </div>
    <div className="case-library-grid" id="case-library-results">
      {items.map(item=>{
        const opensDialog=item.id==='automotive-dfmea-ontology-agent'||scenes.some(scene=>item.source===`${scene.link}.html`);
        const titleId=`case-title-${item.id}`;
        return <article key={item.id} className="case-library-item">
          <span>{item.type}</span><h4 id={titleId}>{item.id==='automotive-dfmea-ontology-agent'?'B 柱 DFMEA：让工程经验可追溯':item.title}</h4><p>{item.description}</p>
          {item.source?<a
            href={item.source.startsWith('https:')?item.source:`https://forflow.ai/${item.source.replace(/\.html$/,'')}`}
            target={opensDialog?undefined:'_blank'} rel="noreferrer" onClick={event=>openCase(event,item)}
            aria-labelledby={titleId} aria-haspopup={opensDialog?'dialog':undefined}
          >{opensDialog?'查看案例':'阅读原文'}<ArrowUpRight size={16}/></a>:<small>{item.status}</small>}
        </article>;
      })}
    </div>
    {!items.length&&<div className="case-library-empty"><p>没有找到匹配案例</p><span>试试其他关键词，或清除筛选。</span><button onClick={()=>{setQuery('');setFilter('all');setExpanded(true);search.current?.focus({preventScroll:true});}}>清除筛选，查看全部<ArrowRight size={16}/></button></div>}
    {!hasQuery&&filter==='all'&&<button className="case-library-more" onClick={toggleExpanded} aria-expanded={expanded} aria-controls="case-library-results">{expanded?'收起，回到精选案例':`查看全部 ${catalog.length} 条案例`}<ArrowRight size={16} className={expanded?'is-collapsed-arrow':''}/></button>}
  </div>;
}
