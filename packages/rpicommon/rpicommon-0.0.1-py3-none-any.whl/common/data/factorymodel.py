# codeing:utf-8

class FactoryModel:
    def __init__(self, FactoryID=0, FactoryName='', CartonWeight=0, AddRadix=0.6):
        self.FactoryID = FactoryID
        self.FactoryName = FactoryName
        self.CartonWeight = CartonWeight
        self.AddRadix = AddRadix

    def setFactoryID(self, FactoryID=0):
        self.FactoryID = FactoryID        

    def setFactoryName(self, FactoryName=''):
        self.FactoryName = FactoryName

    def setCartonWeight(self, CartonWeight=0):
        self.CartonWeight = CartonWeight
    
    def setAddRadix(self, AddRadix=0.6):
        self.AddRadix = AddRadix
