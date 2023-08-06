#coding:utf-8

import sys
sys.path.append('./')

from common.view.farmview import FarmView
from common.data.farmmodel import FarmModel

class FarmViewData:
    def __init__(self, model, mobile=False):
        
        self.view = FarmView()
        self.view.FarmID = model.FarmID
        if mobile:
            self.view.FarmName = model.FarmName
            self.view.RCount = model.ReceiveCount
            self.view.TAmount = model.TotalAmount
        else:
            self.view.FarmName = "{0}{1}".format(model.ContactName, model.FarmName)

    def getView(self):
        return self.view

    