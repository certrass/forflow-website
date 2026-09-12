import React from 'react';
import {FileText} from '@phosphor-icons/react';
import {owners,statusNames} from './q2q-records.js';
export function Avatar({id,small=false}){const owner=owners.find(o=>o.id===id)||owners[0];return <span className={`wq-avatar ${owner.color} ${small?'small':''}`} title={owner.name}>{owner.initial}</span>}
export function Status({record}){return <span className={`wq-status ${record.reviewed?'complete':record.kind}`}><i/>{record.reviewed?'已复核':statusNames[record.kind]}</span>}
export function FileIcon({type='PDF'}){return <span className={`wq-file-icon ${type.toLowerCase()}`}><FileText size={16}/></span>}
export function containDialogFocus(event){
 if(event.key!=='Tab')return;
 const nodes=[...event.currentTarget.querySelectorAll('button,input,textarea,select,[tabindex="0"]')].filter(n=>!n.disabled&&n.getClientRects().length);
 if(!nodes.length)return;
 if(event.shiftKey&&document.activeElement===nodes[0]){event.preventDefault();nodes.at(-1).focus()}
 else if(!event.shiftKey&&document.activeElement===nodes.at(-1)){event.preventDefault();nodes[0].focus()}
 event.stopPropagation();
}
