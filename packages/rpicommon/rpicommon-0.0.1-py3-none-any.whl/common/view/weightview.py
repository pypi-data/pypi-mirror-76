#coding:utf-8

class WeightView:
    def __init__(self,MWeight=0, MaShu=0, Count=0, Time=''):       
        self.MWeight = MWeight
        self.MaShu = MaShu
        self.Count =Count
        self.Time = Time

    def setMWeight(self,MWeight=0):
        self.MWeight = MWeight

    def setMaShu(self, MaShu):
        self.MaShu = MaShu

    def setCount(self, Count):
        self.Count = Count

    def setTime(self, Time=''):
        self.Time = Time
