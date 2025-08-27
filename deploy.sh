#!/bin/bash

echo "🚀 准备部署到 Render..."
echo "================================"

# 检查是否在Git仓库中
if [ ! -d ".git" ]; then
    echo "初始化 Git 仓库..."
    git init
fi

# 添加所有文件
echo "添加文件到 Git..."
git add .

# 提交更改
echo "提交更改..."
git commit -m "Deploy to Render: $(date '+%Y-%m-%d %H:%M:%S')"

# 检查是否设置了远程仓库
if ! git remote get-url origin > /dev/null 2>&1; then
    echo ""
    echo "⚠️  请先设置 GitHub 远程仓库："
    echo "   git remote add origin https://github.com/yourusername/legal-research-app.git"
    echo "   然后运行: git push -u origin main"
    echo ""
else
    echo "推送到 GitHub..."
    git push origin main
    echo "✅ 代码已推送到 GitHub"
fi

echo ""
echo "📋 接下来的步骤："
echo "1. 访问 https://render.com"
echo "2. 创建新的 Web Service"
echo "3. 连接你的 GitHub 仓库"
echo "4. 使用以下配置："
echo "   - Build Command: pip install -r requirements.txt"
echo "   - Start Command: gunicorn --bind 0.0.0.0:\$PORT backend.app:app"
echo "5. 设置环境变量 DEEPSEEK_API_KEY"
echo "6. 部署应用"
echo ""
echo "详细指南请查看 RENDER_DEPLOY_GUIDE.md"