from enum import Enum
from collections import defaultdict


class state_type(Enum):
    S = 1
    E = 2
    M = 3
    I = 4
    D = 5


class State():
    def __init__(self):
        # self.state_type = t
        self.adj_list = []
        self.id = 0
        self.type = None

    def add_transition(self, dest, prob):
        self.adj_list.append((dest,prob))

    def transit(self, dest):
        for d, prob in self.adj_list:
            if d == dest:
                return prob
        else:
            return 0

    def emit(self, aa):
        return 0

    def __str__(self):
        return str(self.type) + " " + str(self.id)


class Start(State):
    def __init__(self):
        super().__init__()
        self.type = state_type(1)


class Stop(State):

    def __init__(self):
        super().__init__()
        self.type = state_type(2)


    def transit(self, dest):
        return 0


class Match(State):
    def __init__(self, id):
        super().__init__()
        self.type = state_type(3)
        self.id = id
        self.not_aa = {'B', 'J', 'O', 'U', 'X', 'Z'}
        self.aa_dist = defaultdict(int)
        self.total = 0


    def add(self, aa: str):
        """
        Add an animo acid to the match state aa distribution
        :param aa:
        :return:
        """
        if len(aa) > 1 or aa in self.not_aa:
            raise KeyError(aa, " is not an amino acid")
        else:
            self.aa_dist[aa] += 1
            self.total += 1

    def emit(self, aa:str):
        """
        Compute the likelihood of emitting a particular amino acid
        :param aa:
        :return:
        """
        if len(aa) != 1 or aa in self.not_aa:
            raise KeyError(aa, " is not a amino acid")
        else:
            if aa in self.aa_dist:
                return (self.aa_dist[aa]/self.total)*0.99
            else:
                return 0.01/(20-len(self.aa_dist))


class Insert(State):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.type = state_type(4)

    def emit(self, aa:str):
        return 1


# class Delete(State):
#
#     def __init__(self):
#         super().__int__()
