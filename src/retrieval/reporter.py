import os
from groq import Groq
from rich.progress import track
from src.retrieval.merger import get_hybrid_context

# 🌟 THE SOLUTION: Use generic Python string templates with placeholders
QUESTION_TEMPLATES = [
    "List the major internal research divisions, centers, or laboratories explicitly belonging to {institute}. Exclude any parent councils, overarching national networks, or separate sister facilities mentioned in the text unless a joint lab is physically hosted within {institute} premises.",
    "Which specific startups or business incubators are physically hosted by or directly registered under {institute}?",
    "List the unique external funding agencies providing grants explicitly to {institute}'s projects. Deduplicate the list; do not repeat the same agency.",
    "What specific patents or commercialized technologies have been developed, filed, or granted explicitly to {institute} or its researchers?",
    "List the specific scientists from {institute} who have won external awards, medals, or academy fellowships (e.g., INSA, NASI, IASc). Do NOT list scientists merely by their internal employment ranking or standard pay-grade designations."
]

def generate_markdown_report(institute_name: str, api_key: str):
    client = Groq(api_key=api_key)
    institute_upper = institute_name.upper()
    
    reports_dir = "data/reports"
    os.makedirs(reports_dir, exist_ok=True)
    output_path = os.path.join(reports_dir, f"{institute_name}_assessment.md")
    
    report_content = f"# Standardized ViRaRe Assessment: {institute_upper}\n\n"
    report_content += f"> *This report was generated using the OT-ViRaRe Data Visitation Pipeline. All facts are strictly grounded in local institutional data structures for {institute_upper}.*\n\n"
    
    # SYSTEM PROMPT UPGRADE: Generic scope boundaries and semantic filtering
    system_prompt = f"""You are an elite research metrics auditor for the CODATA OT-ViRaRe framework.
    Your mission is to analyze the context facts and answer the question with absolute structural precision.

    CRITICAL RULES:
    1. SCOPE PURITY: The current target institute is {institute_upper}. The context text may be pulled from a multi-institutional, joint national council, or shared umbrella report that names other autonomous sister facilities or parent bodies. You MUST completely filter out achievements, startups, or labs belonging to those external entities. Only include data explicitly credited to {institute_upper}.
    2. STRICT AGGREGATION & DEDUPLICATION: Do not repeat any entity name. Combine any scattered mentions into a single, comprehensive entry.
    3. FACTUAL GROUNDING: If a section has no explicit entries matching the criteria in the context, output exactly: 'No explicit data recorded in the current institutional report window.'
    4. NO HR ROSTERS: Standard employment designations or staff directories do not constitute awards. Filter them out unless an explicit fellowship or medal is stated.
    
    Format the output cleanly using markdown bullet points."""

    for template in track(QUESTION_TEMPLATES, description=f"[cyan]Generating High-Fidelity Assessment for {institute_upper}..."):
        # 🔄 Dynamically format the question at run-time with the target institute name
        question = template.format(institute=institute_upper)
        context = get_hybrid_context(question, institute_name)
        
        # Maps human-readable clean headers based on template keywords dynamically
        if "divisions" in template: clean_header = "Major Internal Research Divisions & Labs"
        elif "startups" in template: clean_header = "Associated Startups & Incubators"
        elif "funding" in template: clean_header = "Deduplicated External Funding Agencies"
        elif "patents" in template: clean_header = "Filed/Granted Patents & Technologies"
        elif "scientists" in template: clean_header = "Key Scientists Recognized (Awards & Fellowships)"
        else: clean_header = "Assessment Section"

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context Facts and Texts:\n{context}\n\nObjective: {question}"}
            ],
            temperature=0.0,  
            max_tokens=1000  
        )
        
        answer = response.choices[0].message.content.strip()
        report_content += f"## {clean_header}\n{answer}\n\n---\n\n"
        
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
        
    return output_path


# import os
# from groq import Groq
# from rich.progress import track
# from src.retrieval.merger import get_hybrid_context

# # The standardized questions for Agricultural Assessment
# ASSESSMENT_QUESTIONS = [
#     "List the major research divisions, centers, or labs mentioned in the institute.",
#     "Which specific startups or incubators are associated with the institute?",
#     "List the specific external funding agencies (e.g., DBT, DST, ICAR) providing grants.",
#     "What specific patents or technologies have been developed or filed?",
#     "List the key scientists recognized with awards or fellowships."
# ]

# def generate_markdown_report(institute_name: str, api_key: str):
#     client = Groq(api_key=api_key)
    
#     reports_dir = "data/reports"
#     os.makedirs(reports_dir, exist_ok=True)
#     output_path = os.path.join(reports_dir, f"{institute_name}_assessment.md")
    
#     report_content = f"# Standardized ViRaRe Assessment: {institute_name.upper()}\n\n"
#     report_content += "> *This report was generated using the OT-ViRaRe Data Visitation Pipeline. All facts are strictly grounded in the local Knowledge Graph.*\n\n"
    
#     system_prompt = "You are an AI Assessment Assistant. Answer the user's question concisely using ONLY the provided Context Facts. Use bullet points."

#     for question in track(ASSESSMENT_QUESTIONS, description="[cyan]Generating Assessment Sections..."):
#         context = get_hybrid_context(question, institute_name)
        
#         response = client.chat.completions.create(
#             model="llama-3.1-8b-instant",
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
#             ],
#             temperature=0.1,
#             max_tokens=500
#         )
        
#         answer = response.choices[0].message.content.strip()
#         report_content += f"## {question}\n{answer}\n\n---\n\n"
        
#     with open(output_path, 'w', encoding='utf-8') as f:
#         f.write(report_content)
        
#     return output_path