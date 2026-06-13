import os
from groq import Groq
from rich.progress import track
from src.retrieval.merger import get_hybrid_context

# The standardized questions for Agricultural Assessment
ASSESSMENT_QUESTIONS = [
    "List the major research divisions, centers, or labs mentioned in the institute.",
    "Which specific startups or incubators are associated with the institute?",
    "List the specific external funding agencies (e.g., DBT, DST, ICAR) providing grants.",
    "What specific patents or technologies have been developed or filed?",
    "List the key scientists recognized with awards or fellowships."
]

def generate_markdown_report(institute_name: str, api_key: str):
    client = Groq(api_key=api_key)
    
    reports_dir = "data/reports"
    os.makedirs(reports_dir, exist_ok=True)
    output_path = os.path.join(reports_dir, f"{institute_name}_assessment.md")
    
    report_content = f"# Standardized ViRaRe Assessment: {institute_name.upper()}\n\n"
    report_content += "> *This report was generated using the OT-ViRaRe Data Visitation Pipeline. All facts are strictly grounded in the local Knowledge Graph.*\n\n"
    
    system_prompt = "You are an AI Assessment Assistant. Answer the user's question concisely using ONLY the provided Context Facts. Use bullet points."

    for question in track(ASSESSMENT_QUESTIONS, description="[cyan]Generating Assessment Sections..."):
        context = get_hybrid_context(question, institute_name)
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
            ],
            temperature=0.1,
            max_tokens=500
        )
        
        answer = response.choices[0].message.content.strip()
        report_content += f"## {question}\n{answer}\n\n---\n\n"
        
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
        
    return output_path