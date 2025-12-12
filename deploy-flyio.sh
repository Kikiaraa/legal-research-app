#!/bin/bash

echo "======================================"
echo "部署到 Fly.io"
echo "======================================"

# 检查flyctl是否安装
if ! command -v flyctl &> /dev/null; then
    echo "❌ flyctl 未安装"
    echo ""
    echo "请先安装 flyctl："
    echo "macOS: brew install flyctl"
    echo "或访问: https://fly.io/docs/hands-on/install-flyctl/"
    exit 1
fi

echo "✓ flyctl 已安装"

# 检查是否已登录
if ! flyctl auth whoami &> /dev/null; then
    echo ""
    echo "请先登录 Fly.io："
    echo "运行: flyctl auth login"
    exit 1
fi

echo "✓ 已登录 Fly.io"
echo ""

# 检查应用是否存在
if flyctl apps list | grep -q "legal-research-app"; then
    echo "应用已存在，准备部署..."
    flyctl deploy
else
    echo "首次部署，创建新应用..."
    flyctl launch --no-deploy
    
    echo ""
    echo "设置环境变量..."
    echo "请输入你的 DEEPSEEK_API_KEY:"
    read -s DEEPSEEK_API_KEY
    
    flyctl secrets set DEEPSEEK_API_KEY="$DEEPSEEK_API_KEY"
    
    echo ""
    echo "开始部署..."
    flyctl deploy
fi

echo ""
echo "======================================"
echo "部署完成！"
echo "======================================"
echo ""
echo "查看应用状态: flyctl status"
echo "查看日志: flyctl logs"
echo "打开应用: flyctl open"
echo ""
