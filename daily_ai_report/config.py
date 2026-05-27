"""AI 前沿日报 — 配置模块
数据源：AI HOT API + arXiv API（均免费免 Key）
推送：Notion API + QQ邮箱 SMTP（支持多收件人）
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # ─── AI HOT API ───
    AIHOT_BASE_URL: str = os.getenv("AIHOT_BASE_URL", "https://aihot.virxact.com")

    # ─── 邮件推送 ───
    EMAIL_SMTP_HOST: str = os.getenv("EMAIL_SMTP_HOST", "smtp.qq.com")
    EMAIL_SMTP_PORT: int = int(os.getenv("EMAIL_SMTP_PORT", "587"))
    EMAIL_SENDER: str = os.getenv("EMAIL_SENDER", "")
    EMAIL_AUTH_CODE: str = os.getenv("EMAIL_AUTH_CODE", "")

    # EMAIL_RECEIVER 支持逗号分隔的多收件人，如 "a@qq.com,b@gnust.edu.cn"
    _raw_receivers: str = os.getenv("EMAIL_RECEIVER", "")
    EMAIL_RECEIVERS: list[str] = [
        r.strip() for r in _raw_receivers.split(",") if r.strip()
    ]

    # ─── Notion API ───
    NOTION_API_KEY: str = os.getenv("NOTION_API_KEY", "")
    NOTION_DATABASE_ID: str = os.getenv("NOTION_DATABASE_ID", "")

    # ─── 开关 ───
    ENABLE_EMAIL: bool = bool(EMAIL_SENDER and EMAIL_AUTH_CODE and EMAIL_RECEIVERS)
    ENABLE_NOTION: bool = bool(NOTION_API_KEY and NOTION_DATABASE_ID)


cfg = Config()
