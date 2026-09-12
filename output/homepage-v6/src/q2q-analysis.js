export function analysisFor(r){
 const kind=r.originalKind;
 if(kind==='quantity')return {title:`签收数量比发运少 ${r.shipped-r.received} 箱`,finding:`运单记录 ${r.shipped} 箱，签收回执记录 ${r.received} 箱。同一运单的数量不一致。`,caution:'现有材料不能确定差异原因，需要运输负责人进一步核实。',action:'确认实收数量，保留差异并交给运输负责人跟进。',draft:`已对照运单和签收回执，确认实收 ${r.received} 箱。${r.shipped-r.received} 箱差异由运输负责人继续核实。`,task:`核实 ${r.shipped-r.received} 箱签收差异`,owner:'transport'};
 if(kind==='missing')return {title:'缺少签收依据',finding:'已找到运单，尚未关联与本次运输对应的签收回执。',caution:'缺少实收记录，暂不能确认货物已完整签收。',action:'请运输负责人补充签收凭证，再继续核验。',draft:'当前缺少有效签收凭证，已交运输负责人补齐材料后继续核验。',task:'补充有效签收凭证',owner:'transport'};
 if(kind==='fee')return {title:'附加费用缺少确认依据',finding:'合同基础运费 1,480 元，结算金额 1,560 元，存在 80 元附加费。',caution:'当前材料未说明附加费用的发生原因及确认记录。',action:'由结算负责人核实附加费明细及发生依据。',draft:'已核对基础运费，80 元附加费交结算负责人补充发生依据。',task:'核实 80 元附加费',owner:'finance'};
 if(kind==='identity')return {title:'收货主体名称不一致',finding:'运单收货方与回执签收方名称不同，需要核对授权签收关系。',caution:'名称差异不能直接推定为错误签收。',action:'请业务复核人确认收货主体与授权关系。',draft:'已识别收货主体名称差异，待核对授权签收关系。',task:'核对授权签收关系',owner:'review'};
 return {title:'关键数量字段一致',finding:`运单与签收均记录 ${r.received} 箱，运输单号已对应。`,caution:'结论对应当前关联材料及规则版本。',action:'保留核验结论与材料版本。',draft:'已核对运输单号与货物数量，当前字段一致。',task:'复查当前核验记录',owner:'review'};
}

