# 定时推送配置指南

> 使用独立的 Python 脚本实现每天 09:30 自动推送
> 不依赖 Coze 平台的定时触发器

---

## 🚀 快速开始

### 方案选择

1. **Coze 平台定时器**（推荐，简单）
   - 在 Coze 平台 UI 上配置
   - 参考 [HOW_TO_CONNECT.md](HOW_TO_CONNECT.md) 中的配置步骤

2. **独立脚本 + 系统定时任务**（更灵活）
   - 使用 `daily_push.py` 脚本
   - 在服务器上设置 cron 或任务计划程序

---

## 📋 方案 2：使用独立脚本

### 步骤 1：配置环境变量

创建 `.env` 文件（与脚本同级目录）：

```bash
# .env 文件内容
PUSHPLUS_TOKEN=8dec7824a9d74a1f8cf9738d55708f0b
SUBSCRIPTION_USERS=（留空则推送给自己）
```

或设置系统环境变量：

```bash
# Linux/Mac
export PUSHPLUS_TOKEN=8dec7824a9d74a1f8cf9738d55708f0b
export SUBSCRIPTION_USERS=""

# Windows PowerShell
$env:PUSHPLUS_TOKEN="8dec7824a9d74a1f8cf9738d55708f0b"
$env:SUBSCRIPTION_USERS=""
```

---

### 步骤 2：测试脚本

运行脚本测试是否能正常推送：

```bash
# 进入脚本目录
cd scripts

# 运行脚本
python3 daily_push.py

# 或使用 python
python daily_push.py
```

**预期输出**：

```
============================================================
Yang Daily Intelligence - 定时推送
============================================================

执行时间: 2026-03-06 09:30:00

正在生成情报...
情报日期: 2026年03月06日

推送目标: 自己（未配置订阅用户）

正在推送到自己的微信...
✅ 推送成功 - 消息流水号: xxxxxxxxxxxxxx

============================================================
推送完成
============================================================

成功: 1
失败: 0

日志已保存到: scripts/push_logs.json

🎉 推送成功！
📱 请检查您的微信服务通知。
```

---

### 步骤 3：设置定时任务

#### Linux/Mac (使用 cron)

1. **编辑 crontab**

```bash
crontab -e
```

2. **添加定时任务**

```bash
# 每天上午 09:30 执行
30 9 * * * cd /path/to/your/project/scripts && /usr/bin/python3 daily_push.py >> push.log 2>&1
```

**说明**：
- `30 9 * * *` → 每天 09:30
- `cd /path/to/your/project/scripts` → 切换到脚本目录
- `/usr/bin/python3 daily_push.py` → 执行脚本
- `>> push.log 2>&1` → 记录日志

3. **保存并退出**

- 按 `Esc`，输入 `:wq`，按 `Enter`

4. **查看已设置的定时任务**

```bash
crontab -l
```

---

#### Windows (使用任务计划程序)

1. **打开任务计划程序**

- 按 `Win + R`
- 输入 `taskschd.msc`
- 按 `Enter`

2. **创建基本任务**

- 点击右侧「创建基本任务」
- 名称：`Yang Daily Intelligence 推送`
- 描述：`每天 09:30 自动推送认知情报`
- 点击「下一步」

3. **设置触发器**

- 选择「每天」
- 开始时间：`09:30:00`
- 重复间隔：`1` 天
- 点击「下一步」

4. **设置操作**

- 选择「启动程序」
- 程序或脚本：`python.exe` 的完整路径
  - 例如：`C:\Python39\python.exe`
- 添加参数：`daily_push.py`
- 起始于：脚本的完整路径
  - 例如：`C:\Users\YourName\project\scripts`
- 点击「下一步」

5. **完成**

- 点击「完成」
- 确保勾选「当单击完成时，打开此任务属性的对话框」

6. **配置高级设置**

- 在任务属性中：
  - 勾选「不管用户是否登录都要运行」
  - 配置为：`Windows Vista, Windows Server 2008`
- 点击「确定」

---

## 🔧 高级配置

### 推送给多个用户

修改 `.env` 文件：

```bash
SUBSCRIPTION_USERS=ABC123,XYZ789,LMN456
```

多个用户码用逗号分隔。

### 修改推送时间

#### Linux/Mac (cron)

```bash
# 每天上午 08:00
0 8 * * * cd /path/to/scripts && python3 daily_push.py

# 每天晚上 20:00
0 20 * * * cd /path/to/scripts && python3 daily_push.py

# 工作日（周一到周五）上午 09:30
30 9 * * 1-5 cd /path/to/scripts && python3 daily_push.py
```

#### Windows (任务计划程序)

在「触发器」中修改开始时间。

---

## 📊 查看推送日志

### 脚本日志

脚本运行后会生成 `push_logs.json` 文件：

```json
[
  {
    "timestamp": "2026-03-06 09:30:00",
    "success_count": 1,
    "fail_count": 0,
    "results": [
      {
        "user": "自己",
        "success": true,
        "message": "推送成功",
        "message_id": "eda41faa7ef9465f876544a9fde6e228"
      }
    ]
  }
]
```

### Cron 日志

如果 cron 任务添加了日志重定向：

```bash
# 查看日志
cat scripts/push.log

# 实时查看日志
tail -f scripts/push.log
```

---

## ✅ 检查清单

配置完成后，请确认：

- [ ] 环境变量已配置（PUSHPLUS_TOKEN）
- [ ] 脚本测试运行成功
- [ ] 定时任务已设置（cron 或任务计划程序）
- [ ] 定时任务状态为启用
- [ ] 微信能收到测试消息

---

## 🧪 测试定时任务

### 测试 cron 任务

1. **设置一个临时的测试任务**（例如，5 分钟后执行）

```bash
# 编辑 crontab
crontab -e

# 添加测试任务（5分钟后执行）
*/5 * * * * cd /path/to/scripts && python3 daily_push.py >> push.log 2>&1
```

2. **等待 5 分钟**，检查微信是否收到消息

3. **删除测试任务**，添加正式任务

```bash
# 编辑 crontab
crontab -e

# 删除测试任务，添加正式任务
30 9 * * * cd /path/to/scripts && python3 daily_push.py >> push.log 2>&1
```

---

## 🆚 方案对比

| 特性 | Coze 平台定时器 | 独立脚本 + cron |
|------|----------------|----------------|
| **配置难度** | 简单（UI 操作） | 中等（需要了解 cron） |
| **灵活性** | 一般 | 高 |
| **可定制性** | 低 | 高 |
| **依赖性** | 依赖 Coze 平台 | 独立运行 |
| **日志管理** | Coze 平台查看 | 本地日志文件 |
| **适用场景** | 简单需求 | 高级定制 |

---

## 🎯 推荐方案

**如果您是个人使用，推荐 Coze 平台定时器**：
- 配置简单
- 不需要管理服务器
- 可视化界面

**如果您需要高级定制，推荐独立脚本**：
- 灵活性高
- 完全可控
- 可以修改推送逻辑

---

## 📞 获取帮助

如果遇到问题：

1. 查看日志文件 `push_logs.json`
2. 查看 cron 日志 `push.log`
3. 手动运行脚本测试：`python3 daily_push.py`
4. 检查环境变量是否正确

---

**配置完成后，每天 09:30 自动推送 Yang Daily Intelligence！** 🚀
