from States import Start, Stop, Match, Insert

class PHMM():

    def __init__(self):
        self.training_matrix = ""

        self.start = Start()
        self.stop = Stop()
        self.delete = []
        self.match = []
        self.insert = []



    def train(self, f_name: str):
        data = ""
        with open(f_name) as input:
            for line in input:
                if line[0] == ">":
                    data += ">"
                else:
                    data += line.strip("\n")
        self.training_matrix = data.split(">")[1:]

        # Calculate max sequence length
        max_length = len(max(self.training_matrix, key=len))

        # Create Match States
        self.match = [Match(i) for i in range(max_length)]
        for i in range(len(self.match)-1):
            self.match[i].add_transition(self.match[i+1],0.99)
        self.match[-1].add_transition(self.stop,0.99)

        # The training matrix is complete
        for ch_idx in range(max_length):
            for s in self.training_matrix:
                self.match[ch_idx].add(s[ch_idx])

        #Create the Insert States
        self.insert = [Insert(i) for i in range(max_length + 1)]
        for i in range(len(self.insert)-1):
            self.insert[i].add_transition(self.match[i],0.99)
            self.insert[i].add_transition(self.insert[i], 0.01)
        self.insert[-1].add_transition(self.stop,0.99)
        self.insert[-1].add_transition(self.insert[i], 0.01)


        #Create the Delete States

        #Adjust Start Transitions
        self.start.add_transition(self.match[0], 0.99)
        self.start.add_transition(self.insert[0], 0.01)


    def viterbi(self, seq):

        def rowToState(r):
            if r == 0:
                return self.start
            elif r== len(self):
                return self.stop
            elif r < len(self.match) + 1:
                return self.match[r-1]
        def stateToRow(s):
            if s.type.name == "S":
                    return 0
            elif s.type.name == "M":
                    return s.id + 2
            elif s.type.name == "I":
                    return (s.id + 2 + len(self.match))
            elif s.type.name == "E":
                   return -1

        #Initialize v_mat
        v_mat = [[0 for _ in range(len(seq) + 2)] for _ in range(len(self)+1)]

        for idx, char in enumerate(seq):
            v_mat[0][idx+1] = char

        v_mat[1][0] = ("S", 0)
        v_mat[-1][0] = ("E", 0)
        row_idx = 2
        for mi, m in enumerate(self.match):
            v_mat[row_idx][0] = ("M", mi)
            row_idx += 1
        for ii, i in enumerate(self.insert):
            v_mat[row_idx][0] = ("I", ii)
            row_idx += 1



        #Row constants
        START = 0
        MATCH = 1
        INSERT = 1 + len(self.match)
        DELETE = INSERT + len(self.insert)
        END = -1

        #Adjust for start state
        for d, p in self.start.adj_list:
            idx = d.id + 1
            if d.type.name == 'M':
                idx += MATCH
            elif d.type.name == 'I':
                idx += INSERT
            elif d.type.name == 'D':
                idx += DELETE

            v_mat[idx][1] = p * d.emit(seq[0])

        #For each column
        for col_idx in range(1, len(seq)):
            # fill in each row
            for row_idx in range(1,len(self)-1):
                if v_mat[row_idx][col_idx] == 0:
                    continue
                source_node = None
                source_type, source_id = v_mat[row_idx][0]
                if source_type == 'M':
                    source_node = self.match[source_id]
                elif source_type == 'I':
                    source_node = self.insert[source_id]
                elif source_type == 'S':
                    source_node = self.start

                for dest, prob in source_node.adj_list:
                    new_prob = v_mat[row_idx][col_idx] * source_node.transit(dest) * dest.emit(seq[col_idx])
                    dest_row_idx = stateToRow(dest)
                    v_mat[dest_row_idx][col_idx+1] = max(new_prob,v_mat[dest_row_idx][col_idx+1])

        #adjust for stop state
        col_idx = len(seq) + 1
        for row_idx in range(1,len(self)):
            source_node = None
            source_type, source_id = v_mat[row_idx][0]
            if source_type == 'M':
                source_node = self.match[source_id]
            elif source_type == 'I':
                source_node = self.insert[source_id]
            elif source_type == 'S':
                source_node = self.start
            elif source_type == 'E':
                source_node = self.stop

            v_mat[row_idx][col_idx] = v_mat[row_idx][col_idx-1] * source_node.transit(self.stop)



        #print v_mat
        self.print_viterbi(seq, v_mat)
        return max([v_mat[r][-1] for r in range(len(v_mat))])

    def print_viterbi(self, seq, mat):
        for row in mat:
            for item in row:
                print("\t", item, end="")
            print()


    def __str__(self):
        s = ""
        s += str(self.start) + "\n\n"
        s += str(self.stop) + "\n\n"
        for m in self.match:
            s += str(m) + "\n\n"
        return s

    def __len__(self):
        return 2 + len(self.match) + len(self.delete) + len(self.insert)

if __name__ == "__main__":
    m = PHMM()
    m.train("scratchpad.txt")
    print(m.viterbi("KLM"))
    #print(m)
