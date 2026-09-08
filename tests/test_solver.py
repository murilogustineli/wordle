import math

import pytest

from wordle.solver import Solver, load_word_list


@pytest.fixture(scope="module")
def solver() -> Solver:
    return Solver()


def test_word_lists_load_and_nest(solver):
    assert all(len(w) == 5 for w in solver.answers)
    assert all(len(w) == 5 for w in solver.possible_words)
    assert set(solver.answers) <= set(solver.possible_words)


def test_load_word_list_strips_blank_lines():
    words = load_word_list("answers.txt")
    assert "" not in words
    assert words == [w.lower() for w in words]


def test_green_yellow_gray_filtering(solver):
    words = solver.find_words("lien", [1, 2, 4, 5], "en", [5, 3], "tarykm")
    assert words == ["liven"]
    assert solver.answer == "liven"


def test_gray_letter_also_green_or_yellow_is_not_excluded(solver):
    # Wordle 2026-09-08: an extra "n" typed into gray must not eliminate LIVEN.
    assert solver.find_words("lien", [1, 2, 4, 5], "en", [5, 3], "tarykmn") == ["liven"]
    # NANNY vs LIVEN gives one yellow N and two gray N's.
    assert "liven" in solver.find_words("", [], "n", [1], "any")


def test_gray_letters_without_overlap_still_exclude(solver):
    words = solver.find_words("", [], "", [], "t")
    assert words and not any("t" in w for w in words)


def test_yellow_letter_cannot_sit_at_its_guessed_position(solver):
    words = solver.find_words("", [], "e", [5], "")
    assert words and all("e" in w and w[4] != "e" for w in words)


def test_input_is_case_insensitive(solver):
    lower = solver.find_words("lien", [1, 2, 4, 5], "en", [5, 3], "tarykm")
    upper = solver.find_words("LIEN", [1, 2, 4, 5], "EN", [5, 3], "TARYKM")
    assert lower == upper


def test_mismatched_positions_raise(solver):
    with pytest.raises(ValueError):
        solver.find_words("ab", [1], "", [], "")


def test_answer_is_none_until_solved(solver):
    solver.find_words("", [], "", [], "")
    assert solver.answer is None


def test_feedback_pattern_handles_repeated_letters(solver):
    solver.words = ["liven"]
    pattern = solver.simulate_feedback_pattern("nanny")
    assert pattern["liven"] == ("yellow", "gray", "gray", "gray", "gray")
    # The third N in LINEN is gray because LIVEN's only N is already green.
    pattern = solver.simulate_feedback_pattern("linen")
    assert pattern["liven"] == ("green", "green", "gray", "green", "green")


def test_entropy_of_uniform_patterns_is_log2_n(solver):
    probs = {"a": 0.25, "b": 0.25, "c": 0.25, "d": 0.25}
    assert solver.compute_entropy(probs) == pytest.approx(2.0)


def test_entropy_of_certain_outcome_is_positive_zero(solver):
    entropy = solver.compute_entropy({"a": 1.0})
    assert entropy == 0.0 and math.copysign(1.0, entropy) == 1.0


def test_choose_word_to_play_returns_ranked_frame(solver):
    solver.find_words("", [], "", [], "tarykm", answer_word_list=True)
    df = solver.choose_word_to_play(word_threshold=2, top_k_words=5)
    assert list(df.columns) == ["Word", "Entropy", "Score"]
    assert len(df) == 5
    assert df["Score"].is_monotonic_decreasing
    assert df["Word"].str.isupper().all()


def test_small_candidate_set_only_ranks_candidates(solver):
    solver.find_words("lien", [1, 2, 4, 5], "en", [5, 3], "tarykm")
    df = solver.choose_word_to_play(word_threshold=2)
    assert df["Word"].tolist() == ["LIVEN"]


def test_choose_word_without_candidates_raises(solver):
    solver.words = []
    with pytest.raises(ValueError):
        solver.choose_word_to_play()
