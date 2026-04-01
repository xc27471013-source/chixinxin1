import os
import json
import datetime
from jinja2 import Template
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context, new_context
from coze_coding_dev_sdk import SearchClient, LLMClient
from graphs.state import GenerateIntelligenceInput, GenerateIntelligenceOutput


def generate_intelligence_node(state: GenerateIntelligenceInput, config: RunnableConfig, runtime: Runtime[Context]) -> GenerateIntelligenceOutput:
    """
    title: 情报生成
    desc: 搜索今日全球关键信息，生成 Yang Daily Intelligence 认知情报报告
    integrations: web-search, 大语言模型
    """
    ctx = runtime.context
    
    # 获取当前日期
    current_date = datetime.datetime.now().strftime("%Y年%m月%d日")
    
    # 步骤1：搜索今日关键信息
    search_queries = [
        "今日全球宏观经济变化 通胀 货币",
        "今日AI人工智能最新动态",
        "今日资本流向 产业变化",
        "洛杉矶华人创业活动机会",
        "全球科技趋势 财富机会"
    ]
    
    all_search_results = []
    
    try:
        search_ctx = new_context(method="intelligence.search")
        search_client = SearchClient(ctx=search_ctx)
        
        for query in search_queries:
            try:
                response = search_client.web_search(
                    query=query,
                    count=5,
                    time_range="1d",  # 最近1天
                    need_summary=True
                )
                
                if response.web_items:
                    for item in response.web_items:
                        result_text = f"标题：{item.title}\n来源：{item.site_name}\n摘要：{item.snippet}"
                        if item.summary:
                            result_text += f"\n总结：{item.summary}"
                        all_search_results.append(result_text)
            except Exception as e:
                # 单个搜索失败不影响整体
                continue
                
    except Exception as e:
        raise Exception(f"搜索信息失败: {str(e)}")
    
    # 如果搜索结果为空，使用备用搜索
    if not all_search_results:
        try:
            backup_query = "今日全球重要新闻 宏观 科技"
            search_ctx = new_context(method="intelligence.search.backup")
            search_client = SearchClient(ctx=search_ctx)
            response = search_client.web_search(query=backup_query, count=10, need_summary=True)
            
            if response.web_items:
                for item in response.web_items:
                    result_text = f"标题：{item.title}\n来源：{item.site_name}\n摘要：{item.snippet}"
                    if item.summary:
                        result_text += f"\n总结：{item.summary}"
                    all_search_results.append(result_text)
        except Exception as e:
            pass  # 备用搜索也失败，继续生成报告
    
    # 步骤2：读取 LLM 配置
    cfg_file = os.path.join(os.getenv("COZE_WORKSPACE_PATH"), config['metadata']['llm_cfg'])
    with open(cfg_file, 'r', encoding='utf-8') as fd:
        _cfg = json.load(fd)
    
    llm_config = _cfg.get("config", {})
    sp = _cfg.get("sp", "")
    up = _cfg.get("up", "")
    
    # 步骤3：使用 Jinja2 模板渲染用户提示词
    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({
        "current_date": current_date,
        "search_results": "\n\n".join(all_search_results) if all_search_results else "未搜索到今日关键信息，请基于常识和分析能力生成报告。"
    })
    
    # 步骤4：调用 LLM 生成情报报告
    try:
        llm_ctx = new_context(method="intelligence.llm")
        llm_client = LLMClient(ctx=llm_ctx)
        
        # 构造 LangChain 消息格式
        messages = [
            SystemMessage(content=sp),
            HumanMessage(content=user_prompt_content)
        ]
        
        response = llm_client.invoke(
            messages=messages,
            model=llm_config.get("model", "doubao-seed-2-0-pro-260215"),
            temperature=llm_config.get("temperature", 0.3),
            top_p=llm_config.get("top_p", 0.9),
            max_completion_tokens=llm_config.get("max_completion_tokens", 4000),
            thinking=llm_config.get("thinking", "disabled")
        )
        
        # 提取 LLM 响应内容（安全处理多种类型）
        def get_text_content(content):
            if isinstance(content, str):
                return content
            elif isinstance(content, list):
                if content and isinstance(content[0], str):
                    return " ".join(content)
                else:
                    return " ".join(item.get("text", "") for item in content if isinstance(item, dict) and item.get("type") == "text")
            return str(content)
        
        intelligence_report = get_text_content(response.content)
        
        # 清理可能的 Markdown 代码块标记
        if intelligence_report.startswith("```markdown"):
            intelligence_report = intelligence_report[len("```markdown"):].strip()
        if intelligence_report.startswith("```"):
            intelligence_report = intelligence_report[len("```"):].strip()
        if intelligence_report.endswith("```"):
            intelligence_report = intelligence_report[:-3].strip()
            
    except Exception as e:
        raise Exception(f"生成情报报告失败: {str(e)}")
    
    return GenerateIntelligenceOutput(intelligence_report=intelligence_report)
