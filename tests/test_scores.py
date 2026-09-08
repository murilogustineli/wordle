import pandas as pd
import pytest

from wordle.scores import ScoreBoard


@pytest.fixture
def board(tmp_path) -> ScoreBoard:
    path = tmp_path / "scores.csv"
    pd.DataFrame(
        {"Names": ["Murilo", "Barbara", "Draw"], "Games_Won": [543, 250, 541]}
    ).to_csv(path, index=False)
    return ScoreBoard(path)


def test_load_and_names(board):
    df = board.load()
    assert df["Games_Won"].tolist() == [543, 250, 541]
    assert board.names == ["Murilo", "Barbara", "Draw"]


def test_prompt_matches_original_wording(board):
    prompt = board._prompt(board._letters(board.names))
    assert prompt == (
        "Who won the game? Murilo, Barbara, or Draw?\n"
        "Enter 'M' if Murilo won.\n"
        "Enter 'B' if Barbara won.\n"
        "Enter 'D' if it was a Draw.\n"
        "Please enter [M/B/D]:"
    )


@pytest.mark.parametrize(
    "answer, expected",
    [("M", [544, 250, 541]), ("b", [543, 251, 541]), (" d ", [543, 250, 542])],
)
def test_update_increments_chosen_row(board, monkeypatch, answer, expected):
    monkeypatch.setattr("builtins.input", lambda _: answer)
    df = board.update()
    assert df["Games_Won"].tolist() == expected
    assert board.load()["Games_Won"].tolist() == expected


def test_update_with_unknown_answer_changes_nothing(board, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "x")
    df = board.update()
    assert df["Games_Won"].tolist() == [543, 250, 541]
    assert "scores unchanged" in capsys.readouterr().out


def test_set_scores_by_name(board):
    df = board.set_scores(Murilo=477, Barbara=215, Draw=473)
    assert df["Games_Won"].tolist() == [477, 215, 473]
    df = board.set_scores(Barbara=216)
    assert df["Games_Won"].tolist() == [477, 216, 473]


def test_set_scores_rejects_unknown_player(board):
    with pytest.raises(KeyError):
        board.set_scores(Nobody=1)


def test_reset(board):
    assert board.reset(confirm=False)["Games_Won"].tolist() == [543, 250, 541]
    assert board.reset(confirm=True)["Games_Won"].tolist() == [0, 0, 0]


def test_commit_message(board):
    assert board.commit_message() == 'git commit -m "updated wordle 543-250-541"'
    assert board.commit_message(word="liven") == (
        'git commit -m "updated wordle 543-250-541, word=LIVEN"'
    )


def test_duplicate_initials_rejected(tmp_path):
    path = tmp_path / "scores.csv"
    pd.DataFrame({"Names": ["Bob", "Barbara"], "Games_Won": [0, 0]}).to_csv(
        path, index=False
    )
    with pytest.raises(ValueError):
        ScoreBoard(path)._letters(ScoreBoard(path).names)


def test_plot_writes_png(board, tmp_path):
    pytest.importorskip("matplotlib")
    out = board.plot(tmp_path / "plots" / "scores.png")
    assert out.exists() and out.stat().st_size > 0
