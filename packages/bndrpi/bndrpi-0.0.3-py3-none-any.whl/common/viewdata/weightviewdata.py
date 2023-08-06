#coding:utf-8

import sys
#sys.path.append('./')

from common.view.weightview import WeightView
from common.data.weightmodel import WeightModel

class WeightViewData:
    def __init__(self, model):
        
        self.view = WeightView()
        
        self.view.MWeight = model.GrossWeight
        self.view.MaShu = model.StandardWeight
        self.view.Count = model.ReceiveCount
        self.view.Time = model.ReceiveTime

    def getView(self):
        return self.view

    