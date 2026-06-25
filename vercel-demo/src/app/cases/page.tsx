import Link from "next/link";
import { caseItems } from "@/lib/demo-content";

export default function CasesPage() {
  return (
    <main className="min-h-screen bg-[#f7f8f3] px-5 py-10 text-[#121611]">
      <div className="mx-auto max-w-6xl">
        <Link href="/" className="text-sm font-semibold text-[#31560f]">
          返回 Vercel Demo
        </Link>
        <div className="mt-8 max-w-3xl">
          <p className="font-mono text-sm font-semibold uppercase tracking-normal text-[#4f6b2b]">
            Case Library Pilot
          </p>
          <h1 className="mt-3 text-4xl font-semibold leading-tight">案例中心迁移骨架</h1>
          <p className="mt-4 text-lg leading-8 text-[#566050]">
            这里先验证 TypeScript 数据源、列表组件和 preview 链路。正式案例详情仍保留在当前静态站。
          </p>
        </div>
        <div className="mt-8 grid gap-4 md:grid-cols-2">
          {caseItems.map((item) => (
            <article key={item.slug} className="rounded-[8px] border border-[#dbe3d4] bg-white p-6">
              <span className="text-xs font-semibold text-[#65724f]">{item.domain}</span>
              <h2 className="mt-3 text-xl font-semibold leading-7 text-[#171d16]">{item.title}</h2>
              <p className="mt-3 text-sm leading-6 text-[#5a6555]">{item.summary}</p>
              <code className="mt-5 block rounded-[6px] bg-[#f1f4ec] px-3 py-2 font-mono text-xs text-[#4d5948]">
                slug: {item.slug}
              </code>
            </article>
          ))}
        </div>
      </div>
    </main>
  );
}
