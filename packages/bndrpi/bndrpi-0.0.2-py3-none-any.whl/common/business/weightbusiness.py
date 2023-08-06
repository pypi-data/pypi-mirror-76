# coding:utf-8

import sys
import uuid
import time

sys.path.append('./')

from common.repositories.weightrepository import WeightRepository 
from common.repositories.shipmentlistrepository import ShipMentListRepository
from common.data.weightmodel import WeightModel
from common.data.shipmentlistmodel import ShipMentListModel
from common.view.weightparameter import WeightParameter
from common.view.shipmentlistparameter import ShipMentListParameter
from common.viewdata.weightviewdata import WeightViewData

class WeightBusiness:
    def __init__(self, **dbConfig):
        self._repository = ShipMentListRepository(**dbConfig)
        self._rrepository = WeightRepository(**dbConfig)

    def InsertWeight(self, para):
        """zqk

        添加称重数据逻辑
        参数说明：
            para:对象
            para.fid:养殖场编号  para.fname：养殖场名称 para.weight：重量
        """
        #_repository = WeightRepository()

        model = WeightModel()
        
        model.ReceiveID = para.ID # str(uuid.uuid1())
        model.MessageID = para.MID
        model.ReceiveType = 20
        model.BatchID = '{0}{1}'.format(time.strftime('%y%m%d', time.localtime()), str(para.FID).zfill(4))
        model.FactoryID = para.FID
        model.FactoryName = para.FName
        model.FarmID = para.FFID
        model.FarmName = para.FFName
        model.QRCodeID = para.QRCodeID
        model.SpecificationID = para.SID
        model.CartonWeight = para.CWeight
        model.RealWeight = para.RWeight
        model.GrossWeight = para.GWeight
        model.StandardWeight = para.SWeight
        model.ReceiveCount = 1
        model.ReceiveTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


  
        if self._rrepository.Insert(model)>0:
            return 1
        else:
            return -1

    def InsertSendWeight(self, para):
        
        #_repository = ShipMentListRepository()

        model = ShipMentListModel()
                
        model.id = para.ID # str(uuid.uuid1())
        model.message_id = para.MID
        model.shipment_id = para.ShipMentID
        model.factory_id = para.FID
        model.farm_id = para.FFID
        model.qrcode_id = para.QRCodeID
        model.specification_id = para.SID
        model.carton_weight = para.CWeight
        model.real_weight = para.RWeight
        model.gross_weight = para.GWeight
        model.weight_code = para.SWeight
        model.standard_weight = para.SWeight
        model.update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

  
        if self._repository.Insert(model)>0:
            return 1
        else:
            return -1

    def GetFarmReceiveInfo(self, fid):
        
        models = self._rrepository.GetFarmReceiveInfos(fid)
        
        vmodels = []

        for item in models:
            v = WeightViewData(item).getView()

            vmodels.append(v.__dict__)

        return vmodels


if __name__ == "__main__":
    business = WeightBusiness(host="192.168.199.15", user="root", password="root", database="weight")

    para = WeightParameter()

    para.FFID = 1
    para.FFName = '深州共享工厂'
    para.FID = 1
    para.FName = '张大帅养殖场'
    para.QRCodeID = 'qrcodeid001'
    para.SID = 20
    para.CWeight = 0.5
    para.GWeight = 34
    para.SWeight = 34

    business.InsertWeight(para)
