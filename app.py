from flask import Flask, request, jsonify
import chromadb
import uuid
import requests
from PyPDF2 import PdfReader
from io import BytesIO

from chunker import Chunker
app = Flask(__name__)
stored_entries = {}
chroma_client = chromadb.Client()
@app.route('/pdf-endpoint', methods=['POST'])
def pdf_endpoint():
    api_key = request.headers.get('API-Key')
    if api_key != 'KEY':
        return jsonify({"error": "Invalid API key"}), 401

    data = request.json
    pdf_url = data.get('url')
    if not pdf_url:
        return jsonify({"error": "No URL provided"}), 400

    if pdf_url in stored_entries:
        return jsonify({"error": "Duplicate entry"}), 409

    try:
        uid = str(uuid.uuid4())
        collection = chroma_client.create_collection(name=uid)
        
        response = requests.get(pdf_url)
        response.raise_for_status()

        reader = PdfReader(BytesIO(response.content))
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        chunked_text = Chunker(text, 40)
        lent = len(chunked_text)
        print(lent)
        
        collection.add(documents=chunked_text, metadatas=[{"type": "support"} for _ in range(0, lent)], ids=[str(i) for i in range(0, lent)])
        print(text)
        stored_entries[pdf_url] = uid
        return jsonify({"message": "PDF processed successfully", "uid": uid}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/get-relevant-chunks', methods=['GET'])
def get_relevant_chunks():
    api_key = request.headers.get('API-Key')
    if api_key != 'KEY':
        return jsonify({"error": "Invalid API key"}), 401
    query_text = request.args.get('query')
    uid = request.args.get('uid')
    if not query_text:
        return jsonify({"error": "No query provided"}), 400
    if not uid:
        return jsonify({"error": "No uid provided"}), 400

    try:
        chroma_client = chromadb.Client()
        collection_name = uid 
        collection = chroma_client.get_collection(name=collection_name)
        if not collection:
            return jsonify({"error": "Collection not found"}), 404

        results = collection.query(
            query_texts=[query_text],
            n_results=2
        )

        return jsonify({"results": results}), 200

    except Exception as e:
        return jsonify({"error2": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
