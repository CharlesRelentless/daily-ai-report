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

    # 主收件人
    EMAIL_RECEIVER: str = os.getenv("EMAIL_RECEIVER", "")

    # 抄送（逗号分隔，可选）如 "a@qq.com,b@gnust.edu.cn"
    _raw_cc: str = os.getenv("EMAIL_CC", "")
    EMAIL_CC: list[str] = [r.strip() for r in _raw_cc.split(",") if r.strip()]

    # 实际发送的完整收件人列表（主 + CC）
    @property
    def EMAIL_ALL_RECIPIENTS(self) -> list[str]:
        recips = [self.EMAIL_RECEIVER] if self.EMAIL_RECEIVER else []
        recips.extend(self.EMAIL_CC)
        return recips

    # ─── Notion API ───
    NOTION_API_KEY: str = os.getenv("NOTION_API_KEY", "")
    NOTION_DATABASE_ID: str = os.getenv("NOTION_DATABASE_ID", "")

    # ─── 开关 ───
    ENABLE_EMAIL: bool = bool(EMAIL_SENDER and EMAIL_AUTH_CODE and EMAIL_RECEIVER)
    ENABLE_NOTION: bool = bool(NOTION_API_KEY and NOTION_DATABASE_ID)


cfg = Config()
