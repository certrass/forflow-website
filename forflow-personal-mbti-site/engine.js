/* ============================================================
   计分引擎 — 严格移植自 persona_engine.py
   classify(sub) 逻辑逐行对应，确保与 Python 大样本结果一致。
   ============================================================ */

function emptySub() {
  const s = {};
  SUBDIMS.forEach(d => s[d] = 0);
  return s;
}

function addScore(sub, score) {
  for (const k in score) sub[k] = (sub[k] || 0) + score[k];
}

function moduleScores(sub) {
  const M = {};
  for (const m in MODULES) M[m] = MODULES[m].reduce((a, d) => a + sub[d], 0);
  return M;
}

function floorNeg(sub, floor = -3) {
  const out = {};
  for (const d in sub) out[d] = Math.max(sub[d], floor);
  return out;
}

function classify(subRaw) {
  const sub = floorNeg(subRaw);
  const M = moduleScores(sub);
  const T = M.T, A = M.A, J = M.J, O = M.O, G = M.G;

  const A2 = sub.A2, A3 = sub.A3, A1 = sub.A1;
  const J3 = sub.J3, J1 = sub.J1, J2 = sub.J2;
  const O1 = sub.O1, O2 = sub.O2, O3 = sub.O3;
  const T1 = sub.T1, T2 = sub.T2;
  const G1 = sub.G1, G2 = sub.G2, G3 = sub.G3;

  // ---- 隐藏款：六边形战士 ----
  const modVals = [T, A, J, O, G];
  const maxM = Math.max(...modVals), minM = Math.min(...modVals);
  if (Math.min(A, J, O, G) >= 8 && (maxM - minM) <= 6 && G >= 9) {
    return "HIDDEN";
  }

  // ---- 主导轴（归一化）----
  const MAXM = { T: 29, A: 25, J: 20, O: 32, G: 21 };
  const norm = {};
  for (const k in M) norm[k] = M[k] / MAXM[k];
  let dominant = "T", best = -Infinity;
  for (const k in norm) { if (norm[k] > best) { best = norm[k]; dominant = k; } }

  // === 前置：AI 观察者（街溜子）===
  if (G1 >= 2 && G2 <= 3 && (A2 + A3) <= 6 && J < 9 && O2 < 7 && O3 < 6 && dominant !== "O") {
    return "CtrlS";
  }

  // === G 主导 ===
  if (dominant === "G") {
    if (G2 >= 3) return "CtrlW";
    if (G1 >= 2 && A2 <= 4) return "CtrlS";
    return "CtrlW";
  }

  // === A 主导 ===
  if (dominant === "A") {
    if ((A2 + A3) >= 7 && J >= 7) return "CtrlZ";
    if ((A2 + A3) >= 6) return "CtrlAltDel";
    if (A1 >= 4 && (A2 + A3) <= 4) return T2 >= 3 ? "CtrlCV" : "CtrlS";
    return "CtrlAltDel";
  }

  // === J 主导 ===
  if (dominant === "J") {
    if (J3 >= 5 && T1 >= 5) return "CapsLock";
    if (J1 >= 4 && O3 >= 4) return "Esc";
    return "Fn";
  }

  // === O 主导 ===
  if (dominant === "O") {
    if (O3 >= 5 && O3 >= O2) return "Shift";
    if (O3 >= 5 && (A >= 12 || J >= 10)) return "Esc";
    if (O2 >= 5 && A2 >= 3) return "Tab";
    if (O2 >= 5 && O1 <= 4) return "AltF4";
    if (O3 >= 4) return "Shift";
    return "AltF4";
  }

  // === T 主导 ===
  if (dominant === "T") {
    if (O2 >= 7) return "CtrlZY";
    if (G1 >= 3 && G2 <= 2 && (A2 + A3) <= 5) return "CtrlS";
    if (G1 >= 2) return "CtrlT";
    if (T2 >= T1 && T2 >= 4) return "CtrlCV";
    return "F4";
  }

  // === 兜底 ===
  if (O2 >= 7) return "CtrlZY";
  if (G1 >= 3) return "CtrlS";
  return "CtrlZY";
}
