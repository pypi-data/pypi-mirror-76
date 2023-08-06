# codeing:utf-8

import sys
#sys.path.append('./')

from common.repositories.mysqldb import MysqlHelper
from common.data.farmmodel import FarmModel

class  FarmRepository:
    def __init__(self, **dbConfig):
        #self.helper = MysqlHelper(host=dbConfig["host"], user=dbConfig["user"], password=dbConfig["password"], database=dbConfig["database"])
        self.helper = MysqlHelper(**dbConfig)

    def Select_Datas(self):
        sql = '''select bs.FactoryID,f.FarmID,f.FarmName,f.ContactName,f.FarmAddress from basesetting bs 
                inner join factoryfarm ff on bs.FactoryID=ff.FactoryID 
                inner join farm f on f.FarmID=ff.FarmID; '''

        models = []

        arrs = self.helper.Select(sql)

        for item in arrs:
            model = FarmModel()

            model.FactoryID = item[0]
            model.FarmID = item[1]
            model.FarmName = item[2]
            model.ContactName = item[3]
            model.FarmAddress = item[4]

            models.append(model)

     
        
        return models

    def Select_Data(self, ffid):
        sql = '''select bs.FactoryID,f.FarmID,f.FarmName,f.ContactName,f.FarmAddress from farm f 
                inner join basesetting bs on 1=1 where FarmID={0}'''.format(ffid)
        
        model = FarmModel()

        arrs = self.helper.Select(sql)

        for item in arrs:
            model.FactoryID = item[0]
            model.FarmID = item[1]
            model.FarmName = item[2]
            model.ContactName = item[3]
            model.FarmAddress = item[4]
            

            break

        return model

    def Select_NowDatas(self,fid):
        sql = '''select tb.*,ifnull(tb2.ReceiveCount,0) ReceiveCount from ( 
                select f.FarmID,f.FarmName,f.ContactName,f.FarmAddress from farm f 
                where f.IsValid=1 and exists(select 1 from factoryfarm ff where ff.FactoryID={0} and f.FarmID=ff.FarmID) ) tb 
                left join (select FarmID,sum(ReceiveCount) ReceiveCount from weight_history w 
                where  FactoryID={0} and TO_DAYS(ReceiveTime)=TO_DAYS(now()) 
                group by FarmID) tb2 on tb.FarmID=tb2.FarmID'''.format(fid)

        models = []

        arrs = self.helper.Select(sql)

        for item in arrs:
            model = FarmModel()

            model.FactoryID = fid
            model.FarmID = item[0]
            model.FarmName = item[1]
            model.ContactName = item[2]
            model.FarmAddress = item[3]
            model.ReceiveCount = item[4]

            models.append(model)

     
        
        return models
        
if __name__ == "__main__":

    _resp = FarmRepository(host="192.168.199.15", user="root", password="root", database="weight")

    #models = _resp.Select_Datas()

    model = _resp.Select_Data(1)
    print(model.__dict__)
    #print(len(models))
