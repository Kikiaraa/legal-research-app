# Gunicorn配置文件
import os

# 绑定地址
bind = f"0.0.0.0:{os.environ.get('PORT', '10000')}"

# Worker配置
workers = 1  # 免费计划使用1个worker
worker_class = 'sync'
timeout = 300  # 增加超时时间到300秒（5分钟）
graceful_timeout = 30
keepalive = 5

# 日志配置
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# 进程命名
proc_name = 'legal-research-app'