from typing import List
import logging
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import BatchPushInput, BatchPushOutput, SinglePushInput
from graphs.nodes.single_push_node import single_push_node
import os

logger = logging.getLogger(__name__)


def batch_push_node(state: BatchPushInput, config: RunnableConfig, runtime: Runtime[Context]) -> BatchPushOutput:
    """
    title: 批量推送
    desc: 批量推送情报报告给所有订阅用户
    integrations: PushPlus API
    """
    ctx = runtime.context
    logger.info("开始执行批量推送节点")
    
    # 获取群组列表（从环境变量读取，或使用默认列表）
    # 格式：群组编码1,群组编码2,群组编码3
    subscription_users_str = os.getenv("SUBSCRIPTION_USERS", "")
    
    if subscription_users_str:
        subscription_users = [user.strip() for user in subscription_users_str.split(",") if user.strip()]
    else:
        # 默认群组编码（用于群组推送）
        subscription_users = state.subscription_users if state.subscription_users else ["每日海外留学生资讯推送"]
    
    # 如果没有群组，推送给自己（topic 为空表示推送给自己）
    if not subscription_users:
        logger.info("没有配置群组，将推送给自己")
        subscription_users = [""]  # 空字符串表示推送给自己
    else:
        logger.info(f"群组推送列表: {subscription_users}")
    
    # 批量推送到群组
    push_results = []
    for user in subscription_users:
        user_display = user if user else "自己"
        logger.info(f"开始推送到群组: {user_display}")
        
        try:
            # 构造节点输入（使用格式化后的HTML）
            node_input = SinglePushInput(
                user_code=user,
                report_content=state.formatted_html
            )
            
            # 调用单个推送节点
            node_output = single_push_node(node_input, config, runtime)
            
            # 记录结果
            push_results.append({
                "user_code": user_display,
                "status": node_output.status,
                "message": node_output.message
            })
            
            logger.info(f"用户 {user_display} 推送结果: {node_output.status} - {node_output.message}")
            
        except Exception as e:
            logger.error(f"用户 {user_display} 推送失败: {str(e)}")
            push_results.append({
                "user_code": user_display,
                "status": "failed",
                "message": f"推送异常: {str(e)}"
            })
    
    logger.info(f"批量推送完成，共推送 {len(push_results)} 个用户")
    
    return BatchPushOutput(
        push_results=push_results
    )
