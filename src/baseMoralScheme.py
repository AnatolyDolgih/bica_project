import numpy as np

class BaseMoralScheme():
    def __init__(self, init_state):
        print(f"moral scheme ctor")
        self.cur_state = init_state
    
    def update_state(self, cur_impact):
        self.cur_state += cur_impact