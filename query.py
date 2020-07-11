#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sys
import requests
from lib.sqlite_help import sqliteDB
from lib.config_help import ini2json
from lib.logs_help import Logger
from lib.excel_help import excel2list
from lib.network_help import net2ip

logger = Logger("debug",name=os.path.split(os.path.splitext(os.path.abspath(__file__))[0])[-1])

config_path = "config.ini"
if not os.path.exists(config_path):
    logger.error(f"未找到配置文件 {config_path}")
    sys.exit()

config = ini2json(config_path)

dbname = config["本地"]["dbname"]

create_table = '''CREATE TABLE assets (
                    ip TEXT NOT NULL,
                    net TEXT NOT NULL,
                    info TEXT,
                    dev TEXT, 
                    dep TEXT,
                    user TEXT
                );'''
if not os.path.exists(dbname):
    db = sqliteDB(dbname,create_table)
else:
    db = sqliteDB(dbname)
    
def update_data():
    if os.path.exists(config["本地"]["excel"]):
        for file in os.listdir(config["本地"]["excel"]):
            if not file.endswith(".xls") and not file.endswith(".xlsx"):
                continue
            excel_file = os.path.join(config["本地"]["excel"],file)
            _items = excel2list(excel_file,index=0)
            for item in _items[0][1:]:
                if len(item) != 5:
                    logger.info(f"数据格式不正确 长度不等于5 :{item}")
                    continue
                if db.get("select * from assets where net=?",[item[0]]):
                    logger.info(f"网段已存在 :{item[0]}")
                    continue
                logger.info(f"拆分网段中 :{item[0]}")
                for ip in net2ip(item[0].strip(),_all=True,_error=True):
                    if not db.set("INSERT INTO assets (ip,net,info,dev,dep,user) VALUES (?,?,?,?,?,?)",[ip,]+item):
                        logger.info(f"数据插入错误 :{ip} {item}")
    logger.info("本次更新数据完毕")

def local_query(ip_str):
    _data = {}
    _data.setdefault("list",[])
    logger.info(f"查询:{ip_str}")
    for ip in ip_str.split(","):
        for item in db.get("select * from assets where ip=?",[ip]):
            _data["list"].append(list(item))
    logger.info(f"结果:{_data}")
    return _data

def remote_query(ip_str):
    _data = {}
    _data.setdefault("list",[])
    for name in config:
        if name == "本地":continue
        address = config[name].get("address","")
        token = config[name].get("token","")
        if not address:continue
        logger.info(f"查询:{name},{address},{token},{ip_str}")
        try:
            rj = requests.get(f"{address}/query",params={"ip_str":ip_str,"token":token}).json()
            for item in rj.get("list",[]):
                _data["list"].append([name,]+item)
        except Exception:
            logger.error("查询失败", exc_info=True)
    logger.info(f"结果:{_data}")
    return _data

if __name__ == "__main__":
    ip_str = "192.168.1.1"
    data = local_query(ip_str)
    print(data)
