# codeing:utf-8

class ShipMentModel:
    def __init__(self,shipment_id='',message_id='', factory_id=0, shipment_amount=0, shipment_sum=0, customer_id=0, shipment_truck='', truck_driver_name='', truck_driver_mobile=''):
        self.shipment_id = shipment_id
        self.message_id = message_id
        self.factory_id = factory_id
        self.shipment_amount = shipment_amount
        self.shipment_sum = shipment_sum
        self.customer_id = customer_id
        self.shipment_truck = shipment_truck
        self.truck_driver_name = truck_driver_name
        self.truck_driver_mobile = truck_driver_mobile

    def setshipment_id(self, shipment_id):
        self.shipment_id = shipment_id

    def setfactory_id(self, factory_id):
        self.factory_id = factory_id

    def setshipment_amount(self, shipment_amount=0):
        self.shipment_amount = shipment_amount

    def setshipment_sum(self, shipment_sum=0):
        self.shipment_sum = shipment_sum        

    def setcustomer_id(self, customer_id=0):
        self.customer_id = customer_id

    def setshipment_truck(self, shipment_truck=''):
        self.shipment_truck = shipment_truck

    def settruck_driver_name(self, truck_driver_name=''):
        self.truck_driver_name = truck_driver_name

    def settruck_driver_mobile(self, truck_driver_mobile):
        self.truck_driver_mobile = truck_driver_mobile

