# codeing:utf-8

import sys
sys.path.append('./')

from common.repositories.mysqldb import MysqlHelper
from common.data.qrcodemodel import QRCodeModel

class  QRCodeRepository:
    def __init__(self, **dbConfig):
        #self.helper = MysqlHelper(host=dbConfig["host"], user=dbConfig["user"], password=dbConfig["password"], database=dbConfig["database"])
        self.helper = MysqlHelper(**dbConfig)

    def Select_DatasByID(self, QRCodeID):
        sql = 'select QRcodeID,FarmID,FarmName,ReceiveID from qrcode where QRcodeID="' +QRCodeID + '";'

        model = QRCodeModel()

        arrs = self.helper.Select(sql)

        for item in arrs:
            model.QRcodeID = item[0]
            model.FarmID = item[1]
            model.FarmName = item[2]
            model.ReceiveID = item[3]

            break

        """
        arr = self.helper.SelectDic(sql,['QRcodeID','FarmID','FarmName','ReceiveID'])

        if len(arr)>0:
            model.QRcodeID = arr[0]["QRcodeID"]
            model.FarmID = arr[0]["FarmID"]
            model.FarmName = arr[0]["FarmName"]
            model.ReceiveID = arr[0]["ReceiveID"]

        """
        
        return model

    def Select_DatasByDefautID(self, QRCodeID):
        sql = 'select QRcodeID,FarmID,FarmName,ReceiveID from qrcode qc inner join basesetting bs on bs.FactoryID=qc.FactoryID where QRcodeID="' +QRCodeID + '";'
        
        model = QRCodeModel()

        arrs = self.helper.Select(sql)

        for item in arrs:
            model.QRcodeID = item[0]
            model.FarmID = item[1]
            model.FarmName = item[2]
            model.ReceiveID = item[3]

            break

        """
        arr = self.helper.SelectDic(sql,['QRcodeID','FarmID','FarmName','ReceiveID'])

        if len(arr)>0:
            model.QRcodeID = arr[0]["QRcodeID"]
            model.FarmID = arr[0]["FarmID"]
            model.FarmName = arr[0]["FarmName"]
            model.ReceiveID = arr[0]["ReceiveID"]

        """
        
        return model
    


if __name__ == "__main__":

    obj = QRCodeRepository(host="192.168.199.15", user="root", password="root", database="weight")

    model = obj.Select_DatasByID('')

    #print(model.FarmID)