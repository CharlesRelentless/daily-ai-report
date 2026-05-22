# AI 前沿日报 — GitHub Actions 版

AI HOT 精选 + arXiv 论文补充 → **Notion 数据库** → **QQ邮箱通知**

每天 08:30 自动运行，无需电脑开机。

## 快速部署

### 1. 配置 GitHub Secrets

Settings → Secrets and variables → Actions → New repository secret：

| Secret | 说明 |
|---|---|
| `NOTION_API_KEY` | Notion Integration Token |
| `NOTION_DATABASE_ID` | 数据库 `AI 晨报归档` 的 32 位 UUID |
| `EMAIL_SMTP_HOST` | smtp.qq.com |
| `EMAIL_SMTP_PORT` | 587 |
| `EMAIL_SENDER` | 发件邮箱 |
| `EMAIL_AUTH_CODE` | QQ 邮箱授权码 |
| `EMAIL_RECEIVER` | 收件邮箱 |

### 2. Notion 数据库

确保 Notion 中已有数据库，属性名：
`标题` `日期` `总条数` `模型发布` `产品发布` `行业动态` `论文研究` `技巧观点` `数据来源`

将数据库连接到 Notion Integration（Share → Invite → 选你的 integration）。

### 3. 推送代码

```bash
git add -A && git commit -m "Notion + QQ邮箱 版" && git push
```

### 4. 手动触发

Actions → AI 前沿日报 → Run workflow → 验证跑通。

## 架构

```
GitHub Actions (08:30 BJT, M-F)
    │
    ├── aihot.py    → AI HOT API（5 版块精选）
    ├── arxiv.py    → arXiv API（论文补充）
    ├── main.py     → 合并 & 构建 Notion blocks
    ├── push.py     → Notion API 写入 + QQ邮箱通知
    └── 你手机      → 微信弹提醒 → 点链接看日报
```
