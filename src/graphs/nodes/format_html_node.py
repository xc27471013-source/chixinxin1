"""
Yang Daily Intelligence - HTML格式化节点
将Markdown情报转换为美观的HTML可视化内容
"""
import os
import re
import random
import json
import datetime
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import FormatHtmlInput, FormatHtmlOutput
from typing import Tuple


# ==================== 名人名言库 ====================
BUSINESS_QUOTES = [
    ("预测未来的最好方式，就是创造未来。", "彼得·德鲁克", "现代管理学之父"),
    ("机会不会从天而降，机会是自己创造出来的。", "稻盛和夫", "京瓷创始人"),
    ("在商业世界里，变化是唯一不变的事物。", "杰克·韦尔奇", "通用电气前CEO"),
    ("创新是区分领导者和追随者的标志。", "史蒂夫·乔布斯", "苹果创始人"),
    ("如果你不能简单地解释它，说明你还没有理解它。", "爱因斯坦", "物理学家"),
    ("成功不是终点，失败也不是致命的，重要的是继续前进的勇气。", "丘吉尔", "英国首相"),
    ("最大的风险就是不冒任何风险。", "马克·扎克伯格", "Facebook创始人"),
    ("你的时间有限，不要浪费在过别人的生活上。", "史蒂夫·乔布斯", "苹果创始人"),
    ("简单是终极的复杂。", "达芬奇", "艺术家"),
    ("你不能通过解决产生问题的同一思维水平来解决问题。", "爱因斯坦", "物理学家"),
    ("重要的不是你从哪里来，而是你要到哪里去。", "马云", "阿里巴巴创始人"),
    ("技术本身并不重要，重要的是技术如何服务于人。", "任正非", "华为创始人"),
    ("AI不会取代人类，但会使用AI的人将取代不会使用AI的人。", "李开复", "创新工场CEO"),
    ("在不确定性中寻找确定性，这就是战略的本质。", "迈克尔·波特", "战略管理大师"),
    ("最好的预测未来的方式，就是创造未来。", "艾伦·凯", "计算机科学家"),
    ("数据是新时代的石油。", "克莱夫·亨比", "数据科学家"),
    ("未来已来，只是分布不均。", "威廉·吉布森", "科幻作家"),
    ("认知差距将决定财富差距。", "纳瓦尔·拉维坎特", "AngelList创始人"),
]

QUOTE_HISTORY_FILE = "/tmp/yang_quote_history.json"


# ==================== 辅助函数 ====================
def get_unique_quote() -> Tuple[str, str, str]:
    """获取一条未使用过的名言"""
    used_indices = []
    
    if os.path.exists(QUOTE_HISTORY_FILE):
        try:
            with open(QUOTE_HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                used_indices = data.get('used_indices', [])
        except:
            used_indices = []
    
    # 找到未使用的名言索引
    available_indices = [i for i in range(len(BUSINESS_QUOTES)) if i not in used_indices]
    
    # 如果所有名言都用过了，重置历史
    if not available_indices:
        available_indices = list(range(len(BUSINESS_QUOTES)))
        used_indices = []
    
    # 随机选择
    selected_index = random.choice(available_indices)
    
    # 更新历史记录
    used_indices.append(selected_index)
    try:
        with open(QUOTE_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump({'used_indices': used_indices}, f, ensure_ascii=False)
    except:
        pass
    
    return BUSINESS_QUOTES[selected_index]


def format_label_bold(text: str) -> str:
    """将Markdown加粗标签转为HTML"""
    # 将 **文字** 转为 <strong>文字</strong>
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    
    # 特定标签加粗
    labels = ['今日最重要三条变化', '第一性原理解读', '时代趋势', '财富机会提示', '反直觉洞察', '洛杉矶华人机会', 'AI自主推荐']
    for label in labels:
        if label in text:
            text = text.replace(label, f'<strong style="color:#2563eb">{label}</strong>')
    
    return text


def format_markdown_to_html(markdown_text: str) -> str:
    """将Markdown情报转换为HTML格式"""
    lines = markdown_text.split('\n')
    html_parts = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 标题处理
        if line.startswith('# '):
            title = line[2:]
            html_parts.append(f'<h2 style="color:#1e40af;font-size:18px;margin:20px 0 12px;padding-bottom:8px;border-bottom:2px solid #3b82f6;">{title}</h2>')
        elif line.startswith('## '):
            title = line[3:]
            html_parts.append(f'<h3 style="color:#1e40af;font-size:16px;margin:16px 0 10px;padding-left:10px;border-left:3px solid #3b82f6;">{title}</h3>')
        elif line.startswith('### '):
            title = line[4:]
            html_parts.append(f'<h4 style="color:#374151;font-size:15px;margin:14px 0 8px;">{title}</h4>')
        
        # 列表项处理
        elif line.startswith('- '):
            content = format_label_bold(line[2:])
            html_parts.append(f'<li style="margin:6px 0;color:#374151;line-height:1.6;">{content}</li>')
        
        # 数字列表
        elif re.match(r'^\d+\.\s', line):
            content = re.sub(r'^\d+\.\s', '', line)
            content = format_label_bold(content)
            html_parts.append(f'<li style="margin:6px 0;color:#374151;line-height:1.6;">{content}</li>')
        
        # 普通段落
        else:
            content = format_label_bold(line)
            html_parts.append(f'<p style="margin:8px 0;color:#4b5563;line-height:1.7;">{content}</p>')
    
    return '\n'.join(html_parts)


# ==================== 主HTML模板 ====================
def generate_html_report(intelligence_markdown: str) -> str:
    """生成完整的HTML报告"""
    
    # 获取当前日期
    today = datetime.datetime.now().strftime("%Y年%m月%d日")
    
    # 获取不重复名言
    quote_content, quote_author, quote_title = get_unique_quote()
    
    # 转换情报为HTML
    intelligence_html = format_markdown_to_html(intelligence_markdown)
    
    # 完整HTML模板
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yang Daily Intelligence</title>
    <style>
        /* ==================== 基础样式 ==================== */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: #f8fafc;
            padding: 12px;
            line-height: 1.6;
            color: #334155;
        }}
        
        .container {{
            max-width: 680px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        
        /* ==================== 头部样式 ==================== */
        .header {{
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
            color: white;
            padding: 24px 20px;
            text-align: center;
        }}
        
        .main-title {{
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 8px;
            letter-spacing: 0.5px;
        }}
        
        .date {{
            font-size: 14px;
            opacity: 0.9;
        }}
        
        /* ==================== 名言区块 ==================== */
        .quote-box {{
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            padding: 16px 20px;
            margin: 16px;
            border-radius: 8px;
            border-left: 4px solid #3b82f6;
        }}
        
        .quote-content {{
            font-size: 14px;
            color: #1e40af;
            font-style: italic;
            margin-bottom: 8px;
        }}
        
        .quote-author {{
            font-size: 12px;
            color: #6b7280;
            text-align: right;
        }}
        
        /* ==================== 内容区域 ==================== */
        .content {{
            padding: 0 20px 20px;
        }}
        
        .section {{
            margin-bottom: 20px;
        }}
        
        /* ==================== 底部样式 ==================== */
        .footer {{
            background-color: #f1f5f9;
            padding: 16px 20px;
            text-align: center;
            font-size: 12px;
            color: #64748b;
            border-top: 1px solid #e2e8f0;
        }}
        
        .footer-highlight {{
            color: #3b82f6;
            font-weight: 500;
        }}
        
        /* ==================== 标签样式 ==================== */
        .tag {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 500;
            margin-left: 6px;
        }}
        
        .tag-opportunity {{
            background-color: #dcfce7;
            color: #166534;
        }}
        
        .tag-warning {{
            background-color: #fee2e2;
            color: #991b1b;
        }}
        
        .tag-attention {{
            background-color: #fef3c7;
            color: #92400e;
        }}
        
        /* ==================== 响应式 ==================== */
        @media (max-width: 480px) {{
            body {{
                padding: 8px;
            }}
            .header {{
                padding: 20px 16px;
            }}
            .main-title {{
                font-size: 20px;
            }}
            .content {{
                padding: 0 16px 16px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- 头部 -->
        <div class="header">
            <div class="main-title">🌐 Yang Daily Intelligence</div>
            <div class="date">每日认知情报 · {today}</div>
        </div>
        
        <!-- 名言 -->
        <div class="quote-box">
            <div class="quote-content">"{quote_content}"</div>
            <div class="quote-author">—— {quote_author} <span style="color:#94a3b8;">（{quote_title}）</span></div>
        </div>
        
        <!-- 情报内容 -->
        <div class="content">
            {intelligence_html}
        </div>
        
        <!-- 底部 -->
        <div class="footer">
            <p>🤖 AI驱动 · 全球视野 · 每日更新</p>
            <p style="margin-top:6px;">
                <span class="footer-highlight">Yang Daily Intelligence</span> | 让认知先行
            </p>
        </div>
    </div>
</body>
</html>"""
    
    return html_content


# ==================== 节点函数 ====================
def format_html_node(state: FormatHtmlInput, config: RunnableConfig, runtime: Runtime[Context]) -> FormatHtmlOutput:
    """
    title: HTML格式化
    desc: 将Markdown情报转换为美观的HTML可视化报告
    integrations: 无
    """
    ctx = runtime.context
    
    # 生成HTML
    formatted_html = generate_html_report(state.intelligence_report)
    
    return FormatHtmlOutput(formatted_html=formatted_html)
