import numpy as np
from hmmlearn import hmm

def train_hmm(sequences, n_states, n_symbols, n_iterations=100):
    model = hmm.MultinomialHMM(n_components=n_states, n_iter=n_iterations)

    # Flatten the sequences and convert them to a 2D array
    flat_sequences = np.concatenate(sequences)
    lengths = [len(seq) for seq in sequences]

    # Reshape the sequences to represent individual samples
    reshaped_sequences = np.split(flat_sequences, np.cumsum(lengths)[:-1])

    # Train the HMM model
    model.fit(reshaped_sequences, lengths=lengths)

    return model

def calculate_viterbi_score(model, sequence):
    # Reshape the sequence to represent a single sample
    reshaped_sequence = np.array(sequence).reshape(1, -1)

    # Use the Viterbi algorithm to calculate the most likely state sequence
    _, state_sequence = model.decode(reshaped_sequence)

    return state_sequence

# Example usage:
# Define training sequences and test sequence
training_sequences = [[0, 1, 0, 1, 1, 0], [1, 0, 1, 0, 1, 1]]
test_sequence = [0, 1, 0, 0, 1, 1]

# Define the number of states and symbols
num_states = 2
num_symbols = 2

# Train the HMM
hmm_model = train_hmm(training_sequences, num_states, num_symbols)

# Calculate Viterbi scores for the test sequence
viterbi_scores = calculate_viterbi_score(hmm_model, test_sequence)

print("Viterbi Scores for Test Sequence:", viterbi_scores)
