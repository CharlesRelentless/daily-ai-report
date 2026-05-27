"""AI 前沿日报 — 配置模块"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    AIHOT_BASE_URL: str = os.getenv("AIHOT_BASE_URL", "https://aihot.virxact.com")

    # ─── 邮件 ───
    EMAIL_SMTP_HOST: str = os.getenv("EMAIL_SMTP_HOST", "smtp.qq.com")
    EMAIL_SMTP_PORT: int = int(os.getenv("EMAIL_SMTP_PORT", "587"))
    EMAIL_SENDER: str = os.getenv("EMAIL_SENDER", "")
    EMAIL_AUTH_CODE: str = os.getenv("EMAIL_AUTH_CODE", "")
    EMAIL_RECEIVER: str = os.getenv("EMAIL_RECEIVER", "")

    # 抄送地址（硬编码，不涉密）
    EMAIL_CC: list[str] = ["9320240059@gnust.edu.cn"]

    @property
    def EMAIL_ALL_RECIPIENTS(self) -> list[str]:
        recips = [self.EMAIL_RECEIVER] if self.EMAIL_RECEIVER else []
        recips.extend(self.EMAIL_CC)
        return recips

    # ─── Notion ───
    NOTION_API_KEY: str = os.getenv("NOTION_API_KEY", "")

    # ─── 开关 ───
    ENABLE_EMAIL: bool = bool(EMAIL_SENDER and EMAIL_AUTH_CODE and EMAIL_RECEIVER)
    ENABLE_NOTION: bool = bool(NOTION_API_KEY)


cfg = Config()
