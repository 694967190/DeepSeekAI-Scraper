# DeepSeekAI-Scraper

一个基于 Python 和 AI 的智能企业信息爬虫系统，能够自动搜索和提取企业相关信息，支持 Excel 和 MySQL 两种数据存储方式。

[English](README_EN.md) | 简体中文

## 功能特点

- 支持通过关键词搜索企业信息
- 自动提取企业基本信息、联系方式、财务数据等
- 支持 Excel 和 MySQL 两种数据存储模式
- 支持财务数据的单独更新和补充
- 完善的日志记录系统
- 模块化设计，易于维护和扩展

## 系统要求

- Python 3.8+
- MySQL 5.7+ (如果使用 MySQL 存储模式)

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置说明

1. 复制 `.env.example` 为 `.env`，并根据需要修改配置：

```env
# API配置
OPENAI_API_BASE=http://localhost:1234/v1
API_KEY=not-needed

# 存储模式配置 (excel 或 mysql)
STORAGE_MODE=excel

# MySQL数据库配置（当 STORAGE_MODE=mysql 时需要）
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DATABASE=web-deepseekai
MYSQL_TABLE=company_info
```

2. MySQL 表结构（当使用 MySQL 模式时）：

```sql
CREATE TABLE company_info (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    company_name VARCHAR(255) COMMENT '公司名称',
    company_website VARCHAR(255) COMMENT '公司网址',
    company_desc TEXT COMMENT '公司简介',
    company_email VARCHAR(100) COMMENT '公司邮箱',
    company_phone VARCHAR(50) COMMENT '公司电话',
    company_address TEXT COMMENT '公司地址',
    country_region VARCHAR(100) COMMENT '国家/地区',
    establish_time DATE COMMENT '成立时间',
    employee_count VARCHAR(50) COMMENT '员工人数',
    company_type VARCHAR(50) COMMENT '公司类型',
    revenue_3years TEXT COMMENT '近3年营业额',
    google_maps_link TEXT COMMENT '谷歌地图链接',
    contact_name VARCHAR(100) COMMENT '主要联系人姓名',
    contact_position VARCHAR(100) COMMENT '主要联系人职位',
    contact_email VARCHAR(100) COMMENT '主要联系人邮箱',
    contact_phone VARCHAR(50) COMMENT '主要联系人电话',
    contact_linkedin VARCHAR(255) COMMENT '主要联系人LinkedIn',
    contact_twitter VARCHAR(255) COMMENT '主要联系人Twitter',
    contact_facebook VARCHAR(255) COMMENT '主要联系人Facebook',
    data_source TEXT COMMENT '数据来源',
    data_time DATE COMMENT '数据获取时间',
    remarks TEXT COMMENT '备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='企业信息表';
```

## 项目结构

```
├── data/                      # 数据目录
│   ├── logs/                 # 日志文件
│   └── output/               # Excel输出文件
├── src/                      # 源代码
│   ├── config/              # 配置模块
│   │   └── settings.py     # 配置文件
│   ├── core/               # 核心功能模块
│   │   ├── scraper.py     # 爬虫核心
│   │   └── financial_enricher.py  # 财务数据补充
│   └── utils/              # 工具模块
│       ├── db_handler.py   # 数据库处理
│       ├── excel_handler.py # Excel处理
│       ├── logger.py       # 日志工具
│       └── storage_factory.py # 存储工厂
├── .env                      # 环境配置文件
├── main.py                   # 主程序入口
└── README.md                 # 项目说明文档
```

## 使用说明

1. 运行程序：
```bash
python main.py
```

2. 选择操作模式：
   - 模式1：新数据搜索
   - 模式2：财务数据补充

3. 根据提示输入相关参数

### 模式1：新数据搜索

- 输入搜索关键词
- 输入需要搜索的结果数量（可选）
- 系统会自动搜索并提取企业信息

### 模式2：财务数据补充

- Excel模式：需要指定要处理的Excel文件名
- MySQL模式：自动处理数据库中的所有记录

## 数据存储

### Excel模式
- 数据保存在 `data/output` 目录下
- 文件名格式：
  - 搜索结果：`company_search_YYYYMMDD_HHMMSS.xlsx`
  - 财务更新：`financial_update_YYYYMMDD_HHMMSS.xlsx`

### MySQL模式
- 数据直接保存到配置的数据库表中
- 自动处理数据更新和插入

## 日志系统

- 日志文件位置：`data/logs/scraping_YYYY-MM-DD.log`
- 记录详细的运行信息和错误信息
- 同时在控制台显示关键信息

## 注意事项

1. 使用 MySQL 模式时，确保：
   - MySQL 服务已启动
   - 数据库和表已创建
   - 配置的数据库用户有足够权限

2. 使用 Excel 模式时，确保：
   - `data/output` 目录存在且有写入权限
   - 更新财务数据时提供正确的源文件路径

## 开发说明

- 使用 Python 的 dataclass 进行配置管理
- 采用工厂模式处理不同的存储方式
- 模块化设计，便于扩展新功能
- 完整的类型注解和文档字符串

## 错误处理

- 所有操作都有完整的错误处理和日志记录
- 数据库操作支持事务回滚
- 文件操作有适当的异常处理

## 许可证

MIT License 