# 🚀 立即对接 PushPlus - 您现在需要做什么

> 根据 PushPlus 官方 API 文档（V1.13）分析
> 当前状态：代码已修正，符合 API 规范 ✅

---

## ✅ 已完成的修正

### 1. API 地址修正

**问题**：原代码使用了 `https`
**修正**：改为 `http`（符合官方文档要求）

**修改位置**：
- ✅ `src/graphs/nodes/single_push_node.py` - 已修正
- ✅ `scripts/test_pushplus.py` - 已修正

### 2. 代码符合 API 规范

| 参数 | 要求 | 实际实现 | 状态 |
|------|------|---------|------|
| API 地址 | http://www.pushplus.plus/send | http://www.pushplus.plus/send | ✅ |
| 请求方式 | POST | POST | ✅ |
| Content-Type | application/json | application/json | ✅ |
| token | 必填 | ✅ | ✅ |
| title | 可选 | ✅ | ✅ |
| content | 必填 | ✅ | ✅ |
| template | 可选，默认 html | html | ✅ |
| channel | 可选，默认 wechat | wechat | ✅ |
| to | 可选（好友令牌） | ✅ | ✅ |

---

## 🎯 您现在需要做的事情

### 第 1 步：获取 PushPlus Token（2 分钟）

1. 访问 **https://www.pushplus.plus/**
2. 微信扫码登录
3. 点击左侧菜单「**Token**」
4. 复制您的 Token（32 位字符串）

**示例 Token**：
```
abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
```

### 第 2 步：让用户获取好友令牌（2 分钟）

**重要**：PushPlus 的 `to` 参数使用的是「**好友令牌**」，不是普通用户码！

#### 用户操作步骤：
1. 微信搜索公众号「**pushplus**」并关注
2. 进入公众号
3. 点击底部菜单「**我的**」或「**获取令牌**」
4. 找到「**好友令牌**」或「**Token**」
5. 复制好友令牌（6 位字母数字）

**示例好友令牌**：
```
ABCDEF123
```

### 第 3 步：快速测试连接（1 分钟）

运行快速测试脚本，验证 API 连接是否正常：

```bash
# 运行快速测试脚本
python scripts/quick_test_pushplus.py
```

按照提示输入：
1. 您的 PushPlus Token（32 位）
2. 您的好友令牌（6 位）

如果测试成功，您会收到一条微信测试消息。

### 第 4 步：配置环境变量（1 分钟）

在 Coze 工作流中添加环境变量：

```bash
PUSHPLUS_TOKEN=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
SUBSCRIPTION_USERS=ABCDEF123
```

**如果有多个订阅用户**：
```bash
PUSHPLUS_TOKEN=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
SUBSCRIPTION_USERS=ABCDEF123,GHI456,XYZ789,LMN456
```

### 第 5 步：启动工作流（10 秒）

1. 在 Coze 平台找到 Yang Daily Intelligence 工作流
2. 点击「发布」或「启动」
3. 确保定时触发器已设置（每天 07:30）

---

## 📱 推送到多个用户

### 方式 1：使用环境变量

```bash
# 多个用户用逗号分隔
SUBSCRIPTION_USERS=ABCDEF123,GHI456,XYZ789
```

### 方式 2：动态添加

新用户加入时：
1. 让用户关注 PushPlus 公众号
2. 用户获取好友令牌
3. 将好友令牌添加到 `SUBSCRIPTION_USERS` 环境变量

---

## 🧪 测试工具

### 工具 1：快速测试脚本

**用途**：测试 API 连接是否正常

```bash
python scripts/quick_test_pushplus.py
```

**特点**：
- 交互式输入 Token 和好友令牌
- 实时显示 API 响应
- 无需配置环境变量

### 工具 2：完整测试脚本

**用途**：测试环境变量配置是否正确

```bash
# 先设置环境变量
export PUSHPLUS_TOKEN="your_token"
export SUBSCRIPTION_USERS="user_code1,user_code2"

# 运行测试
python scripts/test_pushplus.py
```

**特点**：
- 自动读取环境变量
- 批量测试多个用户
- 验证配置完整性

---

## 📊 API 响应说明

### 成功响应

```json
{
  "code": 200,
  "msg": "请求成功",
  "data": "3cbc5eab19fe512e80677540fbde332a"
}
```

**解读**：
- `code: 200` → 服务器已接收请求 ✅
- `data` → 消息流水号，可用于查询最终状态
- 实际推送是**异步处理**，需要等待几秒钟

### 失败响应

```json
{
  "code": 401,
  "msg": "Token无效",
  "data": ""
}
```

**常见错误码**：
| 错误码 | 错误信息 | 解决方法 |
|--------|---------|---------|
| 200 | 请求成功 | 等待异步推送完成 |
| 400 | 参数错误 | 检查请求参数格式 |
| 401 | Token 无效 | 重新获取 Token |
| 429 | 请求过于频繁 | 等待 1 分钟后重试 |

---

## ⚠️ 重要提示

### 1. API 地址必须是 HTTP

**错误**：
```python
"https://www.pushplus.plus/send"  ❌
```

**正确**：
```python
"http://www.pushplus.plus/send"   ✅
```

**状态**：我们的代码已修正 ✅

### 2. 响应是异步的

即使收到 `code: 200`，也不代表消息已推送到微信。需要：
- 查看微信服务通知
- 或使用回调函数查询最终状态

### 3. 频率限制

- 免费版：每分钟 1 条，每天 200 条
- 工作流每天只推送 1 次，完全符合限制

### 4. 好友令牌 vs 用户码

根据 PushPlus API 文档：
- `to` 参数使用的是「**好友令牌**」
- 格式：6 位字母数字
- 用户在公众号中获取

---

## 📚 参考文档

| 文档 | 用途 |
|------|------|
| [PUSHPLUS_API_GUIDE.md](PUSHPLUS_API_GUIDE.md) | API 详细说明 |
| [PUSHPLUS_TUTORIAL.md](PUSHPLUS_TUTORIAL.md) | 详细对接教程 |
| [QUICKSTART.md](QUICKSTART.md) | 5 分钟快速开始 |
| [ENV_CONFIG_GUIDE.md](ENV_CONFIG_GUIDE.md) | 环境变量配置 |

---

## ✅ 对接完成清单

完成以下步骤后，对接就成功了：

- [ ] 从 PushPlus 官网获取 Token（32 位）
- [ ] 让用户关注公众号并获取好友令牌（6 位）
- [ ] 运行 `python scripts/quick_test_pushplus.py` 测试连接
- [ ] 微信收到测试消息
- [ ] 配置环境变量（PUSHPLUS_TOKEN 和 SUBSCRIPTION_USERS）
- [ ] 在 Coze 平台启动工作流
- [ ] 等待每天 07:30 自动推送

---

## 🎉 开始对接

### 现在就做：

1. 打开浏览器，访问 https://www.pushplus.plus/
2. 微信扫码登录
3. 获取 Token
4. 关注公众号，获取好友令牌
5. 运行测试脚本：
   ```bash
   python scripts/quick_test_pushplus.py
   ```

**5 分钟内完成对接，明天 07:30 收到第一条情报！** 🚀
