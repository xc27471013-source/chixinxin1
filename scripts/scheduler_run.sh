#!/bin/bash

set -e

WORK_DIR="${COZE_WORKSPACE_PATH:-.}"

echo "Starting Yang Daily Intelligence Scheduler..."
echo "Scheduled time: 09:30 (Asia/Shanghai)"
echo ""

python ${WORK_DIR}/scripts/scheduler.py
