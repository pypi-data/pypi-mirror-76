#coding:utf-8

class ShipMentListParameter:
    def __init__(self,id='',MID='',ShipMentID='', FID=0, FName='', FFID=0, FFName='', PWeight=0, GWeight=0, SWeight=0, RWeight=0, SID=0, CWeight=0,QRCodeID='',Type=0):
        self.Type=Type
        self.ID=id
        self.MID=MID
        self.ShipMentID = ShipMentID
        self.FID = FID
        self.FName = FName
        self.FFID = FFID
        self.FFName = FFName
        self.PWeight = PWeight
        self.GWeight = GWeight
        self.SWeight =SWeight
        self.RWeight = RWeight
        self.SID = SID
        self.CWeight = CWeight
        self.QRCodeID = QRCodeID

    def setShipMentID(self, ShipMentID):
        self.ShipMentID = ShipMentID
        
    def setFid(self,FID=0):
        self.FID = FID

    def setFName(self, fname=''):
        self.fname = fname

    def setGWeight(self, GWeight=0):
        self.GWeight = GWeight

    def setSWeight(self, SWeight=0):
        self.SWeight = SWeight

    def setSID(self, SID=0):
        self.SID = SID

    