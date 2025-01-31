# DeepSeekAI-Scraper

An intelligent enterprise information scraping system based on Python and AI, capable of automatically searching and extracting company information, supporting both Excel and MySQL storage modes.

English | [简体中文](README.md)

## Features

- Keyword-based company information search
- Automatic extraction of company basic info, contacts, and financial data
- Support for both Excel and MySQL storage modes
- Independent financial data updates and enrichment
- Comprehensive logging system
- Modular design for easy maintenance and extension

## Requirements

- Python 3.8+
- MySQL 5.7+ (if using MySQL storage mode)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

1. Copy `.env.example` to `.env` and modify as needed:

```env
# API Configuration
OPENAI_API_BASE=http://localhost:1234/v1
API_KEY=not-needed

# Storage Mode (excel or mysql)
STORAGE_MODE=excel

# MySQL Database Configuration (required when STORAGE_MODE=mysql)
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DATABASE=web-deepseekai
MYSQL_TABLE=company_info
```

2. MySQL Table Structure (when using MySQL mode):

```sql
CREATE TABLE company_info (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    company_name VARCHAR(255) COMMENT 'Company Name',
    company_website VARCHAR(255) COMMENT 'Company Website',
    company_desc TEXT COMMENT 'Company Description',
    company_email VARCHAR(100) COMMENT 'Company Email',
    company_phone VARCHAR(50) COMMENT 'Company Phone',
    company_address TEXT COMMENT 'Company Address',
    country_region VARCHAR(100) COMMENT 'Country/Region',
    establish_time DATE COMMENT 'Establishment Date',
    employee_count VARCHAR(50) COMMENT 'Employee Count',
    company_type VARCHAR(50) COMMENT 'Company Type',
    revenue_3years TEXT COMMENT 'Revenue for Last 3 Years',
    google_maps_link TEXT COMMENT 'Google Maps Link',
    contact_name VARCHAR(100) COMMENT 'Primary Contact Name',
    contact_position VARCHAR(100) COMMENT 'Contact Position',
    contact_email VARCHAR(100) COMMENT 'Contact Email',
    contact_phone VARCHAR(50) COMMENT 'Contact Phone',
    contact_linkedin VARCHAR(255) COMMENT 'Contact LinkedIn',
    contact_twitter VARCHAR(255) COMMENT 'Contact Twitter',
    contact_facebook VARCHAR(255) COMMENT 'Contact Facebook',
    data_source TEXT COMMENT 'Data Source',
    data_time DATE COMMENT 'Data Collection Time',
    remarks TEXT COMMENT 'Remarks',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Created Time',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Updated Time'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Company Information Table';
```

## Project Structure

```
├── data/                      # Data Directory
│   ├── logs/                 # Log Files
│   └── output/               # Excel Output Files
├── src/                      # Source Code
│   ├── config/              # Configuration Module
│   │   └── settings.py     # Settings File
│   ├── core/               # Core Functionality
│   │   ├── scraper.py     # Scraper Core
│   │   └── financial_enricher.py  # Financial Data Enrichment
│   └── utils/              # Utility Modules
│       ├── db_handler.py   # Database Handler
│       ├── excel_handler.py # Excel Handler
│       ├── logger.py       # Logger Utility
│       └── storage_factory.py # Storage Factory
├── .env                      # Environment Configuration
├── main.py                   # Main Program Entry
└── README.md                 # Documentation
```

## Usage

1. Run the program:
```bash
python main.py
```

2. Select operation mode:
   - Mode 1: New Data Search
   - Mode 2: Financial Data Enrichment

3. Follow the prompts to input parameters

### Mode 1: New Data Search

- Enter search keywords
- Enter desired number of results (optional)
- System will automatically search and extract company information

### Mode 2: Financial Data Enrichment

- Excel mode: Specify the Excel file to process
- MySQL mode: Automatically process all database records

## Data Storage

### Excel Mode
- Data saved in `data/output` directory
- File naming convention:
  - Search results: `company_search_YYYYMMDD_HHMMSS.xlsx`
  - Financial updates: `financial_update_YYYYMMDD_HHMMSS.xlsx`

### MySQL Mode
- Data saved directly to configured database table
- Automatic data updates and insertions

## Logging System

- Log file location: `data/logs/scraping_YYYY-MM-DD.log`
- Records detailed operation info and errors
- Displays key information in console

## Important Notes

1. For MySQL mode, ensure:
   - MySQL service is running
   - Database and table are created
   - Configured user has sufficient privileges

2. For Excel mode, ensure:
   - `data/output` directory exists with write permissions
   - Correct source file path for financial data updates

## Development Notes

- Uses Python dataclass for configuration management
- Factory pattern for different storage methods
- Modular design for easy feature extension
- Complete type hints and docstrings

## Error Handling

- Comprehensive error handling and logging
- Transaction rollback support for database operations
- Appropriate exception handling for file operations

## License

MIT License 