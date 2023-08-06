#coding:utf-8


class CustomerView:
    def __init__(self, CID=0, FID=0, Xing='', Name='', Address=''):       
        self.CID = CID
        self.FID = FID
        self.Xing = Xing
        self.Name = Name
        self.Address = Address

    def setCID(self, CID=0):
        self.CID = CID

    def setFID(self, FID):
        self.FID = FID

    def setXing(self, Xing=''):
        self.Xing = Xing

    def setName(self, Name=''):
        self.Name = Name

    def setAddress(self, Address=''):
        self.Address = Address
    
