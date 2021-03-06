'''
Created on Sep 24, 2013

@author: Silver
'''

import logging

class Order:
    def __init__(self):
        self.size  = 0
        self.price = 0
        self.symbol = ""
        self.leaves = 0
        self.timeinforce = "day"
        self.id = ""
        self.executed = 0
        self.side = 0
        self.shown = 0
        self.decay = 1
        self.parent = ""
        
    def __str__(self):
        side = "U"
        if self.side == 1:  side = "Buy"
        if self.side == -1: side = "Sell" 
        return "%s :: %s (%d / %d @ %f | %s) - %s" % (self.id, side, self.leaves, self.size, self.price, self.symbol, self.timeinforce)
        
class ExecutionReport():
    def __init__(self):
        self.size = 0
        self.price = 0
        self.symbol = ""
        self.leaves = self.size
        self.id = ""
        self.parent = ""      
    
    def __str__(self):
        return "Exec %s :: (%d @ %f | %s)" % (self.id, self.size, self.price, self.symbol)
        
class OrderDispatcher():
    def __init__(self, service_locator):
        self.services = service_locator
        
    def new_order(self, order):
        if order.size     == 0 : logging.warning("Order [%s]: size equals zero, unable to send order!" % order); return
        if order.id       == "": logging.warning("Order [%s]: has no id, unable to send order!" % order); return
        if order.symbol   == "": logging.warning("Order [%s]: has no symbol, unable to send order!" % order); return 
        order.leaves = order.size
        
        logging.debug("Inserting Order [%s]" % order)
        self.services.bus.insert_new_order(order)
        self.services.events["ValidNewOrder"].emit(order.id)
    
    