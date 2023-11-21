#Can we begin by seeing how the HMM library works?

import numpy as np
from hmmlearn import hmm

def train_hmm(sequences, n_states, n_symbols, n_iterations=100):
    model = hmm.MultinomialHMM(n_components=n_states, n_iter=n_iterations)
    flat_sequences = np.concatenate(sequences)
    lengths = [len(seq) for seq in sequences]
    reshaped_sequences = np.split(flat_sequences, np.cumsum(lengths)[:-1])
    model.fit(reshaped_sequences, lengths=lengths)

    return model

def calculate_viterbi_score(model, sequence):
    reshaped_sequence = np.array(sequence).reshape(1, -1)
    _, state_sequence = model.decode(reshaped_sequence)

    return state_sequence


training_sequences = [[0, 1, 0, 1, 1, 0], [1, 0, 1, 0, 1, 1]]
test_sequence = [0, 1, 0, 0, 1, 1]

num_states = 2
num_symbols = 2


hmm_model = train_hmm(training_sequences, num_states, num_symbols)
viterbi_scores = calculate_viterbi_score(hmm_model, test_sequence)
print("Viterbi Scores for Test Sequence:", viterbi_scores)
