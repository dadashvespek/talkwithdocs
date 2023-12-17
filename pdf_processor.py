import requests
from PyPDF2 import PdfReader
from io import BytesIO

from chunker import Chunker


def process_pdf(url,collection,chroma_client,uid):
    


    response = requests.get(url)
    response.raise_for_status()

    reader = PdfReader(BytesIO(response.content))
    first_page = reader.pages[0]
    text = first_page.extract_text()
    chunked_text = Chunker(text, 40)
    lent = len(chunked_text)
    print(lent)
    
    collection.add(documents=chunked_text, metadatas=[{"type": "support"} for _ in range(0, lent)], ids=[str(i) for i in range(0, lent)])

    return text, uid
