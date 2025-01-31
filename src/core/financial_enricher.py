import logging
import pandas as pd
from googlesearch import search
from scrapegraphai.graphs import SmartScraperGraph
from src.config.settings import config, StorageMode
from src.utils.storage_factory import StorageFactory
from src.utils.db_handler import DatabaseHandler

def enrich_financial_data(filename=None):
    """
    补充公司财务数据
    :param filename: 可选的输入文件名，如果不指定则使用最新的搜索结果文件
    :return: 存储结果
    """
    logging.info("开始补充财务数据模式")
    try:
        # 根据存储模式获取数据
        if config.storage_mode == StorageMode.MYSQL.lower():
            db = DatabaseHandler()
            data = db.get_all_companies()
            if not data:
                logging.error("从数据库获取数据失败")
                return None
        else:
            # Excel模式
            if filename is None:
                logging.error("Excel模式下必须指定输入文件名")
                return None
            data = pd.read_excel(filename).to_dict('records')
            
        logging.info(f"成功读取数据，共有 {len(data)} 条记录")
        
        # 用于存储更新的财务数据
        updated_data = {}
        
        for index, row in enumerate(data):
            company_name = row['公司名称']
            if company_name == "未知" or pd.isna(company_name):
                logging.warning(f"第 {index + 1} 行公司名称为空或未知，跳过")
                continue
                
            current_revenue = row['近3年营业额']
            if current_revenue != "未知" and not pd.isna(current_revenue):
                logging.info(f"公司 {company_name} 已有财务数据，跳过")
                continue
                
            logging.info(f"开始处理第 {index + 1} 行：{company_name}")
            
            # 构建搜索关键词
            search_query = f'"{company_name}" AND ("revenue" OR "sales" OR "turnover" OR "financial results") AND ("annual report" OR "financial report" OR "investor relations") -job -career -forum -blog'
            
            try:
                # 搜索相关财务信息
                search_results = list(search(search_query, num=3, stop=3, pause=2))
                logging.info(f"找到 {len(search_results)} 个相关结果")
                
                for url in search_results:
                    try:
                        # 创建爬虫实例
                        prompt = """
                        请提取近三年的营业额信息，格式为：
                        "2021: XXX; 2022: XXX; 2023: XXX"
                        如果找不到完整的三年数据，返回能找到的年份数据。
                        如果金额单位不统一，请统一转换为人民币（元）。
                        请确保返回格式正确的字符串，不要包含其他内容。
                        当前时间为2025年。
                        """
                        
                        scraper = SmartScraperGraph(
                            prompt=prompt,
                            source=url,
                            config=config.GRAPH_CONFIG
                        )
                        
                        logging.info(f"正在从 {url} 提取财务数据")
                        result = scraper.run()
                        
                        if result and isinstance(result, str) and ":" in result:
                            # 更新数据
                            updated_data[company_name] = result
                            row['近3年营业额'] = result
                            logging.info(f"成功更新 {company_name} 的财务数据：{result}")
                            break  # 找到数据后就停止搜索
                            
                    except Exception as e:
                        logging.error(f"处理URL {url} 时发生错误: {str(e)}")
                        continue
                        
            except Exception as e:
                logging.error(f"搜索公司 {company_name} 财务信息时发生错误: {str(e)}")
                continue
        
        # 保存更新后的数据
        if updated_data:
            storage_result = StorageFactory.update_financial_data(updated_data, filename)
            if storage_result:
                logging.info("财务数据更新完成")
            else:
                logging.error("保存更新后的数据失败")
            return storage_result
        else:
            logging.info("没有需要更新的财务数据")
            return None
        
    except Exception as e:
        logging.error(f"处理数据时发生错误: {str(e)}")
        return None 