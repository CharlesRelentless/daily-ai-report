"""
AI 前沿捕手 Agent — 配置模块
数据源：AI HOT API（无需 LLM Key）
推送：通用 SMTP 邮件
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # ─── AI HOT API ───
    AIHOT_BASE_URL: str = os.getenv("AIHOT_BASE_URL", "https://aihot.virxact.com")

    # ─── 邮件推送（支持 QQ / Gmail / 任意 SMTP） ───
    EMAIL_SMTP_HOST: str = os.getenv("EMAIL_SMTP_HOST", "smtp.gmail.com")
    EMAIL_SMTP_PORT: int = int(os.getenv("EMAIL_SMTP_PORT", "587"))
    EMAIL_SENDER: str = os.getenv("EMAIL_SENDER", "")
    EMAIL_AUTH_CODE: str = os.getenv("EMAIL_AUTH_CODE", "")
    EMAIL_RECEIVER: str = os.getenv("EMAIL_RECEIVER", "")

    # ─── 推送开关 ───
    ENABLE_EMAIL: bool = bool(EMAIL_SENDER and EMAIL_AUTH_CODE and EMAIL_RECEIVER)


cfg = Config()
