# codeing:utf-8

class WeightModel:
    def __init__(self,ReceiveID='',MessageID='', ReceiveType=20, BatchID='', FactoryID=0, FactoryName='',
    FarmID=0, FarmName='', QRCode='', SpecificationID=0, CartonWeight=0, RealWeight=0, GrossWeight=0, StandardWeight=0,
    ReceiveCount=1, ReceiveTime=''):
        self.ReceiveID = ReceiveID
        self.MessageID = MessageID
        self.ReceiveType = ReceiveType
        self.BatchID = BatchID
        self.FactoryID = FactoryID
        self.FactoryName = FactoryName
        self.FarmID = FarmID
        self.FarmName = FarmName
        self.QRCode = QRCode
        self.SpecificationID = SpecificationID
        self.CartonWeight = CartonWeight
        self.RealWeight = RealWeight
        self.GrossWeight = GrossWeight
        self.StandardWeight = StandardWeight
        self.ReceiveCount = ReceiveCount
        self.ReceiveTime = ReceiveTime

    def setReceiveID(self,ReceiveID=''):
        self.ReceiveID = ReceiveID

    def setReceiveType(self, ReceiveType=20):
        self.ReceiveType = ReceiveType

    def setBatchID(self, BatchID=''):
        self.BatchID = BatchID

    def setFactoryID(self, FactoryID=0):
        self.FactoryID = FactoryID

    def setFactoryName(self, FactoryName=''):
        self.FactoryName = FactoryName

    def setFarmID(self, FarmID=0):
        self.FarmID = FarmID

    def setFarmName(self, FarmName=''):
        self.FarmName = FarmName

    def setSpecificationID(self, SpecificationID=0):
        self.SpecificationID = SpecificationID

    def setCartonWeight(self, CartonWeight=0):
        self.CartonWeight = CartonWeight

    def setRealWeight(self, RealWeight=0):
        self.RealWeight = RealWeight

    def setGrossWeight(self, GrossWeight=0):
        self.GrossWeight = GrossWeight

    def setStandardWeight(self, StandardWeight=0):
        self.StandardWeight = StandardWeight

    def setReceiveCount(self, ReceiveCount=1):
        self.ReceiveCount = ReceiveCount

    def setReceiveTime(self, ReceiveTime=''):
        self.ReceiveTime = ReceiveTime

    def setQRCode(self, QRCode=''):
        self.QRCode = QRCode
    

