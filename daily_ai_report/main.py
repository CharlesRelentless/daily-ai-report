#!/usr/bin/env python3
"""
AI 前沿捕手 Agent — 主入口
每日自动执行：采集 → 筛选 → 生成日报 → QQ邮箱 + Notion 双推送

用法：
    python main.py                  # 一次性执行
    python main.py --dry-run        # 只生成日报，不推送
    python main.py --local          # 仅保存本地文件，不推送
"""
import sys
import os
from datetime import datetime

# 确保能找到同目录模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import cfg
from fetchers import collect_all_raw
from pipeline import run_pipeline
from push import send_via_qqmail, send_via_notion


def main():
    dry_run = "--dry-run" in sys.argv
    local_only = "--local" in sys.argv
    date_str = datetime.now().strftime("%Y-%m-%d")

    print("=" * 60)
    print(f"  AI 前沿捕手 Agent — {date_str}")
    print("=" * 60)

    # 1. 数据采集
    print("\n>>> 正在采集数据...")
    raw_text = collect_all_raw()
    print(f"    采集完成，原始文本约 {len(raw_text)} 字符")

    if not raw_text.strip():
        print("    未采集到任何数据，退出")
        return

    # 2. LLM 流水线
    print("\n>>> 启动 LLM 流水线...")
    selected, report_md = run_pipeline(raw_text, date_str)

    # 3. 保存本地
    output_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, f"daily_report_{date_str}.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"\n>>> 日报已保存: {report_path}")

    if dry_run:
        print("\n[Dry Run] 跳过推送，日报内容如下：\n")
        print(report_md)
        return

    if local_only:
        print("\n[Local Only] 不推送，日报仅保存本地")
        return

    # 4. 推送
    print("\n>>> 开始推送...")
    qq_ok = send_via_qqmail(report_md, date_str)
    notion_ok = send_via_notion(report_md, date_str)

    print("\n" + "=" * 60)
    print(f"  执行完毕 | QQ邮箱: {'✓' if qq_ok else '✗'} | Notion: {'✓' if notion_ok else '✗'}")
    print("=" * 60)


if __name__ == "__main__":
    main()
