from langgraph.graph import StateGraph, END
from graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput
)
from graphs.nodes.generate_intelligence_node import generate_intelligence_node
from graphs.nodes.format_html_node import format_html_node
from graphs.nodes.batch_push_node import batch_push_node


# 创建状态图
builder = StateGraph(GlobalState, input_schema=GraphInput, output_schema=GraphOutput)

# 添加节点
builder.add_node(
    "generate_intelligence",
    generate_intelligence_node,
    metadata={"type": "agent", "llm_cfg": "config/generate_intelligence_cfg.json"}
)
builder.add_node("format_html", format_html_node)  # 新增：HTML格式化节点
builder.add_node("batch_push", batch_push_node)

# 设置入口点
builder.set_entry_point("generate_intelligence")

# 添加边：情报生成 -> HTML格式化 -> 批量推送
builder.add_edge("generate_intelligence", "format_html")
builder.add_edge("format_html", "batch_push")
builder.add_edge("batch_push", END)

# 编译图
main_graph = builder.compile()
