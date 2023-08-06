# codeing:utf-8

import sys
sys.path.append('./')

# from repositories.sqlitedb import SqliteHelper
from common.repositories.mysqldb import MysqlHelper
#from config import DATABASES
from common.data.weightmodel import WeightModel


class WeightRepository:
    def __init__(self, **dbConfig):
        # self.helper = SqliteHelper(DATABASES['default'])
        #self.helper = MysqlHelper(host=dbConfig["host"], user=dbConfig["user"], password=dbConfig["password"], database=dbConfig["database"])
        self.helper = MysqlHelper(**dbConfig)

    def Insert(self, model):
        if not model:
            return -1  

        sql = 'insert into weight values("' + model.ReceiveID + '","' + model.MessageID + '",' + str(model.ReceiveType) + ',"' + model.BatchID +'",' \
        + str(model.FactoryID) + ',"' + model.FactoryName + '",' + str(model.FarmID) + ',"' + model.FarmName +'","' +model.QRCodeID+'",' \
        + str(model.SpecificationID) + ',' + str(model.CartonWeight) + ',' + str(model.RealWeight) + ',' + str(model.GrossWeight) + ',' \
        + str(model.StandardWeight) + ',' + str(model.ReceiveCount) + ',"' + model.ReceiveTime + '");'
        #print(sql)
        return self.helper.Insert(sql)

    def GetFarmReceiveInfos(self, ffid):
        sql = '''select GrossWeight,StandardWeight,ReceiveCount,ReceiveTime from weight 
            where FarmID={0} and TO_DAYS(ReceiveTime)=TO_DAYS(now())'''.format(ffid)

        models = []

        arrs = self.helper.Select(sql)

        for item in arrs:
            model = WeightModel()

            #model.FarmID = ffid
            model.GrossWeight = item[0]
            model.StandardWeight = item[1]
            model.ReceiveCount = item[2]
            model.ReceiveTime = item[3]

            models.append(model)

     
        
        return models

    """
    def Select(self):
        sql = 'select * from weighttb'

        return self.helper.Select(sql)

    def Select_NoSyncDatas(self):
        sql = 'select * from weighttb ' #where syncstatus=0

        return self.helper.SelectDic(sql,['fid','fname','weight'])

    def Update_SetSyncStatus(self, fid, status):
        sql = 'update weighttb set syncstatus='+ str(status) +' where fid='+ fid

        return self.helper.Update(sql)
    """

if __name__ == "__main__":
    _res = WeightRepository(host="192.168.199.15", user="root", password="root", database="weight")

    

