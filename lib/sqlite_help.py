#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import sqlite3

from .logs_help import Logger

logger = Logger("debug",name=os.path.split(os.path.splitext(os.path.abspath(__file__))[0])[-1])

class sqliteDB():
    
    def __init__(self,dbnmae,create_table_sql=None):
        """
        初始化函数，创建数据库连接
        :param dbnmae: 传入数据库名称或数据库文件路径，eg: test.db
        :param create_table_sql: 传入的创建表SQL语句,eg:CREATE TABLE tablename (name TEXT NOT NULL);
        """
        self.conn = sqlite3.connect(dbnmae,check_same_thread = False)
        self.cursor = self.conn.cursor()
        if create_table_sql:
            self.set(create_table_sql)

    def set(self,sql,data=[],many=False):
        """
        数据库的插入、修改、删除函数
        :param sql: 传入的SQL语句 eg:INSERT INTO tablename (name) VALUES (?) / DELETE from tablename where name=? / UPDATE tablename set name = ? where name=?
        :param data: 传入对应数据，many=False:[a,b,c,d] many=True:[[a,b,c,d],[a,b,c,d],[a,b,c,d]]
        :param many: 传入批量数据，many=False
        :return: 返回操作数据库状态
        """
        try:
            if many:
                self.cursor.executemany(sql,data)
            else:
                self.cursor.execute(sql,data)
            i = self.conn.total_changes
        except Exception:
            logger.error(f'数据操作失败,sql:{sql}', exc_info=True)
            return False
        finally:
            self.conn.commit()
        if i > 0:
            return True
        else:
            return False

    def get(self,sql,data=[]): 
        """
        数据库的查询函数
        :param sql: 传入的SQL语句,eg:select * from tablename where name=?
        :param data: 传入查询参数,eg: [name,]
        :return : 返回查询结果
        """
        results = self.cursor.execute(sql,data)
        return results.fetchall()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    create_table = 'CREATE TABLE github (name TEXT NOT NULL,url TEXT NOT NULL,updated_at TEXT NOT NULL,description TEXT NOT NULL, zh_description TEXT NOT NULL);'
    if not os.path.exists("test.db"):
        db = sqliteDB("test.db",create_table)
    else:
        db = sqliteDB("test.db")

    # 增 INSERT INTO github (name,url,updated_at,description,zh_description) VALUES (?,?,?,?,?)
    # 删 DELETE from github where url=?
    # 改 UPDATE github set name = ? where url2=?
    # 查 select * from github where name=?

