# codeing:utf-8

import sys

sys.path.append('./')


from common.repositories.mysqldb import MysqlHelper
from common.data.factorymodel import FactoryModel
from common.data.basemodel import BaseModel


class  FactoryRepository:
    def __init__(self, **dbConfig):
        #self.helper = MysqlHelper(host=dbConfig["host"], user=dbConfig["user"], password=dbConfig["password"], database=dbConfig["database"])
        self.helper = MysqlHelper(**dbConfig)

    def Select_BaseInfo(self):
        sql = 'select FactoryID from basesetting'

        arrs = self.helper.Select(sql)

        model = BaseModel()

        for item in arrs:
            model.devicecode = item[0]

            break

        return model

    def Select_Data(self):
        sql = 'select f.FactoryID,FactoryName,CartonWeight,AddRadix from factories f inner join basesetting bs on f.FactoryID= bs.FactoryID; ' 

        # arr = self.helper.SelectDic(sql,['FactoryID','FactoryName','CartonWeight','AddRadix'])
        arrs = self.helper.Select(sql)

        model = FactoryModel()

        for item in arrs:
            model.FactoryID = item[0]
            model.FactoryName = item[1]
            model.CartonWeight = item[2]
            model.AddRadix = int(10*item[3])

            break

        """
        if len(arr)>0:
            model.FactoryID = arr[0]["FactoryID"]
            model.FactoryName = arr[0]["FactoryName"]
            model.AddRadix = int(arr[0]["AddRadix"]*10)
        """

        return model

    def test(self):
        sql = 'select f.FactoryID,FactoryName,CartonWeight,AddRadix from factories f inner join basesetting bs on f.FactoryID= bs.FactoryID; ' 

        arr = self.helper.Select(sql)

        for item in arr:
            #print(item[0])
            pass


if __name__ == "__main__":

   
    obj = FactoryRepository(host="192.168.199.15", user="root", password="root", database="weight")
    
    model = obj.Select_Data()
   
    if model is None:
        print("is null")
    else:
        print(model.AddRadix)
        
    #print(model.AddRadix)
    #print(model[0]["AddRadix"])

    #obj.test()