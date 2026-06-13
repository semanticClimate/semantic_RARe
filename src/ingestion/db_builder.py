import os
import json
import time
import chromadb
from groq import Groq
from src.ingestion.parser import parse_pdf_by_page
from src.graph.extractor import extract_relationships_from_page
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

def build_databases(pdf_path: str, institute_name: str, api_key: str):
    """
    Orchestrates the entire offline ingestion pipeline.
    Builds both the JSON Knowledge Graph and the persistent ChromaDB Vector Store.
    """
    client = Groq(api_key=api_key)
    
    # 1. Setup persistent paths
    extracted_dir = "data/extracted"
    os.makedirs(extracted_dir, exist_ok=True)
    
    json_path = os.path.join(extracted_dir, f"{institute_name}_graph.json")
    chroma_path = os.path.join(extracted_dir, f"{institute_name}_chroma")
    
    # 2. Parse PDF
    pages = parse_pdf_by_page(pdf_path)
    all_relationships = []
    
    # Initialize Persistent ChromaDB
    chroma_client = chromadb.PersistentClient(path=chroma_path)
    # Get or create collection. Using default sentence-transformers model.
    collection = chroma_client.get_or_create_collection(name="annual_report")

    # 3. Batch Process with Rich Progress Bar
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
    ) as progress:
        
        task = progress.add_task("[cyan]Extracting Knowledge Graph & Vectors...", total=len(pages))
        
        for i, page_text in enumerate(pages):
            # Extract Graph Relationships
            rels = extract_relationships_from_page(page_text, client)
            if rels:
                all_relationships.extend(rels)
                
            # Embed into ChromaDB Vector Store
            doc_id = f"page_{i+1}"
            collection.add(
                documents=[page_text],
                ids=[doc_id]
            )
            
            # Anti-Rate-Limit Pause (Adjust based on your Groq Tier)
            time.sleep(2.5)
            progress.advance(task)

    # 4. Save Final Graph to Disk
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_relationships, f, indent=2)
        
    return json_path, chroma_path, len(all_relationships)