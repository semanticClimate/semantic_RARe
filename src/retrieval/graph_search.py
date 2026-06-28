import os
import json
import glob
import networkx as nx

def load_all_historical_graphs(institute_name: str) -> nx.DiGraph:
    """
    Scans data/extracted/ and compiles all available historical years 
    for the institute into a single consolidated NetworkX Graph.
    """
    extracted_dir = "data/extracted"
    search_pattern = os.path.join(extracted_dir, f"{institute_name}_*_graph.json")
    graph_files = glob.glob(search_pattern)
    
    if not graph_files:
        raise FileNotFoundError(f"No historical graphs found for institute: {institute_name}")
        
    Composite_KG = nx.DiGraph()
    
    for file_path in graph_files:
        # Extract the year from filename (e.g., nipgr_2024_graph.json)
        filename = os.path.basename(file_path)
        year = filename.split("_")[1]
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for rel in data:
            source = rel.get("source", "").strip()
            target = rel.get("target", "").strip()
            relation = rel.get("relation", "RELATED_TO").strip().upper()
            
            if source and target:
                # Add year suffix or attribute to the relation to track timeline shifts
                labeled_relation = f"{relation} (FY_{year})"
                Composite_KG.add_edge(source, target, label=labeled_relation)
                
    return Composite_KG

def search_graph(query: str, KG: nx.DiGraph, max_facts: int = 40) -> list[str]:
    """
    Advanced Tokenized Search: Finds nodes matching query keywords 
    and returns their 1-hop neighborhood.
    """
    query_lower = query.lower()
    
    # Minimal, standard stopwords (Removed "funding", "agency", "science", etc.)
    stopwords = {"who", "is", "what", "which", "mention", "any", "one", "the", "a", "an", "of", "in", "for", "to", "and", "are", "list", "all"}
    
    query_tokens = [t.strip(",?.()") for t in query_lower.split() if t not in stopwords and len(t) > 2]
    
    matched_nodes = set()
    relevant_facts = []
    
    # Phase 1: Match Nodes
    for node in KG.nodes():
        node_lower = node.lower()
        if node_lower in query_lower or any(token in node_lower for token in query_tokens):
            matched_nodes.add(node)
            
    # Phase 2: Pull Connected Edges
    for u, v, data in KG.edges(data=True):
        relation = data.get('label', 'RELATED_TO').lower()
        if u in matched_nodes or v in matched_nodes or any(token in relation for token in query_tokens):
            relevant_facts.append(f"• {u} [{data.get('label')}] {v}")
            
    return list(set(relevant_facts))[:max_facts]

# import os
# import json
# import networkx as nx

# def load_graph(institute_name: str) -> nx.DiGraph:
#     """Loads the pre-processed JSON into a NetworkX Directed Graph."""
#     json_path = f"data/extracted/{institute_name}_graph.json"
    
#     if not os.path.exists(json_path):
#         raise FileNotFoundError(f"Knowledge Graph not found at {json_path}")
        
#     with open(json_path, 'r', encoding='utf-8') as f:
#         data = json.load(f)
        
#     KG = nx.DiGraph()
#     for rel in data:
#         source = rel.get("source", "").strip()
#         target = rel.get("target", "").strip()
#         relation = rel.get("relation", "RELATED_TO").strip().upper()
#         if source and target:
#             KG.add_edge(source, target, label=relation)
            
#     return KG

# def search_graph(query: str, KG: nx.DiGraph, max_facts: int = 40) -> list[str]:
#     """
#     Advanced Tokenized Search: Finds nodes matching query keywords 
#     and returns their 1-hop neighborhood.
#     """
#     query_lower = query.lower()
    
#     # Minimal, standard stopwords (Removed "funding", "agency", "science", etc.)
#     stopwords = {"who", "is", "what", "which", "mention", "any", "one", "the", "a", "an", "of", "in", "for", "to", "and", "are", "list", "all"}
    
#     query_tokens = [t.strip(",?.()") for t in query_lower.split() if t not in stopwords and len(t) > 2]
    
#     matched_nodes = set()
#     relevant_facts = []
    
#     # Phase 1: Match Nodes
#     for node in KG.nodes():
#         node_lower = node.lower()
#         if node_lower in query_lower or any(token in node_lower for token in query_tokens):
#             matched_nodes.add(node)
            
#     # Phase 2: Pull Connected Edges
#     for u, v, data in KG.edges(data=True):
#         relation = data.get('label', 'RELATED_TO').lower()
#         if u in matched_nodes or v in matched_nodes or any(token in relation for token in query_tokens):
#             relevant_facts.append(f"• {u} [{data.get('label')}] {v}")
            
#     return list(set(relevant_facts))[:max_facts]

# # def search_graph(query: str, KG: nx.DiGraph, max_facts: int = 40) -> list[str]:
# #     """
# #     Advanced Tokenized Search: Finds nodes matching query keywords 
# #     and returns their 1-hop neighborhood.
# #     """
# #     query_lower = query.lower()
# #     stopwords = {"who", "is", "which", "specific", "funding", "agency", "provided", "a", "grant", "to", "the", "researcher", "studying", "from", "in", "report", "for", "being", "newly", "elected", "as", "fellows", "major", "national", "science", "academies", "such", "or", "their", "contributions", "and", "with", "develop", "by", "what", "are", "list", "all"}
    
# #     query_tokens = [t.strip(",?.()") for t in query_lower.split() if t not in stopwords and len(t) > 2]
    
# #     matched_nodes = set()
# #     relevant_facts = []
    
# #     # Phase 1: Match Nodes
# #     for node in KG.nodes():
# #         node_lower = node.lower()
# #         if node_lower in query_lower or any(token in node_lower for token in query_tokens):
# #             matched_nodes.add(node)
            
# #     # Phase 2: Pull Connected Edges
# #     for u, v, data in KG.edges(data=True):
# #         relation = data.get('label', 'RELATED_TO').lower()
# #         if u in matched_nodes or v in matched_nodes or any(token in relation for token in query_tokens):
# #             relevant_facts.append(f"• {u} [{data.get('label')}] {v}")
            
# #     return list(set(relevant_facts))[:max_facts]