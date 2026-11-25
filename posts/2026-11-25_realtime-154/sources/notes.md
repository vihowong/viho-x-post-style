# realtime-154 · sources/notes.md（2026-11-25）

> 星数、fork、LICENSE、release 只记这里，不进正文与卡面。正文数字只用“数字本身就是话题点”的锚点（WA 31 国、WB 30 秒、WC 待定、WD 8 美分）。

## WA · koala73/worldmonitor

- 仓库：https://github.com/koala73/worldmonitor
- GitHub API（2026-11-25）：created 2026-01-08，★91,169，forks 14,162，TypeScript，pushed 2026-11-25。
- LICENSE：AGPL-3.0（README 徽标＋License 节）。Release：**未核实**——`get_latest_release` 不在连接器已审核只读工具集内（需 call-tool 另批），与 realtime-150/153 同例。不要在正文或卡面提 release。README 徽标显示有 release。
- 官方 README（全文已读）：
  - 定位："Real-time global intelligence dashboard — AI-powered news aggregation, geopolitical monitoring, and infrastructure tracking in a unified situational awareness interface."
  - 终端仪表盘：`npx worldmonitor`，同一份实时数据跑在 shell 里：world map, news, markets, conflict, military flights, cyber, climate, prediction markets and live TV，带鼠标支持与配色主题。No API key needed.
  - Country Instability Index (CII)：live CII v14 scores, bands, and approximate 24-hour movement for **31 Tier-1 countries**。
  - 六个站点变体：world、tech、finance、commodity、happy、energy（同一代码库）。
  - Local AI：Ollama 全本地跑，不用 API key。
  - 双地图引擎：3D globe（globe.gl）＋ WebGL 平面地图（deck.gl）。
  - MCP server：`https://worldmonitor.app/mcp`。
- 正文锚点（已核）：31 个 Tier-1 国家的动荡指数（CII v14，官方 README）。

## WB · sansan0/TrendRadar

- 仓库：https://github.com/sansan0/TrendRadar
- GitHub API（2026-11-25）：created 2025-04-28，★63,871，forks 24,947，Python，pushed 2026-11-25。
- LICENSE：GPL-3.0（README 徽标）。版本徽标 v6.12.0。Release：**未核实**（同上）。不要在正文或卡面提 release。
- 官方 README（中文，全文已读，101KB）：
  - 定位："最快**30秒**部署的热点助手 —— 告别无效刷屏，只看真正关心的新闻资讯。"
  - 聚合多平台热点＋RSS 订阅＋联网搜索（定向主题追踪，v6.12.0 新增）。
  - AI 智能筛选新闻（v6.5.0）、AI 分析推送（v5.0.0）、AI 多语言翻译推送（v5.2.0）、MCP 客户端（v4.2.0）。
  - 推送渠道：企业微信、个人微信、Telegram、钉钉、飞书、邮件、ntfy、Bark、Slack、通用 Webhook。
  - 数据来源：newsnow 项目 API（多平台数据），作者已确认可用，但请合理控制推送频率。
  - 部署：GitHub Actions 一键 fork、Docker、本地、Cloudflare Pages。
- 正文锚点（已核）：最快 30 秒部署（官方 README 开篇）。

## WC · DeusData/codebase-memory-mcp

- 仓库：https://github.com/DeusData/codebase-memory-mcp
- GitHub API（2026-11-25）：created 2026-02-24，★49,159，forks 4,090，C，pushed 2026-11-25。
- LICENSE：MIT（README 徽标）。Release：**未核实**（同上）。不要在正文或卡面提 release。
- 官方 README（全文已读，119KB）：
  - 定位："local code intelligence for AI agents via MCP"——把代码、文档、配置、基建连进一个持久化本地知识图谱。
  - 17 个 MCP 工具，纯 C 后端，164 种语言／文件格式（vendored tree-sitter grammars），Hybrid LSP 类型解析。
  - CBM Lens（open beta v0.0.1）：可视化伴侣，源码阅读器、架构图、Galaxy 3D 图、覆盖诊断、架构决策、本地代码聊天。
  - Galaxy：3D 探索代码知识图谱，边脉冲表示关系方向。
  - 46 个自动或条件客户端集成（agent 配置、skills、agent profiles、hooks）。
  - 索引与图查询不需要托管服务或 API key；本地处理。
  - Quick Start：装完重启 coding agent，说一句 "Index this project" 即完成。
  - arXiv 论文：2603.27277。
- 正文锚点（已核）：说一句 "Index this project" 即完成索引（官方 README Quick Start）；164 种语言（README 徽标＋正文）。

## WD · assafelovic/gpt-researcher

- 仓库：https://github.com/assafelovic/gpt-researcher
- GitHub API（2026-11-25）：created 2023-05-12，★30,903，forks 4,269，Python，pushed 2026-11-25。
- LICENSE：Apache-2.0（README 声明 "under the Apache 2 license"）。Release：**未核实**（同上）。不要在正文或卡面提 release。
- 官方 README（全文已读）：
  - 定位："the first open deep research agent designed for both web and local research on any given task"——产出带引用的详细、事实、无偏见研究报告。
  - 架构：planner 生成研究问题，execution agents 收集信息，publisher 聚合成报告；多 agent 工作流、递归深度研究、并行运行。
  - 成本："About **$0.08 and a minute per research report** with the default models, with every run's cost tracked."
  - 报告超 2,000 词；聚合 20+ 来源；Jev 智能上下文过滤（默认不用 API key 与 embeddings）；导出 PDF／Word。
  - 可装成 Claude Skill：`npx skills add assafelovic/gpt-researcher`。
  - Why：人工研究的客观结论要花几周；LLM 训练数据过时易幻觉；token 限制写不了长报告。
- 正文锚点（已核）：一份报告约 8 美分、一分钟（官方 README Features，默认模型）。

## 选题与原创性核查（2026-11-25，动笔前）

- 四个仓库名三种写法（org/repo、repo、org）在全部 11 月 `posts.md` 与 `candidates*.md` 里均为 0 命中：koala73/worldmonitor、sansan0/TrendRadar、DeusData/codebase-memory-mcp、assafelovic/gpt-researcher。Claude-BugHunter（当日长贴文）与 153 的四个仓库（LoopedWSP、serena、ruflo、sap-data-mcp）已排除。
- 选题说明：新鲜热门池在 153 批后已基本枯竭——11 月 18–25 日 GitHub trending／search 的 AI 仓库（ECC、hermes-agent、superpowers、rea、qwen-code、caveman、open-code-review、graphify、chrome-devtools-mcp、claude-trading-skills、linger、mobile-agent-testers、line-art-animation、kubai-icons、lot-map、rust-anything、fast-anything、agy-fast、deslop-please、inference-optimisation-skill、agentes-chat、VoiceStudio、deepseek-harness、boring-marketing-skills、datacat、open-artifact、agentic-attack-detections 等）全部在 11 月 posts.md 或 candidates*.md 里有命中。本批改用 153 批已验 0 命中的成熟热门仓库（30k–91k★），从未在 11 月发过，今日重验仍为 0 命中。
- 未选用的成熟 0 命中仓库（备用）：f/prompts.chat（178,493★，org 为单字母 f，repo 名 0 命中）。
- 钩子、金句、收尾问句、卡面标题逐项 grep：见自检报告 C 层，动笔后逐项核查。
