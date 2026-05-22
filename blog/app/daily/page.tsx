/**
 * AI 日报专区 —— 按日期列表展示所有历史日报
 */
import type { Metadata } from "next";
import Link from "next/link";
import { getAllDailyReports } from "@/lib/daily";

export const metadata: Metadata = {
  title: "AI 前沿日报",
  description: "每日 AI 前沿日报归档 —— AI HOT 精选 + 自动生成，每天 08:30 更新。",
};

export default function DailyPage() {
  const reports = getAllDailyReports();

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 py-12">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-3">
        📰 AI 前沿日报
      </h1>
      <p className="text-gray-500 dark:text-gray-400 mb-10">
        每日 08:30 自动生成 · AI HOT 精选 + 五大版块 · 共 {reports.length} 期
      </p>

      {reports.length === 0 ? (
        <div className="text-center py-20 text-gray-400">
          <p className="text-lg mb-2">日报即将上线</p>
          <p className="text-sm">第一期日报将在明天 08:30 自动生成。</p>
        </div>
      ) : (
        <div className="space-y-3">
          {reports.map(({ date, updatedAt }) => {
            const dateObj = new Date(date + "T00:00:00+08:00");
            const weekdays = ["日", "一", "二", "三", "四", "五", "六"];
            const label = `${dateObj.getFullYear()}年${dateObj.getMonth() + 1}月${dateObj.getDate()}日 · 星期${weekdays[dateObj.getDay()]}`;

            return (
              <Link
                key={date}
                href={`/daily/${date}`}
                className="block p-5 rounded-xl border border-gray-100 dark:border-gray-800 hover:border-primary-200 dark:hover:border-primary-800 hover:bg-gray-50 dark:hover:bg-gray-900 transition-all group"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">📰</span>
                    <div>
                      <div className="font-semibold text-gray-900 dark:text-gray-100 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
                        {label}
                      </div>
                      <div className="text-xs text-gray-400 mt-1">
                        更新于 {updatedAt.toLocaleTimeString("zh-CN", { hour: "2-digit", minute: "2-digit" })}
                      </div>
                    </div>
                  </div>
                  <span className="text-gray-300 dark:text-gray-600 group-hover:text-primary-400 transition-colors text-lg">→</span>
                </div>
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
}
