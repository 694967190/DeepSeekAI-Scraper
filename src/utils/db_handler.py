import logging
import pymysql
from datetime import datetime
from src.config.settings import config, FIELDS, FIELD_MAPPING

class DatabaseHandler:
    def __init__(self):
        """初始化数据库连接"""
        self.db_config = config.db
        self.conn = None
        self.cursor = None

    def connect(self):
        """建立数据库连接"""
        try:
            self.conn = pymysql.connect(
                host=self.db_config.host,
                port=self.db_config.port,
                user=self.db_config.user,
                password=self.db_config.password,
                database=self.db_config.database,
                charset=self.db_config.charset
            )
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            logging.error(f"数据库连接失败: {str(e)}")
            return False

    def _process_field_value(self, field_name, value):
        """
        处理字段值，确保其符合数据库字段类型要求
        :param field_name: 字段名（中文）
        :param value: 字段值
        :return: 处理后的值
        """
        db_field = FIELD_MAPPING.get(field_name)
        
        # 处理日期字段
        if db_field == 'establish_time':
            if value == "未知" or not value:
                return None
            try:
                # 尝试解析日期
                if isinstance(value, str):
                    # 尝试多种日期格式
                    date_formats = [
                        '%Y-%m-%d',
                        '%Y/%m/%d',
                        '%Y年%m月%d日',
                        '%Y.%m.%d',
                        '%Y'  # 如果只有年份
                    ]
                    for date_format in date_formats:
                        try:
                            return datetime.strptime(value.strip(), date_format).strftime('%Y-%m-%d')
                        except ValueError:
                            continue
                return None
            except Exception:
                return None
        
        # 处理数值字段（如员工人数）
        elif db_field == 'employee_count':
            if value == "未知" or not value:
                return None
            try:
                # 移除可能的文本描述，只保留数字
                value = ''.join(filter(str.isdigit, str(value)))
                return int(value) if value else None
            except ValueError:
                return None
        
        # 其他字段
        return value if value != "未知" else None

    def save_data(self, data, task_type=None):
        """
        保存数据到数据库
        :param data: 字典或字典列表
        :param task_type: 任务类型（'search' 或 'financial'）
        :return: 是否保存成功
        """
        if not self.connect():
            return False

        try:
            # 确保data是列表形式
            if isinstance(data, dict):
                data = [data]

            for item in data:
                # 确保所有字段都存在
                for field in FIELDS:
                    if field not in item or not item[field]:
                        item[field] = "未知"

                # 构建SQL语句
                db_fields = [FIELD_MAPPING[field] for field in FIELDS]
                placeholders = ', '.join(['%s'] * len(db_fields))
                
                insert_sql = f"""
                INSERT INTO {self.db_config.table} 
                ({', '.join(db_fields)}) 
                VALUES ({placeholders})
                """

                # 处理并准备数据
                values = [self._process_field_value(field, item.get(field, "未知")) for field in FIELDS]

                # 执行SQL
                self.cursor.execute(insert_sql, values)

            # 提交事务
            self.conn.commit()
            logging.info(f"成功保存 {len(data)} 条数据到数据库")
            return True

        except Exception as e:
            logging.error(f"保存数据到数据库失败: {str(e)}")
            self.conn.rollback()
            return False

        finally:
            self.close()

    def update_financial_data(self, company_name, financial_data):
        """
        更新公司财务数据
        :param company_name: 公司名称
        :param financial_data: 财务数据
        :return: 是否更新成功
        """
        if not self.connect():
            return False

        try:
            update_sql = f"""
            UPDATE {self.db_config.table}
            SET revenue_3years = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE company_name = %s
            """
            
            self.cursor.execute(update_sql, (financial_data, company_name))
            self.conn.commit()
            
            affected_rows = self.cursor.rowcount
            if affected_rows > 0:
                logging.info(f"成功更新公司 {company_name} 的财务数据")
                return True
            else:
                logging.warning(f"未找到公司 {company_name} 的记录")
                return False

        except Exception as e:
            logging.error(f"更新财务数据失败: {str(e)}")
            self.conn.rollback()
            return False

        finally:
            self.close()

    def get_all_companies(self):
        """
        获取所有公司数据
        :return: 公司数据列表
        """
        if not self.connect():
            return []

        try:
            self.cursor.execute(f"SELECT * FROM {self.db_config.table}")
            columns = [col[0] for col in self.cursor.description]
            results = []
            
            # 反向映射字段名
            reverse_mapping = {v: k for k, v in FIELD_MAPPING.items()}
            
            for row in self.cursor.fetchall():
                row_dict = dict(zip(columns, row))
                # 转换字段名为中文
                converted_dict = {}
                for key, value in row_dict.items():
                    if key in reverse_mapping:
                        converted_dict[reverse_mapping[key]] = value
                    else:
                        converted_dict[key] = value
                results.append(converted_dict)
            
            return results

        except Exception as e:
            logging.error(f"获取公司数据失败: {str(e)}")
            return []

        finally:
            self.close()

    def close(self):
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close() 