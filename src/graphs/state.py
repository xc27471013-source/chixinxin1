from typing import List, Optional
from pydantic import BaseModel, Field

class GlobalState(BaseModel):
    """全局状态定义"""
    intelligence_report: str = Field(default="", description="生成的认知情报报告（Markdown格式）")
    formatted_html: str = Field(default="", description="格式化后的HTML报告")
    subscription_users: List[str] = Field(default=[], description="订阅用户的 PushPlus 用户码列表")
    push_results: List[dict] = Field(default=[], description="推送结果列表")

class GraphInput(BaseModel):
    """工作流的输入 - 定时触发，无参数"""
    pass

class GraphOutput(BaseModel):
    """工作流的输出"""
    intelligence_report: str = Field(default="", description="生成的认知情报报告（Markdown 格式）")
    push_results: List[dict] = Field(default=[], description="推送结果列表")

# 情报生成节点
class GenerateIntelligenceInput(BaseModel):
    """情报生成节点的输入"""
    pass

class GenerateIntelligenceOutput(BaseModel):
    """情报生成节点的输出"""
    intelligence_report: str = Field(..., description="生成的认知情报报告（Markdown 格式）")

# HTML格式化节点
class FormatHtmlInput(BaseModel):
    """HTML格式化节点的输入"""
    intelligence_report: str = Field(..., description="Markdown格式的情报报告")

class FormatHtmlOutput(BaseModel):
    """HTML格式化节点的输出"""
    formatted_html: str = Field(..., description="格式化后的HTML内容")

# 批量推送节点
class BatchPushInput(BaseModel):
    """批量推送节点的输入"""
    formatted_html: str = Field(..., description="格式化后的HTML情报报告")
    subscription_users: List[str] = Field(default=[], description="推送群组的 PushPlus 群组编码列表")

class BatchPushOutput(BaseModel):
    """批量推送节点的输出"""
    push_results: List[dict] = Field(..., description="推送结果列表")

# 子图：单个群组推送节点（循环中使用）
class SinglePushInput(BaseModel):
    """单个群组推送节点的输入"""
    user_code: str = Field(..., description="PushPlus 群组编码（topic）")
    report_content: str = Field(..., description="情报报告内容（HTML格式）")

class SinglePushOutput(BaseModel):
    """单个群组推送节点的输出"""
    user_code: str = Field(..., description="群组编码")
    status: str = Field(..., description="推送状态：success 或 failed")
    message: str = Field(..., description="推送结果消息")
