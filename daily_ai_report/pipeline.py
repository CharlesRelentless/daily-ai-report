"""
AI 前沿捕手 Agent — LLM 管道
两步流程：① 智能筛选与分类 ② 生成五维雷达日报 + 研究方向专版
"""
import json
import re
from openai import OpenAI
from config import cfg

client = OpenAI(api_key=cfg.OPENAI_API_KEY, base_url=cfg.OPENAI_BASE_URL)


# ──────────────────────────────────────────────
# Step 1: 智能筛选与多维分类
# ──────────────────────────────────────────────

FILTER_SYSTEM_PROMPT = """你是一个极度挑剔的 AI 前沿技术编辑，服务于一名高校科研工作者。他的研究方向是深度学习、遥感图像分析、目标检测、滑坡检测、语义分割。

你的任务：从给定的原始信息列表中，严格筛选出真正有价值的条目，并按以下六个维度分类。

维度说明：
- 模型·产品速递：关键实验室的新模型、重大功能更新、定价变化。
- 前沿研究信号：突破性论文，特别是基准测试飞跃或新架构。
- 开发利器·Agent 生态：编程 Agent、框架、IDE 插件等的更新。
- 范式·观点火花：顶尖研究员的博客、深度文章，改变对 AI 开发根本认知的内容。
- 开源亮点·灵感案例：GitHub 上高星且具创意的新项目。
- 科研方向·遥感目标检测：滑坡检测、遥感图像分割、SAR 分析、变化检测等方向的论文与工具。

筛选要求：
1. 过滤掉纯产品营销、无实质创新的新闻、低质量转载。
2. 每个条目包含以下字段：
   - category：上述六个维度之一
   - title：精简后的标题
   - summary：两句话总结「做了什么」和「对我意味着什么」。
   - url：原始链接（若有）
   - significance_score：1-10 分（10 表示绝对不能错过）
3. 仅输出 JSON 数组，不要任何其他文字。示例格式：
[{"category":"模型·产品速递","title":"GPT-5 发布","summary":"OpenAI 发布 GPT-5，推理能力大幅提升。意味着 Agent 开发门槛进一步降低。","url":"...","significance_score":10}]

原始信息：
{raw_content}"""


def filter_and_classify(raw_text: str) -> list[dict]:
    """发往 LLM 进行筛选分类，返回 JSON 列表。"""
    # 截断防止超 token（≈30K 字符）
    truncated = raw_text[:30000]
    response = client.chat.completions.create(
        model=cfg.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": FILTER_SYSTEM_PROMPT},
            {"role": "user", "content": truncated},
        ],
        temperature=0.3,
    )
    content = response.choices[0].message.content or "[]"
    # 清理可能的 Markdown 代码块包裹
    content = re.sub(r"```json\s*", "", content)
    content = re.sub(r"```\s*$", "", content)
    return json.loads(content)


# ──────────────────────────────────────────────
# Step 2: 生成 Markdown 日报
# ──────────────────────────────────────────────

REPORT_SYSTEM_PROMPT = """你是一名个人 AI 前沿日报主编。根据提供的、已按六个维度分类的内容，生成一份极简、结构化的 Markdown 日报。

日报格式要求：
- 以 "# 【AI 前沿日报 | {date}】" 开头。
- 六个维度为二级标题，每个维度下仅选取 significance_score 最高的 1-2 条。
- 每条内容格式：`- **{title}**：[链接]({url}) → {一句话启示}。`
- 如果一个维度没有内容，保留标题并写"今日无重要更新"。
- 六个维度之后，额外加一个 ## 今日一句话速览 段落，用一句不超过 40 字的话概括今天最值得关注的事。
- 结尾加上一行：`> *本文由 AI 捕手 Agent 自动生成，仅供个人防落伍参考。*`
- 不要输出 JSON，直接输出纯 Markdown。

内容数据：
{selected_json}"""


def generate_report(selected_items: list[dict], date_str: str) -> str:
    """生成最终 Markdown 日报。"""
    response = client.chat.completions.create(
        model=cfg.OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": REPORT_SYSTEM_PROMPT.replace("{date}", date_str),
            },
            {
                "role": "user",
                "content": json.dumps(selected_items, ensure_ascii=False),
            },
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content or "(空日报)"


# ──────────────────────────────────────────────
# 便捷入口
# ──────────────────────────────────────────────

def run_pipeline(raw_text: str, date_str: str) -> tuple[list[dict], str]:
    """完整流水线：原始文本 → 筛选分类 → Markdown 日报。"""
    print("[1/2] 正在筛选与分类...")
    selected = filter_and_classify(raw_text)
    print(f"      筛选出 {len(selected)} 条有价值信息")

    print("[2/2] 正在生成日报...")
    report = generate_report(selected, date_str)
    print("      日报生成完毕")
    return selected, report
