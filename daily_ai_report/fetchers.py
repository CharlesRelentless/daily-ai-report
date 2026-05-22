"""
AI 前沿捕手 Agent — 数据采集模块
四大数据源 + 研究方向专属查询 → 拼接原始信息大文本。
"""
import json
import requests
import feedparser
from datetime import datetime, timedelta
from config import cfg


# ═══════════════════════════════════════════════════════════════
# 1. ArXiv 论文采集（通用 AI + 遥感滑坡专属）
# ═══════════════════════════════════════════════════════════════

def fetch_arxiv_papers_general(max_results: int = None) -> list[dict]:
    """通用 AI 前沿论文"""
    max_results = max_results or cfg.ARXIV_MAX_RESULTS
    query = "(large language model OR AI agent OR autonomous agent OR multimodal model OR computer vision OR deep learning)"
    return _arxiv_query(query, max_results)


def fetch_arxiv_papers_research(max_results: int = 5) -> list[dict]:
    """研究方向专属论文（遥感 + 滑坡检测）"""
    query = " OR ".join(f'all:"{kw}"' for kw in cfg.RESEARCH_KEYWORDS[:5])
    return _arxiv_query(query, max_results)


def _arxiv_query(query: str, max_results: int) -> list[dict]:
    url = (
        f"http://export.arxiv.org/api/query?"
        f"search_query={query}"
        f"&start=0&max_results={max_results}"
        f"&sortBy=submittedDate&sortOrder=descending"
    )
    feed = feedparser.parse(url)
    papers = []
    for entry in feed.entries:
        papers.append({
            "title": entry.title.strip().replace("\n", " "),
            "summary": entry.summary.strip().replace("\n", " "),
            "link": entry.link,
            "published": entry.published,
        })
    return papers


# ═══════════════════════════════════════════════════════════════
# 2. GitHub Trending（Agent / 开源项目）
# ═══════════════════════════════════════════════════════════════

def fetch_github_trending(max_results: int = None) -> list[dict]:
    max_results = max_results or cfg.GITHUB_MAX_RESULTS
    date_7d_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    url = (
        f"https://api.github.com/search/repositories?"
        f"q=agent OR llm OR autonomous OR deep-learning created:>{date_7d_ago}"
        f"&sort=stars&order=desc&per_page={max_results}"
    )
    headers = {"Accept": "application/vnd.github.v3+json"}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        items = r.json().get("items", [])
    except Exception:
        return []
    repos = []
    for item in items:
        repos.append({
            "name": item.get("full_name", ""),
            "description": item.get("description", ""),
            "url": item.get("html_url", ""),
            "stars": item.get("stargazers_count", 0),
        })
    return repos


# ═══════════════════════════════════════════════════════════════
# 3. Hacker News 热门
# ═══════════════════════════════════════════════════════════════

def fetch_hn_top_stories(limit: int = None) -> list[dict]:
    limit = limit or cfg.HN_TOP_LIMIT
    try:
        top = requests.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10
        ).json()
    except Exception:
        return []
    stories = []
    for sid in top[: limit * 2]:
        try:
            item = requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{sid}.json", timeout=10
            ).json()
        except Exception:
            continue
        if item and "title" in item:
            stories.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "score": item.get("score", 0),
                "descendants": item.get("descendants", 0),
            })
    return stories


# ═══════════════════════════════════════════════════════════════
# 4. RSS 官方博客
# ═══════════════════════════════════════════════════════════════

def fetch_rss_feeds(urls: list[str] = None) -> list[dict]:
    urls = urls or cfg.RSS_FEEDS
    entries = []
    for url in urls:
        try:
            feed = feedparser.parse(url)
        except Exception:
            continue
        for entry in feed.entries[:3]:
            entries.append({
                "source": feed.feed.get("title", url),
                "title": entry.title,
                "link": entry.link,
                "summary": getattr(entry, "summary", "")[:300],
            })
    return entries


# ═══════════════════════════════════════════════════════════════
# 汇总
# ═══════════════════════════════════════════════════════════════

def collect_all_raw() -> str:
    """采集所有数据源，拼接为原始信息大文本。"""
    parts = []

    # ArXiv — 通用
    papers_general = fetch_arxiv_papers_general()
    parts.append("=== ArXiv 通用 AI 前沿 ===\n" + json.dumps(papers_general, ensure_ascii=False))
    # ArXiv — 研究方向
    papers_research = fetch_arxiv_papers_research()
    parts.append("=== ArXiv 研究方向（遥感/滑坡检测） ===\n" + json.dumps(papers_research, ensure_ascii=False))
    # GitHub
    repos = fetch_github_trending()
    parts.append("=== GitHub Trending ===\n" + json.dumps(repos, ensure_ascii=False))
    # HN
    stories = fetch_hn_top_stories()
    parts.append("=== Hacker News ===\n" + json.dumps(stories, ensure_ascii=False))
    # RSS
    rss = fetch_rss_feeds()
    parts.append("=== 官方博客 RSS ===\n" + json.dumps(rss, ensure_ascii=False))

    return "\n\n".join(parts)
