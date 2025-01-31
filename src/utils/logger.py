import logging
import os
from datetime import datetime

def setup_logging():
    """
    设置日志配置
    按天生成日志文件，存放在 data/logs 目录下
    """
    # 确保日志目录存在
    log_dir = os.path.join("data", "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # 生成当天的日志文件名
    current_date = datetime.now().strftime('%Y-%m-%d')
    log_filename = os.path.join(log_dir, f"scraping_{current_date}.log")
    
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            # 文件处理器 - 按天生成日志文件
            logging.FileHandler(log_filename, encoding='utf-8'),
            # 控制台处理器
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"日志文件创建成功：{log_filename}")
    
    return logger 