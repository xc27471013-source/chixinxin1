#!/usr/bin/env python3
"""
Yang Daily Intelligence - 定时调度器
使用 APScheduler 实现每天 09:30 自动运行工作流
"""

import os
import sys
import asyncio
import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.main import GraphService
from coze_coding_utils.runtime_ctx.context import new_context

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('/app/work/logs/bypass/scheduler.log')
    ]
)
logger = logging.getLogger(__name__)


async def run_daily_intelligence():
    """
    每天运行情报生成工作流
    """
    logger.info("=" * 60)
    logger.info("定时任务触发 - 开始执行工作流")
    logger.info(f"触发时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    try:
        # 创建图服务实例
        graph_service = GraphService()
        
        # 创建上下文
        ctx = new_context(method="scheduled_daily_push")
        
        # 工作流输入（空输入）
        payload = {}
        
        # 调用工作流
        logger.info("正在调用工作流生成情报并推送...")
        result = await graph_service.run(payload, ctx=ctx)
        
        # 检查结果
        if "intelligence_report" in result and result["intelligence_report"]:
            logger.info("✅ 工作流执行成功！")
            
            # 记录推送结果
            push_results = result.get("push_results", [])
            if push_results:
                for push_result in push_results:
                    user = push_result.get("user_code", "未知")
                    status = push_result.get("status", "未知")
                    message = push_result.get("message", "")
                    logger.info(f"推送结果 - {user}: {status} - {message}")
        else:
            logger.error("❌ 工作流执行失败，未生成情报报告")
            
    except Exception as e:
        logger.error(f"❌ 定时任务执行异常: {str(e)}", exc_info=True)
    
    logger.info("=" * 60)
    logger.info("定时任务执行完成")
    logger.info("=" * 60)


async def main():
    """
    主函数 - 启动定时调度器
    """
    logger.info("=" * 60)
    logger.info("Yang Daily Intelligence - 定时调度器启动")
    logger.info("=" * 60)
    
    # 创建调度器
    scheduler = AsyncIOScheduler(timezone=pytz.timezone('Asia/Shanghai'))
    
    # 添加定时任务 - 每天 09:30 执行
    scheduler.add_job(
        run_daily_intelligence,
        CronTrigger(hour=9, minute=30, timezone=pytz.timezone('Asia/Shanghai')),
        id='daily_intelligence_push',
        name='每日认知情报推送',
        replace_existing=True
    )
    
    logger.info("✅ 定时任务已添加:")
    logger.info("   - 任务名称: 每日认知情报推送")
    logger.info("   - 执行时间: 每天 09:30 (北京时间)")
    logger.info("   - 时区: Asia/Shanghai")
    logger.info("")
    logger.info("调度器正在运行，等待定时触发...")
    logger.info("按 Ctrl+C 停止调度器")
    logger.info("=" * 60)
    
    # 启动调度器
    scheduler.start()
    
    try:
        # 保持调度器运行
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logger.info("收到停止信号，正在关闭调度器...")
        scheduler.shutdown()
        logger.info("调度器已停止")


if __name__ == "__main__":
    # 运行调度器
    asyncio.run(main())
