"""
@Author  : Likianta <likianta@foxmail.com>
@Module  : _typings.py
@Created : 2020-08-06
@Updated : 2020-08-06
@Version : 0.0.1
@Desc    : 加速 IDE 类型推断.
"""
from typing import *

# ------------------------------------------------------------------------------
# excel_writer.py
from xlsxwriter.format import Format as ExlFormat

CellFormat = ExlFormat
Row = List[Union[str, int, float, bool, None]]
Rows = List[Row]
