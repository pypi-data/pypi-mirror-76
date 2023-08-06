from click.testing import CliRunner

from machinable.console.execute import execution


def test_console_execution():
    runner = CliRunner()
    result = runner.invoke(execution, ["./_test_data/storage/tttttt"])
    assert result.exit_code == 0
    result = runner.invoke(execution, ["./_test_data/storage/tttttt/tQtsVCNijRLR"])
    assert result.exception
    assert str(result.exception).startswith("Execution schedule is empty")
