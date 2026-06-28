import os
from groq import Groq
from rich.progress import track
from src.retrieval.merger import get_hybrid_context

TEMPORAL_QUESTIONS = [
    "Trace the evolution of funding over the years. Which external funding agencies have consistently supported the institute, and are there any clear structural shifts in funding channels?",
    "Analyze the growth and trajectories of startups or technology incubators over the past decade. How has the innovation footprint evolved?",
    "Compare the registration, filings, and grant trends of patents or novel plant varieties across different reporting periods. What are the key technology outcomes over time?",
    "Identify patterns of faculty recognition and milestones. Detail any significant historical growth in academy fellowships or awards over the years."
]

def generate_temporal_assessment(institute_name: str, api_key: str):
    client = Groq(api_key=api_key)
    institute_upper = institute_name.upper()
    
    reports_dir = "data/reports"
    os.makedirs(reports_dir, exist_ok=True)
    output_path = os.path.join(reports_dir, f"{institute_name}_10year_trend_analysis.md")
    
    report_content = f"# 📅 Decadal Temporal Assessment Report: {institute_upper}\n\n"
    report_content += f"> *This chronological trend analysis covers the historical data repository compiled dynamically under the OT-ViRaRe Data Visitation Framework.*\n\n"
    
    system_prompt = f"""You are an elite timeline analyst auditing institutional trajectories over a 10-year window.
    Your objective is to compare across different financial years (marked as FY_YYYY in graph facts) and draw analytical summaries of growth, decline, or structural shifts.
    
    CRITICAL RULES:
    1. TIMELINE ACCURACY: Pay absolute attention to the chronological tags (e.g., FY_2024 vs FY_2025). Clearly contrast what existed in earlier periods versus what emerged later.
    2. DEDUPLICATION WITH CHRONOLOGY: Do not list an entity multiple times linearly. Instead, cluster the facts around the entity timeline (e.g., 'Agency X: Funded projects in 2023, increased footprint in 2024').
    3. NO HALLUCINATION: If the historical context does not explicitly contain data for certain years, acknowledge the data gap rather than speculating."""

    for question in track(TEMPORAL_QUESTIONS, description=f"[cyan]Synthesizing Decadal Trends for {institute_upper}..."):
        context = get_hybrid_context(question, institute_name)
        
        if "funding" in question: header = "Funding Trajectory & Structural Shifts"
        elif "startups" in question: header = "Incubator & Startup Footprint Evolution"
        elif "patents" in question: header = "Intellectual Property & Variety Release Timeline"
        elif "faculty" in question or "scientists" in question: header = "Chronological Milestones of Faculty Recognition"
        else: header = "Historical Trend Analysis"

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Multi-Year Context:\n{context}\n\nAnalytical Objective: {question}"}
            ],
            temperature=0.0,
            max_tokens=1500
        )
        
        answer = response.choices[0].message.content.strip()
        report_content += f"## {header}\n{answer}\n\n---\n\n"
        
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
        
    return output_path