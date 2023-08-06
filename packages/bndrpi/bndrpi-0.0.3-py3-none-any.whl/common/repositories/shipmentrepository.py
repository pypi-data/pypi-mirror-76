# codeing:utf-8

import sys
sys.path.append('./')

from common.repositories.mysqldb import MysqlHelper
from common.data.shipmentmodel import ShipMentModel

class  ShipMentRepository:
    def __init__(self, **dbConfig):
        #self.helper = MysqlHelper(host=dbConfig["host"], user=dbConfig["user"], password=dbConfig["password"], database=dbConfig["database"])
        self.helper = MysqlHelper(**dbConfig)

    def Insert(self, model):
        if not model:
            return -1

        sql = '''insert into shipment(shipment_id,message_id,factory_id,shipment_amount,shipment_sum,customer_id,shipment_truck,truck_driver_name,truck_driver_mobile,is_valid) 
                values('{0}','{1}',{2},0,0,{3},'','','',1)'''.format(model.shipment_id, model.message_id, model.factory_id, model.customer_id)

        #print(sql)
        return self.helper.Insert(sql)

    def Select_NowDataByCID(self,factoryid, customer_id):
        
        model = ShipMentModel()

        sql ='''select shipment_id,factory_id,customer_id from shipment 
                where factory_id={0} and customer_id={1} and to_days(update_time)=to_days(now())'''.format(factoryid, customer_id)

        arrs = self.helper.Select(sql)

        for item in arrs:
            
            model.shipment_id = item[0]
            model.factory_id = item[1]
            model.customer_id = item[2]

            break

        return model


if __name__ == "__main__":
    
    _rep = ShipMentRepository(host="192.168.199.15", user="root", password="root", database="weight")

    model = _rep.Select_NowDataByCID(1,1)
    print(model.__dict__)
           