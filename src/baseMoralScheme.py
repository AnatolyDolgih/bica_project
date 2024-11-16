import numpy as np
from oai_interface import Interface

class BaseMoralScheme():
    def __init__(self):
        print(f"moral scheme ctor")
        self.interface = Interface()
        
    
    def update_state(self, cur_impact):
        self.cur_state += cur_impact