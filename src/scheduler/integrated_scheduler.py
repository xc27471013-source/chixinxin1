"""
Yang Daily Intelligence - 集成调度器到主应用
在 FastAPI 启动时自动启动定时调度器
"""

import asyncio
import logging
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
import pytz

logger = logging.getLogger(__name__)

# 全局调度器实例
scheduler = None


async def run_daily_intelligence():
    """
    每天运行情报生成工作流（通过 HTTP 调用本地接口）
    """
    import httpx
    
    logger.info("=" * 60)
    logger.info("定时任务触发 - 开始执行工作流")
    logger.info(f"触发时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    try:
        # 通过 HTTP 调用本地接口（更可靠）
        logger.info("正在调用本地工作流接口...")
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "http://127.0.0.1:5000/run",
                json={},
                headers={"Content-Type": "application/json"}
            )
        
        if response.status_code == 200:
            result = response.json()
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
            logger.error(f"❌ 工作流执行失败，HTTP {response.status_code}")
            logger.error(f"响应: {response.text}")
            
    except Exception as e:
        logger.error(f"❌ 定时任务执行异常: {str(e)}", exc_info=True)
    
    logger.info("=" * 60)
    logger.info("定时任务执行完成")
    logger.info("=" * 60)


def start_scheduler():
    """
    启动定时调度器
    """
    global scheduler
    
    if scheduler is not None:
        logger.warning("调度器已经启动")
        return
    
    logger.info("=" * 60)
    logger.info("Yang Daily Intelligence - 启动定时调度器")
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
    
    # 添加测试任务 - 11:58 执行
    from datetime import datetime
    test_time = datetime.now().replace(hour=11, minute=58, second=0, microsecond=0)
    if test_time > datetime.now():
        scheduler.add_job(
            run_daily_intelligence,
            DateTrigger(run_date=test_time, timezone=pytz.timezone('Asia/Shanghai')),
            id='test_push_1158',
            name=f'测试推送-11:58',
            replace_existing=True
        )
        logger.info(f"✅ 测试任务已添加: 11:58:00 执行")
    
    # 启动调度器
    scheduler.start()
    
    logger.info("✅ 定时任务已添加:")
    logger.info("   - 任务名称: 每日认知情报推送")
    logger.info("   - 执行时间: 每天 09:30 (北京时间)")
    logger.info("   - 时区: Asia/Shanghai")
    logger.info("=" * 60)


def shutdown_scheduler():
    """
    关闭定时调度器
    """
    global scheduler
    
    if scheduler is not None:
        logger.info("正在关闭定时调度器...")
        scheduler.shutdown()
        scheduler = None
        logger.info("定时调度器已关闭")
