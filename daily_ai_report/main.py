#!/usr/bin/env python3
"""AI 前沿日报 — 主入口
AI HOT API + arXiv 补充 → Notion 数据库 → QQ邮箱通知
GitHub Actions 定时运行，无需本地电脑开机。
"""
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from aihot import fetch_daily_report
from arxiv import search_recent_papers
from push import (
    send_via_qqmail,
    send_via_notion,
    build_overview_block,
    build_section_heading,
    build_item_block,
    build_footer,
)
from config import cfg

SECTION_LABELS = [
    "模型发布/更新",
    "产品发布/更新",
    "行业动态",
    "论文研究",
    "技巧与观点",
]

SECTION_KEY_MAP = {
    "模型发布/更新": "模型发布",
    "产品发布/更新": "产品发布",
    "行业动态": "行业动态",
    "论文研究": "论文研究",
    "技巧与观点": "技巧观点",
}


def main():
    dry_run = "--dry-run" in sys.argv
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")

    print("=" * 50)
    print(f"  AI 前沿日报 — {date_str}")
    print(f"  Notion + QQ邮箱 版")
    print("=" * 50)

    # ── 1. 拉取 AI HOT 日报 ──
    print("\n[1/4] 拉取 AI HOT 日报...")
    data = fetch_daily_report()
    if not data:
        print("      AI HOT 不可用，退出")
        return

    sections = data.get("sections", [])
    print(f"      AI HOT: {sum(len(s.get('items', [])) for s in sections)} 条")

    # ── 2. arXiv 补充论文 ──
    print("\n[2/4] arXiv 补充论文...")
    arxiv_papers = search_recent_papers(days=3, max_results=8)
    print(f"      arXiv: {len(arxiv_papers)} 篇")

    # ── 3. 构建内容 ──
    print("\n[3/4] 构建 Notion 内容...")

    # 解析 AI HOT sections
    section_items: dict[str, list] = {}
    for label in SECTION_LABELS:
        section_items[label] = []

    for s in sections:
        label = s.get("label", "")
        if label in section_items:
            section_items[label] = s.get("items", [])

    # 补充论文到「论文研究」
    if arxiv_papers and not section_items.get("论文研究"):
        section_items["论文研究"] = arxiv_papers
    elif arxiv_papers:
        section_items["论文研究"].extend(arxiv_papers)

    # 统计
    section_counts = {}
    aihot_count = 0
    self_count = 0
    for label in SECTION_LABELS:
        items = section_items.get(label, [])
        section_counts[LABEL_TO_KEY(label)] = len(items)
        # 粗略估算 AI HOT vs 自采
        for item in items:
            if item.get("sourceName") == "arXiv":
                self_count += 1
            else:
                aihot_count += 1

    total = sum(section_counts.values())

    # 构建 Notion blocks
    blocks = []

    # 概览
    blocks.append(build_overview_block(total, section_counts, aihot_count, self_count))

    # 五个版块
    global_num = 0
    for label in SECTION_LABELS:
        blocks.append(build_section_heading(label))
        items = section_items.get(label, [])
        if not items:
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": "本期暂无"}}]
                },
            })
            continue
        for item in items:
            global_num += 1
            badge = "自采" if item.get("sourceName") == "arXiv" else "AI HOT"
            blocks.append(build_item_block(global_num, item, badge))

    # 文末
    blocks.append(build_footer(total))
    blocks.append({
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {"type": "text", "text": {"content": f"共 {total} 条 · 数据来自 AI HOT & arXiv"}}
            ]
        },
    })

    if dry_run:
        print(f"      [Dry Run] 跳过推送，共 {total} 条")
        return

    # ── 4. 推送 ──
    print("\n[4/4] 推送...")

    # Notion
    page_url = send_via_notion(
        date_str=date_str,
        section_counts=section_counts,
        total=total,
        aihot_count=aihot_count,
        self_count=self_count,
        content_blocks=blocks,
    )

    if not page_url:
        print("      Notion 创建失败，但继续发送邮件通知...")
        page_url = "(Notion 不可用)"

    # QQ邮箱
    send_via_qqmail(
        date_str=date_str,
        total=total,
        section_counts=section_counts,
        notion_url=page_url,
    )

    print(f"\n{'=' * 50}")
    print(f"  完成 ✓")
    if page_url and page_url != "(Notion 不可用)":
        print(f"  Notion: {page_url}")
    print("=" * 50)


def LABEL_TO_KEY(label: str) -> str:
    """中文版块 label → 数据库属性 key。"""
    return SECTION_KEY_MAP.get(label, label)


if __name__ == "__main__":
    main()
