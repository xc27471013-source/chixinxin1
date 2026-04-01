# PushPlus 对接详细教程 - 从零开始

> 本教程将手把手教您如何从零开始对接 PushPlus，让 Yang Daily Intelligence 自动推送到您的微信。

---

## 📑 目录

1. [什么是 PushPlus](#什么是-pushplus)
2. [第一步：注册 PushPlus 账号](#第一步注册-pushplus-账号)
3. [第二步：获取您的 Token](#第二步获取您的-token)
4. [第三步：关注公众号并获取用户码](#第三步关注公众号并获取用户码)
5. [第四步：配置环境变量](#第四步配置环境变量)
6. [第五步：测试推送](#第五步测试推送)
7. [第六步：添加更多订阅用户](#第六步添加更多订阅用户)
8. [常见问题与解决方法](#常见问题与解决方法)
9. [高级配置](#高级配置)

---

## 什么是 PushPlus

PushPlus 是一个**微信消息推送服务**，它可以将各种消息通过微信服务通知推送到您的手机。

### 为什么需要 PushPlus？

- ✅ 不需要开发微信小程序
- ✅ 免费版每天可推送 200 条消息
- ✅ 支持富文本、图片、Markdown 格式
- ✅ 接口简单，5 分钟即可对接完成

---

## 第一步：注册 PushPlus 账号

### 1.1 打开官网

在浏览器中访问：
```
https://www.pushplus.plus/
```

### 1.2 微信扫码登录

1. 找到页面右上角的「登录」按钮
2. 点击后会显示一个二维码
3. 打开微信，扫描二维码
4. 在微信中确认登录

### 1.3 完成注册

- 扫码后会自动跳转到 PushPlus 个人中心
- 您的账号已经注册成功（使用微信作为登录方式）

**注意**：PushPlus 使用微信登录，**不需要单独注册用户名和密码**。

---

## 第二步：获取您的 Token

Token 是您调用 PushPlus API 的**密钥**，就像一个通行证。

### 2.1 进入个人中心

1. 登录后，您会看到个人中心页面
2. 页面左侧有导航菜单

### 2.2 找到 Token

方式一：
- 在页面左侧菜单中找到「**Token**」或「**我的Token**」
- 点击进入

方式二：
- 在个人中心首页
- 通常会在「个人信息」或「账号信息」区域显示 Token

### 2.3 复制 Token

Token 的格式通常是这样的：
```
abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
```

**重要提示**：
- Token 是**32位字符串**
- Token 是您的**私密信息**，不要泄露给他人
- 每个账号只有一个 Token

### 2.4 验证 Token

可以使用以下命令验证 Token 是否有效：

```bash
# 使用 curl 测试（Mac/Linux）
curl -X POST "https://www.pushplus.plus/send" \
  -H "Content-Type: application/json" \
  -d '{
    "token": "你的Token",
    "title": "测试消息",
    "content": "这是一条测试消息，如果您收到这条消息，说明 Token 配置正确！",
    "template": "html"
  }'

# 使用 PowerShell 测试（Windows）
Invoke-RestMethod -Uri "https://www.pushplus.plus/send" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{
    "token": "你的Token",
    "title": "测试消息",
    "content": "这是一条测试消息，如果您收到这条消息，说明 Token 配置正确！",
    "template": "html"
  }'
```

执行后，查看微信是否收到测试消息。

---

## 第三步：关注公众号并获取用户码

每个需要接收情报的用户都需要一个**用户码**。

### 3.1 关注 PushPlus 公众号

1. 打开微信
2. 点击右上角的「+」号
3. 选择「添加朋友」
4. 选择「公众号」
5. 搜索「**pushplus**」
6. 点击关注

### 3.2 获取用户码

方式一：通过公众号菜单

1. 进入 PushPlus 公众号
2. 点击底部菜单的「**获取用户码**」或「**我的**」
3. 系统会显示您的用户码

方式二：通过官网

1. 登录 PushPlus 官网
2. 在个人中心找到「**用户码**」或「**我的用户码**」
3. 复制显示的用户码

### 3.3 用户码格式

用户码的格式通常是这样的：
```
ABCDEF123
```

- 用户码是**6位字母数字组合**
- 每个用户有唯一的用户码
- 用户码可以随时修改（在公众号中）

### 3.4 为多个用户获取用户码

如果您需要推送给多个用户：

1. 让每个用户都关注 PushPlus 公众号
2. 让每个用户都获取自己的用户码
3. 收集所有用户的用户码
4. 将它们用逗号分隔保存

示例：
```
user_code1,user_code2,user_code3
```

---

## 第四步：配置环境变量

现在您需要将 Token 和用户码配置到工作流中。

### 4.1 准备信息

确保您已经准备好：
- ✅ 您的 Token
- ✅ 所有订阅用户的用户码（用逗号分隔）

示例：
```
Token: abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
用户码列表: ABCDEF123,GHI456,XYZ789
```

### 4.2 在 Coze 平台配置

**方式一：通过工作流编辑器**

1. 打开 Coze 工作流编辑器
2. 找到工作流设置页面
3. 寻找「**环境变量**」、「**变量管理**」或「**Secrets**」选项
4. 添加以下两个环境变量：

```
名称: PUSHPLUS_TOKEN
值: abc123def456ghi789jkl012mno345pqr678stu901vwx234yz

名称: SUBSCRIPTION_USERS
值: ABCDEF123,GHI456,XYZ789
```

5. 点击「保存」

**方式二：通过配置文件**

如果平台支持配置文件，可以创建 `.env` 文件：

```bash
# .env 文件内容
PUSHPLUS_TOKEN=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
SUBSCRIPTION_USERS=ABCDEF123,GHI456,XYZ789
```

### 4.3 验证配置

在工作流中添加一个测试节点，验证环境变量是否正确加载：

```python
import os

def test_env_vars(state, config, runtime):
    token = os.getenv("PUSHPLUS_TOKEN", "")
    users = os.getenv("SUBSCRIPTION_USERS", "")

    print(f"Token 长度: {len(token)}")
    print(f"用户码数量: {len(users.split(',')) if users else 0}")

    return {
        "token_loaded": len(token) > 0,
        "users_loaded": len(users) > 0
    }
```

---

## 第五步：测试推送

### 5.1 手动触发工作流

1. 在 Coze 平台找到您的工作流
2. 点击「运行」或「执行」按钮
3. 等待工作流执行完成

### 5.2 检查执行结果

查看工作流执行日志，应该看到类似这样的输出：

```json
{
  "intelligence_report": "# Yang Daily Intelligence\n\n## 1. 今日最重要三条变化...",
  "push_results": [
    {
      "user_code": "ABCDEF123",
      "status": "success",
      "message": "请求成功"
    },
    {
      "user_code": "GHI456",
      "status": "success",
      "message": "请求成功"
    }
  ]
}
```

### 5.3 检查微信

1. 打开微信
2. 查看「服务通知」
3. 应该会看到一条来自「pushplus」的消息
4. 点击查看情报内容

### 5.4 推送成功示例

微信服务通知会显示：

```
标题: Yang Daily Intelligence | 2026年1月1日 每日认知情报

内容:
# Yang Daily Intelligence

## 1. 今日最重要三条变化
...

[点击查看完整内容]
```

---

## 第六步：添加更多订阅用户

### 6.1 新用户获取用户码

让新用户：
1. 关注 PushPlus 公众号
2. 获取用户码
3. 将用户码发送给您

### 6.2 更新环境变量

将新用户的用户码添加到 `SUBSCRIPTION_USERS` 环境变量中：

```bash
# 原有用户
SUBSCRIPTION_USERS=ABCDEF123,GHI456

# 添加新用户后
SUBSCRIPTION_USERS=ABCDEF123,GHI456,XYZ789,LMN456
```

### 6.3 保存配置

更新环境变量后，点击「保存」。

### 6.4 下次推送自动生效

- 工作流会在下一次执行时自动向新用户推送
- 不需要重启工作流

---

## 常见问题与解决方法

### Q1: 为什么没有收到推送消息？

#### 可能原因及解决方法：

**原因 1: Token 配置错误**

- 检查 Token 是否正确复制
- 确保没有多余的空格或换行符
- 重新从 PushPlus 官网复制 Token

**原因 2: 用户码不正确**

- 确认用户是否关注了 PushPlus 公众号
- 确认用户码是否正确（6位字母数字）
- 让用户重新获取用户码

**原因 3: 微信服务通知被关闭**

1. 打开微信
2. 点击「我」→「设置」→「新消息通知」
3. 确保「服务通知」已开启

**原因 4: 推送频率限制**

- PushPlus 免费版每分钟最多推送 1 条
- 如果频繁推送，会触发频率限制
- 等待 1 分钟后重试

---

### Q2: 推送失败，显示 "用户不存在"

#### 解决方法：

1. 确认用户是否关注了 PushPlus 公众号
2. 让用户在公众号中检查用户码
3. 重新获取用户码并更新环境变量

---

### Q3: 推送失败，显示 "Token 无效"

#### 解决方法：

1. 登录 PushPlus 官网
2. 重新获取 Token
3. 更新环境变量中的 Token
4. 重新测试推送

---

### Q4: 情报内容显示乱码

#### 解决方法：

工作流已设置 `template: "html"`，理论上不会出现乱码。如果仍有问题：

1. 检查情报内容是否包含特殊字符
2. 确保 Markdown 格式正确
3. 联系 PushPlus 官方客服

---

### Q5: 如何查看推送历史？

#### 方法：

1. 登录 PushPlus 官网
2. 进入「消息推送」页面
3. 查看推送历史记录

---

### Q6: 免费版和付费版有什么区别？

| 功能 | 免费版 | 付费版 |
|------|--------|--------|
| 每日推送条数 | 200 条 | 无限制 |
| 推送频率 | 每分钟 1 条 | 更高频率 |
| 群发功能 | 不支持 | 支持 |
| 自定义模板 | 基础 | 高级 |

对于个人订阅用户，免费版已经足够使用。

---

## 高级配置

### 1. 推送时间自定义

工作流默认在每天 07:30 推送。如需修改：

1. 在 Coze 平台找到「定时触发」节点
2. 修改「执行时间」为您想要的时间
3. 确认时区为「北京时间」

### 2. 推送频率自定义

如需每天推送多次：

1. 复制定时触发节点
2. 设置不同的时间
3. 工作流会按多个时间点执行

### 3. 推送内容自定义

修改 `config/generate_intelligence_cfg.json` 文件中的提示词，可以自定义情报内容风格。

### 4. 推送模板自定义

工作流使用 `template: "html"`，支持以下格式：

- `html`: HTML 格式，支持 Markdown
- `txt`: 纯文本格式
- `json`: JSON 格式

---

## 📞 获取帮助

### PushPlus 官方支持

- **官网**: https://www.pushplus.plus/
- **文档**: http://www.pushplus.plus/doc/
- **微信公众号**: pushplus
- **客服**: 在公众号内留言

### 本项目支持

如果您在使用 Yang Daily Intelligence 工作流时遇到问题：

1. 检查 `AGENTS.md` 了解工作流结构
2. 检查 `ENV_CONFIG_GUIDE.md` 了解环境变量配置
3. 检查 `README.md` 了解项目概况
4. 查看工作流执行日志，定位问题

---

## ✅ 对接完成清单

完成以下步骤后，您的 PushPlus 对接就完成了：

- [ ] 注册 PushPlus 账号（微信扫码登录）
- [ ] 获取 Token（32位字符串）
- [ ] 关注 PushPlus 公众号
- [ ] 获取用户码（6位字母数字）
- [ ] 配置环境变量（PUSHPLUS_TOKEN 和 SUBSCRIPTION_USERS）
- [ ] 测试推送成功
- [ ] 微信收到情报消息

**恭喜！您已经成功对接 PushPlus，每天 07:30 将自动收到 Yang Daily Intelligence 认知情报！**

---

## 📝 附录：快速命令参考

### 测试 Token 是否有效

```bash
curl -X POST "https://www.pushplus.plus/send" \
  -H "Content-Type: application/json" \
  -d '{
    "token": "你的Token",
    "title": "测试",
    "content": "测试内容",
    "template": "html"
  }'
```

### 查看环境变量

```bash
# Linux/Mac
echo $PUSHPLUS_TOKEN
echo $SUBSCRIPTION_USERS

# Windows PowerShell
$env:PUSHPLUS_TOKEN
$env:SUBSCRIPTION_USERS
```

### 格式化用户码列表

```bash
# 将多个用户码用逗号分隔
user_codes="ABCDEF123,GHI456,XYZ789,LMN456,PQR789"

# 去除空格
echo "$user_codes" | tr -d ' '
```

---

**最后更新时间**: 2026年1月1日
**文档版本**: v1.0
