#!/usr/bin/env node
const http = require("node:http");
const fs = require("node:fs");
const path = require("node:path");

const root = path.resolve(__dirname, "..");
const port = Number(process.env.PORT || process.argv[2] || 5181);
const captureFile = process.env.QA_CAPTURE_FILE || "";
let payloads = [];

const types = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".svg": "image/svg+xml; charset=utf-8",
  ".json": "application/json; charset=utf-8"
};

function send(res, status, body, headers = {}) {
  res.writeHead(status, { "Cache-Control": "no-store", ...headers });
  res.end(body);
}

function sendJson(res, status, value) {
  send(res, status, JSON.stringify(value, null, 2), { "Content-Type": types[".json"] });
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let body = "";
    req.setEncoding("utf8");
    req.on("data", chunk => {
      body += chunk;
      if (body.length > 1024 * 1024) {
        reject(new Error("Request body too large"));
        req.destroy();
      }
    });
    req.on("end", () => resolve(body));
    req.on("error", reject);
  });
}

function appendCapture(payload) {
  payloads.push(payload);
  if (captureFile) {
    fs.appendFileSync(captureFile, `${JSON.stringify(payload)}\n`);
  }
}

function staticPath(urlPath) {
  const cleanPath = decodeURIComponent(urlPath.split("?")[0]);
  const requested = cleanPath === "/" ? "/index.html" : cleanPath;
  const target = path.normalize(path.join(root, requested));
  if (!target.startsWith(root)) return null;
  return target;
}

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url || "/", `http://${req.headers.host || "127.0.0.1"}`);

    if (req.method === "POST" && url.pathname === "/api/persona-mbti") {
      const body = await readBody(req);
      const payload = JSON.parse(body || "{}");
      appendCapture(payload);
      return sendJson(res, 200, {
        ok: true,
        kind: payload.kind || "event",
        event_id: payload.event_id || null,
        assessment_id: payload.assessment_id || null,
        answer_count: Array.isArray(payload.answers_indexed) ? payload.answers_indexed.length : null
      });
    }

    if (req.method === "GET" && url.pathname === "/__qa/payloads") {
      return sendJson(res, 200, payloads);
    }

    if (req.method === "POST" && url.pathname === "/__qa/reset") {
      payloads = [];
      if (captureFile) fs.writeFileSync(captureFile, "");
      return sendJson(res, 200, { ok: true });
    }

    if (req.method !== "GET" && req.method !== "HEAD") {
      return sendJson(res, 405, { ok: false, error: "Method not allowed" });
    }

    const target = staticPath(url.pathname);
    if (!target || !fs.existsSync(target) || fs.statSync(target).isDirectory()) {
      return sendJson(res, 404, { ok: false, error: "Not found" });
    }

    const contentType = types[path.extname(target).toLowerCase()] || "application/octet-stream";
    res.writeHead(200, { "Content-Type": contentType, "Cache-Control": "no-store" });
    if (req.method === "HEAD") return res.end();
    fs.createReadStream(target).pipe(res);
  } catch (error) {
    sendJson(res, 500, { ok: false, error: error.message || "QA server error" });
  }
});

server.listen(port, "127.0.0.1", () => {
  console.log(`QA capture server: http://127.0.0.1:${port}`);
});
