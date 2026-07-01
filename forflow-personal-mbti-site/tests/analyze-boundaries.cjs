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
const RUNS = Number(process.argv[2] || 80000);
const MAXM = { T: 29, A: 25, J: 20, O: 32, G: 21 };
const expectedAxis = {
  CtrlT: "T", F4: "T", CtrlCV: "T",
  AltF4: "O", Tab: "O", Shift: "O",
  CtrlAltDel: "A", CtrlZ: "A",
  Esc: "O", CapsLock: "J", Fn: "J",
  CtrlS: "G", CtrlZY: "T", CtrlW: "G", HIDDEN: "H"
};

function randomInt(max) {
  return Math.floor(Math.random() * max);
}

function scoreByChoices(choices) {
  const sub = emptySub();
  choices.forEach((choice, index) => addScore(sub, SEQUENCE[index].options[choice].score));
  const persona = classify(sub);
  const modules = moduleScores(floorNeg(sub));
  const norm = Object.fromEntries(Object.entries(modules).map(([k, v]) => [k, v / MAXM[k]]));
  const normSorted = Object.entries(norm).sort((a, b) => b[1] - a[1]);
  return { persona, sub, modules, norm, normSorted };
}

function randomChoices() {
  return SEQUENCE.map(q => randomInt(q.options.length));
}

function answerPath(choices) {
  return choices.map((choice, index) => SEQUENCE[index].options[choice].key).join("");
}

function distanceToHidden(result) {
  const m = result.modules;
  const vals = [m.T, m.A, m.J, m.O, m.G];
  const minAJOG = Math.min(m.A, m.J, m.O, m.G);
  const spread = Math.max(...vals) - Math.min(...vals);
  return {
    minAJOG,
    g: m.G,
    spread,
    missingAJOG: Math.max(0, 8 - minAJOG),
    missingG: Math.max(0, 9 - m.G),
    extraSpread: Math.max(0, spread - 6)
  };
}

const stats = {};
const transitions = {};
const unstableExamples = [];
const semanticOddities = [];
const hiddenNearMisses = [];
const lowFreqExamples = {};
const personaCodes = Object.keys(PERSONAS);

personaCodes.forEach(code => {
  stats[code] = {
    count: 0,
    totalMutations: 0,
    flips: 0,
    same: 0,
    nearTie: 0,
    expectedAxisMismatch: 0
  };
});

for (let i = 0; i < RUNS; i += 1) {
  const choices = randomChoices();
  const base = scoreByChoices(choices);
  const code = base.persona;
  const st = stats[code];
  st.count += 1;
  const top = base.normSorted[0];
  const second = base.normSorted[1];
  if ((top[1] - second[1]) < 0.035) st.nearTie += 1;
  if (expectedAxis[code] !== "H" && expectedAxis[code] && expectedAxis[code] !== top[0]) {
    st.expectedAxisMismatch += 1;
    if (semanticOddities.length < 30) {
      semanticOddities.push({
        code,
        path: answerPath(choices),
        topAxis: top[0],
        secondAxis: second[0],
        modules: base.modules,
        normGap: top[1] - second[1]
      });
    }
  }

  if (code === "CtrlS" || code === "HIDDEN" || code === "CtrlCV") {
    lowFreqExamples[code] ||= { path: answerPath(choices), modules: base.modules, topAxis: top[0] };
  }

  const hiddenDistance = distanceToHidden(base);
  if (code !== "HIDDEN" && hiddenNearMisses.length < 40 && hiddenDistance.missingAJOG + hiddenDistance.missingG + hiddenDistance.extraSpread <= 2) {
    hiddenNearMisses.push({ code, path: answerPath(choices), modules: base.modules, hiddenDistance });
  }

  let localFlips = 0;
  for (let qIndex = 0; qIndex < SEQUENCE.length; qIndex += 1) {
    const q = SEQUENCE[qIndex];
    for (let optionIndex = 0; optionIndex < q.options.length; optionIndex += 1) {
      if (optionIndex === choices[qIndex]) continue;
      const mutated = choices.slice();
      mutated[qIndex] = optionIndex;
      const next = scoreByChoices(mutated);
      st.totalMutations += 1;
      if (next.persona === code) {
        st.same += 1;
      } else {
        st.flips += 1;
        localFlips += 1;
        const key = `${code}->${next.persona}`;
        transitions[key] = (transitions[key] || 0) + 1;
      }
    }
  }

  const mutationCount = SEQUENCE.reduce((sum, q, index) => sum + q.options.length - 1, 0);
  const flipRate = localFlips / mutationCount;
  if (flipRate >= 0.58 && unstableExamples.length < 24) {
    unstableExamples.push({ code, path: answerPath(choices), flipRate, modules: base.modules, topAxis: top[0], normGap: top[1] - second[1] });
  }
}

function pct(value, total) {
  return total ? `${((value / total) * 100).toFixed(2)}%` : "0.00%";
}

console.log(`Boundary scan: ${RUNS.toLocaleString()} random answer paths`);
console.log("\nPersona stability by one-answer mutation:");
Object.entries(stats)
  .filter(([, st]) => st.count > 0)
  .sort((a, b) => (b[1].flips / b[1].totalMutations) - (a[1].flips / a[1].totalMutations))
  .forEach(([code, st]) => {
    console.log([
      code.padEnd(12),
      `count=${String(st.count).padStart(6)}`,
      `flip=${pct(st.flips, st.totalMutations).padStart(7)}`,
      `nearTie=${pct(st.nearTie, st.count).padStart(7)}`,
      `axisMismatch=${pct(st.expectedAxisMismatch, st.count).padStart(7)}`,
      PERSONAS[code].name
    ].join("  "));
  });

console.log("\nMost common one-answer transition pairs:");
Object.entries(transitions)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 28)
  .forEach(([pair, count]) => console.log(`${pair.padEnd(24)} ${count}`));

console.log("\nUnstable examples, many one-answer changes flip result:");
unstableExamples.forEach(item => {
  console.log(`${item.code.padEnd(12)} flip=${(item.flipRate * 100).toFixed(1)}% top=${item.topAxis} gap=${item.normGap.toFixed(3)} path=${item.path} modules=${JSON.stringify(item.modules)}`);
});

console.log("\nSemantic oddities, expected persona family differs from normalized dominant axis:");
semanticOddities.slice(0, 18).forEach(item => {
  console.log(`${item.code.padEnd(12)} top=${item.topAxis}/${item.secondAxis} gap=${item.normGap.toFixed(3)} path=${item.path} modules=${JSON.stringify(item.modules)}`);
});

console.log("\nHidden near misses:");
hiddenNearMisses.slice(0, 18).forEach(item => {
  console.log(`${item.code.padEnd(12)} path=${item.path} modules=${JSON.stringify(item.modules)} hiddenDistance=${JSON.stringify(item.hiddenDistance)}`);
});

console.log("\nLow frequency representative examples:");
Object.entries(lowFreqExamples).forEach(([code, item]) => {
  console.log(`${code.padEnd(12)} top=${item.topAxis} path=${item.path} modules=${JSON.stringify(item.modules)}`);
});
