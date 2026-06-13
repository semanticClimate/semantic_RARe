import json
import time
from groq import Groq

# The Agricultural & Plant-Science Ontology Prompt
AGRICULTURE_KG_PROMPT = """You are an expert AI data extractor analyzing an Annual Report from an Indian Agricultural/Plant-Science Research Institution (e.g., NIPGR, ICAR).
Extract professional, financial, and structural relationships into a Knowledge Graph.

Target Entity Types:
- Person (Researchers, Scientists, Directors, Fellows)
- Department (Divisions, Labs, Centers, Virtual Hubs)
- Institution (Universities, Startups, External Collaborators, Institutes)
- FundingBody (Agencies like DST, DBT, ICAR, CEFIPRA)
- Project (Research titles, Initiatives, Crop/Plant Varieties)
- Patent (Filed/Granted patents, Technologies)
- Award (Fellowships, Recognitions, Medals)
- Startup (Incubated companies, AgTech ventures)

Return ONLY a valid JSON array of objects with 'source', 'target', and 'relation'.
Example: 
[
  {"source": "Dr. Gopaljee Jha", "target": "Indian Academy of Sciences", "relation": "FELLOW_OF"},
  {"source": "Plant Immunity Division", "target": "DBT", "relation": "FUNDED_BY"},
  {"source": "AgriTech Innovations", "target": "NIPGR", "relation": "IS_STARTUP_OF"}
]
Do not output markdown, explanations, or extra text. Just the JSON array.
If no clear relationships exist, return: []
"""

def extract_relationships_from_page(page_text: str, client: Groq) -> list[dict]:
    """Sends a page of text to Groq to extract JSON relationships."""
    messages = [
        {"role": "system", "content": AGRICULTURE_KG_PROMPT},
        {"role": "user", "content": f"Extract relationships from this text:\n\n{page_text}"}
    ]
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.0,
            max_tokens=1024,
        )
        
        raw_output = response.choices[0].message.content.strip()
        if raw_output.startswith("```json"):
            raw_output = raw_output[7:-3]
            
        return json.loads(raw_output)
    except Exception as e:
        # Fails silently for empty/bad JSON to keep the batch processor running
        return []