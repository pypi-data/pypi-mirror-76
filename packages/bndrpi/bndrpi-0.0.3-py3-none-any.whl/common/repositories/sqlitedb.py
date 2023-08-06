
# coding:utf-8

import sqlite3

class SqliteHelper:
    """
    sqlite数据库通用类，可以实现常见的添加、更改、查询操作
    """
    def __init__(self, dbpath=''):
        """
        初始化函数
        参数说明：
            dbpath：数据库地址名称字符串
        """
        self.dbpath = dbpath
        
    def __ConnectionDB(self):
        self.conn = sqlite3.connect(self.dbpath)

    def Insert(self, sql=''):
        """
        添加操作
        参数说明：
            sql:添加语句
        返回字段说明：
            返回一int类型数据，大于0标识添加成功，否则添加失败
        """

        self.conn = sqlite3.connect(self.dbpath)
        #添加操作成功标识
        mark = 0

        if len(sql)<1:
            return mark

        try:
            #获取游标
            self.cur = self.conn.cursor()
            #执行添加操作
            self.cur.execute(sql)
            #关闭游标
            self.cur.close()
            #提交添加的记录
            self.conn.commit()

            mark = 1

        except:
            mark = -1
        finally:
            self.cur.close()
            self.conn.close()

        return mark

    def Update(self, sql=''):
        """
        更新操作
        参数说明：
            sql:更新语句
        返回字段说明：
            返回一int类型数据，大于0标识更新成功，否则更新失败
        """

        self.conn = sqlite3.connect(self.dbpath)
        #更新操作成功标识
        mark = 0

        if len(sql)<1:
            return mark

        try:
            #获取游标
            self.cur = self.conn.cursor()
            #执行更新操作
            self.cur.execute(sql)
            #关闭游标
            self.cur.close()
            #提交更新的记录
            self.conn.commit()

            mark = 1

        except:
            mark = -1
        finally:
            self.cur.close()
            self.conn.close()

        return mark
        
    def Select(self, sql=''):
        """
        检索操作
        参数说明：
            sql:检索语句
        返回字段说明：
            返回一元组数组
        """

        self.conn = sqlite3.connect(self.dbpath)

        #检索操作成功数据对象
        arr = []

        if len(sql)<1:
            return arr

        try:
            #获取游标
            self.cur = self.conn.cursor()
            #执行检索操作
            self.cur.execute(sql)

            arr = self.cur.fetchall()

            #关闭游标
            self.cur.close()           


        except:
            arr = []
        finally:
            self.cur.close()
            self.conn.close()

        return arr

    def SelectDic(self, sql='', titles=[]):
        """
        检索命令
        Args:
            sql:检索语句
            titles:对应的属性名组成的元组
        return:
            返回字典列表
        """

        self.conn = sqlite3.connect(self.dbpath)

        #检索操作成功数据对象
        arr = []

        if len(sql)<1:
            return arr

        try:
            #获取游标
            self.cur = self.conn.cursor()
            #执行检索操作
            self.cur.execute(sql)

            arr = (dict(zip(titles,row)) for row in self.cur.fetchall())

            #关闭游标
            self.cur.close()           


        except:
            arr = []
        finally:
            self.cur.close()
            self.conn.close()
        
        return arr

