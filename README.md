# 法律法规检索应用

## 功能概述
用户可以选择想要回答的问题，系统根据知识库内容调用后端AI API生成检索报告。

## 支持的问题类型
1. 是否有准入要求？
2. 适用于哪些主体？
3. 是否有豁免情形？
4. 在哪注册登记/备案/许可/缴费申请？
5. 是否需要缴费？
6. 是否规定了注册登记/备案/许可/缴费证书的有效期及续展？
7. 没有履行相应数据处理准入的法律义务，会面临什么责任？

## 技术栈
- 前端：HTML + CSS + JavaScript
- 后端：Python + Flask
- AI API：Deepseek API

## 项目结构
```
├── frontend/          # HTML前端应用
├── backend/           # Python Flask后端API
├── knowledge-base/    # 知识库文件
└── README.md
```