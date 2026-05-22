"""AI 前沿日报 — 配置模块
数据源：AI HOT API + arXiv API（均免费免 Key）
推送：Notion API + QQ邮箱 SMTP
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
    EMAIL_RECEIVER: str = os.getenv("EMAIL_RECEIVER", "")

    # ─── Notion API ───
    NOTION_API_KEY: str = os.getenv("NOTION_API_KEY", "")
    NOTION_DATABASE_ID: str = os.getenv("NOTION_DATABASE_ID", "")

    # ─── 开关 ───
    ENABLE_EMAIL: bool = bool(EMAIL_SENDER and EMAIL_AUTH_CODE and EMAIL_RECEIVER)
    ENABLE_NOTION: bool = bool(NOTION_API_KEY and NOTION_DATABASE_ID)


cfg = Config()
