# Yang Daily Intelligence - 环境变量配置指南

## 概述

本工作流需要配置两个环境变量才能完整运行：
1. `PUSHPLUS_TOKEN` - PushPlus API Token
2. `SUBSCRIPTION_USERS` - 订阅用户的 PushPlus 用户码列表

---

## 1. 获取 PushPlus Token

### 步骤：
1. 访问 PushPlus 官网：https://www.pushplus.plus/
2. 点击右上角「登录」或「注册」
3. 使用微信扫码登录
4. 登录后进入「消息推送」页面
5. 在页面左侧菜单找到「Token」
6. 复制您的 Token（格式类似：`abc123def456...`）

---

## 2. 获取用户 PushPlus 用户码

### 用户侧操作：
1. 关注 PushPlus 公众号（微信搜索「pushplus」）
2. 在公众号内点击「获取用户码」
3. 复制显示的用户码（格式类似：`ABCDEF123`）

### 说明：
- 每个用户都有唯一的用户码
- 通过用户码可以精确推送消息到指定用户的微信
- 用户可以随时修改用户码，以保护隐私

---

## 3. 配置环境变量

### 方式一：在 Coze 平台配置

1. 进入工作流编辑页面
2. 找到「环境变量」或「变量管理」设置
3. 添加以下两个环境变量：

```bash
PUSHPLUS_TOKEN=abc123def456...      # 您的 PushPlus Token
SUBSCRIPTION_USERS=ABCDEF123,GHI456  # 订阅用户的用户码（用逗号分隔）
```

### 方式二：在本地测试时配置

在运行工作流前，执行以下命令：

```bash
export PUSHPLUS_TOKEN="your_token_here"
export SUBSCRIPTION_USERS="user_code1,user_code2,user_code3"
```

### 方式三：在 Docker 容器中配置

```yaml
# docker-compose.yml
version: '3'
services:
  yang-daily-intelligence:
    environment:
      - PUSHPLUS_TOKEN=abc123def456...
      - SUBSCRIPTION_USERS=ABCDEF123,GHI456
```

---

## 4. 订阅用户管理

### 添加新用户：
1. 用户获取自己的 PushPlus 用户码
2. 将用户码添加到 `SUBSCRIPTION_USERS` 环境变量中（用逗号分隔）
3. 重新配置环境变量
4. 工作流将在下一次执行时自动向新用户推送情报

### 移除用户：
1. 从 `SUBSCRIPTION_USERS` 环境变量中删除该用户的用户码
2. 重新配置环境变量

### 示例配置：

```bash
# 单个订阅用户
SUBSCRIPTION_USERS=ABCDEF123

# 多个订阅用户（用逗号分隔）
SUBSCRIPTION_USERS=ABCDEF123,GHI456,XYZ789,LMN456
```

---

## 5. 测试配置

配置完成后，可以测试环境变量是否正确：

```bash
# 检查环境变量是否设置成功
echo $PUSHPLUS_TOKEN
echo $SUBSCRIPTION_USERS

# 如果输出为空，说明配置失败，需要重新配置
```

---

## 6. 推送测试

配置完成后，运行工作流测试：

1. 确保 `PUSHPLUS_TOKEN` 和 `SUBSCRIPTION_USERS` 都已正确配置
2. 手动触发工作流（或等待定时触发）
3. 检查微信服务通知是否收到情报报告
4. 查看工作流执行日志中的 `push_results` 字段，确认推送状态

### 推送结果示例：

```json
{
  "push_results": [
    {
      "user_code": "ABCDEF123",
      "status": "success",
      "message": "请求成功"
    },
    {
      "user_code": "GHI456",
      "status": "failed",
      "message": "用户不存在"
    }
  ]
}
```

---

## 7. 常见问题

### Q1: 为什么推送失败？
**A:** 可能的原因：
- PushPlus Token 无效或过期
- 用户码不正确或用户未关注 PushPlus 公众号
- 网络连接问题
- PushPlus API 服务异常

### Q2: 如何查看推送历史？
**A:** 
- 登录 PushPlus 官网
- 进入「消息推送」页面
- 查看推送历史记录

### Q3: 推送有时间限制吗？
**A:** 
- PushPlus 免费版有推送频率限制（每分钟最多 1 条）
- 如需更高频率，可升级到付费版

### Q4: 如何支持 Markdown 格式？
**A:** 
- 本工作流已设置 `template: "html"`
- 推送的情报报告将以 HTML 格式渲染
- 支持标题、列表、粗体等 Markdown 语法

---

## 8. 联系与支持

- PushPlus 官网：https://www.pushplus.plus/
- PushPlus 文档：http://www.pushplus.plus/doc/
- PushPlus 微信公众号：pushplus

---

## 9. 环境变量清单

| 变量名 | 类型 | 必填 | 说明 | 示例 |
|-------|------|------|------|------|
| `PUSHPLUS_TOKEN` | String | 是 | PushPlus API Token | `abc123def456...` |
| `SUBSCRIPTION_USERS` | String | 是 | 订阅用户码列表（逗号分隔） | `ABCDEF123,GHI456` |

---

**配置完成后，工作流将在每天 07:30（北京时间）自动推送 Yang Daily Intelligence 情报报告到订阅用户的微信服务通知。**
