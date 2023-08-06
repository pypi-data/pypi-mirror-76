#coding:utf-8

import sys
sys.path.append('./')

from common.view.qrcodeview import QRCodeView
from common.data.qrcodemodel import QRCodeModel

class QRCodeViewData:
    def __init__(self, model):
        self.view = QRCodeView()

        self.view.QRcodeID = model.QRcodeID
        self.view.FactoryID = model.FactoryID
        self.view.FarmID = model.FarmID
        self.view.FarmName = model.FarmName
        self.view.ReceiveID = model.ReceiveID

  

    def getView(self):
        return self.view

    