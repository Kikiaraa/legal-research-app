"""Gunicorn配置文件 - 优化Render部署"""
import multiprocessing
import os

# 绑定地址
bind = f"0.0.0.0:{os.environ.get('PORT', '5001')}"

# Worker配置
workers = 1  # Render免费套餐内存有限，使用1个worker
worker_class = 'sync'  # 同步worker，更稳定
worker_connections = 1000
max_requests = 100  # 每100个请求后重启worker，防止内存泄漏
max_requests_jitter = 10

# 超时配置
timeout = 300  # 5分钟超时
graceful_timeout = 30  # 优雅关闭超时
keepalive = 5

# 日志配置
loglevel = 'info'
accesslog = '-'  # 输出到stdout
errorlog = '-'   # 输出到stderr
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# 进程命名
proc_name = 'legal-research-app'

# 预加载应用（可选，节省内存）
preload_app = False  # 设为False避免fork问题

# Worker临时目录
worker_tmp_dir = '/dev/shm'  # 使用内存文件系统，更快

# 限制请求体大小（防止过大请求）
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

def worker_int(worker):
    """Worker被中断时的处理"""
    worker.log.info("Worker received INT or QUIT signal")

def worker_abort(worker):
    """Worker异常终止时的处理"""
    worker.log.info("Worker received SIGABRT signal")
