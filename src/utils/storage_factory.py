from src.config.settings import config, StorageMode
from src.utils.excel_handler import save_to_excel
from src.utils.db_handler import DatabaseHandler

class StorageFactory:
    @staticmethod
    def save_data(data, task_type=None, filename=None, is_append=False):
        """
        根据配置选择存储方式保存数据
        :param data: 要保存的数据
        :param task_type: 任务类型
        :param filename: 文件名（仅Excel模式使用）
        :param is_append: 是否追加（仅Excel模式使用）
        :return: 存储结果（Excel模式返回文件路径，MySQL模式返回是否成功）
        """
        if config.is_mysql_mode:
            db = DatabaseHandler()
            return db.save_data(data, task_type)
        else:  # Excel模式
            return save_to_excel(data, task_type, filename, is_append)

    @staticmethod
    def update_financial_data(data, filename=None):
        """
        更新财务数据
        :param data: 要更新的数据
        :param filename: 文件名（仅Excel模式使用）
        :return: 更新结果
        """
        if config.is_mysql_mode:
            db = DatabaseHandler()
            success = True
            for company_name, financial_data in data.items():
                if not db.update_financial_data(company_name, financial_data):
                    success = False
            return success
        else:  # Excel模式
            return save_to_excel(data, task_type='financial', filename=filename) 