const fs = require("fs");
const path = require("path");
const vm = require("vm");

const root = path.resolve(__dirname, "..");
const context = {
  console,
  Math,
};
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

const { Q0, Q05, ALL_QUESTIONS, PERSONAS, SUBDIMS, emptySub, addScore, classify, moduleScores, floorNeg } = context;
const SEQUENCE = [Q0, Q05, ...ALL_QUESTIONS];
const PERSONA_CODES = Object.keys(PERSONAS);
const RUNS = Number(process.argv[2] || 300000);

function randomInt(max) {
  return Math.floor(Math.random() * max);
}

function scoreByChoices(choices) {
  const sub = emptySub();
  const answers = [];
  choices.forEach((choice, index) => {
    const q = SEQUENCE[index];
    const option = q.options[choice];
    addScore(sub, option.score);
    answers.push(option.key);
  });
  const persona = classify(sub);
  return { persona, sub, answers };
}

function randomRun() {
  return scoreByChoices(SEQUENCE.map(q => randomInt(q.options.length)));
}

function topModules(sub) {
  const scores = moduleScores(floorNeg(sub));
  return Object.entries(scores).sort((a, b) => b[1] - a[1]);
}

function normalizedDominant(sub) {
  const scores = moduleScores(floorNeg(sub));
  const max = { T: 29, A: 25, J: 20, O: 32, G: 21 };
  return Object.entries(scores)
    .map(([key, value]) => [key, value / max[key]])
    .sort((a, b) => b[1] - a[1])[0][0];
}

const counts = Object.fromEntries(PERSONA_CODES.map(code => [code, 0]));
const rawModuleLeaders = {};
const normalizedAxisLeaders = {};
const samples = {};
for (let i = 0; i < RUNS; i += 1) {
  const result = randomRun();
  counts[result.persona] = (counts[result.persona] || 0) + 1;
  samples[result.persona] ||= result;
  const rawLeader = topModules(result.sub)[0][0];
  rawModuleLeaders[rawLeader] = (rawModuleLeaders[rawLeader] || 0) + 1;
  const normalizedLeader = normalizedDominant(result.sub);
  normalizedAxisLeaders[normalizedLeader] = (normalizedAxisLeaders[normalizedLeader] || 0) + 1;
}

function pct(value, total = RUNS) {
  return `${((value / total) * 100).toFixed(2)}%`;
}

console.log(`Monte Carlo uniform answer simulation: ${RUNS.toLocaleString()} runs`);
console.log("\nPersona distribution:");
Object.entries(counts)
  .sort((a, b) => b[1] - a[1])
  .forEach(([code, count]) => {
    const p = PERSONAS[code];
    console.log(`${code.padEnd(12)} ${String(count).padStart(7)} ${pct(count).padStart(8)}  ${p.name}`);
  });

console.log("\nAlgorithm normalized dominant-axis distribution:");
Object.entries(normalizedAxisLeaders)
  .sort((a, b) => b[1] - a[1])
  .forEach(([module, count]) => {
    console.log(`${module} ${String(count).padStart(7)} ${pct(count).padStart(8)}`);
  });

console.log("\nRaw module-score leader distribution:");
Object.entries(rawModuleLeaders)
  .sort((a, b) => b[1] - a[1])
  .forEach(([module, count]) => {
    console.log(`${module} ${String(count).padStart(7)} ${pct(count).padStart(8)}`);
  });

console.log("\nMissing personas in random sample:");
console.log(PERSONA_CODES.filter(code => !counts[code]).join(", ") || "none");

console.log("\nRepresentative answer paths found:");
PERSONA_CODES.forEach(code => {
  const sample = samples[code];
  if (!sample) {
    console.log(`${code.padEnd(12)} not found`);
    return;
  }
  const modules = topModules(sample.sub).map(([k, v]) => `${k}:${v}`).join(" ");
  console.log(`${code.padEnd(12)} ${sample.answers.join("")}  ${modules}`);
});

const allSame = [];
for (let optionIndex = 0; optionIndex < 4; optionIndex += 1) {
  const choices = SEQUENCE.map(q => Math.min(optionIndex, q.options.length - 1));
  allSame.push({ label: `all_${optionIndex + 1}`, ...scoreByChoices(choices) });
}
console.log("\nSimple edge paths:");
allSame.forEach(row => {
  console.log(`${row.label.padEnd(8)} -> ${row.persona.padEnd(10)} ${PERSONAS[row.persona].name}`);
});

console.log("\nScore sub-dim ranges from random sample:");
const ranges = Object.fromEntries(SUBDIMS.map(dim => [dim, { min: Infinity, max: -Infinity }]));
for (let i = 0; i < 50000; i += 1) {
  const { sub } = randomRun();
  SUBDIMS.forEach(dim => {
    ranges[dim].min = Math.min(ranges[dim].min, sub[dim]);
    ranges[dim].max = Math.max(ranges[dim].max, sub[dim]);
  });
}
console.log(Object.entries(ranges).map(([dim, r]) => `${dim}:${r.min}/${r.max}`).join(" "));
