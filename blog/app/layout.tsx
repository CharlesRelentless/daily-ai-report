/**
 * 根布局 —— 全局 UI 骨架 + SEO Metadata
 */
import type { Metadata } from "next";
import { ThemeProvider } from "@/components/theme-provider";
import { Header } from "@/components/header";
import { Footer } from "@/components/footer";
import "./globals.css";

const SITE_URL = "https://blog.aihot.virxact.com";
const SITE_NAME = "小悟的博客 —— AI 前沿日报与开发实践";

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: SITE_NAME,
    template: `%s | ${SITE_NAME}`,
  },
  description: "关注 AI 前沿资讯、深度学习、自动化工具与 Next.js 开发实践。每日推送 AI HOT 精选日报。",
  keywords: ["AI", "深度学习", "Next.js", "TypeScript", "博客", "前沿日报"],
  authors: [{ name: "小悟", url: SITE_URL }],
  openGraph: {
    type: "website",
    locale: "zh_CN",
    url: SITE_URL,
    siteName: SITE_NAME,
    title: SITE_NAME,
    description: "关注 AI 前沿资讯、深度学习、自动化工具与 Next.js 开发实践。",
  },
  twitter: {
    card: "summary_large_image",
    title: SITE_NAME,
    description: "关注 AI 前沿资讯、深度学习、自动化工具与 Next.js 开发实践。",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: { index: true, follow: true },
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN" suppressHydrationWarning>
      <body className="min-h-screen flex flex-col">
        <ThemeProvider>
          <Header />
          <main className="flex-1">{children}</main>
          <Footer />
        </ThemeProvider>
      </body>
    </html>
  );
}
