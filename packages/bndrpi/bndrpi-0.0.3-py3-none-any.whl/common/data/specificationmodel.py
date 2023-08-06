# codeing:utf-8

class SpecificationModel:
    def __init__(self, SpecificationID=0, MinWeight=0, MaxWeight=0):
        self.SpecificationID = SpecificationID
        self.MinWeight = MinWeight
        self.MaxWeight = MaxWeight

    def setSpecificationID(self, SpecificationID=0):
        self.SpecificationID = SpecificationID

    def setMinWeight(self, MinWeight=0):
        self.MinWeight = MinWeight

    def setMaxWeight(self, MaxWeight=0):
        self.MaxWeight = MaxWeight
