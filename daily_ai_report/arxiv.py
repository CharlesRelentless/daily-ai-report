"""AI 前沿日报 — arXiv 论文补充
搜索最近 N 天的 AI/ML 论文，用于填充日报的「论文研究」版块。
"""
import requests
from datetime import datetime, timedelta


def search_recent_papers(days: int = 3, max_results: int = 10) -> list[dict]:
    """通过 arXiv API 搜索最近 AI 论文。返回 title/summary/url/source。"""
    papers = []

    queries = [
        "cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CV",
        "cat:cs.CL",
    ]

    for query in queries:
        url = (
            f"http://export.arxiv.org/api/query"
            f"?search_query={query}"
            f"&sortBy=submittedDate&sortOrder=descending"
            f"&max_results={max_results}"
        )
        try:
            resp = requests.get(url, timeout=20)
            if resp.status_code != 200:
                continue

            import xml.etree.ElementTree as ET
            root = ET.fromstring(resp.text)
            ns = {
                "atom": "http://www.w3.org/2005/Atom",
                "arxiv": "http://arxiv.org/schemas/atom",
            }

            for entry in root.findall("atom:entry", ns):
                title_el = entry.find("atom:title", ns)
                summary_el = entry.find("atom:summary", ns)
                link_el = entry.find("atom:id", ns)
                published_el = entry.find("atom:published", ns)

                title = title_el.text.strip() if title_el is not None else ""
                summary = summary_el.text.strip()[:300] if summary_el is not None else ""
                link = link_el.text.strip() if link_el is not None else ""
                published = published_el.text.strip() if published_el is not None else ""

                if not title or not link:
                    continue

                # 过滤：只看近 N 天
                try:
                    pub_dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
                    cutoff = datetime.now(pub_dt.tzinfo) - timedelta(days=days)
                    if pub_dt < cutoff:
                        continue
                except Exception:
                    pass

                papers.append({
                    "title": title,
                    "summary": summary,
                    "sourceUrl": link,
                    "sourceName": "arXiv",
                })

        except Exception as e:
            print(f"[arXiv] 搜索异常: {e}")
            continue

    # 去重
    seen = set()
    unique = []
    for p in papers:
        if p["sourceUrl"] not in seen:
            seen.add(p["sourceUrl"])
            unique.append(p)

    print(f"[arXiv] 补充 {len(unique)} 篇论文")
    return unique[:max_results]
