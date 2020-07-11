#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import xlrd
import xlsxwriter

from .logs_help import Logger

logger = Logger("debug",name=os.path.split(os.path.splitext(os.path.abspath(__file__))[0])[-1])

def excel2list(excle_name,**kwargs):
    """
    读取表格为列表
    :param excle_name: excel文件路径
    :param index: 按索引取sheet eg：0
    :param name: 按sheet名称取sheet eg：Sheet1
    :param row_or_col: 按行或列读取sheet，默认按行，eg：True
    """
    _list = []
    sheets = []
    try:
        workbook = xlrd.open_workbook(filename=excle_name)
    except Exception:
        logger.error(f"Faild open {excle_name}", exc_info=True)
        return _list
    if kwargs.get("name",False):
        try:
            sheets.append(workbook.sheet_by_name(kwargs["name"]))
        except Exception:
            logger.error(f'{excle_name} no have sheet name: {kwargs["name"]}', exc_info=True)
    elif kwargs.get("index",False):
        try:
            sheets.append(workbook.sheet_by_index(kwargs["index"]))
        except Exception:
            logger.error(f'{excle_name} no have index: {kwargs["index"]}', exc_info=True)
    else:
        sheets = workbook.sheets()
    
    for i in range(0,len(sheets)):
        _sheet_list = []
        if kwargs.get("row_or_col",True):
            for n in range(0,sheets[i].nrows):
                _sheet_list.append(sheets[i].row_values(n))
        else:
            for n in range(0,sheets[i].ncols):
                _sheet_list.append(sheets[i].col_values(n))
        _list.append(_sheet_list)
    return _list

def excel2json(excle_name):
    """
    读取表格为json
    :param excle_name: excel文件路径
    """
    _dict = {}
    try:
        workbook = xlrd.open_workbook(filename=excle_name)
    except Exception:
        logger.error(f"Faild open {excle_name}", exc_info=True)
        return _dict
    sheets = workbook.sheets()
    for i in range(0,len(sheets)):
        _dict.setdefault(sheets[i].name,[])
        try:
            title = sheets[i].row_values(0)
        except Exception:
            logger.error(f"{excle_name}/{sheets[i].name}no have data", exc_info=True)
            continue
        for n in range(1, sheets[i].nrows):
            row_value = sheets[i].row_values(n)
            _dict[sheets[i].name].append(dict(zip(title,row_value)))
    return _dict

def write_xlsx(excle_name, **tables):
    ''''
    写入xlsx文件
    :param excle_name: excel文件路径
    :param sheet: sheet名称与数据
    '''
    workbook = xlsxwriter.Workbook(excle_name)
    for name,rows in tables.items():
        if not rows:continue
        worksheet = workbook.add_worksheet(name)
        for index,row in enumerate(rows):
            worksheet.write_row(index,0,row)
    workbook.close()