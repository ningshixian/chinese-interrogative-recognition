#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/15 16:58
# @Author  : CoderCharm
# @File    : logger.py
# @Software: PyCharm
# @Github  : github/CoderCharm
# @Email   : wg_python@163.com
# @Desc    :
"""

日志文件配置 参考链接
https://github.com/Delgan/loguru

# 本来是想 像flask那样把日志对象挂载到app对象上，作者建议直接使用全局对象
https://github.com/tiangolo/fastapi/issues/81#issuecomment-473677039

考虑是否应该把logger 改成单例

"""
import os
import time
import json
from functools import wraps
from loguru import logger
import traceback

# from config import setting
# from utils import tools_func
from schemas.response import response_code

# 定位到log日志文件
log_path = os.path.join('./', 'logs')

if not os.path.exists(log_path):
    os.mkdir(log_path)

log_path_info = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_info.log')
log_path_warning = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_warning.log')
log_path_error = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_error.log')

# 日志简单配置 文件区分不同级别的日志
# rotation="200 MB"：每个 log 文件达到200M就会自动进行日志分隔
# rotation='00:00'：每天 0 点新创建一个 log 文件输出
logger.add(log_path_info, rotation="200 MB", encoding='utf-8', enqueue=True, level='INFO')
logger.add(log_path_warning, rotation="200 MB", encoding='utf-8', enqueue=True, level='WARNING')
logger.add(log_path_error, rotation="200 MB", encoding='utf-8', enqueue=True, level='ERROR')
# logger = ut.LogDecorator.init_logger(setting.log_file, SBERT_CONFIG["logLevel"])  # 日志级别（测试WARNING/生产DEBUG）


def log_filter(func):
    """装饰器来捕获代码异常&记录日志"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = 1000 * time.time()
        logger.info(f"Request: {kwargs['request'].url}")
        logger.info(f"入参: {kwargs['item']}")
        try:
            rsp = func(*args, **kwargs)
            logger.info(f"出参: {rsp.body.decode('utf-8')}") 
            end = 1000 * time.time()
            logger.info(f"Time consuming: {end - start}ms")
            return rsp
        except Exception as e:
            logger.error(traceback.format_exc())  # 错误日志 repr(e)
            logger.error(f"Request: {kwargs['request'].url}")
            logger.error(f"Args: {kwargs['item']}")
            return response_code.resp_500(message="服务异常")
        
    return wrapper


# 装饰器：计算函数运行时间
def elapsed_time(func):
    def wrapper(*args, **kwargs):
        start = 1000 * time.time()
        result = func(*args, **kwargs)
        end = 1000 * time.time()
        print('Time consuming:{} ms'.format(end-start))
        return result
    return wrapper


__all__ = ["logger", "log_filter", "elapsed_time"]
