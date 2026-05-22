"""
AI 前沿捕手 Agent — HTML 生成模块
输入 AI HOT API 日报数据 → 输出双版 HTML：完整仪表盘 + Gmail 安全版。
"""
from datetime import datetime
import json

# ─── 分类色标 / 图标 ───
CATEGORY_STYLE = {
    "模型发布/更新": {"color": "#e04030", "icon": "🧠"},
    "产品发布/更新": {"color": "#f58220", "icon": "🚀"},
    "行业动态":       {"color": "#2d8cf0", "icon": "📡"},
    "论文研究":       {"color": "#7b4fbf", "icon": "📄"},
    "技巧与观点":     {"color": "#19be6b", "icon": "💡"},
}

CSS_VARS = """
  --gradient-start: #ff5e3a;
  --gradient-mid:   #ff7b47;
  --gradient-end:   #ff6b35;
  --hero-bg-start:  #1a0a00;
  --hero-bg-end:    #2d1200;
  --card-bg:        #ffffff;
  --card-border:    #f0e6e0;
  --accent:         #e8552d;
"""


def generate_dashboard_html(data: dict) -> str:
    """生成完整交互式 HTML 仪表盘（浏览器预览）。"""
    date_str = data.get("date", datetime.now().strftime("%Y-%m-%d"))
    sections = data.get("sections", [])
    flashes = data.get("flashes", [])
    lead = data.get("lead")

    # 全局编号
    total_items = sum(len(s.get("items", [])) for s in sections)
    seq = 0

    sections_html = _build_sections_html(sections, lambda: _next_seq())
    nav_html = _build_nav_html(sections)
    hero_html = _build_hero_html(date_str, total_items, sections, lead)
    flashes_html = _build_flashes_html(flashes)

    # 准备内联 JSON 数据（供 JS 动画等）
    items_json = _collect_items_json(sections)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI 前沿日报 | {date_str}</title>
<style>
:root {{ {CSS_VARS} }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif; background:#faf5f2; color:#2c1810; line-height:1.6; }}
.container {{ max-width:1100px; margin:0 auto; padding:0 20px; }}

/* Hero */
.hero {{ background:linear-gradient(135deg,var(--hero-bg-start),var(--hero-bg-end)); color:#fff; padding:48px 0 36px; position:relative; overflow:hidden; }}
.hero::before {{ content:""; position:absolute; top:-80px; right:-80px; width:320px; height:320px; background:radial-gradient(circle,rgba(255,94,58,.25),transparent 70%); border-radius:50%; }}
.hero-date {{ font-size:13px; opacity:.7; letter-spacing:1px; }}
.hero-title {{ font-size:32px; font-weight:800; margin:8px 0 16px; background:linear-gradient(90deg,#ff8a65,#ffb74d); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }}
.hero-stats {{ display:flex; gap:20px; flex-wrap:wrap; margin-top:16px; }}
.hero-stat {{ text-align:center; }}
.hero-stat-num {{ font-size:40px; font-weight:900; background:linear-gradient(180deg,#ff8a65,#fff); -webkit-background-clip:text; -webkit-text-fill-color:transparent; line-height:1; }}
.hero-stat-label {{ font-size:12px; opacity:.6; margin-top:4px; }}
.hero-pills {{ display:flex; gap:8px; flex-wrap:wrap; margin-top:16px; }}
.hero-pill {{ display:flex; align-items:center; gap:5px; background:rgba(255,255,255,.1); border-radius:20px; padding:4px 14px; font-size:12px; }}
.hero-pill-dot {{ width:8px; height:8px; border-radius:50%; flex-shrink:0; }}

/* Lead */
.lead {{ background:linear-gradient(135deg,#fff8f5,#fff3ee); border-left:4px solid var(--accent); padding:20px 24px; margin:24px auto; border-radius:0 12px 12px 0; max-width:1100px; }}
.lead-title {{ font-size:15px; font-weight:700; color:var(--accent); margin-bottom:6px; }}
.lead-text {{ font-size:14px; color:#6b4c3b; line-height:1.7; }}

/* Nav */
.nav {{ position:sticky; top:0; z-index:100; background:rgba(255,255,255,.92); backdrop-filter:blur(12px); border-bottom:1px solid #f0e6e0; padding:10px 0; }}
.nav-inner {{ display:flex; gap:4px; flex-wrap:wrap; max-width:1100px; margin:0 auto; padding:0 20px; }}
.nav-link {{ padding:6px 14px; border-radius:18px; font-size:13px; color:#8c7268; text-decoration:none; transition:all .2s; white-space:nowrap; }}
.nav-link:hover,.nav-link.active {{ background:rgba(255,94,58,.1); color:var(--accent); }}
.nav-badge {{ font-size:11px; background:rgba(255,94,58,.15); color:var(--accent); padding:1px 7px; border-radius:10px; margin-left:4px; }}

/* Section */
.section {{ padding:32px 0; }}
.section-header {{ display:flex; align-items:center; gap:10px; margin-bottom:20px; }}
.section-icon {{ font-size:24px; }}
.section-title {{ font-size:20px; font-weight:700; }}
.section-count {{ font-size:13px; color:#b8a094; margin-left:8px; }}

/* Cards */
.cards {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(320px,1fr)); gap:16px; }}
.card {{ background:var(--card-bg); border:1px solid var(--card-border); border-radius:14px; padding:20px; position:relative; transition:transform .2s,box-shadow .2s; opacity:0; transform:translateY(24px); }}
.card.visible {{ opacity:1; transform:translateY(0); }}
.card:hover {{ transform:translateY(-3px); box-shadow:0 8px 24px rgba(0,0,0,.08); border-color:#ffccbc; }}
.card-seq {{ position:absolute; top:-10px; left:-10px; width:30px; height:30px; background:linear-gradient(135deg,var(--gradient-start),var(--gradient-end)); color:#fff; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:13px; font-weight:700; box-shadow:0 2px 8px rgba(255,94,58,.35); z-index:1; }}
.card-title {{ font-size:15px; font-weight:700; margin:6px 0 10px; line-height:1.4; padding-left:16px; }}
.card-source {{ display:inline-block; background:#fff3ee; color:#e8552d; padding:2px 10px; border-radius:12px; font-size:11px; margin-bottom:8px; }}
.card-summary {{ font-size:13px; color:#8c7268; line-height:1.6; margin-bottom:12px; }}
.card-footer {{ display:flex; justify-content:space-between; align-items:center; }}
.card-time {{ font-size:11px; color:#c4b0a4; }}
.card-link {{ font-size:12px; color:var(--accent); text-decoration:none; font-weight:600; padding:4px 12px; border:1px solid rgba(255,94,58,.25); border-radius:14px; transition:all .2s; }}
.card-link:hover {{ background:rgba(255,94,58,.08); }}

/* Flashes */
.flashes {{ background:linear-gradient(135deg,#fef9f7,#fdf4f0); border-radius:14px; padding:24px; margin:32px auto; max-width:1100px; }}
.flashes-title {{ font-size:14px; font-weight:700; color:#e8552d; margin-bottom:12px; }}
.flash-item {{ padding:8px 0; border-bottom:1px solid rgba(0,0,0,.05); font-size:13px; color:#6b4c3b; }}
.flash-item:last-child {{ border-bottom:none; }}
.flash-item a {{ color:var(--accent); text-decoration:none; }}

/* Footer */
.footer {{ text-align:center; padding:32px 20px; font-size:12px; color:#c4b0a4; }}
.footer a {{ color:var(--accent); text-decoration:none; }}

/* Empty */
.empty {{ text-align:center; padding:40px 20px; color:#c4b0a4; font-size:14px; }}

@media (max-width:640px) {{
  .hero-title {{ font-size:22px; }}
  .hero-stat-num {{ font-size:28px; }}
  .cards {{ grid-template-columns:1fr; }}
}}
</style>
</head>
<body>

{hero_html}

<div class="nav"><div class="nav-inner">{nav_html}</div></div>

{_lead_html(lead)}

<div class="container">
  {sections_html}
</div>

{flashes_html}

<div class="footer">
  <p>共 {total_items} 条 · 数据来源 <a href="https://aihot.virxact.com" target="_blank" rel="noopener noreferrer">AI HOT</a></p>
  <p style="margin-top:6px;">本文由 AI 捕手 Agent 自动生成 · {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
</div>

<script>
// 滚动渐入动画
const observer = new IntersectionObserver((entries) => {{
  entries.forEach(e => {{ if(e.isIntersecting) e.target.classList.add('visible'); }});
}}, {{threshold:0.08}});
document.querySelectorAll('.card').forEach(c => observer.observe(c));

// 导航高亮
const navLinks = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('[id^="section-"]');
const navObserver = new IntersectionObserver((entries) => {{
  entries.forEach(e => {{
    if(e.isIntersecting) {{
      navLinks.forEach(l => l.classList.remove('active'));
      const active = document.querySelector(`.nav-link[href="#${{e.target.id}}"]`);
      if(active) active.classList.add('active');
    }}
  }});
}}, {{threshold:0.3,rootMargin:'-80px 0px -50%'}});
sections.forEach(s => navObserver.observe(s));
</script>
</body>
</html>"""


def generate_email_html(data: dict) -> str:
    """生成 Gmail 安全版 HTML（内联样式，表格布局，无 JS）。"""
    date_str = data.get("date", datetime.now().strftime("%Y-%m-%d"))
    sections = data.get("sections", [])
    flashes = data.get("flashes", [])
    lead = data.get("lead")
    total_items = sum(len(s.get("items", [])) for s in sections)
    seq = [0]

    def _seq(): seq[0] += 1; return seq[0]

    items_rows = ""
    for section in sections:
        label = section.get("label", "")
        style = CATEGORY_STYLE.get(label, {"color": "#e8552d", "icon": "📌"})
        items = section.get("items", [])

        items_rows += f"""
        <tr><td style="padding:24px 0 8px;border-top:2px solid {style['color']};">
          <span style="font-size:16px;font-weight:700;color:{style['color']};">
            {style['icon']} {label}
          </span>
          <span style="font-size:13px;color:#b8a094;margin-left:8px;">{len(items)} 条</span>
        </td></tr>"""

        if not items:
            items_rows += '<tr><td style="padding:16px;color:#c4b0a4;font-size:13px;text-align:center;">本期暂无该版块资讯</td></tr>'

        for item in items:
            s = _seq()
            title = item.get("title", "")
            summary = item.get("summary", "")[:80]
            source = item.get("sourceName", "")
            url = item.get("sourceUrl", "#")

            items_rows += f"""
        <tr><td style="padding:12px 0;border-bottom:1px solid #f0e6e0;">
          <table cellpadding="0" cellspacing="0" border="0" width="100%"><tr>
            <td style="width:30px;vertical-align:top;padding-top:2px;">
              <span style="display:inline-block;width:26px;height:26px;background:linear-gradient(135deg,#ff5e3a,#ff6b35);color:#fff;border-radius:50%;text-align:center;line-height:26px;font-size:12px;font-weight:700;">{s}</span>
            </td>
            <td style="padding-left:10px;">
              <div style="font-size:14px;font-weight:700;color:#2c1810;margin-bottom:4px;">{title}</div>
              <span style="display:inline-block;background:#fff3ee;color:#e8552d;padding:2px 8px;border-radius:10px;font-size:11px;margin-bottom:6px;">{source}</span>
              <div style="font-size:13px;color:#8c7268;line-height:1.5;margin-bottom:8px;">{summary}</div>
              <a href="{url}" style="font-size:12px;color:#e8552d;text-decoration:none;font-weight:600;" target="_blank" rel="noopener noreferrer">查看原文 →</a>
            </td>
          </tr></table>
        </td></tr>"""

    # Lead section
    lead_html = ""
    if lead:
        lead_html = f"""
    <tr><td style="padding:16px 20px;background:#fff8f5;border-left:4px solid #e8552d;border-radius:0 8px 8px 0;">
      <div style="font-size:14px;font-weight:700;color:#e8552d;margin-bottom:4px;">📝 {lead.get('title','主编点评')}</div>
      <div style="font-size:13px;color:#6b4c3b;line-height:1.7;">{lead.get('leadParagraph','')}</div>
    </td></tr>"""

    # Flashes
    flashes_html = ""
    if flashes:
        flash_rows = "".join(
            f'<tr><td style="padding:6px 0;font-size:12px;color:#6b4c3b;border-bottom:1px solid rgba(0,0,0,.04);">⚡ {f.get("title","")} <a href="{f.get("sourceUrl","#")}" style="color:#e8552d;text-decoration:none;">[{f.get("sourceName","")}]</a></td></tr>'
            for f in flashes[:10]
        )
        flashes_html = f"""
    <tr><td style="padding:20px 0 8px;">
      <span style="font-size:15px;font-weight:700;color:#e8552d;">⚡ 快讯</span>
    </td></tr>
    <tr><td style="background:#fef9f7;border-radius:10px;padding:12px 16px;">
      <table cellpadding="0" cellspacing="0" border="0" width="100%">{flash_rows}</table>
    </td></tr>"""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;background:#f5f0ed;">

<table cellpadding="0" cellspacing="0" border="0" width="100%" style="background:#f5f0ed;">
<tr><td align="center" style="padding:20px;">

  <!-- Header -->
  <table cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width:640px;background:linear-gradient(135deg,#1a0a00,#2d1200);border-radius:14px 14px 0 0;">
    <tr><td style="padding:32px 24px;text-align:center;">
      <div style="font-size:12px;color:rgba(255,255,255,.6);letter-spacing:1px;">{date_str}</div>
      <div style="font-size:26px;font-weight:800;color:#ff8a65;margin:8px 0;">AI 前沿日报</div>
      <div style="font-size:42px;font-weight:900;color:#ffb74d;">{total_items}</div>
      <div style="font-size:12px;color:rgba(255,255,255,.5);">条精选资讯</div>
    </td></tr>
  </table>

  <!-- Content -->
  <table cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width:640px;background:#ffffff;border-radius:0 0 14px 14px;">
    <tr><td style="padding:8px 24px 8px;">
      {lead_html}
      {items_rows}
      {flashes_html}
    </td></tr>
  </table>

  <!-- Footer -->
  <table cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width:640px;">
    <tr><td style="padding:24px;text-align:center;">
      <div style="font-size:12px;color:#c4b0a4;">共 {total_items} 条 · 数据来源 AI HOT</div>
      <div style="font-size:11px;color:#d4c4b8;margin-top:4px;">本文由 AI 捕手 Agent 自动生成 · {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
    </td></tr>
  </table>

</td></tr>
</table>

</body>
</html>"""


# ─── helpers ───

_seq_state = [0]

def _next_seq():
    _seq_state[0] += 1
    return _seq_state[0]


def _build_hero_html(date_str, total, sections, lead):
    pills = "".join(
        f'<span class="hero-pill"><span class="hero-pill-dot" style="background:{CATEGORY_STYLE.get(s.get("label",""),{}).get("color","#ccc")}"></span>{s.get("label","")} {len(s.get("items",[]))}</span>'
        for s in sections
    )
    weekday = ["日","一","二","三","四","五","六"]
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        date_display = f"{dt.year} 年 {dt.month} 月 {dt.day} 日 · 星期{weekday[dt.weekday()]}"
    except:
        date_display = date_str

    return f"""
<div class="hero">
  <div class="container">
    <div class="hero-date">{date_display}</div>
    <div class="hero-title">AI 前沿日报</div>
    <div class="hero-stats">
      <div class="hero-stat"><div class="hero-stat-num">{total}</div><div class="hero-stat-label">条精选</div></div>
    </div>
    <div class="hero-pills">{pills}</div>
  </div>
</div>"""


def _lead_html(lead):
    if not lead:
        return ""
    return f"""
<div class="lead">
  <div class="lead-title">📝 {lead.get('title', '主编点评')}</div>
  <div class="lead-text">{lead.get('leadParagraph', '')}</div>
</div>"""


def _build_nav_html(sections):
    links = ""
    for s in sections:
        label = s.get("label", "")
        slug = label.replace("/", "-")
        count = len(s.get("items", []))
        style = CATEGORY_STYLE.get(label, {})
        color = style.get("color", "#ccc")
        icon = style.get("icon", "📌")
        links += f'<a class="nav-link" href="#section-{slug}">{icon} {label}<span class="nav-badge">{count}</span></a>'
    return links


def _build_sections_html(sections, seq_fn):
    html = ""
    for s in sections:
        label = s.get("label", "")
        slug = label.replace("/", "-")
        style = CATEGORY_STYLE.get(label, {"color": "#e8552d", "icon": "📌"})
        items = s.get("items", [])

        html += f"""
<section class="section" id="section-{slug}">
  <div class="section-header">
    <span class="section-icon">{style['icon']}</span>
    <span class="section-title" style="color:{style['color']}">{label}</span>
    <span class="section-count">{len(items)} 条</span>
  </div>"""

        if not items:
            html += '<div class="empty">本期暂无该版块资讯</div>'
        else:
            html += '<div class="cards">'
            for item in items:
                s_num = seq_fn()
                title = item.get("title", "")
                summary = item.get("summary", "")[:70]
                source = item.get("sourceName", "")
                url = item.get("sourceUrl", "#")
                html += f"""
    <div class="card">
      <div class="card-seq">{s_num}</div>
      <div class="card-title">{title}</div>
      <div class="card-source">{source}</div>
      <div class="card-summary">{summary}</div>
      <div class="card-footer">
        <span class="card-time">今天</span>
        <a class="card-link" href="{url}" target="_blank" rel="noopener noreferrer">查看原文 →</a>
      </div>
    </div>"""
            html += '</div>'
        html += '</section>'
    return html


def _build_flashes_html(flashes):
    if not flashes:
        return ""
    items = "".join(
        f'<div class="flash-item">⚡ {f.get("title","")} <a href="{f.get("sourceUrl","#")}" target="_blank" rel="noopener noreferrer">[{f.get("sourceName","")}]</a></div>'
        for f in flashes[:10]
    )
    return f"""
<div class="container">
<div class="flashes">
  <div class="flashes-title">⚡ 快讯</div>
  {items}
</div>
</div>"""


def _collect_items_json(sections):
    return json.dumps([], ensure_ascii=False)
