import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from gensim.models import KeyedVectors
from huggingface_hub import hf_hub_download

app = Flask(__name__)
CORS(app)

# Define the Hugging Face repository and model filename
repo_id = "fse/word2vec-google-news-300"
model_filename = "word2vec-google-news-300.model"
vectors_filename = "word2vec-google-news-300.model.vectors.npy"

# Define the local path where the model should be saved or checked
local_model_path = os.path.join("word2vec", model_filename)
local_vectors_path = os.path.join("word2vec", vectors_filename)

# Ensure the models directory exists
os.makedirs(os.path.dirname(local_model_path), exist_ok=True)
os.makedirs(os.path.dirname(local_vectors_path), exist_ok=True)

# Check if the model exists locally; if not, download it
if not os.path.exists(local_model_path):
    print("Model not found locally. Fetch from Hugging Face / check cache...")
    local_model_path = hf_hub_download(repo_id=repo_id, filename=model_filename)
    print(f"Model loaded from {local_model_path}")
else:
    print("Model found locally.")

if not os.path.exists(local_vectors_path):
    print("Vectors not found locally. Fetch from Hugging Face / check cache...")
    local_vectors_path = hf_hub_download(repo_id=repo_id, filename=vectors_filename)
    print(f"Vectors loaded from {local_vectors_path}")
else:
    print("Vectors found locally.")

# Load the Word2Vec model (requires both the model file and vector file, even though just loading local_model_path)
model = KeyedVectors.load(local_model_path)

@app.route('/calculate-position', methods=['POST'])
def calculate_position():
    data = request.json
    guess = data['guess']
    word1 = data['word1']
    word2 = data['word2']

    # Check if the words are in the model's vocabulary
    if guess not in model.key_to_index or word1 not in model.key_to_index or word2 not in model.key_to_index:
        return jsonify({'error': 'One or more words not found in model vocabulary.'}), 400

    # Calculate similarities
    sim1 = model.similarity(guess, word1)  # Similarity to word1 (e.g., 'tropical')
    sim2 = model.similarity(guess, word2)  # Similarity to word2 (e.g., 'canoe')

    # Corrected calculation to reflect the relative similarity between word1 and word2
    # Position scales between 0 (closer to word1) and 1 (closer to word2)
    normalized_position = sim2 / (sim1 + sim2)  # This places the position closer to the more similar word

    # Convert to a regular Python float before returning
    normalized_position = float(normalized_position)

    # Debugging output to verify calculations
    print(f"Similarity of '{guess}' to '{word1}': {sim1}")
    print(f"Similarity of '{guess}' to '{word2}': {sim2}")
    print(f"Calculated position for '{guess}': {normalized_position}")

    return jsonify({'position': normalized_position})

if __name__ == '__main__':
    app.run(debug=True)
