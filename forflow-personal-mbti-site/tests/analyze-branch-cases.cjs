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

const { Q0, Q05, ALL_QUESTIONS, PERSONAS, emptySub, addScore, classify, moduleScores, floorNeg } = context;
const SEQUENCE = [Q0, Q05, ...ALL_QUESTIONS];
const RUNS = Number(process.argv[2] || 500000);
const MAXM = { T: 29, A: 25, J: 20, O: 32, G: 21 };

function randomInt(max) {
  return Math.floor(Math.random() * max);
}

function scoreByChoices(choices) {
  const sub = emptySub();
  choices.forEach((choice, index) => addScore(sub, SEQUENCE[index].options[choice].score));
  const persona = classify(sub);
  const modules = moduleScores(floorNeg(sub));
  const norm = Object.fromEntries(Object.entries(modules).map(([k, v]) => [k, v / MAXM[k]]));
  const dominant = Object.entries(norm).sort((a, b) => b[1] - a[1])[0][0];
  return { persona, sub: floorNeg(sub), modules, dominant };
}

function randomChoices() {
  return SEQUENCE.map(q => randomInt(q.options.length));
}

function answerPath(choices) {
  return choices.map((choice, index) => SEQUENCE[index].options[choice].key).join("");
}

const counters = {
  ctrlS: { total: 0, preObserver: 0, gDominantObserver: 0, robust: 0, fragile: 0 },
  ctrlZY: { total: 0, tDominantO2: 0, fallbackO2: 0, o2Exactly6: 0, tDominantWithG1: 0 },
  shift: { total: 0, escCandidateBlockedByPriority: 0 },
  esc: { total: 0, fromJPattern: 0, fromODominantPattern: 0 },
  hidden: { total: 0, barelyPass: 0, robust: 0 },
};
const examples = {
  ctrlSFragile: [],
  ctrlZYMaybeTooBroad: [],
  shiftEscBlocked: [],
  hiddenBarely: [],
};

for (let i = 0; i < RUNS; i += 1) {
  const choices = randomChoices();
  const r = scoreByChoices(choices);
  const s = r.sub;
  const M = r.modules;
  const A = M.A, J = M.J, O = M.O, G = M.G;
  const A2 = s.A2, A3 = s.A3, J1 = s.J1, O2 = s.O2, O3 = s.O3, G1 = s.G1, G2 = s.G2, T2 = s.T2;
  const preObserver = G1 >= 2 && G2 <= 2 && (A2 + A3) <= 5 && J < 8 && O2 < 6 && O3 < 5 && r.dominant !== "O";
  const gDominantObserver = r.dominant === "G" && G1 >= 2 && A2 <= 4 && G2 < 3;

  if (r.persona === "CtrlS") {
    counters.ctrlS.total += 1;
    if (preObserver) counters.ctrlS.preObserver += 1;
    if (gDominantObserver) counters.ctrlS.gDominantObserver += 1;
    const fragile = G1 === 2 || G2 === 2 || (A2 + A3) === 5 || J === 7 || O2 === 5 || O3 === 4;
    if (fragile) {
      counters.ctrlS.fragile += 1;
      if (examples.ctrlSFragile.length < 8) examples.ctrlSFragile.push({ path: answerPath(choices), modules: M, sub: s, dominant: r.dominant });
    } else {
      counters.ctrlS.robust += 1;
    }
  }

  if (r.persona === "CtrlZY") {
    counters.ctrlZY.total += 1;
    if (r.dominant === "T" && O2 >= 6) counters.ctrlZY.tDominantO2 += 1;
    if (r.dominant !== "T" && O2 >= 6) counters.ctrlZY.fallbackO2 += 1;
    if (O2 === 6) counters.ctrlZY.o2Exactly6 += 1;
    if (r.dominant === "T" && O2 >= 6 && G1 >= 3) {
      counters.ctrlZY.tDominantWithG1 += 1;
      if (examples.ctrlZYMaybeTooBroad.length < 8) examples.ctrlZYMaybeTooBroad.push({ path: answerPath(choices), modules: M, sub: s, dominant: r.dominant });
    }
  }

  if (r.persona === "Shift") {
    counters.shift.total += 1;
    const escCandidateBlocked = r.dominant === "O" && O3 >= 5 && O3 >= O2 && (A >= 12 || J >= 10);
    if (escCandidateBlocked) {
      counters.shift.escCandidateBlockedByPriority += 1;
      if (examples.shiftEscBlocked.length < 8) examples.shiftEscBlocked.push({ path: answerPath(choices), modules: M, sub: s, dominant: r.dominant });
    }
  }

  if (r.persona === "Esc") {
    counters.esc.total += 1;
    if (r.dominant === "J" && J1 >= 4 && O3 >= 4) counters.esc.fromJPattern += 1;
    if (r.dominant === "O" && O3 >= 5 && (A >= 12 || J >= 10) && !(O3 >= O2)) counters.esc.fromODominantPattern += 1;
  }

  if (r.persona === "HIDDEN") {
    counters.hidden.total += 1;
    const vals = [M.T, M.A, M.J, M.O, M.G];
    const spread = Math.max(...vals) - Math.min(...vals);
    const barely = Math.min(A, J, O, G) === 8 || G === 9 || spread === 6;
    if (barely) {
      counters.hidden.barelyPass += 1;
      if (examples.hiddenBarely.length < 8) examples.hiddenBarely.push({ path: answerPath(choices), modules: M, sub: s, dominant: r.dominant, spread });
    } else {
      counters.hidden.robust += 1;
    }
  }
}

function pct(value, total) {
  return total ? `${((value / total) * 100).toFixed(2)}%` : "0.00%";
}

console.log(`Branch case scan: ${RUNS.toLocaleString()} random answer paths`);
console.log("\nFocused counters:");
Object.entries(counters).forEach(([name, value]) => {
  console.log(name, value);
  Object.entries(value).forEach(([key, count]) => {
    if (key !== "total") console.log(`  ${key}: ${pct(count, value.total)}`);
  });
});

console.log("\nSame-position and simple patterned answer paths:");
const patterns = [
  ["all_A", SEQUENCE.map(() => 0)],
  ["all_B", SEQUENCE.map(q => Math.min(1, q.options.length - 1))],
  ["all_C", SEQUENCE.map(q => Math.min(2, q.options.length - 1))],
  ["all_D", SEQUENCE.map(q => Math.min(3, q.options.length - 1))],
  ["ABAB", SEQUENCE.map((q, i) => Math.min(i % 2, q.options.length - 1))],
  ["CDCD", SEQUENCE.map((q, i) => Math.min(2 + (i % 2), q.options.length - 1))],
  ["AAAA_then_D", SEQUENCE.map((q, i) => Math.min(i < 10 ? 0 : 3, q.options.length - 1))],
  ["DDDD_then_A", SEQUENCE.map((q, i) => Math.min(i < 10 ? 3 : 0, q.options.length - 1))],
];
patterns.forEach(([name, choices]) => {
  const r = scoreByChoices(choices);
  console.log(`${name.padEnd(12)} -> ${r.persona.padEnd(10)} ${PERSONAS[r.persona].name} modules=${JSON.stringify(r.modules)} dominant=${r.dominant}`);
});

console.log("\nExamples:");
Object.entries(examples).forEach(([name, rows]) => {
  console.log(`\n${name}`);
  rows.forEach(row => console.log(`${row.path} dominant=${row.dominant} modules=${JSON.stringify(row.modules)} sub=${JSON.stringify(row.sub)}${row.spread !== undefined ? ` spread=${row.spread}` : ""}`));
});
