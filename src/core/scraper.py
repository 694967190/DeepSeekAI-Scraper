import json
import logging
from datetime import datetime
from googlesearch import search
from scrapegraphai.graphs import SmartScraperGraph
from src.config.settings import FIELDS, config
from src.utils.storage_factory import StorageFactory

def search_and_scrape(keyword, num_results=None):
    """
    搜索和爬取公司信息
    """
    results = []
    storage_result = None
    
    logging.info(f"开始搜索关键词: {keyword}")
    try:
        search_results = list(search(
            keyword, 
            num=100,  # 每页结果数
            stop=None if num_results is None else num_results,
            pause=2
        ))
        logging.info(f"搜索到 {len(search_results)} 个结果")
    except Exception as e:
        logging.error(f"搜索过程发生错误: {str(e)}")
        return results, None
    
    for index, url in enumerate(search_results, 1):
        logging.info(f"正在处理第 {index}/{len(search_results)} 个网址: {url}")
        try:
            # 创建爬虫实例，优化提示词
            prompt = f"""
            请仔细分析网页内容，提取以下信息，以JSON格式返回。对于每个字段：

            1. 公司基本信息：
            - 公司名称：寻找完整的法定名称
            - 公司网址：查找官方网站URL
            - 公司简介：提取简短的业务描述（100-200字）
            - 公司类型：如私营、国企、上市公司等
            - 成立时间：优先查找精确日期（YYYY-MM-DD格式）
            - 员工人数：寻找最新数据

            2. 联系方式：
            - 公司邮箱：查找官方联系邮箱
            - 公司电话：包含国际区号的完整号码
            - 公司地址：完整的实际办公地址
            - 谷歌地图链接：如果有的话

            3. 主要联系人信息：
            - 姓名：优先找管理层或部门负责人
            - 职位：准确的职务头衔
            - 邮箱：个人工作邮箱
            - 电话：直线或手机号码
            - 社交媒体：LinkedIn/Twitter/Facebook链接

            4. 其他信息：
            - 国家/地区：公司总部所在地
            - 近3年营业额：按年份列出（如有）
            - 备注：任何其他重要信息

            请注意：
            1. 如果某项信息未找到，填写"未知"
            2. 确保数据的准确性和完整性
            3. 优先提取官方信息源的数据
            4. 注意区分总部和分支机构信息
            5. 金额单位统一使用人民币（元）

            请以标准JSON格式返回，包含以下字段：
            {', '.join(FIELDS)}
            
            不要包含任何其他内容，只返回JSON数据。
            """
            
            scraper = SmartScraperGraph(
                prompt=prompt,
                source=url,
                config=config.GRAPH_CONFIG
            )
            
            # 运行爬虫
            logging.info(f"开始爬取网址: {url}")
            logging.info(f"发送给 GPT 的提示词: {prompt}")
            result = scraper.run()
            logging.info(f"GPT 返回结果: {json.dumps(result, ensure_ascii=False)}")
            
            # 数据验证和清理
            if isinstance(result, dict):
                # 确保所有字段都存在
                for field in FIELDS:
                    if field not in result or not result[field]:
                        result[field] = "未知"
                
                # 添加数据来源和获取时间
                result['数据来源'] = url
                result['数据获取时间'] = datetime.now().strftime('%Y-%m-%d')
                
                results.append(result)
                
                # 每爬取一个网站就保存一次
                logging.info(f"成功爬取网址: {url}")
                storage_result = StorageFactory.save_data(result, task_type='search', is_append=True)
            else:
                logging.error(f"URL {url} 返回的数据格式不正确")
            
        except Exception as e:
            logging.error(f"爬取 {url} 时发生错误: {str(e)}")
            continue
    
    return results, storage_result 