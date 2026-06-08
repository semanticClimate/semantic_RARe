# Colab Notebook link : https://colab.research.google.com/drive/1nktFH9fynRQxQHWj4eC37gut7ODrTGaI?usp=sharing
# 🌐 semantic_RARe (OT-ViRaRe)

**Open Tools and Visitation Frameworks for Global Research Assessment Reform**

Welcome to the `semantic_RARe` repository. This project is part of the CODATA OT-ViRaRe initiative, focused on co-developing a new generation of open, FAIR-aligned, and visitation-enabled tools for responsible research assessment.

This repository houses the **Data Visitation GraphRAG Pipeline**, designed specifically to ingest, map, and analyze complex Annual Reports from Indian Research Institutions using Semantic AI and Knowledge Graphs.

---

## 🚀 Key Features & Architecture

Standard Retrieval-Augmented Generation (RAG) systems struggle with dense institutional reports due to hierarchical structures and financial tables. This project solves that by upgrading to a **GraphRAG** architecture:

1. **Data Visitation Compliant:** Designed to run entirely within local memory (e.g., local Jupyter/Colab runtimes). No sensitive institutional files or financial data are ever uploaded to external cloud storage. 
2. **Spatial PDF & Table Parsing:** Utilizes `pdfplumber` to extract text page-by-page while preserving the physical layout. This prevents financial ledgers, grant matrices, and faculty lists from being corrupted during text extraction.
3. **Semantic Knowledge Graphs:** Employs the Groq LLM to automatically extract factual nodes (Researchers, Departments, Grants) and edges (Relationships) from the unstructured text, building a traversable graph in `NetworkX`.
4. **Hybrid Retrieval Engine:** Combines dense vector search (`ChromaDB`) with explicit structural graph search to power an AI Assessment Assistant capable of multi-hop reasoning with zero hallucination.

---

## 📂 Repository Structure

```text
semantic_RARe/
├── README.md                           # Project documentation and architecture
├── requirements.txt                    # Python dependencies
├── notebooks/                
│   └── 01_Annual_Report_GraphRAG.ipynb # Core Data Visitation & GraphRAG pipeline
├── data/                     
│   ├── raw/                            # Directory for raw PDFs (e.g., IITD_AR.pdf)
│   └── extracted/                      # Directory for exported JSON Knowledge Graphs
├── src/                                # Modularized Python scripts (WIP)
│   ├── ingestion/                      # PDF and table parsing logic
│   ├── graph/                          # NetworkX construction and traversal
│   └── retrieval/                      # Hybrid ChromaDB + Graph search engine
└── docs/                     
    └── architecture.md                 # Detailed documentation on Data Visitation

```

---

## ⚙️ Quick Start

### 1. Prerequisites

Ensure you have Python 3.9+ installed. You will also need an active [Groq API Key](https://console.groq.com/) for the LLM extraction phase.

### 2. Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/semanticClimate/semantic_RARe.git
cd semantic_RARe
pip install -r requirements.txt

```


### 3. Running the Pipeline

Navigate to the `notebooks/` directory and open `01_Annual_Report_GraphRAG.ipynb` in Jupyter Notebook or Google Colab.

The notebook will guide you through:

1. Entering your Groq API Key securely.
2. Uploading an Institutional Annual Report PDF.
3. Building the Vector DB and Knowledge Graph.
4. Launching the interactive Assessment Assistant console.

---

## 🧠 How the Hybrid Retriever Works

When a user submits an assessment query (e.g., *"Which departments report to the Professorial Committee?"*):

1. **Vector Search:** Converts the query to an embedding and retrieves the Top-K most semantically relevant pages from ChromaDB.
2. **Graph Search:** Scans the NetworkX Knowledge Graph for entities mentioned in the query and pulls their exact deterministic relationships.
3. **Synthesis:** The prompt bundles the structured graph facts and unstructured document extracts together, forcing the LLM to ground its answer entirely in verified institutional data.

---

## 🤝 Contributing

This repository is in active development. Immediate roadmap items include:

* Modularizing the Colab notebook code into distinct Python packages within the `src/` directory.
* Implementing specialized Optical Structure Recognition (OSR) for deeper table parsing.
* Developing a lightweight Streamlit UI for non-technical stakeholders.

For inquiries or contributions, please refer to the core OT-ViRaRe task group guidelines.
