from typer.testing import CliRunner
import typer
from unittest.mock import patch, MagicMock

runner = CliRunner()

def test_main_dry_run():
    # Import here to avoid issues
    from src.main import main
    
    # Create a Typer app for testing
    app = typer.Typer()
    app.command()(main)
    
    with patch("src.printer_core.create_html_file") as mock_create:
        with patch("src.printer_core.sync_playwright") as mock_playwright:
            with patch("src.printer_core.print_img") as mock_print:
                with patch("src.sudoku_module.generator.generate") as mock_generate:
                    mock_generate.return_value = "<div>sudoku</div>"
                    
                    result = runner.invoke(app, ["sudoku", "--dry-run"])
                    
                    assert result.exit_code == 0
                    assert "Dry run: Skipping print." in result.stdout
                    
                    # Verify print_img was NOT called
                    mock_print.assert_not_called()

def test_main_with_config():
    from src.main import main
    
    app = typer.Typer()
    app.command()(main)
    
    with patch("src.printer_core.create_html_file") as mock_create:
        with patch("src.printer_core.sync_playwright") as mock_playwright:
            with patch("src.printer_core.print_img") as mock_print:
                with patch("src.sudoku_module.generator.generate") as mock_generate:
                    mock_generate.return_value = "<div>sudoku</div>"
                    
                    result = runner.invoke(app, ["sudoku", "--vendor-id", "0x1234", "--product-id", "0x5678"])
                    
                    assert result.exit_code == 0
                    
                    # Verify print_img was called with correct args
                    mock_print.assert_called_once_with(
                        img_source="temp.png",
                        id_vendor=0x1234,
                        id_product=0x5678
                    )

def test_no_modules():
    from src.main import main
    
    app = typer.Typer()
    app.command()(main)
    
    result = runner.invoke(app, [])
    assert result.exit_code != 0
    # Typer catches this before our code runs
    assert "Missing argument" in result.output
