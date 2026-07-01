const fs = require("fs");
const path = require("path");
const vm = require("vm");

const root = path.resolve(__dirname, "..");
const context = { console, Math };
context.globalThis = context;
vm.createContext(context);

function loadScript(file) {
  let source = fs.readFileSync(path.join(root, file), "utf8");
  source = source
    .replace(/\bconst\s+(SUBDIMS|MODULES|Q0|Q05|MAIN|EXTRA|ALL_QUESTIONS|LOADING_LINES|PERSONAS)\s*=/g, "globalThis.$1 =")
    .replace(/\bfunction\s+(emptySub|addScore|moduleScores|floorNeg|classify)\s*\(/g, "globalThis.$1 = function (");
  vm.runInContext(source, context, { filename: file });
}

loadScript("data.js");
loadScript("engine.js");

const { Q0, Q05, ALL_QUESTIONS, PERSONAS, emptySub, addScore, moduleScores, floorNeg } = context;
const SEQUENCE = [Q0, Q05, ...ALL_QUESTIONS];
const RUNS = Number(process.argv[2] || 500000);
const MAXM = { T: 29, A: 25, J: 20, O: 32, G: 21 };

function randomInt(max) {
  return Math.floor(Math.random() * max);
}

function scoreSub(choices) {
  const sub = emptySub();
  choices.forEach((choice, index) => addScore(sub, SEQUENCE[index].options[choice].score));
  return floorNeg(sub);
}

function classifyVariant(sub, variant) {
  const M = moduleScores(sub);
  const T = M.T, A = M.A, J = M.J, O = M.O, G = M.G;
  const A2 = sub.A2, A3 = sub.A3, A1 = sub.A1;
  const J3 = sub.J3, J1 = sub.J1;
  const O1 = sub.O1, O2 = sub.O2, O3 = sub.O3;
  const T1 = sub.T1, T2 = sub.T2;
  const G1 = sub.G1, G2 = sub.G2;

  const modVals = [T, A, J, O, G];
  const maxM = Math.max(...modVals), minM = Math.min(...modVals);
  if (Math.min(A, J, O, G) >= 8 && (maxM - minM) <= 6 && G >= 9) return "HIDDEN";

  const norm = {};
  for (const k in M) norm[k] = M[k] / MAXM[k];
  let dominant = "T", best = -Infinity;
  for (const k in norm) if (norm[k] > best) { best = norm[k]; dominant = k; }

  const relaxedCtrlS = variant.includes("relax_ctrls");
  const tightenCtrlZY = variant.includes("tighten_ctrlzy");
  const escBeforeShift = variant.includes("esc_before_shift");

  const observerRule = relaxedCtrlS
    ? (G1 >= 2 && G2 <= 3 && (A2 + A3) <= 6 && J < 9 && O2 < 7 && O3 < 6 && dominant !== "O")
    : (G1 >= 2 && G2 <= 2 && (A2 + A3) <= 5 && J < 8 && O2 < 6 && O3 < 5 && dominant !== "O");
  if (observerRule) return "CtrlS";

  if (dominant === "G") {
    if (G2 >= 3) return "CtrlW";
    if (G1 >= 2 && A2 <= 4) return "CtrlS";
    return "CtrlW";
  }

  if (dominant === "A") {
    if ((A2 + A3) >= 7 && J >= 7) return "CtrlZ";
    if ((A2 + A3) >= 6) return "CtrlAltDel";
    if (A1 >= 4 && (A2 + A3) <= 4) return T2 >= 3 ? "CtrlCV" : "CtrlS";
    return "CtrlAltDel";
  }

  if (dominant === "J") {
    if (J3 >= 5 && T1 >= 5) return "CapsLock";
    if (J1 >= 4 && O3 >= 4) return "Esc";
    return "Fn";
  }

  if (dominant === "O") {
    if (escBeforeShift && O3 >= 5 && (A >= 12 || J >= 10)) return "Esc";
    if (O3 >= 5 && O3 >= O2) return "Shift";
    if (O3 >= 5 && (A >= 12 || J >= 10)) return "Esc";
    if (O2 >= 5 && A2 >= 3) return "Tab";
    if (O2 >= 5 && O1 <= 4) return "AltF4";
    if (O3 >= 4) return "Shift";
    return "AltF4";
  }

  if (dominant === "T") {
    if (O2 >= (tightenCtrlZY ? 7 : 6)) return "CtrlZY";
    if (G1 >= 3 && G2 <= 2 && (A2 + A3) <= 5) return "CtrlS";
    if (G1 >= 2) return "CtrlT";
    if (T2 >= T1 && T2 >= 4) return "CtrlCV";
    return "F4";
  }

  if (O2 >= (tightenCtrlZY ? 7 : 6)) return "CtrlZY";
  if (G1 >= 3) return "CtrlS";
  return "CtrlZY";
}

const variants = [
  "baseline",
  "relax_ctrls",
  "tighten_ctrlzy",
  "esc_before_shift",
  "relax_ctrls+tighten_ctrlzy",
  "relax_ctrls+tighten_ctrlzy+esc_before_shift",
];
const counts = Object.fromEntries(variants.map(v => [v, Object.fromEntries(Object.keys(PERSONAS).map(code => [code, 0]))]));

for (let i = 0; i < RUNS; i += 1) {
  const choices = SEQUENCE.map(q => randomInt(q.options.length));
  const sub = scoreSub(choices);
  variants.forEach(v => {
    const code = classifyVariant(sub, v);
    counts[v][code] = (counts[v][code] || 0) + 1;
  });
}

function pct(count) {
  return `${((count / RUNS) * 100).toFixed(2)}%`;
}

console.log(`Variant simulation: ${RUNS.toLocaleString()} uniform random paths`);
console.log(["persona", ...variants].map(x => x.padStart(18)).join(""));
Object.keys(PERSONAS).forEach(code => {
  console.log([code, ...variants.map(v => pct(counts[v][code]))].map(x => x.padStart(18)).join(""));
});
