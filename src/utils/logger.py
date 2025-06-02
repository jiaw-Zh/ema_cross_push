# src/utils/logger.py
import logging
import os
from config.settings import LOG_FILE, LOG_LEVEL

def setup_logger():
    """配置全局日志记录器"""
    log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    
    # 创建文件处理器
    # os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    file_handler = logging.FileHandler(LOG_FILE,encoding='utf-8')
    file_handler.setLevel(log_level)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 添加处理器到记录器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# 创建全局记录器实例
logger = setup_logger()