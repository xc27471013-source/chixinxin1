#!/usr/bin/env python3
"""
Yang Daily Intelligence - 独立定时推送脚本
每天 09:30 自动调用工作流生成最新情报并推送到微信
"""

import os
import sys
import json
import datetime
import asyncio

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.main import GraphService
from coze_coding_utils.runtime_ctx.context import new_context

# 配置信息
PUSHPLUS_TOKEN = os.getenv("PUSHPLUS_TOKEN", "8dec7824a9d74a1f8cf9738d55708f0b")
SUBSCRIPTION_USERS = os.getenv("SUBSCRIPTION_USERS", "")  # 留空则推送给自己


async def generate_intelligence():
    """
    调用工作流生成情报报告
    工作流会自动联网搜索最新信息 + LLM 生成情报
    """
    print("正在调用工作流生成情报...")
    print("工作流将自动：")
    print("  1. 联网搜索今日全球信息")
    print("  2. LLM 生成最新认知情报")
    print("  3. 自动推送到微信")
    print()

    try:
        # 创建图服务实例
        graph_service = GraphService()

        # 创建上下文
        ctx = new_context(method="daily_push")

        # 工作流输入（空输入，因为 GraphInput 没有参数）
        payload = {}

        # 调用工作流
        print("工作流开始执行...")
        result = await graph_service.run(payload, ctx=ctx)

        # 检查结果
        if "intelligence_report" in result and result["intelligence_report"]:
            print("✅ 工作流执行成功，情报生成完成！")
            print()
            return result["intelligence_report"], result.get("push_results", [])
        else:
            print("❌ 工作流执行失败，未生成情报报告")
            print(f"返回结果: {result}")
            print()
            return None, []

    except Exception as e:
        print(f"❌ 调用工作流时发生异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, []


async def main():
    """主函数"""
    print("=" * 60)
    print("Yang Daily Intelligence - 定时推送")
    print("=" * 60)
    print()

    # 获取当前时间
    now = datetime.datetime.now()
    print(f"执行时间: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 调用工作流生成情报并推送
    intelligence, push_results = await generate_intelligence()

    if not intelligence:
        print("❌ 情报生成失败，推送中止")
        return

    # 显示推送结果
    if push_results:
        print()
        print("=" * 60)
        print("推送结果汇总")
        print("=" * 60)
        for result in push_results:
            user = result.get("user_code", "自己")
            status = "✅ 成功" if result.get("status") == "success" else "❌ 失败"
            message = result.get("message", "")
            print(f"{user}: {status} - {message}")

    print()
    print("=" * 60)
    print("任务完成！")
    print("=" * 60)


if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())
