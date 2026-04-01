# Yang Daily Intelligence - 5 分钟快速开始

> 本指南帮助您在 5 分钟内完成 PushPlus 对接并接收第一条情报。

---

## 🚀 5 分钟快速对接

### 第 1 分钟：注册并获取 Token

1. 打开 [PushPlus 官网](https://www.pushplus.plus/)
2. 微信扫码登录
3. 点击左侧「Token」菜单
4. 复制您的 Token（32 位字符串）

**示例 Token**：
```
abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
```

---

### 第 2 分钟：关注公众号并获取用户码

1. 微信搜索公众号「**pushplus**」并关注
2. 进入公众号，点击底部「获取用户码」
3. 复制您的用户码（6 位字母数字）

**示例用户码**：
```
ABCDEF123
```

---

### 第 3 分钟：配置环境变量

在 Coze 工作流中添加环境变量：

```bash
# 环境变量 1
名称: PUSHPLUS_TOKEN
值: abc123def456ghi789jkl012mno345pqr678stu901vwx234yz

# 环境变量 2
名称: SUBSCRIPTION_USERS
值: ABCDEF123
```

---

### 第 4 分钟：测试推送

#### 方式一：使用测试脚本（推荐）

```bash
# 设置环境变量
export PUSHPLUS_TOKEN="your_token_here"
export SUBSCRIPTION_USERS="your_user_code"

# 运行测试脚本
python scripts/test_pushplus.py
```

#### 方式二：手动触发工作流

1. 在 Coze 平台打开工作流
2. 点击「运行」按钮
3. 等待执行完成

---

### 第 5 分钟：接收测试消息

1. 打开微信
2. 查看「服务通知」
3. 点击查看来自「pushplus」的消息

**测试消息示例**：
```
标题: Yang Daily Intelligence - 测试消息

内容:
🎉 PushPlus 配置测试成功！

如果您看到这条消息，说明：
✅ Token 配置正确
✅ 用户码配置正确
✅ 微信服务通知正常
```

---

## ✅ 对接完成

如果您收到了测试消息，说明对接成功！

现在，工作流将在每天 **07:30（北京时间）** 自动推送 Yang Daily Intelligence 认知情报到您的微信。

---

## 📱 添加更多订阅用户

### 步骤：

1. 让每个用户都关注 PushPlus 公众号
2. 让每个用户获取自己的用户码
3. 将所有用户码用逗号分隔，更新 `SUBSCRIPTION_USERS` 环境变量

**示例**：
```bash
# 单个用户
SUBSCRIPTION_USERS=ABCDEF123

# 多个用户
SUBSCRIPTION_USERS=ABCDEF123,GHI456,XYZ789
```

---

## ❓ 遇到问题？

### 问题 1: 没有收到测试消息

**检查清单**：
- [ ] Token 是否正确（32 位字符串）
- [ ] 用户码是否正确（6 位字母数字）
- [ ] 是否关注了 PushPlus 公众号
- [ ] 微信服务通知是否开启

### 问题 2: 推送失败

**常见错误**：
- `Token 无效`: 重新从官网获取 Token
- `用户不存在`: 让用户重新获取用户码
- `请求超时`: 检查网络连接

---

## 📚 详细文档

如需了解更多详情，请参考：

- [PUSHPLUS_TUTORIAL.md](PUSHPLUS_TUTORIAL.md) - 详细对接教程（包含截图说明）
- [ENV_CONFIG_GUIDE.md](ENV_CONFIG_GUIDE.md) - 环境变量配置指南
- [README.md](README.md) - 项目完整文档
- [AGENTS.md](AGENTS.md) - 项目结构文档

---

## 🎉 开始接收情报

配置完成后，您将每天 07:30 自动收到：

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

**语言简洁正式、不贩卖焦虑、只给确定性！**

---

**享受高质量认知情报，提升您的认知维度！** 🚀
