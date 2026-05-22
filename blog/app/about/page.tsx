/**
 * 关于页面
 */
import type { Metadata } from "next";
import Image from "next/image";

export const metadata: Metadata = {
  title: "关于",
  description: "关于小悟和这个博客",
};

export default function AboutPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 py-12">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-8">
        关于
      </h1>

      <div className="prose prose-gray dark:prose-invert max-w-none">
        <div className="flex items-center gap-4 mb-8 p-4 rounded-xl bg-gray-50 dark:bg-gray-900 border border-gray-100 dark:border-gray-800">
          <div className="w-16 h-16 rounded-full bg-gradient-to-br from-primary-400 to-primary-600 flex items-center justify-center text-white text-2xl font-bold flex-shrink-0">
            🧠
          </div>
          <div>
            <h2 className="!text-lg !font-bold !m-0">小悟</h2>
            <p className="!text-sm !text-gray-500 dark:!text-gray-400 !m-0">
              AI 从业者 · 博客作者 · 工具爱好者
            </p>
          </div>
        </div>

        <h2>这个博客是什么</h2>
        <p>
          一个专注于 <strong>AI 前沿资讯</strong>、<strong>深度学习实践</strong>和
          <strong>自动化工具开发</strong>的个人博客。
        </p>
        <p>
          每篇文章力求精简实用——不写"AI 将改变世界"的废话，
          只写"今天这条信息对我有用"的干货。
        </p>

        <h2>技术栈</h2>
        <ul>
          <li><strong>框架</strong>：Next.js 14 App Router + TypeScript</li>
          <li><strong>样式</strong>：Tailwind CSS + 暗色模式</li>
          <li><strong>内容</strong>：MDX（Markdown + JSX）</li>
          <li><strong>部署</strong>：Vercel（免费）</li>
          <li><strong>日报</strong>：AI HOT API 自动聚合</li>
        </ul>

        <h2>联系方式</h2>
        <ul>
          <li>GitHub：<a href="https://github.com/CharlesRelentless" target="_blank" rel="noopener noreferrer">CharlesRelentless</a></li>
          <li>邮箱：通过 AI 日报推送联系</li>
        </ul>

        <blockquote>
          <p>最好的过滤器，是你自己建立的认知体系。</p>
        </blockquote>
      </div>
    </div>
  );
}
