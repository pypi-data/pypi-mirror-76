# coding:utf-8

import sys
import uuid
import random
import datetime

sys.path.append('./')

from common.repositories.factoryrepository import FactoryRepository
from common.repositories.farmrepository import FarmRepository

from common.view.farmview import FarmView

from common.viewdata.farmviewdata import FarmViewData

from common.data.factorymodel import FactoryModel
from common.data.farmmodel import FarmModel

class FarmBusiness:
    def __init__(self, **dbConfig):
        self._factoryDB = FactoryRepository(**dbConfig)
        self._farmDB = FarmRepository(**dbConfig)

    def getFarms_NowInfos(self):
        
        fModel = self._factoryDB.Select_BaseInfo()
        print(fModel.FactoryID)

        models = self._farmDB.Select_NowDatas(fModel.FactoryID)

        vmodels = []

        for item in models:
            v = FarmViewData(item, True).getView()

            vmodels.append(v.__dict__)

        return vmodels

    def getFarm_ByFFID(self, ffid):
        
        model = self._farmDB.Select_Data(ffid)

        v = FarmViewData(model, True).getView()

        return v


if __name__ == "__main__":
    _bu = FarmBusiness(host="192.168.199.16", user="root", password="root", database="weight")
    #_bu = FarmBusiness(host="127.0.0.1", user="root", password="root", database="weight")

    models = _bu.getFarms_NowInfos()

    print(models)

    

