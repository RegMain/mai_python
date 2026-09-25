import pytest
from toolkit.__main__ import main


def test_cli_exitcode_0(capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["toolkit", "calc", "2 + 2"])
    with pytest.raises(SystemExit) as return_code:
        main()

    assert return_code.value.code == 0
    output = capsys.readouterr().out.lower()
    assert "4" in output


def test_cli_exitcode_2(capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["toolkit", "calc", "3 / 0"])
    with pytest.raises(SystemExit) as return_code:
        main()

    assert return_code.value.code == 2


def test_cli_help(capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["toolkit", "--help"])
    with pytest.raises(SystemExit) as return_code:
        main()

    assert return_code.value.code == 0
    output = capsys.readouterr().out.lower()
    assert "usage" in output
    assert "syntax" in output
    assert "calc" in output
    assert "convert" in output
