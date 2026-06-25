"use client";

import { useMemo, useState } from "react";
import { navigatorOptions } from "@/lib/demo-content";

const readinessCopy = {
  early: "适合先做访谈、流程切片和样本证据整理。",
  process: "适合进入 2 周小步试点，先验证一个 Human + Agent 工作单元。",
  data: "适合把诊断结果接到数据边界、系统调用和验收看板。",
};

type Readiness = keyof typeof readinessCopy;

export function DemoNavigator() {
  const [challenge, setChallenge] = useState(navigatorOptions[0].id);
  const [readiness, setReadiness] = useState<Readiness>("process");

  const selected = useMemo(
    () => navigatorOptions.find((option) => option.id === challenge) ?? navigatorOptions[0],
    [challenge],
  );

  return (
    <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
      <section className="rounded-[8px] border border-[#dce5d3] bg-white p-5">
        <h2 className="text-xl font-semibold text-[#151a14]">业务挑战</h2>
        <div className="mt-5 grid gap-3">
          {navigatorOptions.map((option) => (
            <button
              key={option.id}
              type="button"
              onClick={() => setChallenge(option.id)}
              className={`rounded-[8px] border px-4 py-3 text-left text-sm font-semibold transition ${
                challenge === option.id
                  ? "border-[#8baa44] bg-[#f4ffe0] text-[#17210f]"
                  : "border-[#dbe3d4] text-[#566050] hover:border-[#9fb76e]"
              }`}
            >
              {option.label}
            </button>
          ))}
        </div>
      </section>

      <section className="rounded-[8px] border border-[#dce5d3] bg-white p-5">
        <h2 className="text-xl font-semibold text-[#151a14]">准备度</h2>
        <div className="mt-5 grid gap-3 sm:grid-cols-3">
          {Object.entries(readinessCopy).map(([key, value]) => (
            <button
              key={key}
              type="button"
              onClick={() => setReadiness(key as Readiness)}
              className={`rounded-[8px] border p-4 text-left transition ${
                readiness === key
                  ? "border-[#1f2c1c] bg-[#17210f] text-white"
                  : "border-[#dbe3d4] text-[#566050] hover:border-[#9fb76e]"
              }`}
            >
              <strong className="block text-sm">{key}</strong>
              <span className="mt-2 block text-xs leading-5 opacity-80">{value}</span>
            </button>
          ))}
        </div>

        <div className="mt-6 rounded-[8px] bg-[#f7f8f3] p-5">
          <span className="font-mono text-xs font-semibold uppercase text-[#637544]">
            Demo result
          </span>
          <p className="mt-3 text-lg font-semibold leading-7 text-[#17210f]">{selected.result}</p>
          <p className="mt-2 text-sm leading-6 text-[#596354]">{readinessCopy[readiness]}</p>
        </div>
      </section>
    </div>
  );
}
