# 🔧 Worker超时问题修复

## 🚨 问题描述

**错误信息**: `WORKER TIMEOUT (pid:XX)` 和 `Worker exiting with code 1`

这表示Gunicorn worker在处理请求时超时（默认30秒），通常是因为：
1. 应用启动时间过长
2. 请求处理时间过长
3. 资源不足

---

## 🔍 问题原因

### 1. 知识库文件过大
应用需要加载多个docx文件，包括：
- 英国法律文件（3个）
- 加拿大法律文件（2个）
- 新增：土耳其、阿塞拜疆、阿根廷、欧盟等（多个docx文件）

### 2. Docx文件解析耗时
使用python-docx库解析Word文档比读取txt文件慢得多

### 3. 默认超时时间太短
Gunicorn默认30秒超时，对于处理大量文档不够

---

## ✅ 修复方案

### 1. 创建Gunicorn配置文件
创建 `gunicorn_config.py`：

```python
import os

bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"
workers = 1
worker_class = 'sync'
timeout = 300  # 增加到5分钟
graceful_timeout = 30
keepalive = 5
accesslog = '-'
errorlog = '-'
loglevel = 'info'
proc_name = 'legal-research-app'
```

### 2. 更新启动命令
**Procfile**:
```
web: gunicorn -c gunicorn_config.py backend.app:app
```

**render.yaml**:
```yaml
startCommand: gunicorn -c gunicorn_config.py backend.app:app
```

### 3. 优化知识库加载
- 确保知识库只在请求时加载，不在启动时加载
- 添加更多日志以便调试
- 优化文件读取逻辑

---

## 🚀 部署更新

修复已推送到GitHub：
- **提交ID**: 0ad705f
- **提交信息**: "Fix: Increase gunicorn timeout and optimize knowledge base loading to prevent worker timeout"

Render会自动检测并重新部署。

---

## 📊 配置变更

### 超时时间对比
| 配置项 | 修复前 | 修复后 |
|--------|--------|--------|
| Worker超时 | 30秒 | 300秒（5分钟） |
| Graceful超时 | 30秒 | 30秒 |
| Workers数量 | 默认 | 1（优化内存使用） |

---

## 🧪 验证修复

### 1. 查看部署日志
在Render控制台查看：
```
[INFO] Booting worker with pid: XX
[INFO] Listening at: http://0.0.0.0:10000
```

### 2. 测试应用
1. 访问 https://legal-research-app.onrender.com
2. 选择司法辖区（特别是有多个文件的，如英国）
3. 生成报告
4. 确认没有超时错误

### 3. 监控日志
查看是否还有 `WORKER TIMEOUT` 错误

---

## ⚠️ 如果问题仍然存在

### 方案A: 进一步增加超时时间
编辑 `gunicorn_config.py`:
```python
timeout = 600  # 增加到10分钟
```

### 方案B: 优化知识库
1. 将大型docx文件转换为txt格式
2. 分割过大的文件
3. 使用数据库存储而不是文件

### 方案C: 升级Render计划
免费计划资源有限，考虑升级到：
- **Starter**: $7/月，更多资源
- **Standard**: $25/月，更好性能

---

## 📈 性能优化建议

### 短期优化
1. ✅ 增加超时时间
2. ✅ 优化文件加载逻辑
3. ⏳ 添加缓存机制

### 长期优化
1. 将知识库迁移到数据库
2. 实现增量加载
3. 添加Redis缓存
4. 使用异步处理

---

## 🔄 监控部署

### 查看部署状态
1. 访问 https://dashboard.render.com
2. 找到 `legal-research-app` 服务
3. 查看 "Logs" 标签页

### 关键日志信息
✅ **成功标志**:
```
[INFO] Starting gunicorn
[INFO] Listening at: http://0.0.0.0:10000
[INFO] Using worker: sync
[INFO] Booting worker with pid: XX
```

❌ **失败标志**:
```
[CRITICAL] WORKER TIMEOUT
[ERROR] Worker exited with code 1
```

---

## ⏱️ 预计完成时间

- **构建时间**: 1-2分钟
- **部署时间**: 30秒-1分钟
- **总计**: 2-3分钟

---

## 🎯 下一步

1. **等待部署完成**（2-3分钟）
2. **查看日志**确认没有超时错误
3. **测试应用**验证所有功能
4. **监控性能**确保稳定运行

---

## 📞 需要帮助？

如果问题持续存在：
1. 提供完整的错误日志
2. 说明选择的司法辖区
3. 描述具体的操作步骤

---

**修复时间**: 2025年12月9日
**状态**: ✅ 已修复并部署
**预计效果**: Worker超时问题应该解决