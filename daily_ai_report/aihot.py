"""
AI 前沿日报 — AI HOT API 数据获取
https://aihot.virxact.com — 每日 08:00 自动生成，编辑精选 + LLM 摘要，5 个固定版块。
"""
import requests
from config import cfg

BASE_URL = "https://aihot.virxact.com"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"


def fetch_daily_report(date_str: str = None) -> dict | None:
    """获取指定日期日报，无则回退最近一期。"""
    headers = {"User-Agent": UA}

    url = f"{BASE_URL}/api/public/daily"
    if date_str:
        url = f"{BASE_URL}/api/public/daily/{date_str}"

    resp = requests.get(url, headers=headers, timeout=15)
    if resp.status_code == 200:
        return resp.json()

    # 404 -> 回退最近一期
    if resp.status_code == 404:
        dailies_resp = requests.get(
            f"{BASE_URL}/api/public/dailies?take=3",
            headers=headers, timeout=15
        )
        if dailies_resp.status_code == 200:
            dailies = dailies_resp.json()
            items = dailies.get("items", []) if isinstance(dailies, dict) else dailies
            if isinstance(items, list) and items:
                latest_date = items[0].get("date")
                if latest_date:
                    return fetch_daily_report(latest_date)
        return None

    print(f"[AI HOT] 请求失败 HTTP {resp.status_code}")
    return None
