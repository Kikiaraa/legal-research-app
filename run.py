#!/usr/bin/env python3
"""
法律法规检索应用启动脚本
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_requirements():
    """检查Python依赖"""
    try:
        import flask
        import flask_cors
        import requests
        from dotenv import load_dotenv
        print("✓ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"✗ 缺少依赖: {e}")
        print("请运行: pip install -r backend/requirements.txt")
        return False

def check_env_file():
    """检查环境变量文件"""
    env_file = Path("backend/.env")
    if not env_file.exists():
        print("✗ 未找到 .env 文件")
        print("请复制 backend/.env.example 为 backend/.env 并配置 DEEPSEEK_API_KEY")
        return False
    
    # 检查API密钥是否配置
    with open(env_file, 'r') as f:
        content = f.read()
        if 'your_deepseek_api_key_here' in content:
            print("✗ 请在 backend/.env 文件中配置正确的 DEEPSEEK_API_KEY")
            return False
    
    print("✓ 环境配置文件检查通过")
    return True

def check_knowledge_base():
    """检查知识库文件"""
    kb_dir = Path("knowledge-base")
    txt_files = list(kb_dir.glob("*.txt"))
    
    # 排除README和示例文件
    law_files = [f for f in txt_files if not f.name.startswith('README') and not f.name.startswith('示例')]
    
    if len(law_files) == 0:
        print("⚠ 知识库中没有法律法规文件")
        print("请在 knowledge-base/ 目录下添加 {司法辖区}_{法规名称}.txt 文件")
    else:
        print(f"✓ 找到 {len(law_files)} 个法律法规文件")
        
        # 按司法辖区分组显示
        jurisdictions = {}
        for file in law_files:
            if '_' in file.name:
                jurisdiction = file.name.split('_')[0]
                if jurisdiction not in jurisdictions:
                    jurisdictions[jurisdiction] = []
                jurisdictions[jurisdiction].append(file.name)
        
        for jurisdiction, files in jurisdictions.items():
            print(f"  - {jurisdiction}: {len(files)} 个文件")
    
    return True

def start_backend():
    """启动后端服务"""
    print("启动后端服务...")
    os.chdir("backend")
    return subprocess.Popen([sys.executable, "app.py"])

def open_frontend():
    """打开前端页面"""
    # 返回项目根目录
    os.chdir("..")
    frontend_url = "http://localhost:5001"
    
    print(f"打开前端页面: {frontend_url}")
    webbrowser.open(frontend_url)
    # 回到backend目录
    os.chdir("backend")

def main():
    print("=" * 50)
    print("法律法规检索应用启动器")
    print("=" * 50)
    
    # 检查依赖
    if not check_requirements():
        return
    
    # 检查环境配置
    if not check_env_file():
        return
    
    # 检查知识库
    check_knowledge_base()
    
    try:
        # 启动后端
        backend_process = start_backend()
        
        # 等待后端启动
        print("等待后端服务启动...")
        time.sleep(3)
        
        # 打开前端
        open_frontend()
        
        print("\n" + "=" * 50)
        print("应用已启动！")
        print("后端API: http://localhost:5000")
        print("前端页面已在浏览器中打开")
        print("按 Ctrl+C 停止服务")
        print("=" * 50)
        
        # 等待用户中断
        backend_process.wait()
        
    except KeyboardInterrupt:
        print("\n正在停止服务...")
        if 'backend_process' in locals():
            backend_process.terminate()
        print("服务已停止")

if __name__ == "__main__":
    main()