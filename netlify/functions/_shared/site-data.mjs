const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-8][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

export const POLICY_VERSION = '2026-07-11-v1';

export const env = (name) => globalThis.Netlify?.env?.get(name) || process.env[name] || '';

export const json = (body, status = 200, headers = {}) => Response.json(body, {
  status,
  headers: { 'Cache-Control': 'no-store', ...headers },
});

export const cleanText = (value, max = 200) => String(value || '')
  .replace(/[\u0000-\u001f\u007f]/g, ' ')
  .replace(/\s+/g, ' ')
  .trim()
  .slice(0, max);

export const isUuid = (value) => UUID_RE.test(String(value || ''));

export const assertSameOriginJson = (request, maxBytes = 16_384) => {
  if (request.method !== 'POST') return json({ ok: false, error: 'Method not allowed.' }, 405, { Allow: 'POST' });
  const url = new URL(request.url);
  const origin = request.headers.get('origin');
  if (origin && origin !== url.origin) return json({ ok: false, error: 'Request origin is not allowed.' }, 403);
  const type = request.headers.get('content-type') || '';
  if (!type.toLowerCase().includes('application/json')) return json({ ok: false, error: 'Content-Type must be application/json.' }, 415);
  const length = Number(request.headers.get('content-length') || 0);
  if (Number.isFinite(length) && length > maxBytes) return json({ ok: false, error: 'Request body is too large.' }, 413);
  return null;
};

const supabaseConfig = () => {
  const url = env('SUPABASE_URL').replace(/\/$/, '');
  const key = env('SUPABASE_SECRET_KEY') || env('SUPABASE_SERVICE_ROLE_KEY');
  if (!url || !key) throw new Error('Supabase is not configured.');
  return { url, key };
};

const supabaseHeaders = (key, prefer = '') => {
  const headers = { apikey: key, 'Content-Type': 'application/json' };
  if (!key.startsWith('sb_secret_')) headers.Authorization = `Bearer ${key}`;
  if (prefer) headers.Prefer = prefer;
  return headers;
};

export async function supabaseRequest(path, { method = 'GET', body, prefer = '', accept = 'application/json' } = {}) {
  const { url, key } = supabaseConfig();
  const response = await fetch(`${url}/rest/v1/${path}`, {
    method,
    headers: { ...supabaseHeaders(key, prefer), Accept: accept },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`Supabase ${response.status}: ${detail.slice(0, 500)}`);
  }
  if (response.status === 204) return null;
  const text = await response.text();
  return text ? JSON.parse(text) : null;
}

export const upsertRows = (table, rows, onConflict, returnRows = false) => supabaseRequest(
  `${table}?on_conflict=${encodeURIComponent(onConflict)}`,
  {
    method: 'POST',
    body: rows,
    prefer: `resolution=merge-duplicates,return=${returnRows ? 'representation' : 'minimal'}`,
  },
);

export const insertRows = (table, rows, returnRows = false) => supabaseRequest(table, {
  method: 'POST',
  body: rows,
  prefer: `return=${returnRows ? 'representation' : 'minimal'}`,
});

export const selectRows = (path) => supabaseRequest(path);

export const safeDate = (value) => {
  const date = new Date(value || '');
  return Number.isNaN(date.getTime()) ? null : date.toISOString();
};

export const safeStringArray = (value, allowed, max = 4) => {
  const source = Array.isArray(value) ? value : value ? [value] : [];
  return [...new Set(source.map((item) => cleanText(item, 40)).filter((item) => allowed.has(item)))].slice(0, max);
};

export const escapeHtml = (value) => cleanText(value, 2_000)
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;')
  .replace(/'/g, '&#039;');
