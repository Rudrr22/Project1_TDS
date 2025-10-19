import os
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity

# Initialize Flask app and CORS
app = Flask(__name__)
CORS(app, resources={r"/similarity": {"origins": "*"}}, methods=["OPTIONS", "POST"])

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_embeddings_batched(texts, model="text-embedding-3-small"):
    """Generates embeddings for a list of texts in a single batch call."""
    # OpenAI API expects a list of strings
    texts = [text.replace("\n", " ") for text in texts]
    response = client.embeddings.create(input=texts, model=model)
    # The response contains a list of embedding objects. We extract the embedding vector from each.
    return [item.embedding for item in response.data]

@app.route('/similarity', methods=['POST'])
def calculate_similarity():
    """
    API endpoint to calculate cosine similarity between a query and a list of documents.
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    docs = data.get('docs')
    query = data.get('query')

    if not docs or not query or not isinstance(docs, list):
        return jsonify({"error": "Missing or invalid 'docs' or 'query' field"}), 400

    try:
        # 1. Combine query and docs for a single API call
        all_texts = [query] + docs

        # 2. Generate embeddings in one batch
        all_embeddings = get_embeddings_batched(all_texts)

        # 3. Separate the query embedding from the document embeddings
        query_embedding = np.array(all_embeddings[0]).reshape(1, -1)
        doc_embeddings = all_embeddings[1:]

        # 4. Compute cosine similarity
        similarities = cosine_similarity(query_embedding, doc_embeddings)[0]

        # 5. Rank documents
        ranked_docs = sorted(zip(docs, similarities), key=lambda item: item[1], reverse=True)

        # 6. Prepare the response
        top_3_matches = [doc for doc, score in ranked_docs[:3]]

        return jsonify({"matches": top_3_matches})

    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
