"""
AI 前沿捕手 Agent — 推送模块
QQ邮箱 SMTP + Notion API 双通道推送。
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import cfg


# ═══════════════════════════════════════════════════════════════
# QQ邮箱推送
# ═══════════════════════════════════════════════════════════════

def send_via_qqmail(report_md: str, date_str: str = None) -> bool:
    """通过 QQ邮箱 SMTP 发送日报。"""
    if not cfg.ENABLE_QQMAIL:
        print("[QQ邮箱] 未配置，跳过推送")
        return False

    date_str = date_str or datetime.now().strftime("%Y-%m-%d")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"【AI 前沿日报 | {date_str}】"
    msg["From"] = cfg.QQMAIL_SENDER
    msg["To"] = cfg.QQMAIL_RECEIVER

    # 纯文本 + HTML 双版本
    text_part = MIMEText(report_md, "plain", "utf-8")
    html_report = _md_to_html(report_md)
    html_part = MIMEText(html_report, "html", "utf-8")
    msg.attach(text_part)
    msg.attach(html_part)

    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=15)
        server.login(cfg.QQMAIL_SENDER, cfg.QQMAIL_AUTH_CODE)
        server.sendmail(cfg.QQMAIL_SENDER, cfg.QQMAIL_RECEIVER, msg.as_string())
        server.quit()
        print(f"[QQ邮箱] 日报已发送至 {cfg.QQMAIL_RECEIVER}")
        return True
    except Exception as e:
        print(f"[QQ邮箱] 发送失败: {e}")
        return False


def _md_to_html(md: str) -> str:
    """将简单 Markdown 转为 HTML 邮件格式。"""
    html = md
    # 标题
    html = html.replace("# 【", '<h2 style="color:#1a73e8;">【')
    html = html.replace("# ", "<h3>")
    # 二级标题
    html = html.replace("## ", '<h3 style="color:#333;border-bottom:1px solid #eee;padding-bottom:4px;">')
    # 粗体
    import re
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    # 链接
    html = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" style="color:#1a73e8;">\1</a>", html')
    # 引用
    html = html.replace("> *", '<p style="color:#888;font-size:13px;"><em>')
    html = html.replace("*</p>", "</em></p>") if html.endswith("*</p>") else html
    # 列表
    html = html.replace("- ", '<li style="margin:6px 0;">')
    html = re.sub(r"(<li.*?</li>)", r"\1", html)  # no-op, just outline
    # 换行
    html = html.replace("\n\n", "<br><br>")
    html = html.replace("\n", "<br>")

    wrapper = f"""<html><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:680px;margin:0 auto;padding:20px;line-height:1.7;color:#333;">
{html}
</body></html>"""
    return wrapper


# ═══════════════════════════════════════════════════════════════
# Notion 推送
# ═══════════════════════════════════════════════════════════════

def send_via_notion(report_md: str, date_str: str = None) -> bool:
    """通过 Notion API 将日报写入指定数据库。"""
    if not cfg.ENABLE_NOTION:
        print("[Notion] 未配置，跳过推送")
        return False

    date_str = date_str or datetime.now().strftime("%Y-%m-%d")

    payload = {
        "parent": {"database_id": cfg.NOTION_DATABASE_ID},
        "properties": {
            "Name": {
                "title": [{"text": {"content": f"AI 前沿日报 {date_str}"}}]
            },
            "Date": {
                "date": {"start": date_str}
            },
        },
        "children": _md_to_notion_blocks(report_md),
    }

    headers = {
        "Authorization": f"Bearer {cfg.NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    try:
        import requests
        r = requests.post(
            "https://api.notion.com/v1/pages",
            json=payload,
            headers=headers,
            timeout=20,
        )
        r.raise_for_status()
        page_url = r.json().get("url", "N/A")
        print(f"[Notion] 日报已创建: {page_url}")
        return True
    except Exception as e:
        print(f"[Notion] 推送失败: {e}")
        return False


def _md_to_notion_blocks(md: str) -> list[dict]:
    """将 Markdown 切分为 Notion 块。简单分段处理。"""
    blocks = []
    lines = md.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("# "):
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                },
            })
        elif line.startswith("## "):
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": line[3:]}}]
                },
            })
        elif line.startswith("- "):
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                },
            })
        elif line.startswith("> "):
            blocks.append({
                "object": "block",
                "type": "quote",
                "quote": {
                    "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                },
            })
        elif line.startswith("![") or line.startswith("["):
            # 跳过图片和链接行，纯文本已足够
            pass
        else:
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": line}}]
                },
            })
    return blocks
