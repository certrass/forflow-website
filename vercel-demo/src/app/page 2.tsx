import Image from "next/image";
import Link from "next/link";
import { caseItems, previewGates, routeCards } from "@/lib/demo-content";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#f7f8f3] text-[#121611]">
      <header className="border-b border-[#dfe5d7] bg-white/90">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-4">
          <Image
            src="/forflow/forflow-lockup-header.png"
            alt="ForFlow"
            width={156}
            height={38}
            priority
            className="h-9 w-auto"
          />
          <nav className="hidden items-center gap-6 text-sm font-medium text-[#3f493b] md:flex">
            <Link href="/cases">案例骨架</Link>
            <Link href="/navigator">Navigator</Link>
            <a href="../index.html">静态正式站</a>
          </nav>
        </div>
      </header>

      <section className="mx-auto grid max-w-6xl gap-8 px-5 py-12 lg:grid-cols-[1.05fr_0.95fr] lg:items-center lg:py-16">
        <div>
          <p className="mb-4 font-mono text-sm font-semibold uppercase tracking-normal text-[#4f6b2b]">
            Vercel Demo / Next.js Pilot
          </p>
          <h1 className="max-w-3xl text-4xl font-semibold leading-tight text-[#121611] sm:text-5xl">
            ForFlow 预览试点，不影响 Netlify 正式站。
          </h1>
          <p className="mt-5 max-w-2xl text-lg leading-8 text-[#4b5548]">
            这个目录只用于验证 Next.js 开发体验、Vercel preview 链路、手机与桌面回归检查，以及国内访问体感。正式域名和当前静态站保持不动。
          </p>
          <div className="mt-8 flex flex-col gap-3 sm:flex-row">
            <Link
              href="/navigator"
              className="inline-flex h-12 items-center justify-center rounded-[8px] bg-[#1b2a19] px-5 text-sm font-semibold text-white transition hover:bg-[#2c4128]"
            >
              打开诊断雏形
            </Link>
            <Link
              href="/cases"
              className="inline-flex h-12 items-center justify-center rounded-[8px] border border-[#aab7a0] px-5 text-sm font-semibold text-[#1b2a19] transition hover:bg-white"
            >
              查看案例骨架
            </Link>
          </div>
        </div>

        <div className="overflow-hidden rounded-[8px] border border-[#d7dfcf] bg-white shadow-[0_24px_80px_rgba(28,45,20,0.12)]">
          <Image
            src="/forflow/hero-hand.jpg"
            alt="ForFlow workflow preview"
            width={900}
            height={650}
            priority
            className="h-auto w-full"
          />
          <div className="grid grid-cols-3 border-t border-[#e4eadc] text-center text-sm">
            {previewGates.map((gate) => (
              <div key={gate.label} className="px-3 py-4">
                <strong className="block text-[#1f2c1c]">{gate.label}</strong>
                <span className="mt-1 block text-xs text-[#66705f]">{gate.status}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="border-y border-[#dfe5d7] bg-white">
        <div className="mx-auto grid max-w-6xl gap-4 px-5 py-10 md:grid-cols-3">
          {routeCards.map((card) => (
            <Link
              key={card.href}
              href={card.href}
              className="rounded-[8px] border border-[#dde5d5] p-5 transition hover:border-[#9fb76e] hover:bg-[#fbfff4]"
            >
              <span className="font-mono text-xs font-semibold text-[#61733e]">{card.code}</span>
              <h2 className="mt-3 text-xl font-semibold text-[#161b15]">{card.title}</h2>
              <p className="mt-2 text-sm leading-6 text-[#566050]">{card.description}</p>
            </Link>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-5 py-12">
        <div className="mb-6 flex items-end justify-between gap-4">
          <div>
            <h2 className="text-2xl font-semibold text-[#151a14]">迁移样本</h2>
            <p className="mt-2 text-sm text-[#596354]">先用少量稳定内容测试组件化、路由和预览流程。</p>
          </div>
          <Link href="/cases" className="text-sm font-semibold text-[#31560f]">
            全部样本
          </Link>
        </div>
        <div className="grid gap-4 md:grid-cols-3">
          {caseItems.slice(0, 3).map((item) => (
            <article key={item.slug} className="rounded-[8px] border border-[#dbe3d4] bg-white p-5">
              <span className="text-xs font-semibold text-[#65724f]">{item.domain}</span>
              <h3 className="mt-3 text-lg font-semibold leading-7 text-[#171d16]">{item.title}</h3>
              <p className="mt-2 text-sm leading-6 text-[#5a6555]">{item.summary}</p>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}
