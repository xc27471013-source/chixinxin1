# GitHub Actions 定时推送配置指南

## 📋 前提条件

- 您的代码已推送到 GitHub 仓库
- 您的 Coze 服务有公开访问的 URL

---

## 🚀 配置步骤

### 步骤 1：获取服务 URL

您的 Coze 服务 URL 格式通常是：
```
https://您的项目ID.REGION.coze.cn/run
```

或者在 Coze 平台的部署页面查看。

### 步骤 2：配置 GitHub Secrets

1. 打开您的 GitHub 仓库
2. 点击「Settings」→「Secrets and variables」→「Actions」
3. 点击「New repository secret」
4. 添加：
   - **Name**: `WORKFLOW_URL`
   - **Value**: `http://您的服务地址:5000/run`
5. 点击「Add secret」

### 步骤 3：推送代码到 GitHub

```bash
git add .
git commit -m "feat: 添加 GitHub Actions 定时推送"
git push origin main
```

### 步骤 4：测试定时任务

**手动触发测试**：
1. 进入 GitHub 仓库
2. 点击「Actions」标签
3. 选择「每日认知情报推送」工作流
4. 点击「Run workflow」→「Run workflow」

**查看执行日志**：
- 在 Actions 页面可以看到每次执行的日志
- 确认 HTTP 状态码为 200

---

## ⏰ 定时说明

- **UTC 01:30** = **北京时间 09:30**
- GitHub Actions 使用 UTC 时间
- 配置：`cron: '30 1 * * *'`

---

## ✅ 验证清单

- [ ] 代码已推送到 GitHub
- [ ] WORKFLOW_URL secret 已配置
- [ ] 手动触发测试成功
- [ ] 等待明天 09:30 自动触发

---

## 🔧 故障排查

### 问题 1：Actions 执行失败
- 检查 WORKFLOW_URL 是否正确
- 检查服务是否正常运行
- 查看 Actions 日志了解详细错误

### 问题 2：服务无法访问
- 确认服务已部署到 Coze 平台
- 确认服务 URL 是公开可访问的
- 检查防火墙或安全组设置

### 问题 3：定时任务未执行
- GitHub Actions 的 cron 可能有延迟（最多 10-15 分钟）
- 确认 Actions 已启用（仓库 Settings → Actions → General）

---

## 💡 其他方案

如果 GitHub Actions 不适用，可以考虑：

1. **cron-job.org** - 在线定时任务服务
2. **腾讯云函数** - 云函数定时触发
3. **阿里云函数计算** - 云函数定时触发
4. **自建服务器** - 部署到自己的服务器，使用 crontab
