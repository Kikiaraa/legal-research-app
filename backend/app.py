from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv
import json
import sys
import glob
import docx

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 加载环境变量
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Deepseek API配置
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
if not DEEPSEEK_API_KEY:
    print("警告：未设置 DEEPSEEK_API_KEY 环境变量")
    print("请在生产环境中设置此环境变量")

DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'

# 支持的司法辖区
JURISDICTIONS = [
    "英国",
    "加拿大", 
    "法国",
    "德国",
    "西班牙",
    "爱尔兰",
    "荷兰",
    "阿根廷",
    "阿塞拜疆",
    "土耳其"
]

# 欧盟成员国（适用GDPR）
EU_COUNTRIES = ["法国", "德国", "西班牙", "爱尔兰", "荷兰"]

# 问题模板
QUESTIONS = {
    "1": {
        "title": "是否有准入要求？",
        "prompt": "根据用户选择的司法辖区，检索对应辖区的法律法规，回答是否存在准入要求。若有相关规定，请回答'有'，并给出法律依据。若没有相关规定，请回答'无'。常见的准入要求包括：1）向司法辖区数据保护机构注册登记；或2）向司法辖区数据保护机构事前通知、备案；或3）取得司法辖区数据保护机构的授权或许可；或4）向司法辖区数据保护机构缴纳费用。"
    },
    "2": {
        "title": "适用于哪些主体？",
        "prompt": "根据对应辖区的法律法规，回答哪些主体适用准入要求，并给出相应的法律依据。若有相关规定，请进一步检索规定适用于所有行业的数据控制者或数据处理者，还是特定行业的数据控制者或数据处理者。若明确规定适用于特定行业的数据控制者或数据处理者，请说明是哪些特定行业；若没有规定适用于哪些特定行业或没有明确规定，请说明适用于所有行业。"
    },
    "3": {
        "title": "是否有豁免情形？",
        "prompt": "根据对应辖区的法律法规，回答相关准入要求是否有豁免的情形。若检索到相关规定，请说明哪些情形依法被豁免，并给出法律依据。若未检索到相关规定，请说明'暂不存在豁免情形'。"
    },
    "4": {
        "title": "在哪注册登记/备案/许可/缴费申请？",
        "prompt": "根据检索的司法辖区法律法规，请回答数据控制者或数据处理者办理注册登记/备案/许可/缴费申请的地点或平台。若检索到相关规定，请优先给出申请的官方机构、官方网站、线上系统或线下窗口名称；并提供官方参考链接或联系方式，并给出相应的法律依据。若未检索到相关规定，请说明'暂无相关规定'。"
    },
    "5": {
        "title": "是否需要缴费？",
        "prompt": "根据检索的司法辖区法律法规，判断在该司法辖区内数据控制者或数据处理者是否需要向监管机构或其他机构缴纳费用（如注册费、许可费、年费等）。若有相关规定，请说明缴费的条件、金额范围、缴费周期等具体规定，并给出相应的法律依据。若无相关规定，请直接回答'暂无相关规定'。"
    },
    "6": {
        "title": "是否规定了注册登记/备案/许可/缴费证书的有效期及续展？",
        "prompt": "根据检索的司法辖区法律法规，判断并回答该司法辖区是否规定了数据控制者/数据处理者注册登记/备案/许可/缴费证书的有效期及续展。如果检索到相关规定，请概述规定的内容（包括有效期时长、续展条件、申请程序等），并给出对应条文原文或核心摘录。如果没有规定，请说明'暂无相关规定'。"
    },
    "7": {
        "title": "没有履行相应数据处理准入的法律义务，会面临什么责任？",
        "prompt": "根据检索的相关国家法律法规，判断该司法辖区法律法规中是否有规定没有履行相应数据处理准入的法律义务所面临的法律责任。如检索到相关规定，请分别说明面临的法律责任类型（包括行政处罚、刑事责任、民事责任）、行政处罚类型（包括但不限于警告、罚款、采取纠正措施、暂停/限制数据处理活动等）、刑事责任类型（包括但不限于单处或并处罚金、监禁等）、民事赔偿（包括但不限于向个人信息主体支付赔偿金等），并列明相关法律依据。如未检索到相关规定，请说明'暂无相关规定'。"
    }
}

def load_knowledge_base(jurisdiction=None):
    """加载知识库内容 - 仅在请求时加载，不在启动时加载"""
    knowledge_content = ""
    # 使用绝对路径确保在不同环境中都能正确找到知识库目录
    knowledge_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../knowledge-base')
    
    if not os.path.exists(knowledge_dir):
        print(f"警告：知识库目录不存在: {knowledge_dir}")
        return knowledge_content
    
    # 如果指定了司法辖区，只加载对应文件
    if jurisdiction and jurisdiction in JURISDICTIONS:
        # 匹配以"司法辖区_"开头的txt和docx文件
        txt_pattern = os.path.join(knowledge_dir, f"{jurisdiction}_*.txt")
        docx_pattern = os.path.join(knowledge_dir, f"{jurisdiction}_*.docx")
        matching_files = glob.glob(txt_pattern) + glob.glob(docx_pattern)
        
        # 如果是欧盟成员国，自动添加GDPR文件
        if jurisdiction in EU_COUNTRIES:
            gdpr_file = os.path.join(knowledge_dir, "欧盟_GDPR.docx")
            if os.path.exists(gdpr_file) and gdpr_file not in matching_files:
                matching_files.append(gdpr_file)
        
        if matching_files:
            for filepath in matching_files:
                filename = os.path.basename(filepath)
                try:
                    if filename.lower().endswith('.txt'):
                        # 尝试使用utf-8编码
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # 从文件名提取法规名称
                            law_name = filename.replace(f"{jurisdiction}_", "").replace(".txt", "")
                            knowledge_content += f"""
{filename}
=== {jurisdiction} - {law_name} ===
{content}"""
                    elif filename.lower().endswith('.docx'):
                        # 使用python-docx读取docx文件
                        doc = docx.Document(filepath)
                        content = '\n'.join([para.text for para in doc.paragraphs])
                        law_name = filename.replace(f"{jurisdiction}_", "").replace(".docx", "")
                        knowledge_content += f"""
{filename}
=== {jurisdiction} - {law_name} ===
{content}"""
                except UnicodeDecodeError:
                    try:
                        # 尝试使用gbk编码
                        with open(filepath, 'r', encoding='gbk') as f:
                            content = f.read()
                            law_name = filename.replace(f"{jurisdiction}_", "").replace(".txt", "")
                            knowledge_content += f"\n\n=== {jurisdiction} - {law_name} ===\n\n{content}"
                    except Exception as e:
                        print(f"读取文件 {filename} 失败: {e}")
                except Exception as e:
                    print(f"读取文件 {filename} 失败: {e}")
        else:
            # 如果没有找到以"司法辖区_"开头的文件，尝试查找旧格式的文件（向后兼容）
            old_format_file = os.path.join(knowledge_dir, f"{jurisdiction}.txt")
            if os.path.exists(old_format_file):
                try:
                    with open(old_format_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        knowledge_content = f"=== {jurisdiction}法律法规 ===\n\n{content}"
                except UnicodeDecodeError:
                    try:
                        with open(old_format_file, 'r', encoding='gbk') as f:
                            content = f.read()
                            knowledge_content = f"=== {jurisdiction}法律法规 ===\n\n{content}"
                    except Exception as e:
                        print(f"读取文件 {jurisdiction}.txt 失败: {e}")
                except Exception as e:
                    print(f"读取文件 {jurisdiction}.txt 失败: {e}")
    else:
        # 加载所有文件（保持向后兼容）
        for filename in os.listdir(knowledge_dir):
            # 支持txt和docx格式，排除README文件
            if (filename.lower().endswith(('.txt', '.docx'))) and not filename.startswith('README'):
                try:
                    # 尝试使用utf-8编码
                    with open(os.path.join(knowledge_dir, filename), 'r', encoding='utf-8') as f:
                        content = f.read()
                        knowledge_content += f"\n\n=== {filename} ===\n\n{content}"
                except UnicodeDecodeError:
                    try:
                        # 尝试使用gbk编码
                        with open(os.path.join(knowledge_dir, filename), 'r', encoding='gbk') as f:
                            content = f.read()
                            knowledge_content += f"\n\n=== {filename} ===\n\n{content}"
                    except Exception as e:
                        print(f"读取文件 {filename} 失败: {e}")
                except Exception as e:
                    print(f"读取文件 {filename} 失败: {e}")
    
    return knowledge_content

def call_deepseek_api(prompt, knowledge_content, jurisdiction):
    """调用Deepseek API"""
    if not DEEPSEEK_API_KEY:
        return "错误：未配置 DEEPSEEK_API_KEY 环境变量，无法调用AI服务。请联系管理员配置API密钥。"
    
    headers = {
        'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    system_prompt = f"""你是一个专业的法律法规检索助手。请严格根据以下{jurisdiction}的法律法规知识库内容回答问题，不要添加知识库中没有的信息。

{jurisdiction}法律法规知识库内容：
{knowledge_content}

请严格围绕当前用户问题作答，忽略知识库中与问题无关的内容，仅使用直接相关的知识。回答后使用'法律依据：'标签单独列出法条原文，需从knowledge-base中提取。应注明具体法律法规及条款，条款过长可使用省略号结尾，禁止翻译。
作答时请勿使用Markdown语法（如 **、#、[]() 等符号）。
"""
    
    data = {
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': prompt}
        ],
        'temperature': 0.1,
        'max_tokens': 2000
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"API调用失败: {str(e)}"

@app.route('/api/questions', methods=['GET'])
def get_questions():
    """获取所有问题列表"""
    app.logger.info('Received request for questions list')
    return jsonify(QUESTIONS)

@app.route('/api/jurisdictions', methods=['GET'])
def get_jurisdictions():
    """获取所有司法辖区列表"""
    app.logger.info('Received request for jurisdictions list')
    return jsonify(JURISDICTIONS)



@app.route('/', methods=['GET'])
def serve_frontend():
    """提供前端页面访问"""
    return send_from_directory(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../frontend'), 'index.html')

@app.route('/<path:path>', endpoint='frontend_assets')
def serve_frontend_assets(path):
    """提供前端静态文件访问"""
    return send_from_directory(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../frontend'), path)

@app.route('/api/research', methods=['POST'])
def research():
    """执行法律法规检索"""
    data = request.json
    jurisdiction = data.get('jurisdiction')
    question_ids = data.get('questions', [])
    
    if not jurisdiction:
        return jsonify({'error': '请选择司法辖区'}), 400
    
    if jurisdiction not in JURISDICTIONS:
        return jsonify({'error': f'不支持的司法辖区: {jurisdiction}'}), 400
    
    if not question_ids:
        return jsonify({'error': '请选择问题'}), 400
    
    # 加载指定司法辖区的知识库
    knowledge_content = load_knowledge_base(jurisdiction)
    if not knowledge_content:
        return jsonify({'error': f'未找到{jurisdiction}的法律法规文件，请添加以"{jurisdiction}_"开头的.txt文件'}), 404
    
    # 生成摘要
    summary_prompt = f"请根据以下{jurisdiction}的法律法规内容，撰写一段数据隐私准入制度的摘要（不超过200字，仅概述核心结论，不要包含法律依据）：{knowledge_content[:5000]}"
    summary = call_deepseek_api(summary_prompt, knowledge_content, jurisdiction)
    
    # 生成引言
    intro_prompt = f"请根据以下{jurisdiction}的法律法规内容，撰写一段关于数据隐私准入制度的简介（不超过200字，仅概述核心内容，不要包含法律依据）：{knowledge_content[:5000]}"
    introduction = call_deepseek_api(intro_prompt, knowledge_content, jurisdiction)
    
    results = []
    for question_id in question_ids:
        if question_id in QUESTIONS:
            question = QUESTIONS[question_id]
            prompt = f"针对{jurisdiction}，{question['prompt']}。请仅回答此问题，不要涉及其他任何问题的内容。"
            
            # 调用AI API
            answer = call_deepseek_api(prompt, knowledge_content, jurisdiction)
            
            results.append({
                'question_id': question_id,
                'question_title': question['title'],
                'answer': answer
            })
    
    # 检查知识库内容是否过长
    content_truncated = len(knowledge_content) > 5000
    
    # 构建报告格式
    report = f"出海目标国数据隐私准入法律检索报告\n\n具体要求请见下文\n\n(一) {jurisdiction}\n\n{introduction}"
    
    # 添加内容截断警告
    if content_truncated:
        report += "\n\n⚠️ 注意：由于知识库内容过长，部分信息已被截断以适应模型上下文限制，可能影响回答的完整性。"
    
    for result in results:
        report += f"\n\nQ{result['question_id']}: {result['question_title']}\nA: {result['answer']}"
    
    return jsonify({'report': report})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)