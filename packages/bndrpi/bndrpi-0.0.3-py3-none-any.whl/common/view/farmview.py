#coding:utf-8


class FarmView:
    def __init__(self, FarmID=0, FarmName='', QRCodeID='', RCount=0, TAmount=0):       
        self.FarmID = FarmID
        self.FarmName = FarmName
        self.QRCodeID = QRCodeID
        self.RCount = RCount
        self.TAmount = TAmount

    def setFarmID(self, FarmID=0):
        self.FarmID = FarmID

    def setFarmName(self, FarmName):
        self.FarmName = FarmName

    def setQRCodeID(self, QRCodeID):
        self.QRCodeID = QRCodeID

    def setRCount(self, RCount):
        self.RCount = RCount

    def setTAmount(self, TAmount):
        self.TAmount = TAmount