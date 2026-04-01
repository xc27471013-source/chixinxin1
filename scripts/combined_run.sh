#!/bin/bash

set -e

WORK_DIR="${COZE_WORKSPACE_PATH:-.}"
PORT=8000

usage() {
  echo "用法: $0 -p <端口>"
}

while getopts "p:h" opt; do
  case "$opt" in
    p)
      PORT="$OPTARG"
      ;;
    h)
      usage
      exit 0
      ;;
    \?)
      echo "无效选项: -$OPTARG"
      usage
      exit 1
      ;;
  esac
done

echo "=========================================="
echo "Yang Daily Intelligence - 服务启动"
echo "=========================================="
echo ""
echo "启动模式: HTTP服务 + 定时调度器"
echo "HTTP端口: $PORT"
echo "定时任务: 每天 09:30 (北京时间)"
echo ""
echo "=========================================="
echo ""

# 启动定时调度器（后台运行）
echo "启动定时调度器..."
python ${WORK_DIR}/scripts/scheduler.py &
SCHEDULER_PID=$!
echo "定时调度器已启动 (PID: $SCHEDULER_PID)"
echo ""

# 启动HTTP服务（前台运行）
echo "启动HTTP服务..."
python ${WORK_DIR}/src/main.py -m http -p $PORT
