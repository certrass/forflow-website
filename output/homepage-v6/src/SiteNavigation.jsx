import React, {useEffect, useRef} from 'react';
import {bookingUrl} from './contact-config.js';
import groups from '../public/assets/site/navigation-content.json';
import {mountNavigation} from '../public/assets/site/guru-navigation.js';

const localHref = href => href.startsWith('/product/one/#') ? href.slice('/product/one/'.length) : href === '/product/one/' ? '#main' : href;
const Arrow = () => <span aria-hidden="true">↗</span>;

export function SiteNavigation() {
  const root = useRef(null);
  useEffect(() => mountNavigation(root.current), []);
  return <header className="ff-topbar" data-ff-navigation ref={root}>
    <div className="ff-topbar-inner">
      <a className="ff-topbar-brand" href="/#main" aria-label="ForFlow 萬維流形首页"><img src="/assets/forflow.png" alt="ForFlow 萬維流形" width="112" height="42"/></a>
      <nav className="ff-topbar-nav" id="ff-main-navigation" aria-label="主导航">
        {groups.map(group => <div className="ff-nav-group" key={group.id}>
          <button className="ff-nav-trigger" type="button" aria-expanded="false" aria-controls={`ff-menu-${group.id}`}>{group.label}<svg viewBox="0 0 16 16" aria-hidden="true"><path d="m4 6 4 4 4-4"/></svg></button>
          <div className="ff-nav-panel" id={`ff-menu-${group.id}`} inert>
            <div className="ff-nav-feature"><span className="ff-nav-kicker">{group.kicker}</span><h2>{group.title}</h2><p>{group.description}</p><a href={localHref(group.href)}>{group.cta}<Arrow/></a></div>
            <div className="ff-nav-links">{group.links.map(([title,description,href]) => <a key={title} href={localHref(href)}><span><strong>{title}</strong><small>{description}</small></span><Arrow/></a>)}</div>
          </div>
        </div>)}
        <a className="ff-nav-direct" href="#cases">案例与实践</a>
        <a className="ff-nav-mobile-link" href="https://forflow.ai/navigator.html">开始场景诊断 ↗</a>
      </nav>
      <div className="ff-topbar-actions"><a className="ff-nav-secondary" href="https://forflow.ai/navigator.html">场景诊断</a><a className="ff-nav-cta" href={bookingUrl} target="_blank" rel="noopener noreferrer">预约演示 <Arrow/></a></div>
      <button className="ff-nav-toggle" type="button" aria-label="打开菜单" aria-expanded="false" aria-controls="ff-main-navigation"><span/><span/></button>
    </div>
  </header>;
}
