import os
from dotenv import load_dotenv
import json
import pandas as pd
from googlesearch import search
from datetime import datetime
import logging
from src.utils.logger import setup_logging
from src.core.scraper import search_and_scrape
from src.core.financial_enricher import enrich_financial_data
from src.config.settings import config
from src.utils.excel_handler import save_to_excel

# 环境配置
load_dotenv()  # 加载环境变量

# 设置 OpenAI API 基础 URL
os.environ['OPENAI_API_BASE'] = "http://localhost:1234/v1"

def main():
    # 设置日志
    logger = setup_logging()
    
    logger.info("程序启动")
    logger.info(f"当前存储模式: {config.storage_mode}")
    
    # 选择模式
    mode = input("请选择模式（1: 新数据搜索, 2: 财务数据补充）：")
    
    if mode == "1":
        keyword = input("请输入搜索关键词：")
        num_results_input = input("请输入需要搜索的结果数量（直接回车表示不限制）：")
        num_results = int(num_results_input) if num_results_input else None
        
        logger.info(f"开始搜索和爬取数据... 关键词: {keyword}, 数量: {'不限' if num_results is None else num_results}")
        results, storage_result = search_and_scrape(keyword, num_results)
        
        # 显示爬取完成信息
        logger.info(f"爬取完成，共获取 {len(results)} 条数据")
        if storage_result:
            if config.is_mysql_mode:
                logger.info("数据已成功保存到数据库")
            else:
                logger.info(f"数据已保存到：{storage_result}")
    
    elif mode == "2":
        if config.is_mysql_mode:
            storage_result = enrich_financial_data()
        else:
            filename = input("请输入要处理的Excel文件名：")
            if not filename:
                logger.error("Excel模式下必须指定输入文件名")
                return
            storage_result = enrich_financial_data(filename)
        
        if storage_result:
            if config.is_mysql_mode:
                logger.info("财务数据已成功更新到数据库")
            else:
                logger.info(f"财务数据更新完成，结果已保存到：{storage_result}")
        else:
            logger.error("财务数据更新失败")
    
    else:
        logger.error("无效的模式选择")
    
    logger.info("程序结束")

if __name__ == "__main__":
    main()
