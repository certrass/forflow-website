-- Personal MBTI QA queries for Supabase.
-- Run after a test batch to verify tracking completeness and analysis readiness.

-- 1. Latest completed assessments.
select
  assessment_id,
  visit_id,
  persona_code,
  persona_name,
  quality_flag,
  fill_duration_sec,
  source,
  medium,
  campaign,
  received_at_bj_text
from public.personal_mbti_results
order by received_at desc
limit 50;

-- 2. Completed result -> final answer completeness.
select
  r.assessment_id,
  r.persona_code,
  count(a.step) as answer_rows,
  min(a.step) as min_step,
  max(a.step) as max_step
from public.personal_mbti_results r
left join public.personal_mbti_answers a
  on a.assessment_id = r.assessment_id
group by r.assessment_id, r.persona_code
having count(a.step) <> 20 or min(a.step) <> 1 or max(a.step) <> 20
order by r.assessment_id desc;

-- 3. Duplicate event IDs should be empty.
select
  event_id,
  count(*) as rows
from public.personal_mbti_events
where event_id <> ''
group by event_id
having count(*) > 1
order by rows desc, event_id;

-- 4. Funnel counts by event name.
select
  event_name,
  count(*) as events,
  count(distinct visit_id) as visits,
  count(distinct assessment_id) as assessments
from public.personal_mbti_events
group by event_name
order by events desc, event_name;

-- 5. Answer option integrity for clustering.
select
  question_id,
  step,
  question_option_count,
  answer_option_index,
  count(*) as answers
from public.personal_mbti_answers
group by question_id, step, question_option_count, answer_option_index
order by step, answer_option_index;

-- 6. Potential answer integrity issues should be empty.
select
  assessment_id,
  step,
  question_id,
  question_option_count,
  answer_option_index,
  selected_option_indices,
  selected_option_labels
from public.personal_mbti_answers
where answer_option_index is null
   or question_option_count is null
   or answer_option_index < 1
   or answer_option_index > question_option_count
   or selected_option_indices is null
order by assessment_id desc, step;

-- 7. CTA tracking.
select
  cta_key,
  persona_code,
  source,
  campaign,
  count(*) as clicks
from public.personal_mbti_events
where event_name in ('share_click', 'retry_click')
group by cta_key, persona_code, source, campaign
order by clicks desc, cta_key;

-- 7b. Result-page secondary CTA tracking.
select
  event_name,
  cta_key,
  persona_code,
  count(*) as events
from public.personal_mbti_events
where event_name in ('qr_click', 'diagnosis_id_copy')
group by event_name, cta_key, persona_code
order by events desc, event_name;

-- 8. Attribution summary for analysis batches.
select
  source,
  medium,
  campaign,
  cohort,
  count(distinct visit_id) as visits,
  count(distinct assessment_id) filter (where event_name = 'result_view') as completed_assessments
from public.personal_mbti_events
group by source, medium, campaign, cohort
order by visits desc;

-- 9. Beijing timestamp sanity check.
select
  event_name,
  received_at,
  received_at_bj_text
from public.personal_mbti_events
where received_at_bj_text not like '%+08:00'
order by received_at desc
limit 50;
