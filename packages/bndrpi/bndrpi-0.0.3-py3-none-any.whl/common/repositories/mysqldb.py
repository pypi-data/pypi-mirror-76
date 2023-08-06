
# coding:utf-8

import pymysql

class MysqlHelper:
    def __init__(self, **para):
        self.config = para
        """
        {
            "host" : "192.168.43.253",#"127.0.0.1",
            "user" : "root",
            "password" : "root",
            "database" : "weight"
        }
        """

    def __Connection(self):
        #self.conn = pymysql.connect("localhost","root","root","weight")
        self.conn = pymysql.connect(**self.config)

    def Insert(self, sql=''):
        """
        添加操作
        参数说明：
            sql:添加语句
        返回字段说明：
            返回一int类型数据，大于0标识添加成功，否则添加失败
        """

        self.__Connection()

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

       
    def Select(self, sql=''):
        """
        检索操作
        参数说明：
            sql:检索语句
        返回字段说明：
            返回一元组数组
        """

        self.__Connection()

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

        self.__Connection()

        #检索操作成功数据对象
        arr = []

        if len(sql)<1:
            return arr

        try:
            #获取游标
            self.cur = self.conn.cursor()
            #执行检索操作
            self.cur.execute(sql)

            arr = [dict(zip(titles,row)) for row in self.cur.fetchall()]

            #关闭游标
            self.cur.close()           


        except:
            arr = []
        finally:
            self.cur.close()
            self.conn.close()
        
        return arr


