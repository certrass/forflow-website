// Public presentation fixtures, informed by the Q2Q transport audit schema.
// These are illustrative records, not customer data or production results.
export const workItems = [
  {id:'CU-01', name:'运输审计表单预填', method:'文档理解', status:'候选', action:'生成字段草稿'},
  {id:'CU-02', name:'主体、司机与车辆匹配', method:'规则核对', status:'候选', action:'核对跨系统信息'},
  {id:'CU-03', name:'跨单据一致性核验', method:'规则 + 人工复核', status:'当前选定', action:'查看核验依据'},
  {id:'CU-04', name:'运输事件链重建', method:'事件分析', status:'后续探索', action:'补充事件来源'},
  {id:'CU-05', name:'费用与重复结算核验', method:'规则核对', status:'候选', action:'确认费用范围'},
  {id:'CU-06', name:'异常材料与审核路由', method:'工作流协同', status:'候选', action:'明确复核责任'},
];
export const evidenceItems = [
  {id:'EV-01',name:'运输合同与费率',type:'合同',version:'v1.0',status:'已关联',owner:'合同负责人',source:'运输合同 · 第三条',quote:'运费按双方确认的线路、计费单位与费率版本核对。临时附加费用需单独确认。',use:'核对合同主体、计费方式和费率版本。',boundary:'临时附加费不沿用基础费率的结论。'},
  {id:'EV-02',name:'运单字段快照',type:'业务记录',version:'v1.0',status:'已关联',owner:'运输负责人',source:'运单 · 主体与车辆字段',quote:'运输单据保留发运方、收货方、车辆与货物明细，并关联同一笔运输业务。',use:'对照合同主体、车辆信息和货物记录。',boundary:'来源字段缺失时进入补充材料队列。'},
  {id:'EV-03',name:'签收凭证',type:'单据',version:'v1.0',status:'待复核',owner:'业务复核人',source:'签收单 · 货物明细',quote:'签收数量与运单数量存在一处待核对项，请业务人员确认是否为分批签收。',use:'检查签收信息与运单是否一致。',boundary:'有差异的字段保留待复核状态。'},
  {id:'EV-04',name:'运输事件记录',type:'事件',version:'v1.0',status:'已关联',owner:'系统负责人',source:'运输事件 · 发运与到达',quote:'按运输单号关联发运、在途与到达事件，保留各事件的来源及时间。',use:'定位运输时间链中的缺口。',boundary:'缺少的事件不能由推测补成事实。'},
  {id:'EV-05',name:'结算发票',type:'单据',version:'v1.0',status:'待复核',owner:'结算负责人',source:'发票 · 附加费明细',quote:'基础运费与附加费分项列示。附加费的发生原因与适用条款尚待确认。',use:'核对金额、费用类型与重复结算风险。',boundary:'核验结果供复核使用，付款由业务负责人决定。'},
  {id:'EV-06',name:'结算历史快照',type:'业务记录',version:'v1.0',status:'已关联',owner:'结算负责人',source:'结算记录 · 单据关联',quote:'通过发票标识、运输单号与结算记录建立关联，检查同一单据是否重复出现。',use:'对照本次单据与既有结算记录。',boundary:'结论只覆盖当前关联的记录范围。'},
];
export const reusableAssets = [
  {name:'运输核验任务定义',type:'业务上下文',version:'v1.0',note:'业务目标、处理范围与责任角色'},
  {name:'跨单据核验规则',type:'处理规则',version:'v1.0',note:'主体、车辆、货物与费用匹配条件'},
  {name:'运输单据字段蓝图',type:'文档处理',version:'v1.0',note:'字段定义、原文引用与复核位置'},
  {name:'运输核验评估样本',type:'评估资料',version:'v1.0',note:'开发、验收与保留样本分别管理'},
];
