#!/usr/bin/env python3
"""
AI 前沿日报 — 主入口
AI HOT API → HTML 仪表盘 → 博客部署 + Gmail 推送（摘要 + 日报）
"""
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from aihot import fetch_daily_report
from htmlgen import generate_dashboard_html, generate_email_html
from push import send_via_qqmail

# 博客的内容目录（相对于仓库根目录）
BLOG_DAILY_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "blog", "content", "daily")


def main():
    dry_run = "--dry-run" in sys.argv
    date_str = datetime.now().strftime("%Y-%m-%d")

    print("=" * 50)
    print(f"  AI 前沿日报 — {date_str}")
    print("=" * 50)

    # 1. 拉取 AI HOT 日报
    print("\n>>> 拉取 AI HOT 日报...")
    data = fetch_daily_report()
    if not data:
        print("    获取失败，发送通知后退出")
        _send_fallback_email(date_str)
        return

    actual_date = data.get("date", date_str)
    sections = data.get("sections", [])
    flashes = data.get("flashes", [])
    total = sum(len(s.get("items", [])) for s in sections)
    print(f"    获取成功: {actual_date}, {total} 条")

    # 2. 生成 HTML
    print("\n>>> 生成 HTML...")
    dashboard_html = generate_dashboard_html(data)
    email_html = generate_email_html(data)

    # 保存到本地 reports/
    output_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(output_dir, exist_ok=True)
    dashboard_path = os.path.join(output_dir, f"ai_daily_{actual_date}.html")
    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.write(dashboard_html)

    # 保存到博客 content/daily/（GitHub → Vercel 自动部署）
    os.makedirs(BLOG_DAILY_DIR, exist_ok=True)
    blog_path = os.path.join(BLOG_DAILY_DIR, f"{actual_date}.html")
    with open(blog_path, "w", encoding="utf-8") as f:
        f.write(email_html)  # 邮件版更适合博客嵌入
    print(f"    博客部署: {blog_path}")
    print(f"    本地存档: {dashboard_path}")

    if dry_run:
        print(f"\n[Dry Run] 跳过推送")
        return

    # 3. 生成文字摘要
    summary_text = _generate_summary(sections, flashes, total, actual_date)

    # 4. 推送邮件：先发摘要，再发完整日报
    print("\n>>> 推送摘要邮件...")
    send_via_qqmail(_render_summary_email(summary_text, actual_date, total), actual_date)

    print(">>> 推送日报邮件...")
    send_via_qqmail(email_html, actual_date)

    print(f"\n{'=' * 50}")
    print(f"  完成 | 博客: ✓ | 邮件: ✓")
    print(f"  博客地址: /daily/{actual_date}")
    print("=" * 50)


def _generate_summary(sections: list, flashes: list, total: int, date_str: str) -> str:
    """从日报数据生成文字摘要。"""
    lines = [f"AI 前沿日报 | {date_str}", f"共 {total} 条精选，五大版块速览：", ""]
    for s in sections:
        label = s.get("label", "")
        items = s.get("items", [])
        if items:
            lines.append(f"【{label}】{len(items)} 条")
            for item in items[:2]:  # 每版块最多 2 条
                title = item.get("title", "")
                lines.append(f"  · {title}")
        else:
            lines.append(f"【{label}】今日无更新")
        lines.append("")

    if flashes:
        lines.append(f"⚡ 快讯 {len(flashes)} 条")
        for f in flashes[:3]:
            lines.append(f"  · {f.get('title', '')}")

    lines.append("")
    lines.append(f"完整日报: /daily/{date_str}")
    return "\n".join(lines)


def _render_summary_email(text: str, date_str: str, total: int) -> str:
    """将文字摘要渲染为简短 HTML 邮件。"""
    html_text = text.replace("\n", "<br>").replace("  · ", "&nbsp;&nbsp;· ")
    return f"""<html><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;max-width:600px;margin:0 auto;padding:20px;color:#333;">
<div style="background:linear-gradient(135deg,#1a0a00,#2d1200);border-radius:12px;padding:24px;text-align:center;margin-bottom:16px;">
  <div style="font-size:12px;color:rgba(255,255,255,.6);">{date_str}</div>
  <div style="font-size:22px;font-weight:800;color:#ff8a65;margin:4px 0;">AI 前沿日报</div>
  <div style="font-size:36px;font-weight:900;color:#ffb74d;">{total}</div>
  <div style="font-size:12px;color:rgba(255,255,255,.5);">条精选</div>
</div>
<div style="background:#fff;border-radius:12px;padding:20px;line-height:1.8;font-size:14px;">
{html_text}
</div>
<div style="text-align:center;margin-top:16px;font-size:11px;color:#999;">
  AI 捕手 Agent 自动生成 · 每日 08:30
</div>
</body></html>"""


def _send_fallback_email(date_str: str):
    """AI HOT 不可用时发送通知邮件。"""
    html = f"""<html><body style="font-family:sans-serif;padding:24px;color:#333;">
<h2 style="color:#e8552d;">AI 前沿日报 | {date_str}</h2>
<p>今日 AI HOT 尚未生成日报或 API 不可用，自动重试将在明日 08:30 继续。</p>
<p style="color:#999;font-size:12px;">AI 捕手 Agent</p>
</body></html>"""
    send_via_qqmail(html, date_str)


if __name__ == "__main__":
    main()
