from typer.testing import CliRunner
from ollamacode.main import app
from unittest.mock import patch, MagicMock

runner = CliRunner()

def test_version():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "ollamacode" in result.stdout.lower()

def test_fix_command_missing_file():
    result = runner.invoke(app, ["fix", "file", "nonexistent.py"])
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
        
        result = runner.invoke(app, ["fix", "file", "test.py"])
        
        assert result.exit_code == 0
        # Since we mock the client, display_solution is a mock, so it won't print anything.
        # We verify it was called instead.
        mock_client.trigger_fix.assert_called_once()
        mock_client.display_solution.assert_called_once()
