# Yang Daily Intelligence - 每日认知情报自动推送系统

## 📋 项目简介

Yang Daily Intelligence 是一个自动化认知情报推送系统，每天 07:30（北京时间）自动生成高质量的认知情报报告，并通过 PushPlus 推送到订阅用户的微信服务通知。

### 核心特性

- ✅ **自动生成情报**: 每日自动搜索全球宏观、科技、资本等关键信息
- ✅ **智能分析**: 使用大语言模型进行深度解读和结构化输出
- ✅ **定时推送**: 每天 07:30 自动推送到用户微信
- ✅ **批量管理**: 支持多用户订阅，批量推送
- ✅ **反焦虑设计**: 语言简洁正式，不贩卖焦虑，只给确定性

---

## 📖 情报报告结构

每份情报报告包含以下 7 个板块：

```
# Yang Daily Intelligence

## 1. 今日最重要三条变化
## 2. 第一性原理解读
## 3. 时代趋势与结构变化
## 4. 财富机会提示
## 5. 反直觉洞察
## 6. 洛杉矶华人机会信息
## 7. AI自主推荐信息
```

---

## 🚀 快速开始

### 1. 获取 PushPlus Token

1. 访问 [PushPlus 官网](https://www.pushplus.plus/)
2. 微信扫码登录
3. 在「消息推送」页面获取 Token
4. 复制您的 Token

### 2. 获取用户码

1. 关注 PushPlus 公众号（微信搜索「pushplus」）
2. 在公众号内点击「获取用户码」
3. 复制显示的用户码

### 3. 配置环境变量

在工作流设置中添加以下环境变量：

```bash
PUSHPLUS_TOKEN=your_token_here
SUBSCRIPTION_USERS=user_code1,user_code2,user_code3
```

详细配置指南请参考：[ENV_CONFIG_GUIDE.md](ENV_CONFIG_GUIDE.md)

### 4. 启动工作流

配置完成后，启动工作流即可自动运行。系统将在每天 07:30（北京时间）自动推送情报。

---

## 📂 项目结构

```
.
├── AGENTS.md                      # 项目文档（节点清单、技能使用等）
├── ENV_CONFIG_GUIDE.md           # 环境变量配置详细指南
├── README.md                     # 项目说明文档（本文件）
├── config/
│   └── generate_intelligence_cfg.json  # 情报生成节点的 LLM 配置
├── src/
│   ├── graphs/
│   │   ├── graph.py             # 主图编排
│   │   ├── loop_graph.py        # 子图（批量推送循环）
│   │   ├── state.py             # 状态定义
│   │   └── nodes/
│   │       ├── generate_intelligence_node.py  # 情报生成节点
│   │       ├── batch_push_node.py            # 批量推送节点
│   │       └── single_push_node.py           # 单用户推送节点
│   └── main.py                  # 运行入口
└── requirements.txt             # 依赖包列表
```

---

## 🎯 工作流流程

```
定时触发（每天 07:30）
    ↓
情报生成节点
    ├─ 联网搜索今日全球关键信息
    ├─ LLM 生成结构化情报报告
    └─ 输出 Markdown 格式报告
    ↓
批量推送节点
    ├─ 读取订阅用户列表
    ├─ 调用子图遍历用户
    │   └─ 逐个调用 PushPlus API 推送
    └─ 记录推送结果
    ↓
结束
```

---

## 🔧 技术栈

- **工作流引擎**: LangGraph
- **大语言模型**: 豆包 (Doubao)
- **联网搜索**: Coze Web Search
- **消息推送**: PushPlus API
- **语言**: Python 3.x

---

## 📊 技能使用

- **web-search**: 搜索今日全球宏观、科技、资本等关键信息
- **llm**: 使用豆包模型生成情报报告
- **PushPlus API**: 推送情报到微信服务通知

---

## 🧪 测试

### 测试情报生成功能

```bash
# 运行工作流测试
python -c "from src.graphs.graph import main_graph; print(main_graph.invoke({}))"
```

### 测试推送功能

配置环境变量后，手动触发工作流，检查微信是否收到通知。

---

## 📱 微信小程序（可选）

如需开发微信小程序作为订阅入口，建议实现以下功能：

### 首页
- 展示今日情报预览
- 订阅入口
- 历史情报列表

### 订阅页
- 引导用户关注 PushPlus 公众号
- 获取并提交用户码
- 订阅状态管理

### 与工作流对接
1. 用户在小程序提交用户码
2. 后台将用户码存储到 `SUBSCRIPTION_USERS` 环境变量
3. 工作流自动推送情报到用户微信

---

## 🔐 安全与隐私

- PushPlus Token 仅用于推送功能，不泄露用户隐私
- 用户码由用户自主获取，可随时修改
- 情报内容不包含个人敏感信息

---

## 📝 环境变量清单

| 变量名 | 类型 | 必填 | 说明 | 示例 |
|-------|------|------|------|------|
| `PUSHPLUS_TOKEN` | String | 是 | PushPlus API Token | `abc123def456...` |
| `SUBSCRIPTION_USERS` | String | 是 | 订阅用户码列表（逗号分隔） | `ABCDEF123,GHI456` |

---

## ❓ 常见问题

### Q: 为什么没有收到推送？
A: 请检查：
1. PushPlus Token 是否正确配置
2. 用户码是否正确
3. 是否关注了 PushPlus 公众号
4. 工作流是否正常执行

### Q: 如何添加新订阅用户？
A: 将新用户的 PushPlus 用户码添加到 `SUBSCRIPTION_USERS` 环境变量中（用逗号分隔）。

### Q: 推送有时间限制吗？
A: PushPlus 免费版有推送频率限制（每分钟最多 1 条）。如需更高频率，可升级到付费版。

---

## 📚 相关文档

- [AGENTS.md](AGENTS.md) - 项目结构文档
- [ENV_CONFIG_GUIDE.md](ENV_CONFIG_GUIDE.md) - 环境变量配置指南
- [PUSHPLUS_TUTORIAL.md](PUSHPLUS_TUTORIAL.md) - PushPlus 对接详细教程

## 🧪 快速测试

运行测试脚本验证 PushPlus 配置是否正确：

```bash
# 确保已设置环境变量
export PUSHPLUS_TOKEN="your_token_here"
export SUBSCRIPTION_USERS="your_user_code"

# 运行测试脚本
python scripts/test_pushplus.py
```

测试脚本会自动：
1. 检查环境变量是否正确配置
2. 发送一条测试消息到您的微信
3. 验证推送功能是否正常

---

## 📮 联系与支持

- PushPlus 官网: https://www.pushplus.plus/
- PushPlus 文档: http://www.pushplus.plus/doc/
- PushPlus 微信公众号: pushplus

---

## 📄 许可证

本项目仅供学习和个人使用。

---

**每天 07:30，让高质量认知情报自动送达您的微信。**
