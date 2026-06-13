import os
import chromadb

def search_vectors(query: str, institute_name: str, top_k: int = 3) -> list[str]:
    """
    Queries the persistent ChromaDB vector store for semantic matches.
    """
    chroma_path = f"data/extracted/{institute_name}_chroma"
    
    if not os.path.exists(chroma_path):
        return ["Vector database not found for this institute."]
        
    try:
        chroma_client = chromadb.PersistentClient(path=chroma_path)
        collection = chroma_client.get_collection(name="annual_report")
        
        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        # Flatten the list of documents
        documents = results.get("documents", [[]])[0]
        return documents
    except Exception as e:
        return [f"Vector Search Error: {str(e)}"]