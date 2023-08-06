#coding:utf-8

import sys
sys.path.append('./')

from common.view.factoryview import FactoryView
from common.data.factorymodel import FactoryModel

class FactoryViewData:
    def __init__(self, model):
        self.view = FactoryView()
        self.view.FactoryID = model.FactoryID
        self.view.FactoryName = model.FactoryName
        self.view.CartonWeight = model.CartonWeight
        self.view.AddRadix = model.AddRadix
        
    def getView(self):
        return self.view

    