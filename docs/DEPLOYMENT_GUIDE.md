# GitHub Actions 外部触发配置指南

## 架构说明

```
GitHub Actions (定时触发)
       ↓
   HTTP 请求
       ↓
Render.com (运行服务)
       ↓
   执行工作流
       ↓
  PushPlus → 微信群
```

---

## 第一步：部署到 Render.com（免费）

### 1.1 注册 Render
1. 访问 https://render.com
2. 使用 GitHub 账号登录

### 1.2 创建 Web Service
1. 点击 **New** → **Web Service**
2. 连接您的 GitHub 仓库
3. 配置如下：

| 配置项 | 值 |
|-------|---|
| Name | `yang-daily-intelligence` |
| Region | `Oregon (US West)` 或 `Singapore` |
| Branch | `main` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python src/main.py -m http -p $PORT` |
| Instance Type | `Free` |

### 1.3 添加环境变量
在 **Environment** 标签页添加：

```
COZE_API_KEY = 你的豆包API密钥
PUSHPLUS_TOKEN = 8dec7824a9d74a1f8cf9738d55708f0b
```

### 1.4 部署
点击 **Create Web Service**，等待部署完成。

### 1.5 获取服务 URL
部署成功后，Render 会分配一个 URL，格式如：
```
https://yang-daily-intelligence.onrender.com
```

---

## 第二步：配置 GitHub Actions

### 2.1 推送代码到 GitHub
```bash
git add .
git commit -m "feat: 添加 Render 部署配置"
git push origin main
```

### 2.2 配置 Secrets
1. 打开 GitHub 仓库
2. 进入 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 添加：

| Name | Value |
|------|-------|
| `WORKFLOW_URL` | `https://你的服务地址.onrender.com/run` |

示例：
```
WORKFLOW_URL = https://yang-daily-intelligence.onrender.com/run
```

---

## 第三步：测试

### 3.1 手动触发测试
1. 进入 **Actions** 标签页
2. 选择 **每日认知情报推送** workflow
3. 点击 **Run workflow** → **Run workflow**
4. 查看运行日志

### 3.2 验证推送
检查微信群是否收到消息。

---

## 定时配置

当前配置为 **北京时间 09:30** 自动执行。

修改时间：编辑 `.github/workflows/scheduled-push.yml`：

```yaml
on:
  schedule:
    # 格式: 分 时 日 月 周 (UTC时间)
    # UTC 01:30 = 北京时间 09:30 (UTC+8)
    - cron: '30 1 * * *'
```

**常用时间对照表**：

| 北京时间 | UTC cron |
|---------|----------|
| 08:00 | `0 0 * * *` |
| 09:30 | `30 1 * * *` |
| 12:00 | `0 4 * * *` |
| 18:00 | `0 10 * * *` |
| 21:00 | `0 13 * * *` |

---

## 常见问题

### Q1: Render 免费版会休眠怎么办？
Render 免费版 15 分钟无请求会休眠。GitHub Actions 的请求会自动唤醒服务。

**解决方案**：增加超时时间（已配置 `--max-time 180`）

### Q2: 如何查看日志？
- **GitHub Actions**: Actions → 选择运行记录 → 查看日志
- **Render**: Dashboard → 选择服务 → Logs

### Q3: 推送失败怎么办？
1. 检查 Secrets 配置是否正确
2. 检查 Render 服务是否正常运行
3. 查看 GitHub Actions 日志

### Q4: 需要修改推送内容？
修改 `config/generate_intelligence_llm_cfg.json` 中的提示词。

---

## 备选方案

如果 Render 不稳定，可以使用：

| 平台 | 特点 | 免费额度 |
|-----|------|---------|
| **Railway** | 更稳定 | $5/月免费额度 |
| **Fly.io** | 全球节点 | 3个共享VM |
| **Koyeb** | 简单易用 | 免费 |

部署方式类似，只需修改 `startCommand`。
