"""
1 函数：insert(table, keys, values):添加数据；成功返回1，失败返回0
        updata(table, keys, values):修改数据，如果主键不存在则新增数据；成功返回1，失败返回0
        select(sql):查询数据；返回元祖型结果
2 使用方法：
        conn = pymysql.connect(host='localhost', user='root', password='', port=3306, db='')
        cursor = mysql_test.Cursor(conn)
        cursor.insert(table, keys, values)
"""

import pymysql


class Cursor(object):
    def __init__(self, conn):
        self.conn = conn
        
        
    
    def insert(self, table, keys, values):
        """
        参数：table:str, keys:列表(内容必须为字符串), values:列表中套元祖
        return:0：表示失败；1：表示成功
        """
        self.cursor = self.conn.cursor()
        success = 0
        keys = ', '.join(keys)
        str_values = ', '.join(['%s'] * len(values[0]))
        sql = "INSERT INTO {table}({keys}) VALUES ({values})".format(table=table, keys=keys, values=str_values)
        try:
            self.cursor.executemany(sql, values)
            self.conn.commit()
            success = 1

        except:
            self.conn.rollback()

        self.cursor.close()
        
        return success

    def update(self, table, keys, values):
        """
        参数：table:str, keys:列表(内容必须为字符串), values:列表中套元祖
        return:0：表示失败；1：表示成功
        """
        self.cursor = self.conn.cursor()
        success = 0
        str_keys = ', '.join(keys)
        str_values = ', '.join(['%s'] * len(values[0]))
        sql = "INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE".format(table=table, keys=str_keys, values=str_values)
        update = ','.join([" {key} = %s".format(key=key) for key in keys])
        sql += update
        try:
            for i in range(len(values)):
                self.cursor.execute(sql, values[i]*2)
            self.conn.commit()
            success = 1

        except:
            self.conn.rollback()

        self.cursor.close()
        
        return success

    def select(self, sql):
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            self.cursor.close()
            return results
        except:
            self.cursor.close()
            return None
