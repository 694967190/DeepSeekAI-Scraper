import os
import pandas as pd
import logging
from datetime import datetime
from src.config.settings import FIELDS

def get_output_filepath(task_type=None, filename=None):
    """
    获取输出文件路径
    :param task_type: 任务类型（'search' 或 'financial'）
    :param filename: 可选的指定文件名，如果指定则直接使用
    """
    # 确保输出目录存在
    output_dir = os.path.join("data", "output")
    os.makedirs(output_dir, exist_ok=True)
    
    if filename is None:
        # 生成当前时间戳（精确到秒，避免同一天多次运行覆盖）
        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 根据任务类型生成文件名
        if task_type == 'search':
            filename = f"company_search_{current_time}.xlsx"
        elif task_type == 'financial':
            filename = f"financial_update_{current_time}.xlsx"
        else:
            filename = f"company_data_{current_time}.xlsx"
    
    # 返回完整的文件路径
    return os.path.join(output_dir, filename)

def save_to_excel(data, task_type=None, filename=None, is_append=False):
    """
    保存数据到Excel文件
    :param data: 要保存的数据（字典或字典列表）
    :param task_type: 任务类型（'search' 或 'financial'）
    :param filename: 可选的指定文件名
    :param is_append: 是否追加到现有文件
    """
    try:
        # 获取完整的文件路径
        filepath = get_output_filepath(task_type, filename)
        
        # 创建新的 DataFrame
        new_df = pd.DataFrame([data] if isinstance(data, dict) else data)
        
        # 确保所有字段都存在
        for field in FIELDS:
            if field not in new_df.columns:
                new_df[field] = "未知"
        
        # 重排列顺序
        new_df = new_df[FIELDS]
        
        if is_append and os.path.exists(filepath):
            # 如果文件存在且需要追加，则读取现有文件并追加
            existing_df = pd.read_excel(filepath)
            updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        else:
            updated_df = new_df
        
        # 保存到 Excel
        updated_df.to_excel(filepath, index=False)
        logging.info(f"数据已保存到 {filepath}")
        
        return filepath
        
    except Exception as e:
        logging.error(f"保存Excel时发生错误: {str(e)}")
        return None 