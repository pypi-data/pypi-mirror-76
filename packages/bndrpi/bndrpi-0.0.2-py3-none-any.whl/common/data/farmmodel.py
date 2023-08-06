# codeing:utf-8

class FarmModel:
    def __init__(self,FactoryID=0, FarmID=0, FarmName='', ContactName='', FarmAddress='',ReceiveCount=0,TotalAmount=0):
        self.FactoryID = FactoryID
        self.FarmID = FarmID
        self.FarmName = FarmName
        self.ContactName = ContactName
        self.FarmAddress = FarmAddress
        self.ReceiveCount = ReceiveCount
        self.TotalAmount = TotalAmount


    def setFactoryID(self, FactoryID=0):
        self.FactoryID = FactoryID

    def setFarmID(self, FarmID=0):
        self.FarmID = FarmID        

    def setFarmName(self, FarmName=''):
        self.FarmName = FarmName

    def setContactName(self, ContactName=''):
        self.ContactName = ContactName

    def setFarmAddress(self, FarmAddress=''):
        self.FarmAddress = FarmAddress

    def setReceiveCount(self, ReceiveCount):
        self.ReceiveCount = ReceiveCount

    def setTotalAmount(self, TotalAmount=0):
        self.TotalAmount = TotalAmount

