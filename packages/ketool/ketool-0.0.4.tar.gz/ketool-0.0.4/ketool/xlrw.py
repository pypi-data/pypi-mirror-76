#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  :LiuKe
# @Version : V

import xlrd
import xlwt
from xlutils.copy import copy
import openpyxl


class EditExcel():
    """EditExcel Class"""
    # 构造函数

    def __init__(self, filename=None, sheet_id=0):
        self.filename = filename
        self.sheet_id = sheet_id
        #self.data = self.get_data()

    # 获取sheet内容
    def get_data(self):
        data = xlrd.open_workbook(self.filename)
        table = data.sheets()[self.sheet_id]
        return table

    # 获取行
    def get_lines(self):
        table = self.get_data()
        return table.nrows

    # 获取列
    def get_cols(self):
        table = self.get_data()
        return table.ncols

    # 获取单元格内容
    def get_cells(self, row, col):
        return self.get_data().cell_value(row, col)
    # 获取行数据

    def get_row_value(self, row):
        tables = self.get_data()
        row_data = tables.row_values(row)
        return row_data
    # 获取列数据

    def get_col_value(self, col):
        tables = self.get_data()
        col_data = tables.col_values(col)
        return col_data

    # 更新excel数据
    def update_data(self, row, col, value):
        if self.filename.endswith('.xls'):
            self.wt_update(row, col, value)
        elif self.filename.endswith('.xlsx'):
            self.pyxl_update(row, col, value)
        else:
            print('excel file error')

    # xls格式表数据更新
    def wt_update(self, row, col, value):
        read_data = xlrd.open_workbook(self.filename)
        write_data = copy(read_data)
        sheet_data = write_data.get_sheet(0)
        sheet_data.write(row, col, value)
        write_data.save(self.filename)

    # xlsx格式表数据更新
    def pyxl_update(self, row, col, value):
        '''openpyxl 处理数据下标从1开始，已经做了+1处理'''
        wb = openpyxl.load_workbook(self.filename)  # 生成一个已存在的wookbook对象
        wb1 = wb.active  # 激活sheet
        wb1.cell(row + 1, col + 1, value)  # 写入数据
        wb.save(self.filename)  # 保存

    # 写入excel数据
    # kv=[[row,col,value]]
    def write_xl(self, kv):
        if self.filename.endswith('.xls'):
            self.wt_write(kv)
        elif self.filename.endswith('.xlsx'):
            self.pyxl_write(kv)
        else:
            print('excel file error')
    # 写入xls格式excel数据

    def wt_write(self, kv):
        workbook = xlwt.Workbook()  # 创建一个新的工作簿
        sheet = workbook.add_sheet('sheet1')
        for i in kv:
            row, col, value = i
            sheet.write(row, col, value)
        workbook.save(self.filename)

    # 写入xlsx格式excel数据
    def pyxl_write(self, kv):
        # 创建workbook对象，写入模式
        wb = openpyxl.Workbook()
        ws = wb.create_sheet(index=0)
        for i in kv:
            row, col, value = i
            ws.cell(row=row + 1, column=col + 1, value=value)
        wb.save(self.filename)


if __name__ == '__main__':
    edit = EditExcel('data.xlsx')
    print(edit.get_col_value(1))
    # edit.write_excel2(3, 3, 'value')
