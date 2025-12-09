# 🚀 立即部署到Render - 完整步骤

## 第一步：推送代码到GitHub

### 1.1 初始化Git（如果还没有）
```bash
git init
git add .
git commit -m "Ready for Render deployment"
```

### 1.2 创建GitHub仓库
1. 访问 https://github.com/new
2. 输入仓库名称（例如：`legal-research-app`）
3. 选择 Public 或 Private
4. **不要**勾选 "Initialize with README"
5. 点击 "Create repository"

### 1.3 推送代码
```bash
# 替换为你的GitHub用户名和仓库名
git remote add origin https://github.com/你的用户名/legal-research-app.git
git branch -M main
git push -u origin main
```

---

## 第二步：在Render创建Web Service

### 2.1 登录Render
1. 访问 https://render.com
2. 注册或登录账号（可以使用GitHub账号登录）

### 2.2 创建新服务
1. 点击右上角的 **"New +"** 按钮
2. 选择 **"Web Service"**

### 2.3 连接GitHub仓库
1. 如果是第一次使用，点击 **"Connect GitHub"**
2. 授权Render访问你的GitHub账号
3. 在仓库列表中找到 `legal-research-app`
4. 点击 **"Connect"**

### 2.4 配置服务设置

填写以下信息：

| 配置项 | 值 |
|--------|-----|
| **Name** | `legal-research-app` |
| **Region** | 选择离你最近的区域（如 Singapore） |
| **Branch** | `main` |
| **Root Directory** | 留空 |
| **Environment** | `Python` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn --bind 0.0.0.0:$PORT backend.app:app` |

### 2.5 选择计划
- 选择 **"Free"** 计划（免费）
- 注意：免费计划在无活动时会休眠

---

## 第三步：设置环境变量

### 3.1 添加环境变量
在 **"Environment"** 标签页：

1. 点击 **"Add Environment Variable"**
2. 添加以下变量：

| Key | Value |
|-----|-------|
| `DEEPSEEK_API_KEY` | 你的Deepseek API密钥 |

**重要**：确保API密钥正确，否则AI功能无法工作

---

## 第四步：部署

### 4.1 开始部署
1. 点击页面底部的 **"Create Web Service"** 按钮
2. Render会自动开始构建和部署

### 4.2 监控构建过程
- 在 **"Logs"** 标签页可以看到实时构建日志
- 构建通常需要 2-5 分钟
- 等待看到 "Your service is live" 消息

### 4.3 获取应用URL
- 构建成功后，Render会提供一个URL
- 格式：`https://legal-research-app-xxxx.onrender.com`
- 点击URL访问你的应用

---

## 第五步：验证部署

### 5.1 测试应用功能
1. 访问应用URL
2. 选择一个司法辖区（如"英国"）
3. 勾选一个或多个问题
4. 点击"生成报告"
5. 验证AI是否正常返回结果

### 5.2 检查常见问题
- ✅ 页面能正常加载
- ✅ 司法辖区下拉菜单有选项
- ✅ 问题列表显示正常
- ✅ 生成报告功能正常工作

---

## 🎉 部署完成！

你的应用现在已经在线运行了！

### 📱 分享你的应用
将Render提供的URL分享给其他人即可访问

### 🔄 更新应用
当你修改代码后：
```bash
git add .
git commit -m "描述你的更改"
git push origin main
```
Render会自动检测更改并重新部署

---

## ⚠️ 免费计划注意事项

1. **休眠机制**：15分钟无活动后服务会休眠
2. **唤醒时间**：首次访问可能需要30-60秒唤醒
3. **运行时间**：每月750小时免费运行时间
4. **性能**：免费计划性能有限，适合测试和小规模使用

---

## 🆘 遇到问题？

### 构建失败
- 查看 `RENDER_TROUBLESHOOTING.md`
- 检查构建日志中的具体错误

### 应用无法访问
- 确认服务状态为 "Live"
- 检查环境变量是否正确设置

### AI功能不工作
- 确认 `DEEPSEEK_API_KEY` 已正确设置
- 检查API密钥是否有效
- 查看应用日志中的错误信息

---

## 📞 需要帮助？

查看详细文档：
- `RENDER_DEPLOY_GUIDE.md` - 详细部署指南
- `RENDER_TROUBLESHOOTING.md` - 故障排除指南