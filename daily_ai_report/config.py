"""
AI 前沿捕手 Agent — 配置模块
加载 .env 环境变量，提供统一配置入口。
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # ─── LLM ───
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")

    # ─── QQ邮箱 ───
    QQMAIL_SENDER: str = os.getenv("QQMAIL_SENDER", "")
    QQMAIL_AUTH_CODE: str = os.getenv("QQMAIL_AUTH_CODE", "")
    QQMAIL_RECEIVER: str = os.getenv("QQMAIL_RECEIVER", "")

    # ─── Notion ───
    NOTION_API_KEY: str = os.getenv("NOTION_API_KEY", "")
    NOTION_DATABASE_ID: str = os.getenv("NOTION_DATABASE_ID", "")

    # ─── 研究方向关键词 ───
    RESEARCH_KEYWORDS: list[str] = [
        kw.strip()
        for kw in os.getenv(
            "RESEARCH_KEYWORDS",
            "landslide detection,remote sensing,semantic segmentation,SAR,deep learning,object detection,change detection",
        ).split(",")
        if kw.strip()
    ]

    # ─── 数据采集参数 ───
    ARXIV_MAX_RESULTS: int = 10
    GITHUB_MAX_RESULTS: int = 5
    HN_TOP_LIMIT: int = 20
    RSS_FEEDS: list[str] = [
        "https://openai.com/blog/rss.xml",
        "https://www.anthropic.com/blog/rss.xml",
        "https://blog.google/technology/ai/rss/",
    ]

    # ─── 推送开关 ───
    ENABLE_QQMAIL: bool = bool(QQMAIL_SENDER and QQMAIL_AUTH_CODE and QQMAIL_RECEIVER)
    ENABLE_NOTION: bool = bool(NOTION_API_KEY and NOTION_DATABASE_ID)


cfg = Config()
