import typer
from pathlib import Path
from ollamacode.client import APIClient
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def file(
    path: Path = typer.Argument(..., exists=True, help="Path to the file to fix"),
    line: int = typer.Option(None, help="Specific line number to focus on"),
    context: str = typer.Option(None, help="Additional error context or instructions")
):
    """
    Request an AI fix for a specific file.
    """
    try:
        with open(path, "r") as f:
            content = f.read()
    except Exception as e:
        console.print(f"[red]Error reading file:[/red] {e}")
        raise typer.Exit(1)

    client = APIClient()
    response = client.trigger_fix(
        filename=path.name,
        content=content,
        line=line,
        user_context=context
    )
    
    client.display_solution(response)
