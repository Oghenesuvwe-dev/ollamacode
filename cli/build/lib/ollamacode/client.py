import httpx
from rich.console import Console
from ollamacode.config import load_config

console = Console()

class APIClient:
    def __init__(self):
        self.settings = load_config()
        self.base_url = self.settings.api_url
        self.headers = {}
        if self.settings.api_key:
            self.headers["Authorization"] = f"Bearer {self.settings.api_key}"

    def trigger_fix(self, filename: str, content: str, line: int = None, user_context: str = None):
        """Send a fix request to the backend."""
        payload = {
            "filename": filename,
            "content": content,
            "line": line,
            "context": user_context
        }
        
        try:
            with console.status("[bold green]Asking AI for a fix..."):
                response = httpx.post(
                    f"{self.base_url}/api/v1/fix",
                    json=payload,
                    headers=self.headers,
                    timeout=60.0
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            console.print(f"[bold red]Error communicating with backend:[/bold red] {e}")
            return None

    def display_solution(self, response: dict):
        """Render the solution to the terminal."""
        if not response:
            return

        console.print("\n[bold blue]🤖 AI Suggestion:[/bold blue]")
        console.print(response.get("explanation", "No explanation provided."))
        
        if "code" in response:
            console.print("\n[bold]Suggested Code:[/bold]")
            console.print(f"```python\n{response['code']}\n```")
