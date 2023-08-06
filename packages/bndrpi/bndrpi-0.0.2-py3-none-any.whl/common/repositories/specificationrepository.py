# codeing:utf-8

import sys


sys.path.append('./')

from common.repositories.mysqldb import MysqlHelper
from common.data.specificationmodel import SpecificationModel

class  SpecificationRepository:
    def __init__(self, **dbConfig):
        #self.helper = MysqlHelper(host=dbConfig["host"], user=dbConfig["user"], password=dbConfig["password"], database=dbConfig["database"])
        self.helper = MysqlHelper(**dbConfig)

    def Select_Datas(self):
        sql = 'select SpecificationID,MinWeight,MaxWeight from specifications s inner join basesetting bs on s.FactoryID= bs.FactoryID where s.IsValid=1; ' 

        models = []

        arrs = self.helper.Select(sql)

        for item in arrs:
            model = SpecificationModel()

            model.SpecificationID = item[0]
            model.MinWeight = item[1]
            model.MaxWeight = item[2]

            models.append(model)

        """
        arr = self.helper.SelectDic(sql,['SpecificationID','MinWeight','MaxWeight'])

        for item in arr:
            model = SpecificationModel()
            model.SpecificationID = item["SpecificationID"]
            model.MaxWeight = item["MaxWeight"]
            model.MinWeight = item["MinWeight"]

            models.append(model)
        """
        
        return models

if __name__ == "__main__":

    _resp = SpecificationRepository(host="192.168.199.15", user="root", password="root", database="weight")

    models = _resp.Select_Datas()

    #print(len(models))
