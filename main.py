import typer
import os
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from groq import Groq

from src.ingestion.db_builder import build_databases
from src.retrieval.merger import get_hybrid_context
from src.graph.guardrail import verify_factual_grounding
from src.retrieval.reporter import generate_markdown_report
from src.graph.exporter import export_to_graphml

app = typer.Typer(
    name="virare",
    help="OT-ViRaRe Assessment CLI Tool for Agricultural Institutes",
    add_completion=False
)
console = Console()

def get_api_key():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        console.print("[bold red]Error:[/bold red] GROQ_API_KEY environment variable not set.")
        raise typer.Exit(code=1)
    return api_key

# Import the new dynamic temporal reporter inside main.py
from src.retrieval.temporal_reporter import generate_temporal_assessment

# Update the ingest command signature
@app.command()
def ingest(
    pdf_path: str, 
    institute_name: str = typer.Option(..., "--name", "-n", help="Short name of the institute"),
    year: int = typer.Option(..., "--year", "-y", help="Financial Year of the annual report (e.g., 2024)")
):
    """Ingest a specific year's PDF report, updating the local historical repository."""
    api_key = get_api_key()
    console.print(f"[bold cyan]🚀 Initializing Data Visitation Ingestion for:[/bold cyan] {institute_name.upper()} (Year: {year})")
    try:
        json_path, chroma_path, rel_count = build_databases(pdf_path, institute_name, year, api_key)
        console.print(f"\n[bold green]✅ Year {year} Ingestion Complete![/bold green]")
    except Exception as e:
        console.print(f"\n[bold red]❌ Pipeline Failed:[/bold red] {str(e)}")
        raise typer.Exit(code=1)

# Add the new temporal report command at the bottom of main.py
@app.command()
def temporal_report(institute_name: str):
    """
    Generate a 10-year chronological trend analysis across all ingested historical reports.
    """
    api_key = get_api_key()
    console.print(f"[bold yellow]📅 Activating Decadal Temporal Assessment for:[/bold yellow] {institute_name.upper()}")
    try:
        output_path = generate_temporal_assessment(institute_name, api_key)
        console.print(f"\n[bold green]✅ Temporal Trend Report Compiled![/bold green]")
        console.print(f"📄 Saved to: [yellow]{output_path}[/yellow]")
    except Exception as e:
        console.print(f"\n[bold red]❌ Assessment Failed:[/bold red] {str(e)}")

@app.command()
def chat(institute_name: str):
    """Launch the interactive, hallucination-safe chat."""
    api_key = get_api_key()
    client = Groq(api_key=api_key)
    
    console.print(Panel.fit(
        f"[bold green]🛡️ OT-ViRaRe Chat Session: {institute_name.upper()}[/bold green]\n"
        "[dim]Type 'quit' or 'q' to exit.[/dim]",
        border_style="green"
    ))
    
    # system_prompt = "You are an AI Assessment Assistant. Answer based strictly on the provided Context. If the answer is not in the context, output exactly: 'Data not available in the processed report.' Use bullet points."
    system_prompt = """You are an AI Assessment Assistant for OT-ViRaRe. 
    Answer the user's question in clear, natural language using ONLY the provided Context Facts. 
    Do not just copy-paste the raw graph edges (e.g., 'A [RELATION] B'); synthesize them into proper sentences. 
    If the context lacks the answer, output exactly: 'Data not available in the processed report.'"""


    while True:
        user_input = typer.prompt("\n🧑‍🔬 Ask")
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
            
        console.print("[dim]🔍 Querying Hybrid GraphRAG...[/dim]")
        context = get_hybrid_context(user_input, institute_name)
        
        try:
            # 1. Generate Answer
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Context Facts:\n{context}\n\nQuestion: {user_input}"}
                ],
                temperature=0.1,
                max_tokens=600,
            )
            proposed_answer = response.choices[0].message.content.strip()
            
            # 2. Run Guardrail
            console.print("[dim]🛡️ Verifying contextual grounding...[/dim]")
            is_safe = verify_factual_grounding(context, proposed_answer, client)
            
            if not is_safe:
                console.print("\n[bold red]⚠️ [BLOCKED] System attempted to generate unverified facts.[/bold red]")
                console.print("[bold yellow]🤖 Response:[/bold yellow] Data not available in the processed report.")
            else:
                console.print("\n[bold cyan]🤖 System Assessment:[/bold cyan]")
                console.print(Markdown(proposed_answer))
                
        except Exception as e:
            console.print(f"[bold red]⚠️ Error:[/bold red] {e}")

@app.command()
def report(institute_name: str):
    """Generate a standardized markdown assessment report."""
    api_key = get_api_key()
    console.print(f"[bold yellow]📊 Generating standard assessment report for:[/bold yellow] {institute_name.upper()}")
    
    try:
        output_path = generate_markdown_report(institute_name, api_key)
        console.print(f"\n[bold green]✅ Report Generated Successfully![/bold green]")
        console.print(f"📄 Saved to: [yellow]{output_path}[/yellow]")
    except Exception as e:
        console.print(f"\n[bold red]❌ Report Generation Failed:[/bold red] {str(e)}")

@app.command()
def export(institute_name: str):
    """
    Export the institute's Knowledge Graph into a Cytoscape-compatible .graphml file.
    """
    console.print(f"[bold cyan]🕸️ Exporting Knowledge Graph for {institute_name.upper()} to GraphML format...[/bold cyan]")
    try:
        output_path = export_to_graphml(institute_name)
        console.print(f"\n[bold green]✅ GraphML Export Complete![/bold green]")
        console.print(f"📊 File saved to: [yellow]{output_path}[/yellow]")
        console.print("[dim]You can now directly drag and drop this file into Cytoscape! [/dim]")
    except Exception as e:
        console.print(f"\n[bold red]❌ Export Failed:[/bold red] {str(e)}")

if __name__ == "__main__":
    app()

# import typer
# import os
# from rich.console import Console
# from src.ingestion.db_builder import build_databases

# app = typer.Typer(
#     name="virare",
#     help="OT-ViRaRe Assessment CLI Tool for Agricultural Institutes",
#     add_completion=False
# )
# console = Console()

# @app.command()
# def ingest(pdf_path: str, institute_name: str = typer.Option(..., "--name", "-n", help="Short name of the institute (e.g., nipgr)")):
#     """
#     Ingest a PDF report, extract entities, and build the Knowledge Graph & Vector DB.
#     """
#     api_key = os.environ.get("GROQ_API_KEY")
#     if not api_key:
#         console.print("[bold red]Error:[/bold red] GROQ_API_KEY environment variable not set.")
#         raise typer.Exit(code=1)
        
#     console.print(f"[bold cyan]🚀 Initializing Data Visitation Ingestion for:[/bold cyan] {institute_name.upper()}")
#     console.print(f"[dim]Reading from: {pdf_path}[/dim]")
    
#     try:
#         json_path, chroma_path, rel_count = build_databases(pdf_path, institute_name, api_key)
        
#         console.print("\n[bold green]✅ Ingestion Complete![/bold green]")
#         console.print(f"🕸️ Knowledge Graph saved to: [yellow]{json_path}[/yellow] ({rel_count} relationships)")
#         console.print(f"📦 Vector Database saved to: [yellow]{chroma_path}[/yellow]")
#         console.print(f"\n[dim]You can now run 'python main.py chat {institute_name}'[/dim]")
        
#     except Exception as e:
#         console.print(f"\n[bold red]❌ Pipeline Failed:[/bold red] {str(e)}")
#         raise typer.Exit(code=1)

# @app.command()
# def chat(institute_name: str):
#     """Launch the interactive, hallucination-safe chat."""
#     console.print(f"[bold green]🛡️ Starting secure chat session for:[/bold green] {institute_name}")

# @app.command()
# def report(institute_name: str):
#     """Generate a standardized markdown assessment report."""
#     console.print(f"[bold yellow]📊 Generating standard assessment report for:[/bold yellow] {institute_name}")

# if __name__ == "__main__":
#     app()

# # import typer
# # from rich.console import Console

# # # Initialize Typer App and Rich Console
# # app = typer.Typer(
# #     name="virare",
# #     help="OT-ViRaRe Assessment CLI Tool for Agricultural Institutes",
# #     add_completion=False
# # )
# # console = Console()

# # @app.command()
# # def ingest(pdf_path: str):
# #     """
# #     Ingest a PDF report, extract entities, and build the Knowledge Graph & Vector DB.
# #     """
# #     console.print(f"[bold cyan]🚀 Initializing ingestion for:[/bold cyan] {pdf_path}")
# #     console.print("[dim]This will run asynchronously in the background...[/dim]")
# #     # TODO: Wire up src.ingestion modules in Phase 2

# # @app.command()
# # def chat(institute_name: str):
# #     """
# #     Launch the interactive, hallucination-safe chat for a specific institute.
# #     """
# #     console.print(f"[bold green]🛡️ Starting secure chat session for:[/bold green] {institute_name}")
# #     # TODO: Wire up src.retrieval and Guardrail modules in Phase 3 & 4

# # @app.command()
# # def report(institute_name: str):
# #     """
# #     Generate a standardized markdown assessment report for the institute.
# #     """
# #     console.print(f"[bold yellow]📊 Generating standard assessment report for:[/bold yellow] {institute_name}")
# #     # TODO: Wire up automated reporting logic in Phase 4

# # if __name__ == "__main__":
# #     app()