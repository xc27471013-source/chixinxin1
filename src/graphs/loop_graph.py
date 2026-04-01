from typing import List
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from graphs.state import SinglePushInput, SinglePushOutput
from graphs.nodes.single_push_node import single_push_node


# 子图状态
class LoopState(BaseModel):
    """子图循环状态"""
    users: List[str] = Field(default=[], description="待处理的用户列表")
    current_user: str = Field(default="", description="当前处理的用户")
    report_content: str = Field(default="", description="情报内容")
    push_results: List[dict] = Field(default=[], description="已完成的推送结果列表")


# 子图节点：提取下一个用户
def extract_next_user(state: LoopState) -> LoopState:
    """从用户列表中提取下一个用户"""
    if not state.users:
        return LoopState(
            users=[],
            current_user="",
            report_content=state.report_content,
            push_results=state.push_results
        )
    
    # 取出第一个用户
    current_user = state.users[0]
    remaining_users = state.users[1:]
    
    return LoopState(
        users=remaining_users,
        current_user=current_user,
        report_content=state.report_content,
        push_results=state.push_results
    )


# 子图节点：调用单个推送
def call_single_push(state: LoopState) -> LoopState:
    """调用单个推送节点"""
    if not state.current_user:
        return state
    
    # 构造节点输入
    node_input = SinglePushInput(
        user_code=state.current_user,
        report_content=state.report_content
    )
    
    # 调用节点函数（传入 dummy config 和 runtime）
    from langchain_core.runnables import RunnableConfig
    from langgraph.runtime import Runtime
    from coze_coding_utils.runtime_ctx.context import Context, new_context
    
    dummy_config = RunnableConfig({})
    dummy_ctx = new_context(method="loop.single_push")
    dummy_runtime = Runtime[Context](context=dummy_ctx)
    
    node_output = single_push_node(node_input, dummy_config, dummy_runtime)
    
    # 将结果添加到 push_results
    new_results = state.push_results.copy()
    new_results.append({
        "user_code": node_output.user_code,
        "status": node_output.status,
        "message": node_output.message
    })
    
    return LoopState(
        users=state.users,
        current_user=state.current_user,
        report_content=state.report_content,
        push_results=new_results
    )


# 子图节点：清理当前用户（为下一次循环做准备）
def clear_current_user(state: LoopState) -> LoopState:
    """清理当前用户标记"""
    return LoopState(
        users=state.users,
        current_user="",
        report_content=state.report_content,
        push_results=state.push_results
    )


# 条件判断：是否还有用户需要处理
def has_more_users(state: LoopState) -> str:
    """判断是否还有用户需要处理"""
    if len(state.users) > 0:
        return "继续处理"
    else:
        return "结束"


# 创建子图
def create_batch_push_loop_graph():
    """创建批量推送循环子图"""
    # 创建子图
    loop_graph = StateGraph(LoopState)
    
    # 添加节点
    loop_graph.add_node("extract_next_user", extract_next_user)
    loop_graph.add_node("call_single_push", call_single_push)
    loop_graph.add_node("clear_current_user", clear_current_user)
    
    # 设置入口点
    loop_graph.set_entry_point("extract_next_user")
    
    # 添加边
    loop_graph.add_edge("extract_next_user", "call_single_push")
    loop_graph.add_edge("call_single_push", "clear_current_user")
    
    # 添加条件边
    loop_graph.add_conditional_edges(
        source="clear_current_user",
        path=has_more_users,
        path_map={
            "继续处理": "extract_next_user",
            "结束": END
        }
    )
    
    # 编译子图
    return loop_graph.compile()


# 创建子图实例（供主图调用）
batch_push_loop_graph = create_batch_push_loop_graph()


# 主图调用子图的包装函数
def invoke_batch_push_loop(users: List[str], report_content: str) -> List[dict]:
    """
    主图调用子图的包装函数
    
    Args:
        users: 订阅用户列表
        report_content: 情报报告内容
    
    Returns:
        push_results: 推送结果列表
    """
    # 构造子图初始状态
    initial_state = LoopState(
        users=users,
        current_user="",
        report_content=report_content,
        push_results=[]
    )
    
    # 调用子图
    final_state = batch_push_loop_graph.invoke(initial_state)
    
    # 确保 final_state 是 LoopState 类型，并提取 push_results
    if isinstance(final_state, LoopState):
        return final_state.push_results
    else:
        return []
