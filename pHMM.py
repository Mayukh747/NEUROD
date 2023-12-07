from enum import Enum
from collections import defaultdict

class state_type(Enum):
    Start = 1
    Stop = 2
    Match = 3
    Insert = 4
    Delete = 5

class State():
    def __int__(self):
        # self.state_type = t
        self.adj_list = []

class Start(State):
    def __init__(self):
        super().__init__()

class Stop(State):

    def __init__(self):
        super().__init__()

class Match(State):
    def __init__(self):
        super().__init__()
        self.not_aa = {'B', 'J', 'O', 'U', 'X', 'Z'}
        self.aa_dist = defaultdict(int)


    def add(self, aa: str):
        if len(aa) > 1 or aa in self.not_aa:
            raise KeyError(aa, " is not an amino acid")
        else:
            self.aa_dist[aa] += 1

class Insert(State):
    def __init__(self):
        super().__int__()


class Delete(State):

    def __init__(self):
        super().__int__()


class PHMM():

    def __init__(self):
        self.training_matrix = ""

        self.start = Start()
        self.stop = Stop()
        self.delete = []
        self.match = []
        self.inserts = []

    '''
    '''
    def train(self, f_name: str):
        data = ""
        with open(f_name) as input:
            for line in input:
                if line[0] == ">":
                    data += ">"
                else:
                    data += line.strip("\n")
        self.training_matrix = data.split(">")[1:]

        #Calculate max sequence length
        max_length = len(max(self.training_matrix, key=len))

        #Create Match States
        self.match = [Match() for _ in range(max_length)]

        # The training matrix is complete
        for ch_idx in range(max_length):
            for s in self.training_matrix:
                self.match[ch_idx].add(s[ch_idx])






if __name__ == "__main__":
    m = PHMM()
    m.train("PrimateProtein/primate_training.fa")
    print("fuck this")



