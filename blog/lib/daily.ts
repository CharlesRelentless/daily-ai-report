/**
 * 日报读取模块 —— 从 content/daily/ 目录读取每日 AI 日报 HTML
 */
import fs from "fs";
import path from "path";

/** 日报存放目录 */
const DAILY_DIR = path.join(process.cwd(), "content", "daily");

export interface DailyReport {
  /** 日期 (YYYY-MM-DD) */
  date: string;
  /** HTML 内容 */
  html: string;
  /** 文件修改时间 */
  updatedAt: Date;
}

/**
 * 获取所有日报列表（按日期降序）
 */
export function getAllDailyReports(): { date: string; updatedAt: Date }[] {
  if (!fs.existsSync(DAILY_DIR)) return [];

  return fs
    .readdirSync(DAILY_DIR)
    .filter((f) => f.endsWith(".html"))
    .map((f) => {
      const date = f.replace(/\.html$/, "");
      const stat = fs.statSync(path.join(DAILY_DIR, f));
      return { date, updatedAt: stat.mtime };
    })
    .sort((a, b) => b.date.localeCompare(a.date));
}

/**
 * 按日期读取单期日报
 */
export function getDailyReportByDate(date: string): DailyReport | null {
  const filePath = path.join(DAILY_DIR, `${date}.html`);
  if (!fs.existsSync(filePath)) return null;

  const html = fs.readFileSync(filePath, "utf-8");
  const stat = fs.statSync(filePath);

  return { date, html, updatedAt: stat.mtime };
}
