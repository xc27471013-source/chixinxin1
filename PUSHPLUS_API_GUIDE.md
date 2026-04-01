# PushPlus API 对接指南 - 基于官方文档

> 根据 PushPlus 官方 API 文档（V1.13）整理
> 文档地址：https://www.pushplus.plus/doc/guide/api.html

---

## 📋 API 核心信息

### 1. 请求地址

```
http://www.pushplus.plus/send
```

**注意**：使用的是 `http`，不是 `https`

### 2. 请求方式

支持多种请求方式：
- GET
- POST
- PUT
- DELETE

推荐使用 **POST** 方法

### 3. 请求头

```
Content-Type: application/json
```

---

## 🔑 请求参数详解

### 必填参数

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `token` | String | 用户 Token 或消息 Token |

### 可选参数

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `title` | String | 无 | 消息标题 |
| `content` | String | 无 | 消息内容（必填） |
| `template` | String | html | 发送模板 |
| `channel` | String | wechat | 发送渠道 |
| `to` | String | 无 | 好友令牌（发送给指定用户） |
| `callbackUrl` | String | 无 | 发送结果回调地址 |
| `timestamp` | Long | 无 | 毫秒时间戳 |
| `pre` | String | 无 | 预处理编码（会员功能） |

---

## 📱 发送渠道（channel）

| 渠道 | 是否免费 | 描述 |
|------|---------|------|
| `wechat` | ✅ 免费 | 微信公众号（默认） |
| `webhook` | ✅ 免费 | 第三方 webhook |
| `cp` | ✅ 免费 | 企业微信应用 |
| `mail` | ✅ 免费 | 邮箱 |
| `sms` | ❌ 收费 | 短信（0.1元/条） |
| `voice` | ❌ 收费 | 语音（0.3元/条） |
| `extension` | ✅ 免费 | 浏览器扩展和桌面应用 |
| `app` | ✅ 免费 | 安卓、鸿蒙、iOS 应用 |

---

## 📝 模板类型（template）

| 模板名 | 描述 |
|--------|------|
| `html` | 默认模板，支持 HTML 文本（推荐） |
| `txt` | 纯文本，不转义 HTML |
| `json` | JSON 格式展示 |
| `markdown` | Markdown 格式展示 |
| `cloudMonitor` | 阿里云监控报警定制模板 |
| `jenkins` | Jenkins 插件定制模板 |
| `route` | 路由器插件定制模板 |
| `pay` | 支付成功通知模板 |

---

## 📤 请求示例

### 基础推送

```bash
curl -X POST "http://www.pushplus.plus/send" \
  -H "Content-Type: application/json" \
  -d '{
    "token": "your_token_here",
    "title": "测试消息",
    "content": "这是一条测试消息",
    "template": "html",
    "channel": "wechat"
  }'
```

### 发送给指定用户（使用 to 参数）

```bash
curl -X POST "http://www.pushplus.plus/send" \
  -H "Content-Type: application/json" \
  -d '{
    "token": "your_token_here",
    "title": "Yang Daily Intelligence | 2026年1月1日",
    "content": "# Yang Daily Intelligence\n\n## 1. 今日最重要三条变化...",
    "template": "html",
    "channel": "wechat",
    "to": "ABCDEF123"
  }'
```

### 使用 Markdown 格式

```bash
curl -X POST "http://www.pushplus.plus/send" \
  -H "Content-Type: application/json" \
  -d '{
    "token": "your_token_here",
    "title": "Markdown 测试",
    "content": "# 标题\n\n## 二级标题\n\n- 列表项1\n- 列表项2\n\n**粗体文字**",
    "template": "markdown",
    "channel": "wechat"
  }'
```

---

## 📥 响应内容

### 成功响应

```json
{
  "code": 200,
  "msg": "请求成功",
  "data": "3cbc5eab19fe512e80677540fbde332a"
}
```

**重要说明**：
- `code: 200` 仅表示服务端收到了请求
- `data` 是消息流水号，用于查询最终发送结果
- 实际推送是**异步处理**的

### 错误响应

```json
{
  "code": 400,
  "msg": "Token无效",
  "data": ""
}
```

常见错误码：
- `200`: 请求成功（不代表发送成功）
- `400`: 参数错误
- `401`: Token 无效
- `429`: 请求过于频繁

---

## 🔍 查询发送结果

由于是异步处理，您可以通过以下方式查询最终发送结果：

### 方法 1: 使用回调（推荐）

在请求时添加 `callbackUrl` 参数：

```bash
curl -X POST "http://www.pushplus.plus/send" \
  -H "Content-Type: application/json" \
  -d '{
    "token": "your_token_here",
    "title": "测试消息",
    "content": "测试内容",
    "callbackUrl": "https://your-server.com/callback"
  }'
```

PushPlus 会在消息处理完成后，POST 请求到您的回调地址：

```json
{
  "event": "message_complete",
  "messageInfo": {
    "message": "",
    "shortCode": "88*********50fe",
    "sendStatus": 2
  }
}
```

`sendStatus` 状态码：
- `0`: 未发送
- `1`: 发送中
- `2`: 发送成功 ✅
- `3`: 发送失败 ❌

### 方法 2: 在线查询

登录 PushPlus 官网，在「消息推送」页面查看发送历史。

---

## ⚠️ 重要注意事项

### 1. 使用 HTTP 协议

**错误示例**：
```
https://www.pushplus.plus/send  ❌
```

**正确示例**：
```
http://www.pushplus.plus/send  ✅
```

### 2. 响应是异步的

即使收到 `code: 200`，也不代表消息已经成功推送到用户微信。需要通过回调或查询流水号确认最终状态。

### 3. 频率限制

- 免费版每分钟最多推送 1 条
- 每天最多推送 200 条
- 如需更高频率，请升级到付费版

### 4. 内容格式

- `template: html`: 支持 HTML 标签，如 `<h2>`, `<ul>`, `<strong>`
- `template: markdown`: 支持 Markdown 语法
- `template: txt`: 纯文本，不会解析 HTML

### 5. 发送给好友

使用 `to` 参数发送给指定用户：
- `to` 参数是**好友令牌**
- 多个好友用逗号分隔，如：`to="token1,token2,token3"`
- 实名用户最多发送给 10 人
- 会员最多发送给 100 人

---

## 🔧 我们的实现检查

### 当前代码（src/graphs/nodes/single_push_node.py）

让我检查一下我们的实现是否符合规范：

```python
# 当前使用的 API 地址
response = requests.post(
    "https://www.pushplus.plus/send",  # ⚠️ 使用了 HTTPS
    json=request_body,
    headers={"Content-Type": "application/json"},
    timeout=30
)
```

**问题**：使用了 `https`，应该改为 `http`

### 需要修正的地方

1. ✅ 请求方式：POST（正确）
2. ✅ Content-Type：application/json（正确）
3. ✅ 参数：token, title, content, template, channel, to（正确）
4. ❌ API 地址：需要从 `https` 改为 `http`

---

## 🚀 立即对接步骤

### 第 1 步：获取 Token

1. 访问 https://www.pushplus.plus/
2. 微信扫码登录
3. 在个人中心获取 Token（32 位字符串）

### 第 2 步：获取好友令牌（to 参数）

1. 让用户关注 PushPlus 公众号
2. 用户在公众号中获取**好友令牌**
3. 好友令牌格式：6 位字母数字

### 第 3 步：配置环境变量

```bash
PUSHPLUS_TOKEN=your_32_digit_token
SUBSCRIPTION_USERS=user_code1,user_code2,user_code3
```

### 第 4 步：修正 API 地址

将代码中的 API 地址从 `https` 改为 `http`：

```python
# 修改前
"https://www.pushplus.plus/send"

# 修改后
"http://www.pushplus.plus/send"
```

### 第 5 步：测试推送

```bash
python scripts/test_pushplus.py
```

---

## 📊 完整示例代码

```python
import requests
import os

def send_to_pushplus(token, title, content, to_user_code):
    """
    发送消息到 PushPlus

    Args:
        token: PushPlus Token（32 位字符串）
        title: 消息标题
        content: 消息内容（HTML 或 Markdown）
        to_user_code: 好友令牌（6 位字母数字）

    Returns:
        dict: 推送结果
    """
    url = "http://www.pushplus.plus/send"  # ⚠️ 注意使用 http，不是 https

    payload = {
        "token": token,
        "title": title,
        "content": content,
        "template": "html",
        "channel": "wechat",
        "to": to_user_code
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )

        result = response.json()

        if result.get("code") == 200:
            return {
                "status": "success",
                "message": result.get("msg", "请求成功"),
                "message_id": result.get("data", "")
            }
        else:
            return {
                "status": "failed",
                "message": result.get("msg", "请求失败")
            }

    except Exception as e:
        return {
            "status": "failed",
            "message": str(e)
        }

# 使用示例
if __name__ == "__main__":
    token = os.getenv("PUSHPLUS_TOKEN", "")
    user_code = os.getenv("SUBSCRIPTION_USERS", "").split(",")[0]

    result = send_to_pushplus(
        token=token,
        title="测试消息",
        content="<h2>测试成功！</h2><p>如果您看到这条消息，说明配置正确。</p>",
        to_user_code=user_code
    )

    print(f"推送结果: {result}")
```

---

## ✅ 对接完成清单

- [ ] 获取 PushPlus Token（32 位字符串）
- [ ] 让订阅用户关注公众号并获取好友令牌（6 位）
- [ ] 配置环境变量（PUSHPLUS_TOKEN 和 SUBSCRIPTION_USERS）
- [ ] 修正 API 地址为 `http://www.pushplus.plus/send`
- [ ] 运行测试脚本
- [ ] 微信收到测试消息

---

**现在您已经了解了 PushPlus API 的全部细节，可以开始对接了！**
