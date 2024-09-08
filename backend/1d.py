from gensim.models import KeyedVectors
from concurrent.futures import ThreadPoolExecutor
import re
import numpy as np
import matplotlib.pyplot as plt

# Load your pre-trained word vector model (e.g., Word2Vec, GloVe, FastText)
model_path = './word2vec-google-news-300.model'  # Replace with the correct model path
model = KeyedVectors.load(model_path)

def calculate_similarity(word, word1, word2, model):
    """Calculate the average similarity of a word to two target words with a penalty for imbalance."""
    similarity_to_word1 = model.similarity(word, word1)
    similarity_to_word2 = model.similarity(word, word2)
    balance_penalty = abs(similarity_to_word1 - similarity_to_word2)
    average_similarity = (similarity_to_word1 + similarity_to_word2) / 2 - balance_penalty
    return word, average_similarity, similarity_to_word1, similarity_to_word2, balance_penalty

def find_top_median_words(word1, word2, model, max_workers=10, top_n=10):
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(calculate_similarity, word, word1, word2, model) 
                   for word in model.index_to_key]

        for future in futures:
            word, avg_sim, sim1, sim2, penalty = future.result()
            # Exclude words with underscores and words too similar to the input words
            if not re.match(rf".*{re.escape(word1)}.*|.*{re.escape(word2)}.*", word, re.IGNORECASE) and "_" not in word:
                results.append((word, avg_sim, sim1, sim2, penalty))

    # Sort results by average similarity score in descending order
    results.sort(key=lambda x: x[1], reverse=True)

    # Print the top N results
    print(f"Top {top_n} semantic median words between '{word1}' and '{word2}':")
    for i, (word, avg_sim, sim1, sim2, penalty) in enumerate(results[:top_n]):
        print(f"{i+1}. '{word}' | Avg. Similarity: {avg_sim:.4f} | "
              f"Similarity to '{word1}': {sim1:.4f} | Similarity to '{word2}': {sim2:.4f} | "
              f"Balance Penalty: {penalty:.4f}")

    # Return the top result and all results
    return results[0], results if results else (("No suitable common word found.", -float('inf')), [])


def project_onto_line_1d(vectors, line_start, line_end):
    """Project vectors onto a 1D line defined by line_start and line_end."""
    line_vector = line_end - line_start
    line_vector /= np.linalg.norm(line_vector)  # Normalize the line vector

    # Project each vector onto the line and convert to scalar positions
    positions = np.dot(vectors - line_start, line_vector)
    return positions

def plot_words_1d(word1, word2, best_word, guess_word, model):
    # Extract vectors for the input words, best guess, and person's guess
    vectors = np.array([
        model[word1],
        model[word2],
        model[best_word],
        model[guess_word]
    ])

    # Project the vectors onto a 1D line between the input words
    positions = project_onto_line_1d(vectors, vectors[0], vectors[1])

    # Plot the words in 1D
    plt.figure(figsize=(12, 2))
    plt.scatter(positions, np.zeros_like(positions), c=['blue', 'green', 'red', 'orange'], s=100)

    # Annotate the points on the line
    plt.annotate(word1, (positions[0], 0), textcoords="offset points", xytext=(0, 10), ha='center')
    plt.annotate(word2, (positions[1], 0), textcoords="offset points", xytext=(0, 10), ha='center')
    plt.annotate(best_word, (positions[2], 0), textcoords="offset points", xytext=(0, 10), ha='center')
    plt.annotate(guess_word, (positions[3], 0), textcoords="offset points", xytext=(0, 10), ha='center')

    # Set plot details
    plt.title("1D Semantic Positions of Words")
    plt.xlabel("Semantic Distance")
    plt.yticks([])  # Hide y-axis
    plt.grid(True)
    plt.show()

# Example usage
word1 = "tropical"
word2 = "canoe"

# Find the best median word that balances between the two input words
best_word_info, top_results = find_top_median_words(word1, word2, model)
best_word = best_word_info[0]  # Extract the word itself from the top result

print(f"The best semantic median word between '{word1}' and '{word2}' is: '{best_word}'")

# Prompt the user for their guess
guess_word = input("Enter your guess for the word that fits between 'tropical' and 'canoe': ")

# Check if the guess is in the model's vocabulary
if guess_word not in model:
    print(f"The word '{guess_word}' is not in the model's vocabulary.")
else:
    # Plot the words including the real answer and the person's guess
    plot_words_1d(word1, word2, best_word, guess_word, model)
