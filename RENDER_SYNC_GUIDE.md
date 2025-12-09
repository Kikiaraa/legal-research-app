# 🔄 Render自动同步指南

## ✅ 代码已推送到GitHub

你的更新已经成功推送到：
- **仓库**: https://github.com/Kikiaraa/legal-research-app
- **分支**: main
- **提交**: 包含Render配置文件和新的知识库文档

---

## 🚀 Render会自动部署

### 如果你已经在Render创建了服务：

Render会**自动检测**GitHub的更新并重新部署！

1. **访问Render控制台**: https://dashboard.render.com
2. **找到你的服务**: `legal-research-app`
3. **查看部署状态**: 
   - 应该会看到 "Deploying..." 状态
   - 或者已经显示 "Live" 状态

### 如果还没有在Render创建服务：

按照以下步骤创建：

#### 1. 登录Render
访问 https://render.com 并登录

#### 2. 创建Web Service
1. 点击 **"New +"** → **"Web Service"**
2. 选择 **"Build and deploy from a Git repository"**
3. 点击 **"Connect"** 连接GitHub
4. 找到并选择 `legal-research-app` 仓库
5. 点击 **"Connect"**

#### 3. 配置服务

| 配置项 | 值 |
|--------|-----|
| **Name** | `legal-research-app` |
| **Region** | Singapore (或其他离你近的区域) |
| **Branch** | `main` |
| **Root Directory** | 留空 |
| **Environment** | `Python` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn --bind 0.0.0.0:$PORT backend.app:app` |
| **Instance Type** | Free |

#### 4. 设置环境变量

在 **Environment** 标签页添加：

```
DEEPSEEK_API_KEY = 你的Deepseek API密钥
```

**重要**: 没有这个环境变量，AI功能无法工作！

#### 5. 创建服务

点击 **"Create Web Service"** 按钮

---

## 📊 监控部署进度

### 查看构建日志
1. 在Render控制台点击你的服务
2. 切换到 **"Logs"** 标签页
3. 实时查看构建和部署日志

### 部署状态说明
- 🟡 **Building**: 正在构建（安装依赖）
- 🟡 **Deploying**: 正在部署
- 🟢 **Live**: 部署成功，服务运行中
- 🔴 **Failed**: 部署失败，需要检查日志

### 预计时间
- 首次部署: 3-5分钟
- 后续更新: 2-3分钟

---

## 🔄 以后如何更新

每次修改代码后，只需要：

```bash
# 1. 添加更改
git add .

# 2. 提交更改
git commit -m "描述你的更改"

# 3. 推送到GitHub
git push origin main
```

**Render会自动检测并重新部署！** 🎉

---

## 🎯 验证部署

### 1. 获取应用URL
在Render控制台顶部会显示你的应用URL：
```
https://legal-research-app-xxxx.onrender.com
```

### 2. 测试功能
1. 访问应用URL
2. 选择司法辖区
3. 勾选问题
4. 生成报告
5. 验证AI回答是否正常

### 3. 检查清单
- ✅ 页面正常加载
- ✅ 司法辖区下拉菜单有选项
- ✅ 问题列表显示
- ✅ 生成报告功能工作
- ✅ AI返回结果

---

## ⚠️ 常见问题

### 问题1: 部署失败
**解决方案**:
1. 查看构建日志中的错误信息
2. 检查 `requirements.txt` 格式
3. 确认 `runtime.txt` 中的Python版本
4. 参考 `RENDER_TROUBLESHOOTING.md`

### 问题2: AI功能不工作
**解决方案**:
1. 确认环境变量 `DEEPSEEK_API_KEY` 已设置
2. 检查API密钥是否有效
3. 查看应用日志中的错误

### 问题3: 服务休眠
**说明**: 免费计划在15分钟无活动后会休眠
**影响**: 首次访问需要30-60秒唤醒
**解决**: 升级到付费计划或接受休眠机制

---

## 📱 分享你的应用

部署成功后，你可以：
1. 复制Render提供的URL
2. 分享给其他人使用
3. 可以考虑绑定自定义域名（付费功能）

---

## 🎉 完成！

你的应用现在已经：
- ✅ 代码推送到GitHub
- ✅ 准备好在Render部署
- ✅ 配置文件齐全
- ✅ 自动部署已启用

访问 https://dashboard.render.com 查看你的服务状态！