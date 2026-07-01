import type { Config, Context } from "@netlify/functions";

type Payload = Record<string, any>;

declare const Netlify: {
  env: {
    get(name: string): string | undefined;
  };
};

const PROJECT_KEY = "forflow_personal_mbti";
const JSON_HEADERS = { "Content-Type": "application/json" };

function env(name: string): string {
  return (globalThis as any).Netlify?.env?.get(name) || process.env[name] || "";
}

function supabaseConfig() {
  const url = env("SUPABASE_URL") || env("SUPABASE_DATABASE_URL");
  const serviceRoleKey = env("SUPABASE_SERVICE_ROLE_KEY");
  if (!url || !serviceRoleKey) {
    throw new Error("Missing SUPABASE_URL/SUPABASE_DATABASE_URL or SUPABASE_SERVICE_ROLE_KEY");
  }
  return { url: url.replace(/\/$/, ""), serviceRoleKey };
}

function serverId(prefix: string): string {
  return `${prefix}-${crypto.randomUUID()}`;
}

function asIso(value: any): string | null {
  if (!value) return null;
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? null : date.toISOString();
}

function asNumber(value: any): number | null {
  if (value === "" || value === null || value === undefined) return null;
  const n = Number(value);
  return Number.isFinite(n) ? n : null;
}

function asBoolean(value: any): boolean | null {
  return typeof value === "boolean" ? value : null;
}

function asJson(value: any): any {
  if (value === undefined) return null;
  if (typeof value === "string") {
    try {
      return JSON.parse(value);
    } catch {
      return value;
    }
  }
  return value;
}

function beijingText(date: Date): string {
  const formatted = new Intl.DateTimeFormat("sv-SE", {
    timeZone: "Asia/Shanghai",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false
  }).format(date);
  return `${formatted.replace(" ", "T")}+08:00`;
}

function geoFromContext(context: Context): Payload | null {
  const geo = (context as any).geo;
  if (!geo) return null;
  return {
    city: geo.city || "",
    country_code: geo.country?.code || "",
    country_name: geo.country?.name || "",
    subdivision: geo.subdivision || "",
    timezone: geo.timezone || ""
  };
}

async function upsertRows(table: string, rows: Payload | Payload[], onConflict: string): Promise<void> {
  const { url, serviceRoleKey } = supabaseConfig();
  const response = await fetch(`${url}/rest/v1/${table}?on_conflict=${encodeURIComponent(onConflict)}`, {
    method: "POST",
    headers: {
      apikey: serviceRoleKey,
      Authorization: `Bearer ${serviceRoleKey}`,
      "Content-Type": "application/json",
      Prefer: "resolution=merge-duplicates,return=minimal"
    },
    body: JSON.stringify(rows)
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`Supabase ${table} ${response.status}: ${detail}`);
  }
}

function attribution(payload: Payload) {
  return {
    page_opened_at: asIso(payload.page_opened_at),
    page_url: payload.page_url || "",
    page_path: payload.page_path || "",
    page_query: payload.page_query || "",
    page_title: payload.page_title || "",
    referrer: payload.referrer || "",
    utm_source: payload.utm_source || "",
    utm_medium: payload.utm_medium || "",
    utm_campaign: payload.utm_campaign || "",
    utm_content: payload.utm_content || "",
    utm_term: payload.utm_term || "",
    source: payload.source || "",
    medium: payload.medium || "",
    campaign: payload.campaign || "",
    channel: payload.channel || "",
    cohort: payload.cohort || "",
    client_time_zone: payload.client_time_zone || "",
    language: payload.language || "",
    user_agent_family: payload.user_agent_family || "",
    viewport_width: asNumber(payload.viewport_width),
    viewport_height: asNumber(payload.viewport_height),
    screen_width: asNumber(payload.screen_width),
    screen_height: asNumber(payload.screen_height)
  };
}

function visitRow(payload: Payload, context: Context, receivedAt: Date): Payload {
  return {
    visit_id: payload.visit_id || serverId("VISIT"),
    project_key: payload.project_key || PROJECT_KEY,
    visitor_id: payload.visitor_id || "",
    session_id: payload.session_id || "",
    initial_assessment_id: payload.assessment_id || "",
    first_seen_at: asIso(payload.page_opened_at) || receivedAt.toISOString(),
    last_seen_at: receivedAt.toISOString(),
    ...attribution(payload),
    server_geo: geoFromContext(context),
    payload
  };
}

function eventRow(payload: Payload, context: Context, receivedAt: Date): Payload {
  return {
    event_id: payload.event_id || serverId("EVT"),
    project_key: payload.project_key || PROJECT_KEY,
    event_name: payload.event_name || payload.kind || "event",
    event: payload.event || "",
    event_seq: asNumber(payload.event_seq),
    event_at: asIso(payload.event_at || payload.timestamp),
    received_at: receivedAt.toISOString(),
    received_at_bj_text: beijingText(receivedAt),
    visitor_id: payload.visitor_id || "",
    session_id: payload.session_id || "",
    visit_id: payload.visit_id || null,
    assessment_id: payload.assessment_id || "",
    result_id: payload.result_id || "",
    answer_id: payload.answer_id || "",
    answer_revision: asNumber(payload.answer_revision),
    screen: payload.screen || "",
    step: asNumber(payload.step),
    from_step: asNumber(payload.from_step),
    to_step: asNumber(payload.to_step),
    question_id: payload.question_id || "",
    question_title: payload.question_title || "",
    question_kind: payload.question_kind || "",
    question_option_count: asNumber(payload.question_option_count),
    answer_key: payload.answer_key || "",
    answer_label: payload.answer_label || "",
    answer_desc: payload.answer_desc || "",
    answer_option_index: asNumber(payload.answer_option_index),
    selected_option_indices: asJson(payload.selected_option_indices),
    selected_option_labels: asJson(payload.selected_option_labels),
    selected_values: asJson(payload.selected_values),
    score_json: asJson(payload.score_json),
    cta_key: payload.cta_key || "",
    cta_text: payload.cta_text || "",
    cta_href: payload.cta_href || "",
    persona_code: payload.persona_code || "",
    persona_name: payload.persona_name || "",
    persona_class: payload.persona_class || "",
    risk: asNumber(payload.risk),
    risk_text: payload.risk_text || "",
    hidden: asBoolean(payload.hidden),
    quality_flag: payload.quality_flag || "",
    quality_flags: asJson(payload.quality_flags),
    answer_entropy: asNumber(payload.answer_entropy),
    max_option_ratio: asNumber(payload.max_option_ratio),
    elapsed_sec: asNumber(payload.elapsed_sec),
    fill_duration_sec: asNumber(payload.fill_duration_sec),
    ...attribution(payload),
    netlify_request_id: (context as any).requestId || "",
    server_geo: geoFromContext(context),
    payload
  };
}

function resultRow(payload: Payload, context: Context, receivedAt: Date): Payload {
  return {
    assessment_id: payload.assessment_id || serverId("FFP"),
    result_id: payload.result_id || payload.result?.result_id || serverId("RES"),
    project_key: payload.project_key || PROJECT_KEY,
    algorithm_version: payload.algorithm_version || "",
    visitor_id: payload.visitor_id || "",
    session_id: payload.session_id || "",
    visit_id: payload.visit_id || null,
    submitted_at: asIso(payload.submitted_at),
    received_at: receivedAt.toISOString(),
    received_at_bj_text: beijingText(receivedAt),
    started_at: asIso(payload.started_at),
    completed_at: asIso(payload.completed_at),
    fill_duration_sec: asNumber(payload.fill_duration_sec),
    persona_code: payload.persona_code || "",
    persona_name: payload.persona_name || "",
    persona_class: payload.persona_class || "",
    persona_theme: payload.persona_theme || "",
    risk: asNumber(payload.risk),
    risk_text: payload.risk_text || "",
    hidden: asBoolean(payload.hidden),
    quality_flag: payload.quality_flag || "",
    quality_flags: asJson(payload.quality_flags),
    answer_entropy: asNumber(payload.answer_entropy),
    max_option_ratio: asNumber(payload.max_option_ratio),
    sub_scores: asJson(payload.sub_scores),
    module_scores: asJson(payload.module_scores),
    answers_indexed: asJson(payload.answers_indexed),
    result_json: asJson(payload.result || {}),
    ...attribution(payload),
    netlify_request_id: (context as any).requestId || "",
    server_geo: geoFromContext(context),
    payload
  };
}

function answerRows(payload: Payload): Payload[] {
  const answers = Array.isArray(payload.answers_indexed) ? payload.answers_indexed : [];
  return answers.map((answer: Payload) => ({
    assessment_id: payload.assessment_id,
    visit_id: payload.visit_id || "",
    session_id: payload.session_id || "",
    visitor_id: payload.visitor_id || "",
    persona_code: payload.persona_code || "",
    quality_flag: payload.quality_flag || "",
    answer_id: answer.answer_id || "",
    answer_revision: asNumber(answer.answer_revision),
    step: asNumber(answer.step),
    question_id: answer.question_id || "",
    question_title: answer.question_title || "",
    question_kind: answer.question_kind || "",
    question_option_count: asNumber(answer.question_option_count),
    answer_key: answer.answer_key || "",
    answer_label: answer.answer_label || "",
    answer_desc: answer.answer_desc || "",
    answer_option_index: asNumber(answer.answer_option_index),
    selected_option_indices: asJson(answer.selected_option_indices),
    selected_option_labels: asJson(answer.selected_option_labels),
    selected_values: asJson(answer.selected_values),
    score: asJson(answer.score),
    answered_at: asIso(answer.answered_at),
    elapsed_sec: asNumber(answer.elapsed_sec),
    payload: answer
  })).filter(row => row.assessment_id && row.step && row.question_id);
}

export default async (req: Request, context: Context) => {
  if (req.method !== "POST") {
    return new Response(JSON.stringify({ ok: false, error: "Method not allowed" }), {
      status: 405,
      headers: JSON_HEADERS
    });
  }

  let payload: Payload;
  try {
    payload = await req.json();
  } catch {
    return new Response(JSON.stringify({ ok: false, error: "Invalid JSON" }), {
      status: 400,
      headers: JSON_HEADERS
    });
  }

  if ((payload.project_key || PROJECT_KEY) !== PROJECT_KEY) {
    return new Response(JSON.stringify({ ok: false, error: "Invalid project_key" }), {
      status: 400,
      headers: JSON_HEADERS
    });
  }

  const receivedAt = new Date();
  const kind = payload.kind || "event";

  try {
    await upsertRows("personal_mbti_visits", visitRow(payload, context, receivedAt), "visit_id");

    if (kind === "result") {
      await upsertRows("personal_mbti_results", resultRow(payload, context, receivedAt), "assessment_id");
      const rows = answerRows(payload);
      if (rows.length) await upsertRows("personal_mbti_answers", rows, "assessment_id,step");
      await upsertRows("personal_mbti_events", eventRow({ ...payload, event_name: "result" }, context, receivedAt), "event_id");
      return new Response(JSON.stringify({
        ok: true,
        kind,
        assessment_id: payload.assessment_id,
        answer_count: rows.length
      }), { status: 200, headers: JSON_HEADERS });
    }

    await upsertRows("personal_mbti_events", eventRow(payload, context, receivedAt), "event_id");
    return new Response(JSON.stringify({
      ok: true,
      kind,
      event_id: payload.event_id || null
    }), { status: 200, headers: JSON_HEADERS });
  } catch (error: any) {
    console.error("persona-mbti ingest failed", error?.message || error);
    return new Response(JSON.stringify({ ok: false, error: "Analytics write failed" }), {
      status: 500,
      headers: JSON_HEADERS
    });
  }
};

export const config: Config = {
  path: "/api/persona-mbti"
};
