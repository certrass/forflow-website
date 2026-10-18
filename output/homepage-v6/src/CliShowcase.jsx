import React, {useEffect, useRef, useState} from 'react';
import {ArrowLeft, ArrowRight, Check, CheckCircle, Code, Copy, FileCode, FileText, LinkSimple, TerminalWindow, WarningCircle} from '@phosphor-icons/react';
import {DetailTabs} from './ProductDetailUI.jsx';
import {ShowcaseViewport} from './ShowcaseViewport.jsx';
import {useShowcaseFilm} from './useShowcaseFilm.js';
import {FilmControls, FilmCursor} from './ShowcaseFilmUI.jsx';

const duration = 21000;
const chapters = [['准备输入', 0], ['执行核验', 5400], ['回看结果', 14000]];
const command = 'python3 q2q_case_runner.py run \\\n  --case transport-case.json \\\n  --phase all --db q2q.sqlite3 --out result.json';
const logSteps = ['校验任务与输入', '关联材料与判断', '生成结果与待办'];
const entryPoints = [[TerminalWindow,'本地终端'],[Code,'开发工具'],[FileCode,'自动化脚本']];

export function CliShowcase() {
  const root = useRef(null);
  const commandText = useRef(null);
  const film = useShowcaseFilm(root, duration);
  const [entry, setEntry] = useState(0);
  const [details, setDetails] = useState(false);
  const [copied, setCopied] = useState('');
  const [showCommand, setShowCommand] = useState(false);
  const chapter = film.time >= 14000 ? 2 : film.time >= 5400 ? 1 : 0;
  const complete = film.time >= 13600;
  const automaticEvidence = film.time >= 18900;
  const partial = film.reduced || showCommand ? command : command.slice(0, Math.floor(Math.min(1, Math.max(0, (film.time - 1000) / 4900)) * command.length));
  useEffect(() => { if (!copied) return; const timer = setTimeout(() => setCopied(''), 2400); return () => clearTimeout(timer); }, [copied]);
  useEffect(() => { if (film.playing) { setDetails(false); setShowCommand(false); } }, [film.playing]);
  useEffect(() => { if (film.playing) setDetails(automaticEvidence); }, [film.playing, automaticEvidence]);
  const copy = async () => {
    film.pause();
    setShowCommand(true);
    try { await navigator.clipboard.writeText(command); setCopied('完整命令已复制'); }
    catch { requestAnimationFrame(()=>window.getSelection()?.selectAllChildren(commandText.current)); setCopied('复制未完成，已选中完整命令'); }
  };
  return <section className="cli-showcase v6-container" id="cli" ref={root} data-chapter={chapter} data-playing={film.playing} data-time={Math.floor(film.time)}>
    <div className="cli-heading"><span className="overline"><TerminalWindow size={14}/>CLI 接入</span><h2>把核验接入<br/><span>你的工作流。</span></h2><p>在终端运行任务，取回结果、依据和待复核事项。</p></div>
    <ShowcaseViewport label="ForFlow CLI · Q2Q Runner" width={1280} focusVersion={film.revision} focusTarget={chapter === 2 ? '.cli-result' : '.cli-terminal'} extraControls={<button onClick={film.toggle}>{film.playing ? '暂停' : '播放'}</button>}>
      <div className="cli-canvas">
        <div className="cli-workspace-title"><TerminalWindow size={17}/><strong>ForFlow CLI</strong><span>/</span><span>Q2Q Runner</span></div>
        <div className="cli-entry-points" aria-label="选择命令使用位置">{entryPoints.map(([Icon, title], i) => <button key={title} aria-pressed={entry === i} onClick={() => { setEntry(i); setDetails(false); setShowCommand(false); setCopied(''); film.seek(0, !film.reduced); }}><Icon size={21}/>{title}</button>)}</div>
        <article className="cli-terminal" aria-label="CLI 命令与执行过程">
          <header><span className="cli-window-dots"><i/><i/><i/></span><div><strong>ForFlow CLI</strong><small>Q2Q Runner</small></div><span>{entryPoints[entry][1]}</span></header>
          <div className="cli-terminal-body"><div className="cli-filebar"><span><TerminalWindow size={13}/>q2q_case_runner.py</span><span title="命令使用位置">{['项目目录','开发工具终端','自动化步骤'][entry]}</span></div><div className="cli-command-area"><span className="cli-line-numbers" aria-hidden="true">1<br/>2<br/>3</span><span className="cli-prompt">$</span><pre ref={commandText} aria-label="核验命令"><code>{partial || '\u00a0'}{!showCommand && film.playing && film.time < 5900 && <i className="cli-caret"/>}</code></pre><button onClick={copy} aria-label="复制 CLI 命令" title="复制完整命令">{copied === '完整命令已复制' ? <Check size={16}/> : <Copy size={16}/>}</button></div>
            <div className="cli-run-log">{logSteps.map((text, i) => { const done = film.time >= 7900 + i * 2800; return <div key={text} className={done ? 'is-done' : 'is-waiting'}><span>{done ? <Check size={12}/> : <i/>}</span><div>{text}<small>{['transport-case.json', 'case → evidence → decision', 'result.json'][i]}</small></div>{done && <span className="cli-log-time">{['01','02','03'][i]}</span>}</div>; })}</div>
            <div className={`cli-output ${complete ? 'is-ready' : ''}`}><span>›</span>{complete ? '结果已保存至 result.json' : chapter === 0 ? '等待执行' : '正在执行核验'}<span className="cli-output-dot"/></div>
          </div>
          {copied && <div className="cli-copy-status" role="status">{copied}</div>}
        </article>
        <article className={`cli-result ${complete ? 'is-ready' : ''}`} aria-label="CLI 运行结果">
          <header><FileText size={20}/><span>Q2Q <i>/</i> 核验结果</span><span className="cli-result-status">{complete ? '已生成' : '待生成'}</span></header><DetailTabs value={details?'evidence':'result'} onChange={value=>{film.pause();setDetails(value==='evidence');if(value==='evidence')film.seek(duration)}} items={[['result','结果概览'],['evidence','核验依据']]} label="CLI 结果视图"/>
          {details ? <div className="cli-evidence-detail"><h3>本次运行的核验依据</h3>{[['任务与输入','transport-case.json'],['当前判断','投入条件 / 生产边界 / 业务价值'],['复核事项','等待补证与业务复核']].map(([title, body]) => <div key={title}><LinkSimple size={15}/><span><strong>{title}</strong><small>{body}</small></span><Check size={13}/></div>)}</div> : <>
            <h3>运输单据一致性核验</h3>
            <div className="cli-result-rows">{[[CheckCircle, '试点准备','可进入受控试点'],[WarningCircle,'生产执行','等待业务与风险复核'],[FileText,'价值验证','需要补充验证材料']].map(([Icon,title,status],i) => <div key={title}><Icon className={complete ? `result-state-${i}` : ''} size={17}/><strong>{title}</strong><span>{complete ? status : '等待核验'}</span></div>)}</div>

            <button className="cli-details-link" onClick={() => { film.seek(duration); setDetails(true); }}>查看核验依据<ArrowRight size={14}/></button>
          </>}
        </article>
        <div className="cli-workspace-status"><span><i/>{complete ? '运行完成' : chapter === 0 ? '准备运行' : '正在核验'}</span></div>
        <div className={film.time < 6000 ? 'cli-pointer-input' : 'cli-pointer-result'}><FilmCursor x={film.time < 6000 ? 514 : 810} y={film.time < 6000 ? 193 : 481} name="工程师" visible={film.playing && !film.reduced && ((film.time > 500 && film.time < 2300) || film.time > 15500)} click={film.time > 18500 && film.time <19000}/></div>
      </div>
    </ShowcaseViewport>
    <FilmControls film={film} chapter={chapter} chapters={chapters} duration={duration} name="CLI 工作过程"></FilmControls>
  </section>;
}
