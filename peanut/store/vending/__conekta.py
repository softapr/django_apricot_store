'''
Created on 7 sep. 2019

@author: orishiku
'''
import conekta
from django.conf import settings

from peanut.store.vending.__base import CustomerBaseObject, PaymentMethodBaseObject, ShippingContactBaseObject

class Customer(CustomerBaseObject):
    '''
    classdocs
    '''

    def __init__(self, user, phone=None):
        '''
        Constructor
        '''
        CustomerBaseObject.__init__(self, user, phone)
        conekta.api_key = settings.CONEKTA_PRIVATE_KEY

        if self.customer.api_id is None:
            try:
                customer = conekta.Customer.create({
                    "name": self.customer.name,
                    "email": self.customer.email})
                self.customer.api_id = customer.id
                self.customer.save()

            except conekta.ConektaError as e:
                self.usable = False
                raise Exception(e)

        else:
            self.usable = False if self.conekta_customer is None else True

    @property
    def conekta_customer(self):
        try:
            customer = conekta.Customer.find(self.customer.api_id)
            return customer

        except Exception as e:
            self.usable = False
            raise Exception(e)

        return None

    def update_customer(self, data):
        '''
        Update most of the data from user instance.
        '''
        super(Customer, self).update_customer(data)
        conketa_data = {"name": self.customer.name,
                        "email": self.customer.email,
                        "phone": self.customer.phone}

        try:
            self.conekta_customer.update(conketa_data)

        except Exception as e:
            raise Exception(e)

    def delete_customer(self):
        super(Customer, self).delete_customer()
        try:
            if not self.method.is_default:
                self.conekta_customer.delete()

        except Exception as e:
            raise Exception(e)

    def add_payment_method(self, name, reference, exp_month, exp_year,
                           api_data=None, m_type=None):
        method = PaymentMethod(name, reference, exp_month, exp_year,
                               self.customer, api_data, m_type)
        
        super(Customer, self).add_payment_method(method)

    def set_default_payment_method(self, method):
        '''
        @todo: set default payment source in conekta
        '''
        super(Customer, self).set_default_payment_method(method)

    def add_shipping_address(self, phone, name, between_streets, address_data):
        contact = ShippingContact(phone, name, between_streets, address_data, self.customer)
        
        super(Customer, self).add_payment_method(contact)

    def set_default_shipping_address(self, contact):
        '''
        @todo: set default payment source in conekta
        '''
        super(Customer, self).set_default_shipping_address(contact)

class ShippingContact(ShippingContactBaseObject):
    '''
    classdocs
    '''
    
    def __init__(self, phone, name, between_streets, address_data, customer):
        '''
        Constructor
        '''
        ShippingContactBaseObject.__init__(self, phone, name, between_streets, address_data, customer)

        if self.created:
            try:
                customer = conekta.Customer.find(customer.api_id)
                address = customer.createShippingContact({
                    "receiver": address_data.name,
                    "phone": address_data.phone,
                    "between_streets": address_data.between_streets,
                    "address": {
                        "street1": address_data.street1,
                        "street2": address_data.street2,
                        "city": address_data.city,
                        "state": address_data.state,
                        "country": address_data.country,
                        "postal_code": address_data.postalcode,
                        "residential": address_data.residential,
                    }})
                self.contact.api_id = address.id
                self.contact.save()
    
            except Exception as e:
                self.usable = False
                raise Exception(e)
        
    def conekta_contact(self, contact_id=None):
        try:
            customer = conekta.Customer.find(self.method.customer.api_id)
            contacts  = customer.shipping_address
            
            for address in contacts:
                if ((contact_id is None and address.id==self.method.api_id) or
                    (contact_id is not None and address.id==contact_id)):
                    return address

            self.usable = False

        except Exception as e:
            self.usable = False
            raise Exception(e)

        return None
    


    def update_shipping_contact(self, phone, name, between_streets, address_data):
        super(PaymentMethod, self).update_payment_method(phone, name, between_streets, address_data)

        try:
            self.conekta_contact().update({
                    "receiver": address_data.name,
                    "phone": address_data.phone,
                    "between_streets": address_data.between_streets,
                    "address": {
                        "street1": address_data.street1,
                        "street2": address_data.street2,
                        "city": address_data.city,
                        "state": address_data.state,
                        "country": address_data.country,
                        "postal_code": address_data.postalcode,
                        "residential": address_data.residential,
                    }})

        except Exception as e:
            raise Exception(e)

    def delete_shipping_contact(self):
        deleted, contact_api_id = super(ShippingContact, self).delete_shipping_contact()

        try:
            if deleted:
                self.conekta_contact(contact_api_id).delete()
            
        except Exception as e:
            raise Exception(e)
    
    def set_default(self):
        '''
        @todo: set default payment source in conekta
        '''
        super(ShippingContact, self).set_default()
        
class PaymentMethod(PaymentMethodBaseObject):
    '''
    classdocs
    '''

    def __init__(self, name, reference, exp_month, exp_year, customer,
                 api_data=None, m_type=None):
        '''
        Constructor
        '''
        PaymentMethodBaseObject.__init__(self, name, reference, exp_month,
                                         exp_year, customer, api_data, m_type)
        
        if self.created:
            try:
                customer = conekta.Customer.find(api_data["customer"])
                method = customer.createPaymentSource({
                    "type": self.method.type,
                    "token_id": api_data["token"]})
                self.method.api_id = method.id
                self.method.brand = method.brand
                self.method.save()
    
            except Exception as e:
                self.usable = False
                raise Exception(e)

    def conekta_method(self, method_id=None):
        try:
            customer = conekta.Customer.find(self.method.customer.api_id)
            methods  = customer.payment_sources
            
            for method in methods:
                if ((method_id is None and method.id==self.method.api_id) or
                    (method_id is not None and method.id==method_id)):
                    return method

            self.usable = False

        except Exception as e:
            self.usable = False
            raise Exception(e)

        return None

    def update_payment_method(self, name, exp_month, exp_year):
        super(PaymentMethod, self).update_payment_method(name,
                                                         exp_month,
                                                         exp_year)

        try:
            self.conekta_method().update({"name": self.method.name,
                                          "exp_month": self.method.exp_month,
                                          "exp_year": self.method.exp_year})

        except Exception as e:
            raise Exception(e)

    def delete_payment_method(self):
        deleted, method_api_id = super(PaymentMethod, self).delete_payment_method()

        try:
            if deleted:
                self.conekta_method(method_api_id).delete()
            
        except Exception as e:
            raise Exception(e)
    
    def set_default(self):
        '''
        @todo: set default payment source in conekta
        '''
        super(PaymentMethod, self).set_default()

    def add_billing_address(self, address):
        try:
            self.conekta_method().update({
                "address": {
                    "street1": address.street1,
                    "street2": address.street2,
                    "city": address.city,
                    "state": address.state,
                    "country": address.country,
                    "postal_code": address.postalcode}
                })
            super(PaymentMethod, self).add_billing_address(address)
            
        except Exception as e:
            raise Exception(e)
        
    def update_billing_address(self, address):
        
        try:
            self.conekta_method().update({
                "address": {
                    "street1": address.street1,
                    "street2": address.street2,
                    "city": address.city,
                    "state": address.state,
                    "country": address.country,
                    "postal_code": address.postalcode}
                })
            super(PaymentMethod, self).update_billing_address()
            
        except Exception as e:
            raise Exception(e)
