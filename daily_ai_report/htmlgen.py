#!/usr/bin/env python3
"""
AI 前沿日报 — HTML 生成器
从 Notion 数据库回读最新日报 → 静态 HTML → GitHub Pages。
"""
import os
import requests

NOTION_API_KEY = os.environ["NOTION_API_KEY"]
DATABASE_ID = "3690725a-bcba-811d-a5fc-db9d9fa62f6e"
HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}


def get_latest_page():
    resp = requests.post(
        f"https://api.notion.com/v1/databases/{DATABASE_ID}/query",
        json={"sorts": [{"property": "日期", "direction": "descending"}], "page_size": 1},
        headers=HEADERS,
    )
    resp.raise_for_status()
    results = resp.json().get("results", [])
    if not results:
        raise RuntimeError("No pages in database")
    return results[0]["id"], results[0].get("properties", {})


def get_page_blocks(page_id):
    """获取页面所有块，并递归拉取子块。"""
    blocks = _fetch_blocks(page_id)
    # 递归获取子块
    for b in blocks:
        if b.get("has_children"):
            b["children"] = _fetch_blocks(b["id"])
    return blocks


def _fetch_blocks(block_or_page_id):
    """拉取某个 block/page 的所有直接子块。"""
    blocks, cursor = [], None
    while True:
        params = {"page_size": 100}
        if cursor:
            params["start_cursor"] = cursor
        resp = requests.get(
            f"https://api.notion.com/v1/blocks/{block_or_page_id}/children",
            params=params, headers=HEADERS,
        )
        resp.raise_for_status()
        data = resp.json()
        blocks.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")
    return blocks


def extract_prop(props, key):
    prop = props.get(key, {})
    ptype = prop.get("type", "")
    if ptype == "title":
        return "".join(t.get("plain_text", "") for t in prop.get("title", []))
    if ptype == "number":
        return prop.get("number", 0) or 0
    if ptype == "date":
        return prop.get("date", {}).get("start", "")
    if ptype == "select":
        return prop.get("select", {}).get("name", "")
    return None


def block_to_html(block):
    btype = block.get("type", "")
    content = block.get(btype, {})
    rich_text = content.get("rich_text", [])

    if btype == "quote":
        text = "".join(t.get("plain_text", "") for t in rich_text)
        return f'<div class="overview">{text.replace(chr(10), "<br>")}</div>'

    if btype == "heading_2":
        text = "".join(t.get("plain_text", "") for t in rich_text)
        return f"<h2>{text}</h2>"

    if btype == "bulleted_list_item":
        parts = []
        for rt in rich_text:
            txt = rt.get("plain_text", "")
            ann = rt.get("annotations", {})
            if ann.get("code"):
                color = ann.get("color", "default")
                parts.append(f'<span class="badge badge-{color}">{txt}</span>')
            elif ann.get("bold"):
                parts.append(f"<span>{txt}</span>")
            else:
                parts.append(txt)
        main_html = "".join(parts).rstrip()

        children_html = ""
        children = block.get("children", [])
        for child in children:
            ctype = child.get("type", "")
            cbody = child.get(ctype, {})
            for c in cbody.get("rich_text", []):
                ctext = c.get("plain_text", "")
                link = c.get("text", {}).get("link")
                if link and link.get("url"):
                    children_html += f' <a href="{link["url"]}" target="_blank" rel="noopener">{ctext}</a>'
                elif ctext.strip():
                    children_html += ctext

        if children_html.strip():
            children_html = f'<div class="item-detail">{children_html.strip()}</div>'

        cls = "item" if children_html else "item no-detail"
        return f'<li class="{cls}">{main_html}{children_html}</li>'

    if btype == "paragraph":
        text = "".join(t.get("plain_text", "") for t in rich_text)
        return f"<p>{text}</p>" if text.strip() else ""

    if btype == "divider":
        return "<hr>"
    return ""


def extract_stats(props):
    sections = {}
    for key in ["模型发布", "产品发布", "行业动态", "论文研究", "技巧观点"]:
        sections[key] = extract_prop(props, key) or 0
    total = extract_prop(props, "总条数") or sum(sections.values())
    return {
        "title": extract_prop(props, "标题") or "",
        "date": extract_prop(props, "日期") or "",
        "total": int(total) if total else 0,
        "sections": {k: int(v) if v else 0 for k, v in sections.items()},
        "source": extract_prop(props, "数据来源") or "",
    }


CSS = """  :root { --bg:#fafafa; --card:#fff; --text:#1a1a1a; --muted:#888; --border:#eee; --blue:#2563eb; --purple:#7c3aed; --orange:#ea580c; }
  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--text);line-height:1.75;max-width:720px;margin:0 auto;padding:24px 16px 60px}
  .header{text-align:center;padding:40px 0 32px;border-bottom:2px solid var(--border);margin-bottom:32px}
  .header h1{font-size:28px;margin-bottom:8px}
  .header .date{color:var(--muted);font-size:14px}
  .stat-bar{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:20px 0 0}
  .stat-item{background:#f3f4f6;padding:4px 12px;border-radius:20px;font-size:13px;color:#555}
  .overview{background:#eff6ff;border-left:4px solid var(--blue);padding:16px 20px;border-radius:0 8px 8px 0;margin-bottom:36px;font-size:15px;line-height:1.9}
  h2{font-size:20px;margin:36px 0 16px;padding-bottom:8px;border-bottom:1px solid var(--border)}
  ul{list-style:none}
  .item{background:var(--card);border-radius:8px;padding:14px 18px;margin-bottom:10px;border:1px solid var(--border);transition:box-shadow .15s}
  .item:hover{box-shadow:0 2px 8px rgba(0,0,0,.06)}
  .badge{display:inline-block;font-family:monospace;font-size:11px;padding:1px 7px;border-radius:4px;margin-right:6px;vertical-align:1px}
  .badge-orange{background:#fff7ed;color:var(--orange)}
  .badge-purple{background:#f5f3ff;color:var(--purple)}
  .badge-blue{background:#eff6ff;color:var(--blue)}
  .badge-green{background:#f0fdf4;color:#16a34a}
  .badge-default{background:#f3f4f6;color:#555}
  .item-detail{margin-top:8px;font-size:14px;color:var(--muted);line-height:1.6}
  .item-detail a{color:var(--blue);text-decoration:none;border-bottom:1px dashed var(--blue)}
  .item-detail a:hover{border-bottom-style:solid}
  hr{margin:40px 0 20px;border:none;border-top:1px solid var(--border)}
  .footer{text-align:center;font-size:13px;color:var(--muted);padding:20px 0}
  .footer a{color:var(--muted)}
  p{margin:8px 0}
  @media(max-width:480px){body{padding:12px 10px 40px}.header{padding:28px 0 24px}.header h1{font-size:22px}.item{padding:12px 14px}}"""


def generate_html(blocks, stats):
    body_parts = [block_to_html(b) for b in blocks if block_to_html(b).strip()]
    body_content = "\n".join(body_parts)

    stat_items = "".join(
        f'<span class="stat-item">{k[:2]} {v}</span>'
        for k, v in stats["sections"].items()
    )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{stats['title']}</title>
<style>{CSS}</style>
</head>
<body>
<div class="header">
<h1>🤖 {stats['title']}</h1>
<div class="date">{stats['date']}</div>
<div class="stat-bar">
<span class="stat-item">📊 共 {stats['total']} 条</span>
{stat_items}
<span class="stat-item">🏷️ {stats['source']}</span>
</div>
</div>
{body_content}
<div class="footer">
<hr>
<p>数据来源 AI HOT · arXiv · 每日 08:30 自动更新</p>
<p><a href="#">↑ 回到顶部</a></p>
</div>
</body>
</html>"""


def main():
    print("[htmlgen] 从 Notion 获取最新日报...")
    page_id, props = get_latest_page()
    stats = extract_stats(props)
    print(f"  {stats['title']} ({stats['date']}), 共 {stats['total']} 条")

    print("[htmlgen] 获取页面 blocks (含子块递归)...")
    blocks = get_page_blocks(page_id)
    print(f"  共 {len(blocks)} 个顶层 block")

    html = generate_html(blocks, stats)
    os.makedirs("public", exist_ok=True)
    with open("public/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[htmlgen] ✓ public/index.html ({len(html)} bytes)")


if __name__ == "__main__":
    main()
