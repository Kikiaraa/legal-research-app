# 🚀 Render 部署完整指南

## 📋 部署步骤

### 第一步：准备GitHub仓库

1. **初始化Git仓库**（如果还没有）：
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Render deployment"
   ```

2. **创建GitHub仓库**：
   - 访问 [GitHub](https://github.com)
   - 点击 "New repository"
   - 输入仓库名称（如：`legal-research-app`）
   - 选择 "Public" 或 "Private"
   - 点击 "Create repository"

3. **推送代码到GitHub**：
   ```bash
   git remote add origin https://github.com/yourusername/legal-research-app.git
   git branch -M main
   git push -u origin main
   ```

### 第二步：在Render创建Web Service

1. **访问Render**：
   - 打开 [render.com](https://render.com)
   - 注册或登录账号

2. **创建新服务**：
   - 点击 "New +" 按钮
   - 选择 "Web Service"

3. **连接GitHub仓库**：
   - 选择 "Build and deploy from a Git repository"
   - 点击 "Connect" 连接GitHub账号
   - 选择你的仓库

4. **配置服务设置**：
   ```
   Name: legal-research-app
   Environment: Python
   Region: 选择离你最近的区域
   Branch: main
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn --bind 0.0.0.0:$PORT backend.app:app
   ```

### 第三步：设置环境变量

在 "Environment" 标签页添加：
- **Key**: `DEEPSEEK_API_KEY`
- **Value**: 你的Deepseek API密钥

### 第四步：部署

1. 点击 "Create Web Service"
2. 等待构建完成（通常需要2-5分钟）
3. 构建成功后，Render会提供一个 `.onrender.com` 域名

## 🔍 部署后验证

### 1. 访问应用
打开Render提供的域名，应该能看到应用首页

### 2. 功能测试
- 选择司法辖区
- 勾选问题
- 生成报告
- 验证AI回答功能

### 3. 查看日志
在Render控制台的 "Logs" 标签页查看应用运行日志

## 🛠️ 常见问题解决

### 构建失败
**问题**: Build failed
**解决方案**:
1. 检查 `requirements.txt` 文件格式
2. 确保Python版本兼容（使用3.11.0）
3. 查看构建日志中的具体错误信息

### 启动失败
**问题**: Application failed to start
**解决方案**:
1. 检查 `Procfile` 中的启动命令
2. 确保 `backend/app.py` 文件存在
3. 检查代码中是否有语法错误

### API调用失败
**问题**: AI功能不工作
**解决方案**:
1. 确认已设置 `DEEPSEEK_API_KEY` 环境变量
2. 检查API密钥是否有效
3. 查看应用日志中的错误信息

### 静态文件404
**问题**: 前端资源加载失败
**解决方案**:
1. 确认 `frontend/` 目录结构正确
2. 检查Flask静态文件配置
3. 验证文件路径是否正确

## 🔄 更新部署

当你修改代码后：

1. **提交更改**：
   ```bash
   git add .
   git commit -m "描述你的更改"
   git push origin main
   ```

2. **自动重新部署**：
   Render会自动检测到代码更改并重新部署

## 📊 监控和维护

### 查看应用状态
- 在Render控制台查看服务状态
- 监控CPU和内存使用情况
- 查看请求日志和错误日志

### 性能优化
- 考虑升级到付费计划获得更好性能
- 优化代码以减少响应时间
- 添加缓存机制

## 💡 提示

1. **免费计划限制**：
   - 服务在无活动时会休眠
   - 每月有750小时的运行时间限制
   - 首次访问可能需要等待服务唤醒

2. **域名**：
   - 免费计划提供 `.onrender.com` 子域名
   - 付费计划可以使用自定义域名

3. **数据持久化**：
   - 免费计划的文件系统不持久化
   - 重要数据应存储在外部数据库

## 🎉 完成！

恭喜！你的法律法规检索应用现在已经成功部署到Render平台。你可以通过Render提供的域名访问你的应用，并与他人分享。