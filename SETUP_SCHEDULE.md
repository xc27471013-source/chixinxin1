# ⏰ 配置定时推送 - 必读指南

## ❗ 重要说明

**为什么当前定时推送不工作？**

Coze 沙箱环境是**按需启动**的，不是 24/7 持续运行的服务器：
- 服务只在访问时启动
- 空闲一段时间后会自动停止
- APScheduler 定时任务无法在此环境中工作

---

## ✅ 解决方案：使用 Coze 平台定时触发器

### 方法 1：Coze 平台 UI 配置（推荐）

#### 步骤 1：进入 Coze 平台
1. 登录 [Coze 平台](https://www.coze.cn/)
2. 进入您的项目空间

#### 步骤 2：找到工作流
1. 找到「Yang Daily Intelligence」工作流
2. 点击进入编辑页面

#### 步骤 3：添加定时触发器
1. 在工作流编辑器中，找到「触发器」或「Trigger」节点
2. 添加「定时触发」节点
3. 配置：
   - **触发时间**：每天 09:30
   - **时区**：Asia/Shanghai（北京时间）

#### 步骤 4：保存并发布
1. 保存工作流
2. 点击「发布」或「部署」

---

### 方法 2：使用外部定时服务

如果 Coze 平台没有定时触发器，可以使用外部服务定时调用 webhook：

#### 选项 A：使用 cron-job.org（免费）
1. 访问 [cron-job.org](https://cron-job.org/)
2. 注册账号
3. 创建新任务：
   - **URL**: `http://您的服务地址:5000/run`
   - **Method**: POST
   - **Body**: `{}`
   - **Schedule**: 每天 09:30
   - **时区**: Asia/Shanghai

#### 选项 B：使用 GitHub Actions（免费）

创建 `.github/workflows/scheduled-push.yml`：

```yaml
name: Daily Push
on:
  schedule:
    - cron: '30 1 * * *'  # UTC 01:30 = 北京时间 09:30
  workflow_dispatch:  # 支持手动触发

jobs:
  push:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Workflow
        run: |
          curl -X POST http://您的服务地址:5000/run \
            -H "Content-Type: application/json" \
            -d '{}'
```

#### 选项 C：使用腾讯云函数 / 阿里云函数
1. 创建云函数
2. 设置定时触发器（每天 09:30）
3. 函数内容：HTTP 调用工作流接口

---

## 🔧 临时解决方案：手动触发

在配置好定时触发器之前，您可以：

### 方式 1：HTTP 接口触发
```bash
curl -X POST http://您的服务地址:5000/run \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 方式 2：Python 脚本触发
```bash
python scripts/daily_push.py
```

---

## 📋 检查清单

- [ ] 已了解 Coze 沙箱环境限制
- [ ] 选择定时触发方案（Coze 平台 / 外部服务）
- [ ] 配置定时触发器
- [ ] 测试定时推送是否成功

---

## 💡 推荐方案

**如果您有 Coze 平台访问权限**：
→ 使用 Coze 平台内置定时触发器（最简单）

**如果您没有平台访问权限**：
→ 使用 GitHub Actions（免费且稳定）

---

## ❓ 常见问题

### Q: 为什么不能用 APScheduler？
A: APScheduler 需要服务持续运行，但 Coze 沙箱环境是按需启动的。

### Q: 服务什么时候会启动？
A: 当有 HTTP 请求访问时，服务会被唤醒启动。

### Q: 服务什么时候会停止？
A: 空闲一段时间后（通常几分钟），服务会自动停止以节省资源。

### Q: 如何确认定时触发是否工作？
A: 检查 Coze 平台的执行日志，或查看微信群是否收到推送。
