# codeing:utf-8

import sys
sys.path.append('./')

from common.repositories.mysqldb import MysqlHelper
from common.data.shipmentlistmodel import ShipMentListModel

class  ShipMentListRepository:
    def __init__(self, **dbConfig):
        #self.helper = MysqlHelper(host=dbConfig["host"], user=dbConfig["user"], password=dbConfig["password"], database=dbConfig["database"])
        self.helper = MysqlHelper(**dbConfig)

    def Insert(self, model):
        if not model:
            return -1

        sql = '''insert into shipment_list 
                values('{0}','{13}', '{1}',0,{2},{3},'{4}',{5},{6},{7},{8},{9},{10},{11},'{12}',1)'''

        sql = sql.format(model.id,model.shipment_id,model.factory_id,model.farm_id,model.qrcode_id,model.specification_id,model.carton_weight,model.real_weight,model.gross_weight,model.weight_code,model.standard_weight,model.unit_price,model.update_time,model.message_id)


        return self.helper.Insert(sql)


if __name__ == "__main__":
    db = ShipMentListRepository(host="192.168.199.15", user="root", password="root", database="weight")
