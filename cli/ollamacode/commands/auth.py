import typer
from rich.console import Console
from ollamacode.config import save_config, load_config

app = typer.Typer()
console = Console()

@app.command()
def login(
    api_key: str = typer.Option(..., prompt=True, hide_input=True, help="Your OllamaCode API Key"),
    api_url: str = typer.Option("http://localhost:8000", help="Backend URL")
):
    """
    Configure authentication settings.
    """
    settings = load_config()
    settings.api_key = api_key
    settings.api_url = api_url
    
    save_config(settings)
    console.print(f"[green]Successfully saved configuration to ~/.ollamacode/config.json[/green]")

@app.command()
def status():
    """
    Check current configuration.
    """
    settings = load_config()
    console.print(f"API URL: [blue]{settings.api_url}[/blue]")
    if settings.api_key:
        console.print("API Key: [green]Set[/green]")
    else:
        console.print("API Key: [red]Not Set[/red]")
