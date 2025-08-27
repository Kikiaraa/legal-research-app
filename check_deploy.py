#!/usr/bin/env python3
"""
部署前检查脚本
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """检查文件是否存在"""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description}: {filepath} (缺失)")
        return False

def check_directory_structure():
    """检查目录结构"""
    print("检查项目结构...")
    print("=" * 50)
    
    required_files = [
        ("requirements.txt", "项目依赖文件"),
        ("render.yaml", "Render配置文件"),
        ("Procfile", "启动配置文件"),
        ("runtime.txt", "Python版本文件"),
        (".gitignore", "Git忽略文件"),
        ("backend/app.py", "后端应用"),
        ("frontend/index.html", "前端页面"),
        ("frontend/script.js", "前端脚本"),
    ]
    
    all_good = True
    for filepath, description in required_files:
        if not check_file_exists(filepath, description):
            all_good = False
    
    return all_good

def check_knowledge_base():
    """检查知识库文件"""
    print("\n检查知识库文件...")
    print("=" * 50)
    
    kb_dir = Path("knowledge-base")
    if not kb_dir.exists():
        print("✗ 知识库目录不存在")
        return False
    
    txt_files = list(kb_dir.glob("*.txt"))
    law_files = [f for f in txt_files if not f.name.startswith('README')]
    
    if len(law_files) == 0:
        print("✗ 没有找到法律法规文件")
        return False
    
    print(f"✓ 找到 {len(law_files)} 个法律法规文件")
    
    # 按司法辖区分组
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

def check_environment():
    """检查环境配置"""
    print("\n检查环境配置...")
    print("=" * 50)
    
    env_file = Path("backend/.env")
    if env_file.exists():
        print("✓ 找到本地环境配置文件")
        print("⚠ 注意：部署时需要在Render中设置DEEPSEEK_API_KEY环境变量")
    else:
        print("⚠ 未找到本地环境配置文件")
        print("⚠ 确保在Render中设置DEEPSEEK_API_KEY环境变量")
    
    return True

def main():
    print("Render 部署前检查")
    print("=" * 50)
    
    checks = [
        check_directory_structure(),
        check_knowledge_base(),
        check_environment()
    ]
    
    if all(checks):
        print("\n🎉 所有检查通过！项目已准备好部署到Render")
        print("\n下一步：")
        print("1. 将代码推送到GitHub")
        print("2. 在Render创建Web Service")
        print("3. 设置DEEPSEEK_API_KEY环境变量")
        print("4. 部署应用")
    else:
        print("\n❌ 检查失败，请修复上述问题后重试")
        sys.exit(1)

if __name__ == "__main__":
    main()