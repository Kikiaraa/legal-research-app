# 🚨 紧急修复：Worker超时持续问题

## 当前状态

Worker超时问题仍在发生，尽管已经：
1. ✅ 增加超时时间到300秒
2. ✅ 添加健康检查端点
3. ✅ 优化知识库加载逻辑

## 🔍 可能的根本原因

### 1. Render健康检查触发知识库加载
Render可能在健康检查时访问根路径，触发了知识库加载

### 2. 内存不足
免费计划内存有限（512MB），加载多个docx文件可能导致内存不足

### 3. 首次请求超时
即使增加了超时时间，首次加载所有docx文件仍然可能超时

---

## 🆘 紧急修复方案

### 方案A: 临时禁用docx文件（推荐）

将所有docx文件转换为txt格式或临时移除：

```bash
# 在本地执行
cd knowledge-base
# 备份docx文件
mkdir -p ../backup_docx
mv *.docx ../backup_docx/

# 提交更改
git add .
git commit -m "Temp: Remove docx files to fix worker timeout"
git push origin main
```

### 方案B: 修改代码跳过docx文件

修改 `backend/app.py` 中的 `load_knowledge_base` 函数：

```python
# 临时只加载txt文件
if filename.lower().endswith('.txt'):  # 移除 '.docx'
    # 处理txt文件
```

### 方案C: 使用更简单的启动配置

修改 `Procfile`:
```
web: gunicorn --bind 0.0.0.0:$PORT --timeout 600 --workers 1 --worker-class sync --log-level debug backend.app:app
```

---

## 🔧 立即执行的修复

### 步骤1: 简化知识库
```bash
# 只保留txt文件
cd knowledge-base
mkdir ../docx_backup
mv *.docx ../docx_backup/ 2>/dev/null || true
```

### 步骤2: 修改代码只加载txt
在 `backend/app.py` 中：

```python
def load_knowledge_base(jurisdiction=None):
    """加载知识库内容 - 临时只加载txt文件"""
    knowledge_content = ""
    knowledge_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../knowledge-base')
    
    if not os.path.exists(knowledge_dir):
        return knowledge_content
    
    if jurisdiction and jurisdiction in JURISDICTIONS:
        # 只匹配txt文件
        txt_pattern = os.path.join(knowledge_dir, f"{jurisdiction}_*.txt")
        matching_files = glob.glob(txt_pattern)
        
        for filepath in matching_files:
            filename = os.path.basename(filepath)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    law_name = filename.replace(f"{jurisdiction}_", "").replace(".txt", "")
                    knowledge_content += f"\n\n=== {jurisdiction} - {law_name} ===\n\n{content}"
            except Exception as e:
                print(f"读取文件 {filename} 失败: {e}")
    
    return knowledge_content
```

### 步骤3: 推送更改
```bash
git add backend/app.py
git commit -m "Emergency fix: Only load txt files to prevent timeout"
git push origin main
```

---

## 📊 Render控制台操作

### 如果代码修复不够快

1. **手动重启服务**
   - 在Render控制台点击 "Manual Deploy"
   - 选择 "Clear build cache & deploy"

2. **查看详细日志**
   - 切换到 "Logs" 标签
   - 查看完整的启动日志
   - 找到具体卡住的地方

3. **临时解决方案**
   - 考虑暂时使用更简单的应用版本
   - 或升级到付费计划获得更多资源

---

## 🎯 长期解决方案

### 1. 将docx转换为txt
```bash
# 使用python脚本批量转换
python convert_docx_to_txt.py
```

### 2. 使用数据库
- 将知识库内容存储在数据库中
- 避免每次请求都读取文件

### 3. 实现缓存
- 使用Redis缓存已加载的知识库
- 减少重复加载

### 4. 升级Render计划
- Starter ($7/月): 更多内存和CPU
- Standard ($25/月): 更好的性能

---

## 🔍 调试信息

### 查看当前使用的资源
在Render控制台的 "Metrics" 标签页查看：
- CPU使用率
- 内存使用率
- 请求响应时间

### 查看启动日志
关键信息：
```
[INFO] Starting gunicorn
[INFO] Listening at: http://0.0.0.0:10000
[INFO] Booting worker with pid: XX
```

如果卡在某个地方超过30秒，就会触发超时。

---

## ⚡ 快速测试

### 测试健康检查端点
```bash
curl https://legal-research-app.onrender.com/health
```

应该立即返回：
```json
{
  "status": "healthy",
  "service": "legal-research-app",
  "api_configured": true
}
```

---

## 📞 需要立即帮助？

如果问题紧急，考虑：
1. 临时回滚到之前的工作版本
2. 移除所有docx文件
3. 升级到付费计划
4. 联系Render支持

---

**创建时间**: 2025年12月9日
**优先级**: 🔴 紧急
**状态**: 等待验证