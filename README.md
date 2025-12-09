# 法律法规检索应用

基于AI的法律法规检索系统，支持多个司法辖区的数据保护法律查询。

## 🌐 在线访问

**应用地址**: https://legal-research-app.onrender.com

## 📋 功能特性

- 支持多个司法辖区：英国、加拿大、法国、德国、西班牙、爱尔兰、荷兰、土耳其、阿塞拜疆、阿根廷
- 基于AI的专业法律分析（Deepseek API）
- 响应式用户界面
- 支持txt和docx格式的知识库文件

## 🚀 本地运行

### 前置要求
- Python 3.11+
- Deepseek API密钥

### 安装步骤

1. 克隆项目
```bash
git clone https://github.com/Kikiaraa/legal-research-app.git
cd legal-research-app
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置环境变量
```bash
# 创建 backend/.env 文件
echo "DEEPSEEK_API_KEY=your_api_key_here" > backend/.env
```

4. 运行应用
```bash
python run.py
```

5. 访问应用
打开浏览器访问 http://localhost:5001

## 📁 项目结构

```
legal-research-app/
├── backend/
│   ├── app.py              # Flask后端应用
│   └── .env               # 环境变量配置
├── frontend/
│   ├── index.html         # 前端页面
│   ├── script.js          # JavaScript逻辑
│   └── styles.css         # 样式文件
├── knowledge-base/
│   ├── 英国_*.txt         # 英国法律文件
│   ├── 加拿大_*.txt       # 加拿大法律文件
│   └── ...                # 其他司法辖区文件
├── requirements.txt       # Python依赖
├── Procfile              # Render启动配置
├── render.yaml           # Render部署配置
└── runtime.txt           # Python版本
```

## 🔧 知识库管理

### 文件命名规范
```
{司法辖区}_{法规名称}.txt
{司法辖区}_{法规名称}.docx
```

### 示例
```
英国_DPA2018.txt
加拿大_PIPEDA.txt
法国_《法国国家信息与自由法》切片.docx
```

### 添加新的司法辖区

1. 在 `knowledge-base/` 目录添加文件
2. 在 `backend/app.py` 的 `JURISDICTIONS` 列表中添加司法辖区名称
3. 重启应用

## 🌐 部署到Render

详细部署指南请查看 [RENDER_DEPLOY_GUIDE.md](RENDER_DEPLOY_GUIDE.md)

### 快速部署

1. 推送代码到GitHub
2. 在Render创建Web Service
3. 设置环境变量 `DEEPSEEK_API_KEY`
4. 部署完成

## 🛠️ 技术栈

- **后端**: Python Flask + Gunicorn
- **前端**: HTML5 + CSS3 + JavaScript
- **AI服务**: Deepseek API
- **部署**: Render Platform
- **知识库**: txt/docx文件

## 📞 使用说明

1. 选择司法辖区
2. 勾选要查询的问题
3. 点击"生成报告"
4. 查看AI生成的法律分析报告

## ⚙️ 配置说明

### 环境变量
- `DEEPSEEK_API_KEY`: Deepseek API密钥（必需）
- `PORT`: 应用端口（默认5001）

### API超时设置
- 连接超时: 10秒
- 读取超时: 60秒

## 📄 许可证

本项目仅供学习和研究使用。

## 🤝 贡献

欢迎提交Issue和Pull Request。

---

**最后更新**: 2025年12月9日