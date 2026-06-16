# 🌐 semantic_RARe (OT-ViRaRe)

**Open Tools and Visitation Frameworks for Global Research Assessment Reform**

Welcome to the `semantic_RARe` repository. This project is part of the CODATA OT-ViRaRe initiative, focused on co-developing a new generation of open, FAIR-aligned, and visitation-enabled tools for responsible research assessment.

This repository houses an offline **Data Visitation Hybrid GraphRAG Pipeline**, designed specifically to ingest, map, and analyze complex Annual Reports from **Indian Agricultural and Plant-Science Institutions** (e.g., NIPGR, ICAR) using Semantic AI.

> 🧪 **Prototype & Interactive Demo:** > Want to see the foundational architecture in action? Check out our original interactive [Colab Notebook Prototype](https://colab.research.google.com/drive/1nktFH9fynRQxQHWj4eC37gut7ODrTGaI?usp=sharing).

---

## 🚀 Key Features & Architecture

Standard Retrieval-Augmented Generation (RAG) systems and commercial cloud LLMs struggle with dense institutional reports and fail to protect data sovereignty. This project solves that by upgrading to an asynchronous, local CLI architecture:

1. **Data Visitation Compliant:** Designed to run entirely on the researcher's local machine. No sensitive institutional files, PDFs, or financial data are ever uploaded to external cloud storage.
2. **Offline Asynchronous Ingestion:** Safely crawls massive 200+ page PDFs in the background, utilizing `pdfplumber` (with `layout=True`) to preserve the spatial integrity of complex financial ledgers, grant matrices, and faculty lists.
3. **Dynamic Agricultural Ontology:** Employs the Groq API (`llama-3.1-8b-instant`) to systematically extract domain-specific entities (Startups, Patents, Funding Agencies, Labs, Crop Varieties) into a traversable `NetworkX` Knowledge Graph.
4. **Hybrid Retrieval Engine:** Fuses dense semantic vector search (`ChromaDB`) with explicit multi-hop structural graph search to capture both narrative descriptions and hard relational facts.
5. **Anti-Hallucination Guardrails:** Features a strict "Two-Pass Verification" system. The AI generates an answer and then cross-examines its own response against the local graph to block unverified facts or hallucinated scientists.

---

## 📂 Repository Structure

```text
semantic_RARe/
├── README.md                           # Project documentation and architecture
├── requirements.txt                    # Python dependencies
├── main.py                             # Typer CLI Entry Point
├── notebooks/                
│   └── 01_Annual_Report_GraphRAG.ipynb # Original Colab Data Visitation prototype
├── data/                     
│   ├── raw/                            # Directory for raw PDFs (e.g., NIPGR_AR.pdf)
│   ├── extracted/                      # Pre-processed JSON Graphs & ChromaDB vectors
│   └── reports/                        # Exported Markdown assessment reports
├── src/                                
│   ├── ingestion/                      # PDF parsing and DB compilation (db_builder)
│   ├── graph/                          # LLM extractors and Anti-Hallucination Guardrails
│   └── retrieval/                      # Hybrid ChromaDB + Graph search engine
└── docs/                     
    └── architecture.md                 # Detailed documentation on Data Visitation

```

---

## ⚙️ Quick Start & Installation

### 1. Prerequisites
Ensure you have Python 3.9+ installed. You will also need an active [Groq API Key](https://console.groq.com/) for the local entity extraction and chat generation phases.

### 2. Installation
Clone the repository and install the required dependencies:

```bash
git clone https://github.com/semanticClimate/semantic_RARe.git
cd semantic_RARe
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt

```

### 3. Environment Setup

Set your API key as an environment variable in your terminal:

```bash
# On Mac/Linux:
export GROQ_API_KEY="your_api_key_here"

# On Windows (Command Prompt):
set GROQ_API_KEY=your_api_key_here

# On Windows (PowerShell):
$env:GROQ_API_KEY="your_api_key_here"

```

### 4. Prepare the Data

Because this tool relies on local data visitation, you must provide the PDF you want to assess.

* Place your target Annual Report PDF (e.g., `NIPGR_AR.pdf`) into the `data/raw/` directory before running the pipeline.

---

## 🛠️ Usage (CLI Commands)

The pipeline is entirely operated via a clean, terminal-based CLI built with `Typer` and formatted with `Rich`.

### 1. Ingest an Annual Report

Process a massive PDF asynchronously to build the local databases. This will safely extract relationships and build the Vector DB without hitting rate limits.

```bash
python main.py ingest data/raw/NIPGR_AR.pdf --name nipgr
```

### 2. Generate a Standardized Assessment Report

Automatically generate a standardized Markdown report comparing labs, funding agencies, patents, and incubated startups based on the ingested graph.

```bash
python main.py report nipgr
```

### 3. Interactive Assessment Chat

Launch the hallucination-safe terminal to query the Knowledge Graph and Vector DB directly.

```bash
python main.py chat nipgr
```

---

## 🤝 Contributing & Roadmap

This repository is in active development, fulfilling the 2025-2026 ORAT (Open Research Assessment Toolkit) roadmap. Immediate upcoming items include:

* **Neo4j AuraDB Migration:** Transitioning from in-memory `NetworkX` to Neo4j for native Cypher querying and visual exploration.
* **Streamlit UI Development:** Wrapping the CLI into a lightweight, local web interface for non-technical stakeholders.
* **Broader Institute Benchmarking:** Stress-testing the Agricultural Ontology against additional institutes (e.g., ICAR, IARI).

For inquiries or contributions, please refer to the core OT-ViRaRe task group guidelines.