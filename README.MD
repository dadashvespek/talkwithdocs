# PDF Processing and Query API
## Endpoints

1. **PDF Processing Endpoint**
   - **POST**: `/pdf-endpoint`
   - Parses, chunks, and vectorizes a PDF document.
   - Usage: 
     ```bash
     curl -X POST "https://<your-domain>/pdf-endpoint" -H "content-type: application/json" -H "API-Key: KEY" -d "{\"url\":\"<pdf-url>\"}"
     ```

2. **Query Endpoint**
   - **GET**: `/get-relevant-chunks`
   - Retrieves relevant text chunks based on a provided query.
   - Usage: 
     ```bash
     curl -X GET "https://<your-domain>/get-relevant-chunks?uid=<document-uid>&query=<query-text>" -H "content-type: application/json" -H "API-Key: KEY"
     ```