/**
 * 单期日报详情页 —— 直接渲染预生成的 HTML
 */
import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import { getDailyReportByDate, getAllDailyReports } from "@/lib/daily";

interface DailyDetailProps {
  params: { date: string };
}

/** 静态生成所有日报页 */
export function generateStaticParams() {
  return getAllDailyReports().map(({ date }) => ({ date }));
}

export function generateMetadata({ params }: DailyDetailProps): Metadata {
  return {
    title: `AI 前沿日报 ${params.date}`,
    description: `${params.date} AI 前沿日报 —— AI HOT 精选推送`,
  };
}

export default function DailyDetailPage({ params }: DailyDetailProps) {
  const report = getDailyReportByDate(params.date);
  if (!report) notFound();

  const dateObj = new Date(report.date + "T00:00:00+08:00");
  const weekdays = ["日", "一", "二", "三", "四", "五", "六"];
  const label = `${dateObj.getFullYear()}年${dateObj.getMonth() + 1}月${dateObj.getDate()}日 · 星期${weekdays[dateObj.getDay()]}`;

  // 获取上一期/下一期
  const allReports = getAllDailyReports();
  const currentIndex = allReports.findIndex((r) => r.date === report.date);
  const prevReport = currentIndex > 0 ? allReports[currentIndex - 1] : null;
  const nextReport = currentIndex < allReports.length - 1 ? allReports[currentIndex + 1] : null;

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 py-12">
      {/* 导航 */}
      <div className="flex items-center justify-between mb-8">
        <Link href="/daily" className="text-sm text-gray-500 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
          ← 日报列表
        </Link>
        <div className="flex gap-3">
          {prevReport && (
            <Link href={`/daily/${prevReport.date}`} className="text-sm text-gray-500 hover:text-primary-600 transition-colors">
              ← 前一天
            </Link>
          )}
          {nextReport && (
            <Link href={`/daily/${nextReport.date}`} className="text-sm text-gray-500 hover:text-primary-600 transition-colors">
              后一天 →
            </Link>
          )}
        </div>
      </div>

      {/* 标题 */}
      <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-8">
        📰 AI 前沿日报 · {label}
      </h1>

      {/* 日报 HTML（用 iframe 隔离样式冲突，或直接 dangerouslySetInnerHTML） */}
      <div
        className="daily-content rounded-xl border border-gray-100 dark:border-gray-800 bg-white dark:bg-gray-900 overflow-hidden"
        dangerouslySetInnerHTML={{ __html: report.html }}
      />

      {/* 底部导航 */}
      <div className="flex justify-between mt-12 pt-8 border-t border-gray-100 dark:border-gray-800">
        <Link href="/daily" className="text-sm text-gray-500 hover:text-primary-600 transition-colors">
          ← 日报列表
        </Link>
        {prevReport && (
          <Link href={`/daily/${prevReport.date}`} className="text-sm text-gray-500 hover:text-primary-600 transition-colors">
            ← {prevReport.date}
          </Link>
        )}
        {nextReport && (
          <Link href={`/daily/${nextReport.date}`} className="text-sm text-gray-500 hover:text-primary-600 transition-colors">
            {nextReport.date} →
          </Link>
        )}
      </div>
    </div>
  );
}
