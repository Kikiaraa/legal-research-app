# Fly.io 部署指南

## 为什么选择 Fly.io？

相比 Render，Fly.io 提供：
- ✅ **更多内存**：1GB vs 512MB
- ✅ **更好的性能**：更快的CPU和网络
- ✅ **更灵活的配置**：可以自定义资源
- ✅ **更稳定**：没有严格的Worker超时限制

## 前置要求

1. **安装 flyctl**
   ```bash
   # macOS
   brew install flyctl
   
   # Linux
   curl -L https://fly.io/install.sh | sh
   
   # Windows
   # 访问 https://fly.io/docs/hands-on/install-flyctl/
   ```

2. **注册并登录 Fly.io**
   ```bash
   flyctl auth signup  # 注册新账号
   # 或
   flyctl auth login   # 登录已有账号
   ```

## 快速部署

### 方法1：使用部署脚本（推荐）

```bash
./deploy-flyio.sh
```

脚本会自动：
1. 检查 flyctl 是否安装
2. 检查是否已登录
3. 创建应用（首次）或更新应用
4. 设置环境变量
5. 部署应用

### 方法2：手动部署

#### 步骤1：创建应用

```bash
flyctl launch
```

按提示操作：
- 应用名称：legal-research-app（或自定义）
- 区域：选择离你最近的（如 sjc 旧金山、hkg 香港）
- 是否设置数据库：No
- 是否立即部署：No（先设置环境变量）

#### 步骤2：设置环境变量

```bash
flyctl secrets set DEEPSEEK_API_KEY="your_api_key_here"
```

#### 步骤3：部署

```bash
flyctl deploy
```

## 部署后操作

### 查看应用状态
```bash
flyctl status
```

### 查看实时日志
```bash
flyctl logs
```

### 打开应用
```bash
flyctl open
```

### 查看应用信息
```bash
flyctl info
```

## 配置说明

### fly.toml 配置

```toml
[vm]
  memory_mb = 1024  # 1GB内存
  cpus = 1          # 1个CPU核心
```

如果需要更多资源，可以调整：
```bash
flyctl scale memory 2048  # 增加到2GB
flyctl scale count 2      # 增加到2个实例
```

### 环境变量管理

查看所有secrets：
```bash
flyctl secrets list
```

更新secret：
```bash
flyctl secrets set KEY=VALUE
```

删除secret：
```bash
flyctl secrets unset KEY
```

## 常见问题

### 1. 部署失败

查看详细日志：
```bash
flyctl logs --app legal-research-app
```

### 2. 应用无法访问

检查健康检查：
```bash
flyctl checks list
```

### 3. 内存不足

增加内存：
```bash
flyctl scale memory 2048
```

### 4. 更新代码

```bash
git add .
git commit -m "更新"
flyctl deploy
```

## 成本

Fly.io 免费套餐包括：
- 3个共享CPU虚拟机
- 3GB持久化存储
- 160GB出站流量/月

我们的应用配置（1个VM，1GB内存）完全在免费额度内！

## 监控和调试

### 查看资源使用
```bash
flyctl vm status
```

### SSH到容器
```bash
flyctl ssh console
```

### 查看应用指标
```bash
flyctl dashboard
```

## 回滚

如果新版本有问题，可以回滚：
```bash
flyctl releases list
flyctl releases rollback <version>
```

## 删除应用

如果需要删除应用：
```bash
flyctl apps destroy legal-research-app
```

## 支持

- 文档：https://fly.io/docs/
- 社区：https://community.fly.io/
- 状态：https://status.flyio.net/
