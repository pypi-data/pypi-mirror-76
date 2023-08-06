# codeing:utf-8

class ShipMentListModel:
    def __init__(self,id='',message_id='',shipment_id='', weight_type=0, factory_id=0, farm_id=0, qrcode_id='', specification_id=0, carton_weight=0, real_weight=0, gross_weight=0, weight_code=0, standard_weight=0, unit_price=0, update_time=''):
        self.id = id
        self.message_id = message_id
        self.shipment_id = shipment_id
        self.factory_id = factory_id
        self.weight_type = weight_type
        self.farm_id = farm_id
        self.qrcode_id = qrcode_id
        self.specification_id = specification_id
        self.carton_weight = carton_weight
        self.real_weight = real_weight
        self.gross_weight = gross_weight
        self.weight_code = weight_code
        self.standard_weight = standard_weight
        self.unit_price = unit_price
        self.update_time = update_time

    def setid(self, id):
        self.id = id

    def setshipment_id(self, shipment_id):
        self.shipment_id = shipment_id

    def setweight_type(self, weight_type):
        self.weight_type = weight_type

    def setfactory_id(self, factory_id):
        self.factory_id = factory_id

    def setfarm_id(self, farm_id):
        self.farm_id = farm_id
    
    def setqrcode_id(self, qrcode_id):
        self.qrcode_id = qrcode_id

    def setspecification_id(self, specification_id):
        self.specification_id = specification_id

    def setcarton_weight(self, carton_weight):
        self.carton_weight = carton_weight

    def setreal_weight(self, real_weight):
        self.real_weight = real_weight

    def setgross_weight(self, gross_weight):
        self.gross_weight = gross_weight
    
    def setweight_code(self, weight_code):
        self.weight_code = weight_code
    
    def setstandard_weight(self, standard_weight):
        self.standard_weight = standard_weight

    def setunit_price(self, unit_price):
        self.unit_price = unit_price

    def setupdate_time(self, update_time):
        self.update_time = update_time

