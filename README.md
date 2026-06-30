# 🌐 semantic_RARe (OT-ViRaRe)

**Open Tools and Visitation Frameworks for Global Research Assessment Reform**

Welcome to the `semantic_RARe` repository. This project is part of the CODATA OT-ViRaRe initiative, focused on co-developing a new generation of open, FAIR-aligned, and visitation-enabled tools for responsible research assessment.

This repository houses an offline **Data Visitation Hybrid GraphRAG Pipeline**, designed specifically to ingest, map, and analyze complex Annual Reports from **Indian Agricultural and Plant-Science Institutions** (e.g., NIPGR, ICAR) using Semantic AI.

> 🧪 **Prototype & Interactive Demo:** Want to see the foundational architecture in action? Check out our original interactive [Colab Notebook Prototype](https://colab.research.google.com/drive/1nktFH9fynRQxQHWj4eC37gut7ODrTGaI?usp=sharing).

---

## 🚀 Key Features & Architecture

Standard Retrieval-Augmented Generation (RAG) systems and commercial cloud LLMs struggle with dense institutional reports and fail to protect data sovereignty. This project solves that by upgrading to an asynchronous, local CLI architecture:

1. **Data Visitation Compliant:** Designed to run entirely on the researcher's local machine. No sensitive institutional files, PDFs, or financial data are ever uploaded to external cloud storage.


2. **Offline Asynchronous Ingestion:** Safely crawls massive 200+ page PDFs in the background, utilizing `pdfplumber` (with `layout=True`) to preserve the spatial integrity of complex financial ledgers, grant matrices, and faculty lists.


3. **Dynamic Agricultural Ontology:** Employs the Groq API (`llama-3.1-8b-instant`) to systematically extract domain-specific entities (Startups, Patents, Funding Agencies, Labs, Crop Varieties) into a traversable `NetworkX` Knowledge Graph.


4. **Hybrid Retrieval Engine:** Fuses dense semantic vector search (`ChromaDB`) with explicit multi-hop structural graph search to capture both narrative descriptions and hard relational facts.


5. **Anti-Hallucination Guardrails:** Features a strict **Two-Pass Verification** system. The AI generates an initial response and then cross-examines it against the local graph structure (`nipgr_graph.json`) to block unverified claims or hallucinated personnel.


6. **Decadal Temporal Analytics:** Features metadata-driven multi-pass indexing to ingest and analyze up to 10 years of historical institutional reports simultaneously, tracking longitudinal trends across funding streams and technology pipelines.


7. **GraphML Cytoscape Interoperability:** Exports local graph data directly to open-standard `.graphml` files, allowing visual topological assessment across Force-Directed, Circular, and Hierarchical structural views.



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
│   ├── raw/                            # Directory for raw PDFs (e.g., NIPGR_2024.pdf)
│   ├── extracted/                      # Pre-processed JSON Graphs & ChromaDB vectors
│   ├── reports/                        # Exported Markdown assessment reports
│   └── exports/                        # Generated GraphML files for Cytoscape
├── src/                                
│   ├── ingestion/                      # PDF parsing and DB compilation (db_builder)
│   ├── graph/                          # LLM extractors, exporters, and guardrails
│   └── retrieval/                      # Hybrid search engine and temporal reporters
└── docs/                     
    └── architecture.md                 # Detailed documentation on Data Visitation

```

---

## ⚙️ Quick Start & Installation

### 1. Prerequisites

Ensure you have Python 3.9+ installed. You will also need an active [Groq API Key](https://console.groq.com/) for the local entity extraction and chat verification phases.

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

Because this tool complies strictly with data visitation principles, you must provide the PDF you want to assess locally.

* Place your target Annual Report PDFs (e.g., `NIPGR_2024.pdf`, `NIPGR_2025.pdf`) into the `data/raw/` directory before running the pipeline.

---

## 🛠️ Usage (CLI Reference Commands)

The pipeline is entirely operated via a clean, terminal-based CLI built with `Typer` and formatted with `Rich`.

### 1. Ingest Multi-Year Annual Reports

Process institutional PDFs page-by-page asynchronously. You **must** specify a short lowercase name for the target institute and the corresponding financial year to index data chronologically.

```bash
# Ingest Year 2024
python main.py ingest data/raw/NIPGR_2024.pdf --name nipgr --year 2024

# Ingest Year 2025
python main.py ingest data/raw/NIPGR_2025.pdf --name nipgr --year 2025

```

*(Note: Re-running ingestion for an existing name and year combination automatically performs a clean-slate wipe on that specific metadata shard to prevent database corruption.)*

### 2. Compile a 10-Year Temporal Assessment Report

Execute cross-year trend queries to scan all multi-year shards in a single pass. This automatically generates a standardized markdown analysis tracking funding flows, incubator growth, and patent pipeline evolutions over time.

```bash
python main.py temporal_report nipgr

```

* **Output Artifact:** `data/reports/nipgr_10year_trend_analysis.md`

### 3. Interactive Grounded Assessment Chat

Launch the hallucination-safe terminal session to query your local knowledge graphs and vector databases directly. The **Two-Pass Guardrail** ensures that if an asset or claim cannot be verified against the local graph structure, a hard block is issued.

```bash
python main.py chat nipgr

```

### 4. Export Graph Network to GraphML

Compile the consolidated multi-year institutional knowledge graph into an industry-standard network file for topological rendering.

```bash
python main.py export nipgr

```

* **Output Artifact:** `data/exports/nipgr_historical_network.graphml`

---

## 📊 Network Topology Analysis (Cytoscape Workflow)

The exported `.graphml` files are fully optimized for advanced visual mapping inside **Cytoscape**:

1. Open Cytoscape and navigate to **File ➔ Import ➔ Network from File...** and load your generated `.graphml` file.
2. Under the **Style** panel, select **Edge** and map the `Label` property column to render edge relations (e.g., `FUNDED_BY (FY_2024)`) directly on visual connections.
3. Utilize the top **Layout** menu to cycle through evaluation perspectives:
* **Prefuse Force Directed Layout:** Isolates organic clusters, exposing high-output laboratories and heavily funded research hubs.


* **Circular Layout:** Organizes external funding entities along a ring topology, visualizing institutional reliance profiles and diversification metrics.


* **Hierarchical Layout:** Renders a top-down tree map showcasing macro structural hierarchies and showing exactly how national grants flow down into patents and varieties.





---

## 🤝 Contributing & Roadmap

This repository is in active development, fulfilling the 2025-2026 ORAT (Open Research Assessment Toolkit) roadmap. Immediate upcoming items include:

* **Neo4j AuraDB Migration:** Transitioning from in-memory `NetworkX` to Neo4j for native Cypher querying and visual exploration.
* **Streamlit UI Development:** Wrapping the CLI into a lightweight, local web interface for non-technical stakeholders.
* **Broader Institute Benchmarking:** Stress-testing the Agricultural Ontology against additional institutes (e.g., ICAR, IARI).

For inquiries or contributions, please refer to the core OT-ViRaRe task group guidelines.
