import json
import os
from unittest.mock import patch
import numpy as np

# A mock embedding function that returns predictable vectors for a batch of texts
def mock_get_embeddings_batched(texts, model="text-embedding-3-small"):
    """A mock of the get_embeddings_batched function for testing."""
    embeddings = []
    for text in texts:
        if "cat" in text or "feline" in text or "rug" in text:
            embeddings.append(np.array([1.0, 0.1, 0.1]).tolist())  # Vector for 'cat'
        elif "dog" in text or "ball" in text:
            embeddings.append(np.array([0.1, 1.0, 0.1]).tolist())  # Vector for 'dog'
        else:
            embeddings.append(np.array([0.1, 0.1, 1.0]).tolist())  # Generic vector
    return embeddings

# Use the patch decorator to replace the real function with our mock
@patch('main.get_embeddings_batched', side_effect=mock_get_embeddings_batched)
def test_similarity_endpoint(mock_embedding_func):
    """
    Tests the /similarity endpoint with a mocked batched embedding function.
    """
    from main import app
    client = app.test_client()

    payload = {
        "docs": [
            "The cat sat on the mat.",
            "The dog chased the ball.",
            "A feline enjoys resting on a rug."
        ],
        "query": "A cat is on a rug."
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = client.post('/similarity', headers=headers, data=json.dumps(payload))

    # Assertions
    assert response.status_code == 200
    response_json = json.loads(response.data)
    assert "matches" in response_json
    assert len(response_json["matches"]) == 3

    # With the new mock data, the query and all "cat" related docs have the same vector,
    # so they will have a similarity score of 1.0. The "dog" document will be less similar.
    # The order between the two cat documents might be stable, but let's check for presence.
    top_matches = response_json["matches"]
    assert "The cat sat on the mat." in top_matches
    assert "A feline enjoys resting on a rug." in top_matches
    # Ensure the least similar doc is last
    assert top_matches[2] == "The dog chased the ball."

    print("API test passed successfully!")

if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"] = "dummy_key_for_testing"
    test_similarity_endpoint()
