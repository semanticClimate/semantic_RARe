import os
import networkx as nx
from src.retrieval.graph_search import load_all_historical_graphs

def export_to_graphml(institute_name: str) -> str:
    """
    Loads all available historical graphs and exports the consolidated composite network
    as a Cytoscape-compatible .graphml file tracking chronological shifts.
    """
    # 1. Load the composite graph across all available financial years
    Composite_KG = load_all_historical_graphs(institute_name)
    
    # 2. Setup export directory
    export_dir = "data/exports"
    os.makedirs(export_dir, exist_ok=True)
    output_path = os.path.join(export_dir, f"{institute_name}_historical_network.graphml")
    
    # 3. Export to GraphML (NetworkX embeds the node attributes and edge temporal labels)
    nx.write_graphml(Composite_KG, output_path)
    
    return output_path

# import os
# import networkx as nx
# from src.retrieval.graph_search import load_graph

# def export_to_graphml(institute_name: str) -> str:
#     """
#     Loads the local NetworkX graph and exports it as a Cytoscape-compatible .graphml file.
#     """
#     # 1. Load the existing graph using our Phase 3 retrieval loader
#     KG = load_graph(institute_name)
    
#     # 2. Setup export directory
#     export_dir = "data/exports"
#     os.makedirs(export_dir, exist_ok=True)
#     output_path = os.path.join(export_dir, f"{institute_name}_network.graphml")
    
#     # 3. Export to GraphML (NetworkX automatically packages node strings and edge labels)
#     nx.write_graphml(KG, output_path)
    
#     return output_path