# coding:utf-8

import sys
import uuid
import random
import datetime

sys.path.append('./')

from common.repositories.factoryrepository import FactoryRepository
from common.repositories.specificationrepository import SpecificationRepository
from common.repositories.qrcoderepository import QRCodeRepository
from common.repositories.customerrepository import CustomerRepository
from common.repositories.shipmentrepository import ShipMentRepository
from common.repositories.farmrepository import FarmRepository

from common.view.factoryview import FactoryView
from common.view.qrcodeview import QRCodeView
from common.view.farmview import FarmView
from common.view.customerview import CustomerView

from common.viewdata.factoryviewdata import FactoryViewData
from common.viewdata.qrcodeviewdata import QRCodeViewData
from common.viewdata.farmviewdata import FarmViewData
from common.viewdata.customerviewdata import CustomerViewData

from common.data.factorymodel import FactoryModel
from common.data.specificationmodel import SpecificationModel
from common.data.farmmodel import FarmModel
from common.data.customermodel import CustomerModel
from common.data.basemodel import BaseModel

# from view.weightparameter import WeightParameter

class DeviceBusiness:
    def __init__(self, **dbConfig):
        self._factoryRepository = FactoryRepository(**dbConfig)
        self._specRepository = SpecificationRepository(**dbConfig)
        self._qrcodeRepository = QRCodeRepository(**dbConfig)
        self._farmRepository = FarmRepository(**dbConfig)
        self._customerRepository = CustomerRepository(**dbConfig)
        self._shipmentRepository = ShipMentRepository(**dbConfig)

    def getFactoryInfo(self):
        model = self._factoryRepository.Select_Data()

        model.AddRadix = int(model.AddRadix)

        return FactoryViewData(model).getView()

    def getSpecifications(self):
        
        models = self._specRepository.Select_Datas()

        return models

    def getQRCodeInfo(self, qrcodeid):
        
        if not qrcodeid:
            return None
        
        # qrcodeid=0 获取默认养殖场数据
        if qrcodeid=='0':
            model = self._qrcodeRepository.Select_DatasByDefautID(qrcodeid)
        else:
            model = self._qrcodeRepository.Select_DatasByID(qrcodeid)

        vmodel = QRCodeViewData(model).getView()

        return vmodel

    def getFarmInfo(self, fid):
        
        if not fid:
            model = FarmModel()
            
            vmodel = FarmViewData(model).getView()

            return vmodel
        else:
            model = self._farmRepository.Select_Data(fid)

            vmodel = FarmViewData(model).getView()

            return vmodel

    def getFarmList(self):
        models = self._farmRepository.Select_Datas()

        vmodels = []

        for item in models:
            v = FarmViewData(item).getView()

            vmodels.append(v.__dict__)

        return vmodels

    def getBaseInfo(self):
        model = self._factoryRepository.Select_BaseInfo()

        return model
    
    def getCustomerByID(self, cid):
        
        model = self._customerRepository.Select_DataByID(cid)

        return CustomerViewData(model).getView()
    


    def getCustomerList(self):
        
        models = self._customerRepository.Select_Datas()

        vmodels = []

        for item in models:
            v = CustomerViewData(item).getView()

            vmodels.append(v.__dict__)

        return vmodels


    def shipMentInsertOrExists(self,factoryID, customer_id,message_id):

        model = self._shipmentRepository.Select_NowDataByCID(factoryID, customer_id)
        
        if model and model.factory_id>0:
            
            return model.shipment_id
        else:
            
            model.shipment_id = "{0}{1}".format(datetime.datetime.now().strftime("%y%m%d%H%M%S"),random.randint(0,9))
            model.message_id = message_id
            model.factory_id = factoryID
            model.customer_id = customer_id

            if self._shipmentRepository.Insert(model)>0:
                return model.shipment_id
            else:
                return -1
            

        
if __name__ == "__main__":
    
    #business = DeviceBusiness(host="127.0.0.1", user="root", password="root", database="weight")
    business = DeviceBusiness(host="192.168.199.16", user="root", password="root", database="weight")

    #business.shipMentInsertOrExists(1,1)
    #model = business.getFactoryInfo()
    models = business.getCustomerList()

    print(models)
        

        

        



