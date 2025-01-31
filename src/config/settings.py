"""
配置模块
包含所有应用程序配置项
"""

import os
from typing import Dict, List
from dotenv import load_dotenv
from dataclasses import dataclass

# 加载环境变量
load_dotenv()

@dataclass
class APIConfig:
    """API配置类"""
    base_url: str = os.getenv('OPENAI_API_BASE', "http://localhost:1234/v1")
    api_key: str = os.getenv('API_KEY', "not-needed")
    model: str = "openai/gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 2000
    top_p: float = 0.9
    request_timeout: int = 300

@dataclass
class DatabaseConfig:
    """数据库配置类"""
    host: str = os.getenv('MYSQL_HOST', 'localhost')
    port: int = int(os.getenv('MYSQL_PORT', 3306))
    user: str = os.getenv('MYSQL_USER', 'root')
    password: str = os.getenv('MYSQL_PASSWORD', 'root')
    database: str = os.getenv('MYSQL_DATABASE', 'web-deepseekai')
    table: str = os.getenv('MYSQL_TABLE', 'company_info')
    charset: str = 'utf8mb4'

class StorageMode:
    """存储模式枚举"""
    EXCEL = 'excel'
    MYSQL = 'mysql'

    @staticmethod
    def is_valid(mode: str) -> bool:
        """验证存储模式是否有效"""
        return mode.lower() in [StorageMode.EXCEL, StorageMode.MYSQL]

# 字段映射关系
FIELD_MAPPING: Dict[str, str] = {
    "公司名称": "company_name",
    "公司网址": "company_website",
    "公司简介": "company_desc",
    "公司邮箱": "company_email",
    "公司电话": "company_phone",
    "公司地址": "company_address",
    "国家/地区": "country_region",
    "成立时间": "establish_time",
    "员工人数": "employee_count",
    "公司类型": "company_type",
    "近3年营业额": "revenue_3years",
    "谷歌地图链接": "google_maps_link",
    "主要联系人姓名": "contact_name",
    "主要联系人职位": "contact_position",
    "主要联系人邮箱": "contact_email",
    "主要联系人电话": "contact_phone",
    "主要联系人LinkedIn": "contact_linkedin",
    "主要联系人Twitter": "contact_twitter",
    "主要联系人Facebook": "contact_facebook",
    "数据来源": "data_source",
    "数据获取时间": "data_time",
    "备注": "remarks"
}

# 要提取的字段列表
FIELDS: List[str] = list(FIELD_MAPPING.keys())

@dataclass
class Config:
    """全局配置类"""
    def __init__(self):
        self.api = APIConfig()
        self.db = DatabaseConfig()
        self.storage_mode = os.getenv('STORAGE_MODE', StorageMode.EXCEL).lower()
        
        # 验证存储模式
        if not StorageMode.is_valid(self.storage_mode):
            raise ValueError(f"无效的存储模式: {self.storage_mode}")
        
        # 爬虫配置
        self.GRAPH_CONFIG = {
            "llm": {
                "api_key": self.api.api_key,
                "model": self.api.model,
                "temperature": self.api.temperature,
                "max_tokens": self.api.max_tokens,
                "top_p": self.api.top_p,
                "request_timeout": self.api.request_timeout,
            },
            "verbose": True,
            "headless": True,
        }
        
        # 设置OpenAI API基础URL
        os.environ['OPENAI_API_BASE'] = self.api.base_url

    @property
    def is_mysql_mode(self) -> bool:
        """是否为MySQL存储模式"""
        return self.storage_mode == StorageMode.MYSQL

    @property
    def is_excel_mode(self) -> bool:
        """是否为Excel存储模式"""
        return self.storage_mode == StorageMode.EXCEL

# 创建全局配置实例
config = Config()

# 导出配置
__all__ = ['config', 'FIELDS', 'FIELD_MAPPING', 'StorageMode'] 