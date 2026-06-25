import Link from "next/link";
import { DemoNavigator } from "@/components/demo-navigator";

export default function NavigatorPage() {
  return (
    <main className="min-h-screen bg-[#f7f8f3] px-5 py-10 text-[#121611]">
      <div className="mx-auto max-w-6xl">
        <Link href="/" className="text-sm font-semibold text-[#31560f]">
          返回 Vercel Demo
        </Link>
        <div className="mt-8 max-w-3xl">
          <p className="font-mono text-sm font-semibold uppercase tracking-normal text-[#4f6b2b]">
            Navigator Pilot
          </p>
          <h1 className="mt-3 text-4xl font-semibold leading-tight">AI 场景诊断雏形</h1>
          <p className="mt-4 text-lg leading-8 text-[#566050]">
            先验证客户端交互、状态切换和移动端触控，再决定是否迁移完整问卷和推荐结果。
          </p>
        </div>
        <div className="mt-8">
          <DemoNavigator />
        </div>
      </div>
    </main>
  );
}
