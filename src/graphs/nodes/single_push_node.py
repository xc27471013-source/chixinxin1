import os
import requests
import datetime
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import SinglePushInput, SinglePushOutput


def single_push_node(state: SinglePushInput, config: RunnableConfig, runtime: Runtime[Context]) -> SinglePushOutput:
    """
    title: 群组推送
    desc: 通过 PushPlus API 向群组推送情报报告
    integrations: PushPlus API
    """
    ctx = runtime.context
    
    # 获取 PushPlus Token（从环境变量读取，或使用默认值）
    pushplus_token = os.getenv("PUSHPLUS_TOKEN", "8dec7824a9d74a1f8cf9738d55708f0b")
    
    if not pushplus_token:
        return SinglePushOutput(
            user_code=state.user_code,
            status="failed",
            message="PushPlus Token 未配置"
        )
    
    # 构建邮件标题
    current_date = datetime.datetime.now().strftime("%Y年%m月%d日")
    title = f"Yang Daily Intelligence | {current_date} 每日认知情报"
    
    # 构建请求体（群组推送使用 topic 参数）
    request_body = {
        "token": pushplus_token,
        "title": title,
        "content": state.report_content,
        "template": "html",
        "channel": "wechat",
        "topic": state.user_code  # 使用 topic 参数进行群组推送
    }
    
    # 调用 PushPlus API（注意：官方文档使用 http，不是 https）
    try:
        response = requests.post(
            "http://www.pushplus.plus/send",
            json=request_body,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        response_data = response.json()
        
        # PushPlus 返回格式：{"code": 200, "msg": "请求成功", "data": {...}}
        if response_data.get("code") == 200:
            return SinglePushOutput(
                user_code=state.user_code,
                status="success",
                message=response_data.get("msg", "推送成功")
            )
        else:
            return SinglePushOutput(
                user_code=state.user_code,
                status="failed",
                message=f"PushPlus API 错误: {response_data.get('msg', '未知错误')}"
            )
            
    except requests.exceptions.Timeout:
        return SinglePushOutput(
            user_code=state.user_code,
            status="failed",
            message="请求超时"
        )
    except requests.exceptions.RequestException as e:
        return SinglePushOutput(
            user_code=state.user_code,
            status="failed",
            message=f"网络请求失败: {str(e)}"
        )
    except Exception as e:
        return SinglePushOutput(
            user_code=state.user_code,
            status="failed",
            message=f"推送失败: {str(e)}"
        )
