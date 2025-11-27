import typer
from rich.console import Console
from ollamacode.commands import fix, review, auth

app = typer.Typer(
    name="ollamacode",
    help="🤖 Open Source AI Code Reviewer CLI",
    add_completion=False,
    no_args_is_help=True
)

console = Console()

app.add_typer(fix.app, name="fix", help="Fix code issues")
app.add_typer(review.app, name="review", help="Trigger code reviews")
app.add_typer(auth.app, name="auth", help="Manage authentication")

if __name__ == "__main__":
    app()
