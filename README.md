# Semantic Search API

This project provides a simple Flask-based API for semantic search. It uses OpenAI's `text-embedding-3-small` model to generate text embeddings and calculates cosine similarity to find the most relevant documents for a given query.

## Prerequisites
- Python 3.8+
- An OpenAI API Key

## Setup and Installation

1.  **Clone the repository or download the source code.**
    Create a directory for the project and place `main.py`, `test_api.py`, and `requirements.txt` inside it.

2.  **Create and activate a virtual environment.**
    Open a terminal in your project directory and run the following commands:

    ```bash
    # Create the virtual environment
    python3 -m venv venv

    # Activate the environment
    # On macOS and Linux:
    source venv/bin/activate
    # On Windows:
    .\venv\Scripts\activate
    ```

3.  **Install the required dependencies.**
    With your virtual environment active, install the packages from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set your OpenAI API Key.**
    The application requires your OpenAI API key to be set as an environment variable.

    - **On macOS and Linux:**
      ```bash
      export OPENAI_API_KEY="your-openai-api-key-goes-here"
      ```
    - **On Windows (Command Prompt):**
      ```bash
      set OPENAI_API_KEY="your-openai-api-key-goes-here"
      ```
    - **On Windows (PowerShell):**
      ```bash
      $env:OPENAI_API_KEY="your-openai-api-key-goes-here"
      ```
    Replace `"your-openai-api-key-goes-here"` with your actual API key.

## Running the Application

This application uses the `waitress` WSGI server, which is cross-platform and works on Windows, macOS, and Linux.

1.  **Start the server:**
    From your project directory (with the virtual environment activated and the API key set), run the following command. Using `python -m waitress` is the most reliable method and works on all operating systems.
    ```bash
    python -m waitress --host 127.0.0.1 --port=8000 main:app
    ```

2.  **Verify the server is running.**
    You should see output in your terminal indicating that the server is listening on `http://127.0.0.1:8000`.

## Using the API

You can send a `POST` request to the `/similarity` endpoint to get the top 3 matching documents for your query.

**Example with `curl`:**
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{
  "docs": [
    "The cat sat on the mat.",
    "The dog chased the ball.",
    "A feline enjoys resting on a rug."
  ],
  "query": "A cat is on a rug."
}' \
http://127.0.0.1:8000/similarity
```

**Expected Response:**
```json
{
  "matches": [
    "The cat sat on the mat.",
    "A feline enjoys resting on a rug.",
    "The dog chased the ball."
  ]
}
```

## Running the Tests (Optional)

You can run the provided unit tests to verify the application's logic.
```bash
python test_api.py
```
You should see the output: `API test passed successfully!`
