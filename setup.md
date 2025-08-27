# 法律法规检索应用 - 安装和使用指南

## 快速开始

### 1. 安装Python依赖
```bash
pip install -r backend/requirements.txt
```

### 2. 配置API密钥
```bash
# 复制环境变量模板
cp backend/.env.example backend/.env

# 编辑 .env 文件，添加你的 Deepseek API Key
# DEEPSEEK_API_KEY=your_actual_api_key_here
```

### 3. 准备知识库
将各司法辖区的法律法规文件放入 `knowledge-base/` 目录，文件命名格式：`{司法辖区名称}_{法规简称}.txt`

例如：
- `英国_DPA2018.txt`
- `英国_数据保护费指南.txt`
- `法国_GDPR.txt`
- `德国_联邦数据保护法.txt`

一个司法辖区可以有多个法规文件，系统会自动加载所有匹配的文件。

### 4. 启动应用
```bash
python run.py
```

或者手动启动：

```bash
# 启动后端
cd backend
python app.py

# 在浏览器中打开 frontend/index.html
```

## 目录结构

```
├── backend/              # Python Flask后端
│   ├── app.py           # 主应用文件
│   ├── requirements.txt # Python依赖
│   ├── .env.example     # 环境变量模板
│   └── .env             # 环境变量配置（需要创建）
├── frontend/            # HTML前端
│   ├── index.html       # 主页面
│   ├── styles.css       # 样式文件
│   └── script.js        # JavaScript逻辑
├── knowledge-base/      # 知识库目录
│   ├── README.md        # 知识库说明
│   └── *.txt            # 各司法辖区法律法规文件
├── run.py              # 启动脚本
├── setup.md            # 本文件
└── README.md           # 项目说明
```

## API接口

### 获取问题列表
```
GET /api/questions
```

### 获取司法辖区列表
```
GET /api/jurisdictions
```

### 执行法律检索
```
POST /api/research
Content-Type: application/json

{
  "jurisdiction": "司法辖区名称",
  "questions": ["1", "2", "3"]
}
```

### 获取司法辖区列表
```
GET /api/jurisdictions
```

## 使用说明

1. **选择司法辖区**：从下拉菜单中选择要查询的司法辖区（英国、加拿大、法国、德国、西班牙、爱尔兰、荷兰）
2. **选择问题**：勾选一个或多个要查询的问题
3. **生成报告**：点击"生成检索报告"按钮
4. **查看结果**：系统将调用AI API分析对应司法辖区的法律法规并生成专业报告

## 注意事项

- 确保 Deepseek API Key 配置正确
- 知识库文件应包含完整的法律法规内容
- 文件编码应为 UTF-8
- 后端默认运行在 5000 端口
- 支持每个司法辖区多个法规文件
- 文件命名格式：{司法辖区}_{法规名称}.txt

## 故障排除

### 常见问题

1. **API调用失败**
   - 检查 API Key 是否正确配置
   - 确认网络连接正常
   - 查看后端控制台错误信息

2. **知识库加载失败**
   - 确认文件路径正确
   - 检查文件编码为 UTF-8
   - 确认文件内容不为空

3. **前端无法连接后端**
   - 确认后端服务正常启动
   - 检查端口 5000 是否被占用
   - 查看浏览器控制台错误信息