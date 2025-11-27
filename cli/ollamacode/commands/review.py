import typer
from ollamacode.client import APIClient
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def pr(
    pr_number: int = typer.Argument(..., help="Pull Request Number"),
    repo: str = typer.Option(None, help="Repository name (owner/repo). Defaults to current git repo.")
):
    """
    Trigger a manual review for a Pull Request.
    """
    # TODO: Auto-detect repo from git config if not provided
    if not repo:
        console.print("[yellow]Please provide --repo owner/name[/yellow]")
        raise typer.Exit(1)

    console.print(f"[blue]Triggering review for PR #{pr_number} in {repo}...[/blue]")
    
    # This would trigger the Pipedream webhook manually
    # For now, we'll just print a placeholder
    console.print("[green]Review triggered! Check the PR for comments shortly.[/green]")
