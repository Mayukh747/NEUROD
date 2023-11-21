from enum import Enum

class state_type(Enum):
    Start = 1
    Stop = 2
    Match = 3
    Insert = 4
    Delete = 5

class State():
    def __int__(self, t):
        self.state_type = t
        self.edge_list = []

class pHMM():

    def read_alingment(self):
        '''
        need a function to parse the output of an msa alignment and start putting together the right amount of states
        :return:
        '''



