# codeing:utf-8

class QRCodeModel:
    def __init__(self, QRcodeID='', FactoryID=0, FarmID=0, FarmName='', ReceiveID=''):
        self.QRcodeID = QRcodeID
        self.FactoryID = FactoryID
        self.FarmID = FarmID
        self.FarmName = FarmName
        self.ReceiveID = ReceiveID

    def setQRcodeID(self, QRcodeID=''):
        self.QRcodeID = QRcodeID

    def setFactoryID(self, FactoryID=0):
        self.FactoryID = FactoryID

    def setFarmID(self, FarmID=0):
        self.FarmID = FarmID

    def setFarmName(self, FarmName=''):
        self.FarmName = FarmName

    def setReceiveID(self, ReceiveID=''):
        self.ReceiveID = ReceiveID