/* ============================================================
   FORFLOW H5 — 交互流程
   流程：封面 → Q0 → Q0.5 → Q1..Q18 → 过场 → 结果 → CTA
   ============================================================ */

// 题目序列：Q0、Q0.5 单独 6 选项；主题题 4 选项
const SEQUENCE = [
  { kind:"intro", data:Q0 },
  { kind:"intro", data:Q05 },
  ...ALL_QUESTIONS.map(q => ({ kind:"main", data:q })),
];
const TOTAL = SEQUENCE.length;
const PROJECT_KEY = "forflow_personal_mbti";
const ANALYTICS_ENDPOINT = "/api/persona-mbti";
const STORAGE_PREFIX = "forflow-personal-mbti";
const VISITOR_KEY = `${STORAGE_PREFIX}-visitor-id`;
const EVENT_QUEUE_KEY = `${STORAGE_PREFIX}-event-queue`;
const RESULT_QUEUE_KEY = `${STORAGE_PREFIX}-result-queue`;
const ALGORITHM_VERSION = "forflow_persona_mbti_v1";
const pageOpenedAt = new Date().toISOString();
const pageOpenedAtMs = Date.now();

const state = {
  idx: 0,
  sub: emptySub(),
  answers: [],   // 每题选中的答案详情（用于回退时扣除）
  answerRevisions: {},
  eventSeq: 0,
  started_at: pageOpenedAt,
  started_at_ms: pageOpenedAtMs,
  completed_at: "",
  fill_duration_sec: null,
  completed: false,
};

function nowIso(){ return new Date().toISOString(); }
function elapsed(){
  const started = Number(state.started_at_ms) || pageOpenedAtMs;
  return Math.max(0, Math.round((Date.now() - started) / 1000));
}
function createId(prefix){
  const date = new Date();
  const ymd = [
    date.getFullYear(),
    String(date.getMonth() + 1).padStart(2, "0"),
    String(date.getDate()).padStart(2, "0")
  ].join("");
  let suffix = Math.random().toString(36).slice(2, 8);
  try {
    const bytes = new Uint8Array(4);
    crypto.getRandomValues(bytes);
    suffix = [...bytes].map(byte => byte.toString(36).padStart(2, "0")).join("").slice(0, 6);
  } catch (_) {}
  return `${prefix}-${ymd}-${suffix.toUpperCase()}`;
}
function persistentValue(key, fallback){
  try {
    const existing = localStorage.getItem(key);
    if (existing) return existing;
    localStorage.setItem(key, fallback);
  } catch (_) {}
  return fallback;
}
const visitorId = persistentValue(VISITOR_KEY, createId("VISITOR"));
const sessionId = createId("SES");
const visitId = createId("VISIT");
let assessmentId = createId("FFP");
function refreshAssessmentId(){
  assessmentId = createId("FFP");
  return assessmentId;
}

// DOM
const $ = id => document.getElementById(id);
const screens = {
  cover:   $("screen-cover"),
  quiz:    $("screen-quiz"),
  loading: $("screen-loading"),
  result:  $("screen-result"),
};
function show(name){
  for (const k in screens) screens[k].hidden = (k !== name);
  $("progressWrap").hidden = (name !== "quiz");
  window.scrollTo(0,0);
  const step = name === "quiz" ? state.idx + 1 : Math.min(state.idx + 1, TOTAL);
  track("screen_view", { screen:name, step, total_steps:TOTAL });
}

function persistQueue(key, payload, max){
  try {
    const queue = JSON.parse(localStorage.getItem(key) || "[]");
    queue.push(payload);
    localStorage.setItem(key, JSON.stringify(queue.slice(-max)));
  } catch (_) {}
}
async function postAnalyticsPayload(payload, keepalive = false){
  const options = {
    method:"POST",
    headers:{ "Content-Type":"application/json", Accept:"application/json" },
    body:JSON.stringify(payload)
  };
  if (keepalive) options.keepalive = true;
  const response = await fetch(ANALYTICS_ENDPOINT, options);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response;
}
async function flushQueue(key, maxBatch = 20){
  let queue = [];
  try { queue = JSON.parse(localStorage.getItem(key) || "[]"); } catch (_) {}
  if (!Array.isArray(queue) || !queue.length) return;

  const remaining = [...queue];
  for (let i = 0; i < Math.min(maxBatch, queue.length); i++) {
    const payload = remaining[0];
    try {
      await postAnalyticsPayload(payload, false);
      remaining.shift();
      localStorage.setItem(key, JSON.stringify(remaining));
    } catch (_) {
      break;
    }
  }
}
function flushQueues(){
  flushQueue(EVENT_QUEUE_KEY);
  flushQueue(RESULT_QUEUE_KEY);
}
function basePayload(){
  const params = new URLSearchParams(location.search);
  return {
    project_key: PROJECT_KEY,
    visitor_id: visitorId,
    session_id: sessionId,
    visit_id: visitId,
    assessment_id: assessmentId,
    page_opened_at: pageOpenedAt,
    page_path: location.pathname || "/",
    page_query: location.search,
    page_url: location.href,
    page_title: document.title,
    referrer: document.referrer || "",
    utm_source: params.get("utm_source") || "",
    utm_medium: params.get("utm_medium") || "",
    utm_campaign: params.get("utm_campaign") || "",
    utm_content: params.get("utm_content") || "",
    utm_term: params.get("utm_term") || "",
    source: params.get("utm_source") || params.get("source") || "",
    medium: params.get("utm_medium") || "",
    campaign: params.get("utm_campaign") || "",
    channel: params.get("channel") || "",
    cohort: params.get("cohort") || "",
    started_at: state.started_at || pageOpenedAt,
    completed_at: state.completed_at || "",
    elapsed_sec: elapsed(),
    fill_duration_sec: Number.isFinite(Number(state.fill_duration_sec)) ? Number(state.fill_duration_sec) : null,
    user_agent_family: navigator.userAgentData?.platform || navigator.platform || "",
    client_time_zone: Intl.DateTimeFormat().resolvedOptions().timeZone || "",
    language: navigator.language || "",
    viewport_width: window.innerWidth,
    viewport_height: window.innerHeight,
    screen_width: window.screen?.width || null,
    screen_height: window.screen?.height || null
  };
}
function sendBeaconPayload(payload){
  if (!navigator.sendBeacon) return false;
  try {
    const blob = new Blob([JSON.stringify(payload)], { type:"application/json" });
    return navigator.sendBeacon(ANALYTICS_ENDPOINT, blob);
  } catch (_) {
    return false;
  }
}
function submitEvent(payload, options = {}){
  const eventPayload = { kind:"event", ...payload };
  if (options.keepalive && sendBeaconPayload(eventPayload)) return;
  postAnalyticsPayload(eventPayload, Boolean(options.keepalive))
    .catch(() => persistQueue(EVENT_QUEUE_KEY, { kind:"event", ...payload }, 200));
}
function track(name, props = {}, options = {}){
  state.eventSeq += 1;
  const payload = {
    event_id:createId("EVT"),
    event_seq:state.eventSeq,
    event:`persona_${name}`,
    event_name:name,
    event_at:nowIso(),
    timestamp:nowIso(),
    ...basePayload(),
    ...props
  };
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push(payload);
  window.dispatchEvent(new CustomEvent("forflow-persona:track", { detail:payload }));
  submitEvent(payload, options);
  return payload;
}
window.forflowPersonaTrack = track;

function resetAssessment(options = {}){
  if (options.newAssessmentId !== false) refreshAssessmentId();
  state.idx = 0;
  state.sub = emptySub();
  state.answers = [];
  state.answerRevisions = {};
  state.started_at = nowIso();
  state.started_at_ms = Date.now();
  state.completed_at = "";
  state.fill_duration_sec = null;
  state.completed = false;
  delete state.resultSubmittedAt;
}

// ---------- 启动 ----------
$("startBtn").addEventListener("click", () => {
  resetAssessment({ newAssessmentId:false });
  track("start_click", { screen:"cover", cta_key:"start", cta_text:$("startBtn").textContent.trim() });
  show("quiz");
  renderQuestion();
});

// ---------- 进度 ----------
function updateProgress(){
  const pct = ((state.idx) / TOTAL) * 100;
  $("progressBar").style.width = Math.max(5, pct) + "%";
  $("progressText").textContent = (state.idx + 1) + " / " + TOTAL;
}

// ---------- 渲染题目 ----------
function renderQuestion(){
  updateProgress();
  const step = SEQUENCE[state.idx];
  const q = step.data;
  const stage = $("qStage");
  const qid = questionId(step, q);

  let title, sub, tag, opts;
  if (step.kind === "intro"){
    title = q.title.replace(/^Q[\d.]+｜?/, "");
    sub = q.sub || "";
    tag = q.title.startsWith("Q0.5") ? "暖场 · 02" : "暖场 · 01";
    opts = q.options;
  } else {
    const mainNum = state.idx - 1; // Q0,Q0.5 占前两位
    title = q.title;
    sub = "";
    tag = "第 " + mainNum + " 题 / 18";
    opts = q.options;
  }

  let optsHTML = opts.map((o, index) => `
    <button class="option" data-key="${o.key}" data-option-index="${index + 1}">
      <span class="opt-key">${o.key}</span>
      <span class="opt-label">${o.label}</span>
      ${o.desc ? `<span class="opt-desc">${o.desc}</span>` : ""}
    </button>
  `).join("");

  stage.innerHTML = `
    <div class="q-head">
      <span class="q-tag">${tag}</span>
      <h2 class="q-title">${title}</h2>
      ${sub ? `<p class="q-sub">${sub}</p>` : ""}
    </div>
    <div class="options">${optsHTML}</div>
    <div class="q-foot">
      <button class="q-back" id="backBtn" ${state.idx === 0 ? "disabled" : ""}>← 上一题</button>
    </div>
  `;
  stage.style.animation = "none";
  void stage.offsetWidth;
  stage.style.animation = "fadeUp .4s both";

  let answered = false;
  stage.querySelectorAll(".option").forEach(btn => {
    btn.addEventListener("click", () => {
      if (answered) return;
      answered = true;
      stage.querySelectorAll(".option").forEach(option => option.disabled = true);
      const key = btn.dataset.key;
      const opt = opts.find(o => o.key === key);
      const optionIndex = Number(btn.dataset.optionIndex);
      const answerRevision = (state.answerRevisions[qid] || 0) + 1;
      const answerId = createId("ANS");
      state.answerRevisions[qid] = answerRevision;
      btn.classList.add("selected");
      // 记录并加分
      state.answers[state.idx] = {
        answer_id:answerId,
        answer_revision:answerRevision,
        step:state.idx + 1,
        question_id:qid,
        question_title:q.title,
        question_kind:step.kind,
        question_option_count:opts.length,
        answer_key:key,
        answer_label:opt.label,
        answer_desc:opt.desc || "",
        answer_option_index:optionIndex,
        selected_option_indices:[optionIndex],
        selected_option_labels:[opt.label],
        selected_values:[key],
        score:{ ...opt.score },
        answered_at:nowIso(),
        elapsed_sec:elapsed()
      };
      addScore(state.sub, opt.score);
      track("answer_select", {
        screen:"quiz",
        answer_id:answerId,
        answer_revision:answerRevision,
        step:state.idx + 1,
        question_id:qid,
        question_title:q.title,
        question_kind:step.kind,
        question_option_count:opts.length,
        answer_key:key,
        answer_label:opt.label,
        answer_option_index:optionIndex,
        selected_option_indices:[optionIndex],
        selected_option_labels:[opt.label],
        selected_values:[key],
        score_json:JSON.stringify(opt.score)
      });
      setTimeout(advance, 230);
    });
  });

  $("backBtn").addEventListener("click", goBack);
  track("question_view", { screen:"quiz", step:state.idx + 1, question_id:qid, question_title:q.title, question_kind:step.kind, question_option_count:opts.length });
}

function questionId(step, q){
  if (step.kind === "intro") return q.title.startsWith("Q0.5") ? "Q0_5" : "Q0";
  return q.id || `Q${state.idx - 1}`;
}
function answerRows(){
  return state.answers.filter(Boolean).map(item => ({
    answer_id:item.answer_id,
    answer_revision:item.answer_revision,
    step:item.step,
    question_id:item.question_id,
    question_title:item.question_title,
    question_kind:item.question_kind,
    question_option_count:item.question_option_count,
    answer_key:item.answer_key,
    answer_label:item.answer_label,
    answer_desc:item.answer_desc,
    answer_option_index:item.answer_option_index,
    selected_option_indices:item.selected_option_indices,
    selected_option_labels:item.selected_option_labels,
    selected_values:item.selected_values,
    score:item.score,
    answered_at:item.answered_at,
    elapsed_sec:item.elapsed_sec
  }));
}
function answerQuality(result = {}){
  const rows = answerRows();
  const total = rows.length || 1;
  const counts = {};
  rows.forEach(row => {
    const key = String(row.answer_option_index || row.answer_key || "");
    counts[key] = (counts[key] || 0) + 1;
  });
  const maxCount = Math.max(0, ...Object.values(counts));
  const maxOptionRatio = maxCount / total;
  const entropy = -Object.values(counts).reduce((sum, count) => {
    const p = count / total;
    return sum + (p ? p * Math.log2(p) : 0);
  }, 0);
  const flags = [];
  const duration = Number(result.fill_duration_sec ?? state.fill_duration_sec ?? elapsed());

  if (duration > 0 && duration < 35) flags.push("very_fast_completion");
  else if (duration > 0 && duration < 60) flags.push("fast_completion");
  if (maxOptionRatio >= 0.85) flags.push("single_position_path");
  else if (maxOptionRatio >= 0.7) flags.push("low_answer_variety");
  if (rows.length < TOTAL) flags.push("incomplete_answers");

  return {
    quality_flag:flags.join(",") || "ok",
    quality_flags:flags,
    answer_count:rows.length,
    max_option_ratio:Number(maxOptionRatio.toFixed(3)),
    answer_entropy:Number(entropy.toFixed(3)),
    duration_sec:duration
  };
}

function advance(){
  state.idx++;
  if (state.idx >= TOTAL){
    runLoadingThenResult();
  } else {
    renderQuestion();
  }
}

function goBack(){
  if (state.idx === 0) return;
  state.idx--;
  // 撤销上一题加分
  const prevAnswer = state.answers[state.idx];
  const prevScore = prevAnswer?.score;
  if (prevScore){
    for (const k in prevScore) state.sub[k] -= prevScore[k];
    state.answers[state.idx] = null;
  }
  track("step_back", {
    screen:"quiz",
    from_step:state.idx + 2,
    to_step:state.idx + 1,
    removed_answer_id:prevAnswer?.answer_id || "",
    removed_question_id:prevAnswer?.question_id || "",
    removed_answer_option_index:prevAnswer?.answer_option_index || null
  });
  renderQuestion();
}

// ---------- 过场 ----------
function runLoadingThenResult(){
  state.completed = true;
  state.completed_at = nowIso();
  state.fill_duration_sec = elapsed();
  track("quiz_complete", { screen:"loading", answer_count:answerRows().length, fill_duration_sec:state.fill_duration_sec });
  $("progressBar").style.width = "100%";
  $("progressText").textContent = TOTAL + " / " + TOTAL;
  $("loaderText").textContent = LOADING_LINES[Math.floor(Math.random()*LOADING_LINES.length)];
  show("loading");
  let t = 0;
  const swap = setInterval(() => {
    $("loaderText").textContent = LOADING_LINES[Math.floor(Math.random()*LOADING_LINES.length)];
    t++;
    if (t >= 2){ clearInterval(swap); renderResult(); }
  }, 950);
}

// ---------- 结果 ----------
const THEME = {
  CtrlT:"A", F4:"A", CtrlCV:"A",
  AltF4:"B", Tab:"B", Shift:"B",
  CtrlAltDel:"C", CtrlZ:"C", Esc:"C",
  CapsLock:"D", Fn:"D",
  CtrlS:"E", CtrlZY:"E",
  CtrlW:"F",
  HIDDEN:"H",
};

function stars(n){ return "⚠️".repeat(n); }

function renderResult(){
  const code = classify(state.sub);
  const p = PERSONAS[code];
  const theme = THEME[code] || "A";
  const result = {
    result_id:createId("RES"),
    algorithm_version:ALGORITHM_VERSION,
    project_key:PROJECT_KEY,
    visitor_id:visitorId,
    visit_id:visitId,
    assessment_id:assessmentId,
    session_id:sessionId,
    persona_code:code,
    persona_name:p.name,
    persona_class:p.cls,
    persona_quote:p.quote,
    persona_review:p.review,
    persona_advice:p.advice || "",
    persona_theme:theme,
    risk:p.risk,
    risk_text:p.riskText,
    hidden:Boolean(p.hidden),
    started_at:state.started_at,
    completed_at:state.completed_at || nowIso(),
    fill_duration_sec:Number.isFinite(Number(state.fill_duration_sec)) ? Number(state.fill_duration_sec) : elapsed(),
    sub_scores:{ ...state.sub },
    module_scores:moduleScores(floorNeg(state.sub)),
    answers_indexed:answerRows()
  };
  const quality = answerQuality(result);
  result.quality = quality;
  result.quality_flag = quality.quality_flag;
  result.quality_flags = quality.quality_flags;
  window.__forflowPersonaResult = result;

  let html = `
    <div class="result-card">
      <div class="rc-top theme-${theme}">
        <div class="rc-label">你的 AI 职场人格是</div>
        <div class="rc-emoji">${p.emoji}</div>
        <h2 class="rc-name">${p.name}</h2>
        <span class="rc-cls">${p.cls}</span>
      </div>
      <div class="rc-body">
        <p class="rc-quote">“${p.quote}”</p>

        <div class="rc-block b-review">
          <p class="rc-bt"><span class="rc-ic">🔪</span>AI 锐评</p>
          <p class="rc-btext">${p.review}</p>
        </div>

        <div class="rc-block b-risk">
          <p class="rc-bt"><span class="rc-ic">⚠️</span>被 AI 替代风险</p>
          <div class="risk-row">
            <span class="risk-stars">${stars(p.risk)}</span>
            <span class="risk-text">${p.riskText}</span>
          </div>
        </div>

        ${p.advice ? `
        <div class="rc-block b-advice">
          <p class="rc-bt"><span class="rc-ic">🚀</span>翻盘建议</p>
          <p class="rc-btext">${p.advice}</p>
        </div>` : ""}
      </div>
  `;

  if (p.hidden){
    html += `
      <div class="egg">
        <p class="egg-title">🎁 隐藏款 · 展会现场限定</p>
        <p class="egg-text">${p.egg}</p>
        <span class="rare-badge">稀有度 < 2% · 100 人里挑不出 2 个</span>
      </div>`;
  }

  html += `
      <div class="cta">
        <p class="cta-kicker">FORFLOW NEXT</p>
        <p class="cta-h">你的饭碗诊断书已出炉</p>
        <p class="cta-p">关注公众号，领取保饭碗指南和后续 AI 转型材料。</p>

        <button class="qr-box" id="qrCta" type="button" aria-label="关注万维流形公众号二维码">
          <img class="qr-img qr-img--personal" src="qr-forflow-personal.png" alt="万维流形公众号二维码" />
          <p class="qr-name">关注公众号 <b>万维流形</b></p>
          <p class="qr-sub">长按识别二维码，领取保饭碗指南</p>
        </button>

        <div class="cta-extra">
          <p class="cta-extra-tag">👆 这个二维码是真的可以扫的。</p>
          <p class="cta-extra-sub">测评只是入口，真正值钱的是下一步怎么升级。</p>
        </div>
      </div>

      <div class="share-row">
        <button class="share-btn share-btn--full" id="shareSelf">独乐乐不如众破防。测测谁先被 AI 优化 →</button>
      </div>

      <button class="retry" id="retryBtn">结果太准了受不了，重测一个不准的 →</button>
      <button class="diagnosis-id" id="diagnosisId" type="button" aria-label="复制测试编号">测试编号 ${result.assessment_id}</button>
    </div>
  `;

  $("resultInner").innerHTML = html;
  show("result");
  track("result_view", {
    screen:"result",
    persona_code:code,
    persona_name:p.name,
    persona_class:p.cls,
    risk:p.risk,
    risk_text:p.riskText,
    hidden:Boolean(p.hidden),
    fill_duration_sec:result.fill_duration_sec,
    quality_flag:result.quality_flag,
    quality_flags:result.quality_flags,
    answer_entropy:quality.answer_entropy,
    max_option_ratio:quality.max_option_ratio
  });
  submitResult(result);

  $("retryBtn").addEventListener("click", () => {
    track("retry_click", { screen:"result", cta_key:"retry", cta_text:$("retryBtn").textContent.trim(), persona_code:code });
    resetAssessment();
    show("cover");
  });
  $("qrCta").addEventListener("click", () => {
    track("qr_click", { screen:"result", cta_key:"qr_follow", cta_text:"关注公众号 万维流形", persona_code:code });
    toast("长按二维码识别");
  });
  $("diagnosisId").addEventListener("click", () => {
    track("diagnosis_id_copy", { screen:"result", cta_key:"diagnosis_id", cta_text:result.assessment_id, persona_code:code });
    copyText(result.assessment_id, "测试编号已复制");
  });
  const copyLink = () => {
    const url = new URL(location.pathname || "/", location.origin).toString();
    track("share_click", { screen:"result", cta_key:"share_test", cta_text:$("shareSelf").textContent.trim(), cta_href:url, persona_code:code });
    copyText(url, "测试链接已复制");
  };
  $("shareSelf").addEventListener("click", copyLink);
}

async function submitResult(result){
  if (!result || state.resultSubmittedAt) return;
  const payload = {
    ...basePayload(),
    kind:"result",
    result_id:result.result_id,
    submitted_at:nowIso(),
    algorithm_version:ALGORITHM_VERSION,
    persona_code:result.persona_code,
    persona_name:result.persona_name,
    persona_class:result.persona_class,
    persona_theme:result.persona_theme,
    risk:result.risk,
    risk_text:result.risk_text,
    hidden:result.hidden,
    quality_flag:result.quality_flag,
    quality_flags:result.quality_flags,
    answer_entropy:result.quality?.answer_entropy,
    max_option_ratio:result.quality?.max_option_ratio,
    sub_scores:result.sub_scores,
    module_scores:result.module_scores,
    answers_indexed:result.answers_indexed,
    result
  };
  try {
    await postAnalyticsPayload(payload, false);
    state.resultSubmittedAt = payload.submitted_at;
    track("result_submit_ok", { screen:"result", persona_code:result.persona_code, persona_name:result.persona_name });
  } catch (error) {
    persistQueue(RESULT_QUEUE_KEY, payload, 80);
    track("result_submit_failed", { screen:"result", persona_code:result.persona_code, reason:error?.message || "unknown" });
  }
}

// ---------- 复制降级方案 ----------
function copyText(text, successMessage){
  if (navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(text).then(()=>toast(successMessage)).catch(()=>fallbackCopy(text, successMessage));
  } else {
    fallbackCopy(text, successMessage);
  }
}
function fallbackCopy(text, successMessage = "已复制"){
  try{
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.style.position = "fixed"; ta.style.opacity = "0";
    document.body.appendChild(ta);
    ta.focus(); ta.select();
    document.execCommand("copy");
    document.body.removeChild(ta);
    toast(successMessage);
  }catch(e){
    toast(successMessage);
  }
}

// ---------- toast ----------
let toastTimer;
function toast(msg){
  let el = document.querySelector(".toast");
  if (!el){ el = document.createElement("div"); el.className = "toast"; document.body.appendChild(el); }
  el.textContent = msg;
  el.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(()=>el.classList.remove("show"), 2200);
}

track("page_view", { screen:"cover", referrer:document.referrer || "" });
setTimeout(flushQueues, 1200);
window.addEventListener("beforeunload", () => {
  if (!state.completed && state.idx > 0) {
    track("quiz_abandon", { screen:"quiz", step:state.idx + 1, answer_count:answerRows().length }, { keepalive:true });
  }
});
