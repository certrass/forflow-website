create extension if not exists pgcrypto;

create table if not exists public.website_events (
  event_id uuid primary key default gen_random_uuid(),
  session_id uuid not null,
  assessment_id uuid,
  event_name text not null check (event_name in (
    'page_view',
    'service_view',
    'case_view',
    'navigator_start',
    'navigator_step_complete',
    'navigator_complete',
    'result_sort',
    'result_service_click',
    'contact_start',
    'contact_submit'
  )),
  page_key text not null default '',
  route text not null default '',
  referrer_host text not null default '',
  source text not null default '',
  medium text not null default '',
  campaign text not null default '',
  properties jsonb not null default '{}'::jsonb,
  occurred_at timestamptz,
  received_at timestamptz not null default now(),
  netlify_request_id text not null default '',
  constraint website_events_route_no_query check (position('?' in route) = 0),
  constraint website_events_properties_object check (jsonb_typeof(properties) = 'object')
);

create table if not exists public.assessments (
  assessment_id uuid primary key,
  session_id uuid not null,
  status text not null default 'complete' check (status in ('complete')),
  challenges text[] not null default '{}',
  goals text[] not null default '{}',
  constraints text[] not null default '{}',
  readiness text not null default '',
  deployment text not null default '',
  timeline text not null default '',
  team_size text not null default '',
  industry text not null default '',
  hr_stage text not null default '',
  result_summary jsonb not null default '{}'::jsonb,
  completed_at timestamptz,
  received_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint assessments_summary_object check (jsonb_typeof(result_summary) = 'object')
);

create table if not exists public.assessment_answers (
  assessment_id uuid not null references public.assessments(assessment_id) on delete cascade,
  field_key text not null check (field_key in (
    'challenge', 'goal', 'constraint', 'readiness', 'deployment',
    'timeline', 'teamSize', 'industry', 'hrStage'
  )),
  value_json jsonb not null,
  recorded_at timestamptz not null default now(),
  primary key (assessment_id, field_key)
);

create table if not exists public.leads (
  lead_id uuid primary key default gen_random_uuid(),
  submission_id uuid not null unique,
  assessment_id uuid references public.assessments(assessment_id) on delete set null,
  source_type text not null default 'contact' check (source_type in ('contact', 'assessment_report')),
  email text not null,
  name text not null default '',
  company text not null default '',
  problem text not null default '',
  service_interest text not null default '',
  preferred_time text not null default '',
  source text not null default '',
  medium text not null default '',
  campaign text not null default '',
  status text not null default 'new' check (status in ('new', 'contacted', 'qualified', 'closed')),
  consent_at timestamptz not null,
  notification_sent_at timestamptz,
  report_sent_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint leads_email_length check (char_length(email) between 3 and 254)
);

create table if not exists public.consent_records (
  consent_id uuid primary key default gen_random_uuid(),
  lead_id uuid not null references public.leads(lead_id) on delete cascade,
  purpose text not null check (purpose in ('contact_follow_up', 'assessment_report')),
  policy_version text not null,
  consented_at timestamptz not null,
  created_at timestamptz not null default now(),
  unique (lead_id, purpose, policy_version)
);

create index if not exists website_events_session_received_idx
  on public.website_events (session_id, received_at desc);
create index if not exists website_events_name_received_idx
  on public.website_events (event_name, received_at desc);
create index if not exists website_events_assessment_idx
  on public.website_events (assessment_id, received_at desc)
  where assessment_id is not null;
create index if not exists assessments_received_idx
  on public.assessments (received_at desc);
create index if not exists leads_created_idx
  on public.leads (created_at desc);
create index if not exists leads_assessment_idx
  on public.leads (assessment_id)
  where assessment_id is not null;

alter table public.website_events enable row level security;
alter table public.assessments enable row level security;
alter table public.assessment_answers enable row level security;
alter table public.leads enable row level security;
alter table public.consent_records enable row level security;

revoke all on table public.website_events from anon, authenticated;
revoke all on table public.assessments from anon, authenticated;
revoke all on table public.assessment_answers from anon, authenticated;
revoke all on table public.leads from anon, authenticated;
revoke all on table public.consent_records from anon, authenticated;

grant select, insert, update, delete on table public.website_events to service_role;
grant select, insert, update, delete on table public.assessments to service_role;
grant select, insert, update, delete on table public.assessment_answers to service_role;
grant select, insert, update, delete on table public.leads to service_role;
grant select, insert, update, delete on table public.consent_records to service_role;

comment on table public.website_events is 'ForFlow first-party product events. assessment_id is a logical correlation id because events may arrive before the assessment row. No email, phone, free-text form fields, query strings, or raw payloads.';
comment on table public.assessments is 'Anonymous AI Navigator assessment records. Identity is linked only through leads.assessment_id.';
comment on table public.assessment_answers is 'Normalized final Navigator answers without contact information.';
comment on table public.leads is 'Contact and assessment-report requests. This is the only website table containing contact identity.';
comment on table public.consent_records is 'Versioned evidence of consent for contact follow-up or assessment report delivery.';
