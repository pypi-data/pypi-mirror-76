# codeing:utf-8

import sys

sys.path.append('./')


from common.repositories.mysqldb import MysqlHelper
from common.data.customermodel import CustomerModel

class  CustomerRepository:
    def __init__(self, **dbConfig):
        #self.helper = MysqlHelper(host=dbConfig["host"], user=dbConfig["user"], password=dbConfig["password"], database=dbConfig["database"])
        self.helper = MysqlHelper(**dbConfig)

    def Select_DataByID(self, customer_id):
        
        model = CustomerModel()

        sql = "select customer_id,factory_id,customer_name,customer_address from shipment_customer where customer_id={0}".format(customer_id)

        arrs = self.helper.Select(sql)


        for item in arrs:            

            model.customer_id = item[0]
            model.factory_id = item[1]
            model.customer_name = item[2]
            model.customer_address = item[3]

            break

        return model

    def Select_Datas(self):
        sql = '''select customer_id,factory_id,customer_name,customer_address from shipment_customer c 
                inner join basesetting bs on c.factory_id=bs.FactoryID 
                where c.customer_isvalid=1;'''


        models = []

        arrs = self.helper.Select(sql)

        for item in arrs:
            model = CustomerModel()

            model.customer_id = item[0]
            model.factory_id = item[1]
            model.customer_name = item[2]
            model.customer_address = item[3]

            models.append(model)

     
        
        return models

if __name__ == "__main__":

    _resp = CustomerRepository(host="192.168.199.15", user="root", password="root", database="weight")

    models = _resp.Select_Datas()

    #print(len(models))
