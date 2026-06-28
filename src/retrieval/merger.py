from src.retrieval.vector_search import search_vectors
from src.retrieval.graph_search import load_all_historical_graphs, search_graph

def get_hybrid_context(query: str, institute_name: str) -> str:
    """
    Executes both Vector and Graph searches and merges them into a Master Context.
    """
    # 1. Get Graph Facts
    try:
        KG = load_all_historical_graphs(institute_name)
        graph_facts = search_graph(query, KG)
    except Exception as e:
        graph_facts = [f"Graph Error: {str(e)}"]
        
    # 2. Get Vector Text
    vector_texts = search_vectors(query, institute_name)
    
    # 3. Merge Output
    master_context = "=== EXACT GRAPH FACTS ===\n"
    if graph_facts:
        master_context += "\n".join(graph_facts)
    else:
        master_context += "No direct relational facts found."
        
    master_context += "\n\n=== SEMANTIC DOCUMENT TEXT ===\n"
    if vector_texts:
        for i, text in enumerate(vector_texts):
            master_context += f"[Excerpt {i+1}]: {text.strip()}\n\n"
    else:
        master_context += "No relevant semantic text found."
        
    return master_context