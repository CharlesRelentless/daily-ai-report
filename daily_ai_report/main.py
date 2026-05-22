#!/usr/bin/env python3
"""
AI 前沿日报 — 主入口
AI HOT API → HTML 仪表盘 → Gmail 推送（自备微信提醒）
"""
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from aihot import fetch_daily_report
from htmlgen import generate_dashboard_html, generate_email_html
from push import send_via_qqmail  # 通用 SMTP


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
        print("    获取失败，退出")
        return

    actual_date = data.get("date", date_str)
    total = sum(len(s.get("items", [])) for s in data.get("sections", []))
    print(f"    获取成功: {actual_date}, {total} 条")

    # 2. 生成 HTML
    print("\n>>> 生成 HTML...")
    dashboard_html = generate_dashboard_html(data)
    email_html = generate_email_html(data)

    output_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(output_dir, exist_ok=True)

    dashboard_path = os.path.join(output_dir, f"ai_daily_{actual_date}.html")
    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.write(dashboard_html)
    print(f"    仪表盘: {dashboard_path}")

    email_path = os.path.join(output_dir, f"ai_daily_email_{actual_date}.html")
    with open(email_path, "w", encoding="utf-8") as f:
        f.write(email_html)
    print(f"    邮件版: {email_path}")

    if dry_run:
        print(f"\n[Dry Run] 跳过推送")
        return

    # 3. 推送
    print("\n>>> 推送邮件...")
    ok = send_via_qqmail(email_html, actual_date)
    print(f"\n{'=' * 50}")
    print(f"  完成 | 邮件: {'✓' if ok else '✗'}")
    print("=" * 50)


if __name__ == "__main__":
    main()
