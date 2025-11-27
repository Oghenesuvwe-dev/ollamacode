from typer.testing import CliRunner
from ollamacode.main import app
from unittest.mock import patch, MagicMock

runner = CliRunner()

def test_version():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "OllamaCode" in result.stdout

def test_fix_command_missing_file():
    result = runner.invoke(app, ["fix", "nonexistent.py"])
    assert result.exit_code != 0

@patch("ollamacode.commands.fix.APIClient")
def test_fix_command_success(mock_client_cls):
    # Setup mock
    mock_client = MagicMock()
    mock_client.trigger_fix.return_value = {"explanation": "Fixed", "code": "pass"}
    mock_client_cls.return_value = mock_client

    # Create dummy file
    with runner.isolated_filesystem():
        with open("test.py", "w") as f:
            f.write("print('hello')")
        
        result = runner.invoke(app, ["fix", "test.py"])
        
        assert result.exit_code == 0
        assert "AI Suggestion" in result.stdout
        mock_client.trigger_fix.assert_called_once()
