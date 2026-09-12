import React from 'react';
import {ArrowCounterClockwise, Pause, Play} from '@phosphor-icons/react';
import {formatPlaybackTime} from './ScenePlayback.jsx';

export function FilmControls({film, chapters, chapter, duration, name, children}) {
  return <div className="film-controls">
    <div className="film-chapters" aria-label={`${name}播放章节`}>
      {chapters.map(([title, at], i) => <button key={title} aria-pressed={chapter === i} onClick={() => film.seek(at, !film.reduced)}>
        <span className="film-chapter-track"><i style={{width: `${i < chapter ? 100 : i > chapter ? 0 : Math.min(100, (film.time - at) / ((chapters[i + 1]?.[1] || duration) - at) * 100)}%`}}/></span>
        <span className="film-chapter-label"><small>0{i + 1}</small><strong>{title}</strong></span>
      </button>)}
    </div>
    <div className="film-transport">
      <span className="playback-time">{formatPlaybackTime(film.time)}<span> / {formatPlaybackTime(duration)}</span></span>
      <button onClick={film.toggle} title={film.playing?'暂停，查看当前内容':film.complete?'从头播放':'继续播放'} aria-label={`${film.playing ? '暂停' : film.complete ? '重新播放' : '播放'}${name}`} >{film.playing ? <Pause size={15} weight="fill"/> : film.complete ? <ArrowCounterClockwise size={16}/> : <Play size={15} weight="fill"/>}</button>
      <button onClick={film.replay} aria-label={`重播${name}`}><ArrowCounterClockwise size={17}/></button>
    </div>
    {children}
  </div>;
}

export function FilmCursor({x, y, visible, click, name = '业务复核人'}) {
  return <div className={`film-cursor ${visible ? 'is-visible' : ''} ${click ? 'is-clicking' : ''}`} style={{transform: `translate3d(${x}px, ${y}px, 0)`}} aria-hidden="true">
    <i/><svg width="25" height="31" viewBox="0 0 25 31"><path d="M3 2.5L21.5 19H12.8L8.5 26.5L3 2.5Z" fill="#426ce4" stroke="white" strokeWidth="1.7" strokeLinejoin="round"/></svg>
    <span>{name}</span>
  </div>;
}

export function Person({kind = 'review', small = false}) {
  return <span className={`film-person ${kind} ${small ? 'small' : ''}`} aria-hidden="true">{kind === 'review' ? '复' : kind === 'transport' ? '运' : '结'}</span>;
}
