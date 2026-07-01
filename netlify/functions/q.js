const FILE_ROUTES = require("./qr-routes.json");
const JSON_HEADER = { "content-type": "application/json; charset=utf-8" };
const NO_STORE_HEADERS = {
  "cache-control": "no-store, max-age=0",
  pragma: "no-cache",
  expires: "0",
  "x-robots-tag": "noindex, nofollow",
};

function response(statusCode, body, headers = {}) {
  return {
    statusCode,
    headers: { ...NO_STORE_HEADERS, ...headers },
    body: typeof body === "string" ? body : JSON.stringify(body),
  };
}

function loadFileRoutes() {
  return FILE_ROUTES;
}

function loadEnvRoutes() {
  const raw = process.env.QR_REDIRECTS_JSON;
  if (!raw) return {};

  try {
    return JSON.parse(raw);
  } catch (error) {
    console.error("Invalid QR_REDIRECTS_JSON", error);
    return {};
  }
}

function normalizeRoute(value) {
  if (typeof value === "string") {
    return { target: value, active: true };
  }

  if (!value || typeof value !== "object") {
    return null;
  }

  return {
    ...value,
    active: value.active !== false,
  };
}

function routeMap() {
  return { ...loadFileRoutes(), ...loadEnvRoutes() };
}

function codeFromEvent(event) {
  const parameterCode = event.pathParameters && event.pathParameters.code;
  if (parameterCode) return parameterCode;

  const pathname = (event.path || "").split("?")[0];
  const qMatch = pathname.match(/\/q\/([^/?#]+)/);
  if (qMatch) return decodeURIComponent(qMatch[1]);

  const functionMatch = pathname.match(/\/\.netlify\/functions\/q\/([^/?#]+)/);
  return functionMatch ? decodeURIComponent(functionMatch[1]) : "";
}

function sameSiteOrigin(event) {
  const headers = event.headers || {};
  const proto = headers["x-forwarded-proto"] || "https";
  const host = headers.host;
  return host ? `${proto}://${host}` : "";
}

function buildTarget(target, event) {
  if (!target || typeof target !== "string") {
    throw new Error("Missing target URL");
  }

  const origin = sameSiteOrigin(event);
  const base = origin || "https://forflow.local";
  const targetUrl = new URL(target, base);

  if (!["http:", "https:"].includes(targetUrl.protocol)) {
    throw new Error("QR target must use http or https");
  }

  const incoming = event.queryStringParameters || {};
  for (const [key, value] of Object.entries(incoming)) {
    if (key === "code" || key === "target" || value === undefined || value === null) {
      continue;
    }
    if (!targetUrl.searchParams.has(key)) {
      targetUrl.searchParams.set(key, value);
    }
  }

  if (target.startsWith("/")) {
    return `${targetUrl.pathname}${targetUrl.search}${targetUrl.hash}`;
  }

  return targetUrl.toString();
}

exports.handler = async (event) => {
  if (!["GET", "HEAD"].includes(event.httpMethod)) {
    return response(405, { error: "Method not allowed" }, { ...JSON_HEADER, allow: "GET, HEAD" });
  }

  const code = codeFromEvent(event).trim().toLowerCase();
  if (!/^[a-z0-9][a-z0-9_-]{1,63}$/.test(code)) {
    return response(400, { error: "Invalid QR code" }, JSON_HEADER);
  }

  const route = normalizeRoute(routeMap()[code]);
  if (!route) {
    return response(404, { error: "QR code not found", code }, JSON_HEADER);
  }

  if (!route.active) {
    return response(410, { error: "QR code disabled", code }, JSON_HEADER);
  }

  let location;
  try {
    location = buildTarget(route.target, event);
  } catch (error) {
    console.error("Invalid QR target", { code, error });
    return response(500, { error: "QR target is not configured correctly", code }, JSON_HEADER);
  }

  return {
    statusCode: 302,
    headers: {
      ...NO_STORE_HEADERS,
      location,
    },
    body: "",
  };
};
