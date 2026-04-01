## 项目概述
- **名称**: Yang Daily Intelligence Push
- **功能**: 每日自动生成认知情报报告，并通过 PushPlus 推送到微信群

### 节点清单
| 节点名 | 文件位置 | 类型 | 功能描述 | 分支逻辑 | 配置文件 |
|-------|---------|------|---------|---------|---------|
| generate_intelligence | `nodes/generate_intelligence_node.py` | agent | 搜索今日全球关键信息并生成情报报告 | - | `config/generate_intelligence_cfg.json` |
| format_html | `nodes/format_html_node.py` | task | 将 Markdown 转换为美观的 HTML 报告 | - | - |
| batch_push | `nodes/batch_push_node.py` | task | 批量推送情报报告给所有订阅群组 | - | - |

**类型说明**: task(task节点) / agent(大模型) / condition(条件分支) / looparray(列表循环) / loopcond(条件循环)

## 技能使用
- 节点 `generate_intelligence` 使用 web-search 技能进行联网搜索
- 节点 `generate_intelligence` 使用 llm 技能调用大语言模型生成情报
- 节点 `batch_push` 使用 PushPlus API 进行微信推送

## 环境变量配置
- `PUSHPLUS_TOKEN`: PushPlus API Token（必填，默认值: `8dec7824a9d74a1f8cf9738d55708f0b`）
- `SUBSCRIPTION_USERS`: 推送群组的 PushPlus 群组编码列表，用逗号分隔（可选，默认：`每日海外留学生资讯推送`）

## 定时推送配置

### 方案一：Render.com + GitHub Actions（推荐生产环境）

**架构**：
```
GitHub Actions (定时触发 09:30)
       ↓
   HTTP 请求
       ↓
Render.com (运行服务)
       ↓
   执行工作流 → PushPlus → 微信群
```

**部署步骤**：
1. 部署到 Render.com（免费）
2. 配置 GitHub Secrets: `WORKFLOW_URL = https://你的服务.onrender.com/run`
3. GitHub Actions 自动在 09:30 触发

**详细文档**: `docs/DEPLOYMENT_GUIDE.md`

### 方案二：本地运行（开发测试）

```bash
# 启动服务（包含定时调度器）
python src/main.py -m http -p 5000
```

**注意**：需要保持服务持续运行。

## 工作流流程
1. **定时触发**（GitHub Actions 或本地调度器）
2. **生成情报**: 调用 `generate_intelligence` 节点
   - 使用 web-search 技能搜索今日全球宏观、科技、资本等关键信息
   - 使用 LLM 生成结构化的认知情报报告
3. **HTML格式化**: 调用 `format_html` 节点
   - 将 Markdown 转换为美观的 HTML
   - 包含渐变色头部、名人名言、响应式设计
4. **批量推送**: 调用 `batch_push` 节点
   - 通过 PushPlus 推送到微信群组

## 文件结构
```
├── .github/workflows/scheduled-push.yml  # GitHub Actions 定时配置
├── render.yaml                           # Render.com 部署配置
├── config/                               # LLM 配置文件
│   └── generate_intelligence_cfg.json
├── src/
│   ├── graphs/
│   │   ├── state.py                      # 状态定义
│   │   ├── graph.py                      # 工作流编排
│   │   └── nodes/                        # 节点实现
│   │       ├── generate_intelligence_node.py
│   │       ├── format_html_node.py
│   │       └── batch_push_node.py
│   └── scheduler/                        # 定时调度器
│       └── integrated_scheduler.py
└── docs/
    └── DEPLOYMENT_GUIDE.md               # 详细部署指南
```
