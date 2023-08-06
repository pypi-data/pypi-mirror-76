# codeing:utf-8

class CustomerModel:
    def __init__(self, customer_id=0,factory_id=0, customer_name='', customer_address=''):
        self.customer_id = customer_id
        self.factory_id = factory_id
        self.customer_name = customer_name
        self.customer_address = customer_address

    def setcustomer_id(self, customer_id=0):
        self.customer_id = customer_id        

    def setcustomer_name(self, customer_name=''):
        self.customer_name = customer_name

    def setcustomer_address(self, customer_address=''):
        self.customer_address = customer_address


