// Authored public records, using Q2Q's per-ticket object/evidence relationships.
export const owners=[{id:'review',name:'业务复核人',initial:'复',color:'blue'},{id:'transport',name:'运输负责人',initial:'运',color:'green'},{id:'finance',name:'结算负责人',initial:'结',color:'purple'}];
const rows=[
 [24,'苏州','上海','quantity',240,238,'review',5,4],
 [23,'杭州','南京','missing',160,null,'transport',18,3],
 [22,'无锡','合肥','fee',180,180,'finance',32,5],
 [21,'苏州','上海','complete',120,120,'review',60,4],
 [20,'杭州','南京','quantity',72,70,'transport',84,4],
 [19,'无锡','合肥','missing',96,null,'transport',120,2],
 [18,'苏州','上海','identity',48,48,'review',180,3],
 [17,'杭州','南京','complete',210,210,'finance',240,5],
 [16,'无锡','合肥','complete',144,144,'review',300,4],
 [15,'苏州','上海','complete',80,80,'transport',360,4],
 [14,'杭州','南京','complete',180,180,'finance',420,3],
 [13,'无锡','合肥','complete',120,120,'review',480,4],
];
export const initialRecords=rows.map(([number,from,to,kind,shipped,received,owner,minutes,files])=>({id:`T-260906-${String(number).padStart(3,'0')}`,number,from,to,kind,originalKind:kind,shipped,received,owner,minutes,files,reviewed:kind==='complete',reviewedBy:kind==='complete'?owner:null,requested:false,note:'',rule:'v1.2'}));
export const statusNames={quantity:'数量差异',missing:'待补签收',fee:'费用待核对',identity:'主体待核对',complete:'已复核'};
export const recordCategory=r=>r.reviewed?'complete':r.kind==='missing'?'missing':'review';
export const timeLabel=m=>m===0?'刚刚':m<60?`${m} 分钟前`:`${Math.floor(m/60)} 小时前`;
export const recordFiles=r=>[
 {id:'waybill',name:`运单_${String(r.number).padStart(3,'0')}.pdf`,type:'PDF',source:'运输管理系统',size:'1.24 MB',version:'v1.0'},
 ...(r.received!==null?[{id:'receipt',name:`签收回执_${String(r.number).padStart(3,'0')}.pdf`,type:'PDF',source:'仓储签收记录',size:'1.08 MB',version:'v1.0'}]:[]),
 {id:'contract',name:'华东线路_合同费率.xlsx',type:'XLSX',source:'合同管理台账',size:'86 KB',version:r.rule},
 {id:'invoice',name:`结算明细_${String(r.number).padStart(3,'0')}.xlsx`,type:'XLSX',source:'结算单据',size:'124 KB',version:'v1.0'},
 {id:'events',name:`运输事件_${String(r.number).padStart(3,'0')}.csv`,type:'CSV',source:'运输事件记录',size:'12 KB',version:'v1.0'},
].slice(0,r.files);
export const assetRecords=[
 {id:'AS-01',name:'跨单据一致性核验',type:'核验规则',version:'v1.2',status:'使用中',detail:'主体、货物、签收和费用按同一运单关联。',fields:['主体一致性','货物数量','签收凭证','费用与费率']},
 {id:'AS-02',name:'运输单据字段定义',type:'字段蓝图',version:'v1.1',status:'使用中',detail:'运单、签收单和结算单使用统一字段映射。',fields:['运输单号','发运与收货方','发运数量','签收数量']},
 {id:'AS-03',name:'数量差异复核流程',type:'工作流程',version:'v1.0',status:'使用中',detail:'保留差异与来源，将复核意见关联到当前记录。',fields:['关联来源','检查差异','分配负责人','保留复核意见']},
 {id:'AS-04',name:'运输核验评估资料',type:'评估资料',version:'v1.0',status:'已归档',detail:'按版本维护输入、预期判断和复核记录。',fields:['输入资料','预期结果','差异记录','版本比较']},
];
