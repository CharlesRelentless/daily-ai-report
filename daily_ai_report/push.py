"""AI 前沿日报 — 推送模块
Notion API（主）+ QQ邮箱 SMTP（通知链接）。
"""
import smtplib
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import cfg


# ═══════════════════════════════════════
# QQ邮箱 — 发送 Notion 链接通知
# ═══════════════════════════════════════

def send_via_qqmail(date_str: str, total: int, section_counts: dict, notion_url: str) -> bool:
    """发送一封极简通知邮件，只含统计 + Notion 链接。"""
    if not cfg.ENABLE_EMAIL:
        print("[邮件] 未配置，跳过")
        return False

    body = f"""2026 年 5 月 22 日 AI 日报已生成。

📊 模型 {section_counts.get('模型发布', 0)} · 产品 {section_counts.get('产品发布', 0)} · 行业 {section_counts.get('行业动态', 0)} · 论文 {section_counts.get('论文研究', 0)} · 观点 {section_counts.get('技巧观点', 0)}
🏷️ AI HOT 精选 + arXiv 补充

📎 {notion_url}

⏰ 数据来源 AI HOT & arXiv"""
    # Replace date in body dynamically
    body = body.replace("2026 年 5 月 22 日", datetime.now().strftime("%Y 年 %-m 月 %-d 日"))

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🤖 AI 晨报 · {date_str} — 共 {total} 条"
        msg["From"] = cfg.EMAIL_SENDER
        msg["To"] = cfg.EMAIL_RECEIVER

        text_part = MIMEText(body, "plain", "utf-8")
        html_body = body.replace("\n", "<br>")
        html_part = MIMEText(
            f"<html><body style='font-family:sans-serif;padding:20px;line-height:1.8;'>{html_body}</body></html>",
            "html", "utf-8"
        )
        msg.attach(text_part)
        msg.attach(html_part)

        server = smtplib.SMTP(cfg.EMAIL_SMTP_HOST, cfg.EMAIL_SMTP_PORT, timeout=15)
        server.starttls()
        server.login(cfg.EMAIL_SENDER, cfg.EMAIL_AUTH_CODE)
        server.sendmail(cfg.EMAIL_SENDER, cfg.EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print(f"[邮件] 已发送至 {cfg.EMAIL_RECEIVER}")
        return True
    except Exception as e:
        print(f"[邮件] 发送失败: {e}")
        traceback.print_exc()
        return False


# ═══════════════════════════════════════
# Notion API — 写入数据库
# ═══════════════════════════════════════

def send_via_notion(
    date_str: str,
    section_counts: dict,
    total: int,
    aihot_count: int,
    self_count: int,
    content_blocks: list[dict],
) -> str | None:
    """通过 Notion API 创建数据库页面。返回页面 URL。"""
    if not cfg.ENABLE_NOTION:
        print("[Notion] 未配置，跳过")
        return None

    headers = {
        "Authorization": f"Bearer {cfg.NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    # 1. 创建页面
    page_payload = {
        "parent": {"database_id": cfg.NOTION_DATABASE_ID},
        "properties": {
            "标题": {
                "title": [{"text": {"content": f"AI 晨报 · {date_str}"}}]
            },
            "日期": {
                "date": {"start": date_str}
            },
            "总条数": {
                "number": total
            },
            "模型发布": {
                "number": section_counts.get("模型发布", 0)
            },
            "产品发布": {
                "number": section_counts.get("产品发布", 0)
            },
            "行业动态": {
                "number": section_counts.get("行业动态", 0)
            },
            "论文研究": {
                "number": section_counts.get("论文研究", 0)
            },
            "技巧观点": {
                "number": section_counts.get("技巧观点", 0)
            },
            "数据来源": {
                "select": {"name": "多源聚合"}
            },
        },
        "children": content_blocks,
    }

    try:
        import requests
        r = requests.post(
            "https://api.notion.com/v1/pages",
            json=page_payload,
            headers=headers,
            timeout=20,
        )
        r.raise_for_status()
        page_url = r.json().get("url", "")
        print(f"[Notion] 页面已创建: {page_url}")
        return page_url
    except Exception as e:
        detail = ""
        if hasattr(e, "response") and e.response is not None:
            detail = e.response.text[:500]
        print(f"[Notion] 创建失败: {e} | {detail}")
        traceback.print_exc()
        return None


def build_overview_block(total: int, section_counts: dict, aihot_count: int, self_count: int) -> dict:
    """构建概览 callout 块。"""
    parts = [f"共 {total} 条"]
    for label, key in [
        ("模型", "模型发布"), ("产品", "产品发布"),
        ("行业", "行业动态"), ("论文", "论文研究"), ("观点", "技巧观点")
    ]:
        parts.append(f"{label} {section_counts.get(key, 0)}")
    text = " | ".join(parts)

    return {
        "object": "block",
        "type": "quote",
        "quote": {
            "rich_text": [
                {"type": "text", "text": {"content": f"📊 今日概览 — {text}"}},
                {"type": "text", "text": {"content": f"\n🏷️ AI HOT {aihot_count} 条 + arXiv 补充 {self_count} 条"}},
            ]
        },
    }


def build_section_heading(label: str) -> dict:
    """构建版块标题块。"""
    icons = {
        "模型发布/更新": "🤖",
        "产品发布/更新": "🚀",
        "行业动态": "🌐",
        "论文研究": "📄",
        "技巧与观点": "💡",
    }
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{"type": "text", "text": {"content": f"{icons.get(label, '')} {label}"}}]
        },
    }


def build_item_block(num: int, item: dict, badge: str) -> dict:
    """构建单条资讯 bullet 块（含子块：摘要 + 链接）。"""
    title = item.get("title", "")
    source = item.get("sourceName", "")
    summary = item.get("summary", "")[:120]
    url = item.get("sourceUrl", "")

    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": [
                {"type": "text", "text": {"content": f"{badge} "},
                 "annotations": {"code": True, "color": "orange" if badge == "AI HOT" else "purple"}},
                {"type": "text", "text": {"content": f"{num}. {title} — {source}"},
                 "annotations": {"bold": True}},
            ],
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": summary}}]
                    },
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {"type": "text", "text": {"content": "↗ 原文", "link": {"url": url}}}
                        ]
                    },
                },
            ],
        },
    }


def build_footer(total: int) -> dict:
    """构建文末分隔线 + 来源标注。"""
    return {
        "object": "block",
        "type": "divider",
        "divider": {},
    }
