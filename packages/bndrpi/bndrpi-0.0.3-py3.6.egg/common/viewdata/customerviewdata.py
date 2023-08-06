#coding:utf-8

import sys
sys.path.append('./')

from common.view.customerview import CustomerView
from common.data.customermodel import CustomerModel

class CustomerViewData:
    def __init__(self, model):
        self.view = CustomerView()
        self.view.CID = model.customer_id
        self.view.FID = model.factory_id
        if model.customer_name and len(model.customer_name)>1:
            self.view.Xing = model.customer_name[0]
        else:
            self.view.Xing = "*"
            model.customer_name = "***"

        self.view.Name = model.customer_name
        self.view.Address = model.customer_address


    def getView(self):
        return self.view

    