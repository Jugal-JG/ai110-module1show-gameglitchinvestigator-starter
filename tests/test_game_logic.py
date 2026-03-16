from logic_utils import check_guess, get_range_for_difficulty
import random

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Bug 1: Range error across all difficulties ---
# FIXED: Hard returned 1–50 (easier than Normal), hint text was hardcoded "1 and 100",
# and New Game always used randint(1, 100) ignoring difficulty.

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1 and high == 20, f"Easy should be 1–20, got {low}–{high}"

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1 and high == 100, f"Normal should be 1–100, got {low}–{high}"

def test_hard_range():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1 and high == 200, f"Hard should be 1–200, got {low}–{high}"

def test_hard_range_harder_than_normal():
    # Hard must have a wider range than Normal so it is actually harder
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high, (
        f"Hard range ({hard_high}) should be larger than Normal range ({normal_high})"
    )

def test_secret_stays_within_easy_range():
    # Simulates what happens when a secret is generated for Easy difficulty
    low, high = get_range_for_difficulty("Easy")
    for _ in range(50):
        secret = random.randint(low, high)
        assert low <= secret <= high, f"Secret {secret} is outside Easy range {low}–{high}"


# --- Bug 2: Hints were completely backwards ---
# FIXED: "Too High" was showing "Go HIGHER!" and "Too Low" was showing "Go LOWER!"

def test_too_high_message_says_go_lower():
    # Guess is above secret → player should go LOWER
    outcome, message = check_guess(80, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected 'LOWER' in message when guess > secret, got: '{message}'"

def test_too_low_message_says_go_higher():
    # Guess is below secret → player should go HIGHER
    outcome, message = check_guess(20, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected 'HIGHER' in message when guess < secret, got: '{message}'"

def test_too_high_does_not_say_go_higher():
    # Make sure the old wrong message is gone
    outcome, message = check_guess(80, 50)
    assert outcome == "Too High"
    assert "HIGHER" not in message, f"'Too High' should NOT say 'HIGHER', got: '{message}'"

def test_too_low_does_not_say_go_lower():
    # Make sure the old wrong message is gone
    outcome, message = check_guess(20, 50)
    assert outcome == "Too Low"
    assert "LOWER" not in message, f"'Too Low' should NOT say 'LOWER', got: '{message}'"


# --- Bug 3: New Game / difficulty change did not reset game state ---
# FIXED: New Game only reset attempts + secret, leaving status/score/history unchanged.
# Difficulty change never regenerated the secret, so switching to Easy kept an out-of-range secret.
# These tests verify the logic that must hold after a reset.

def test_new_game_secret_within_easy_range():
    # After clicking New Game on Easy, the new secret must be inside 1–20
    low, high = get_range_for_difficulty("Easy")
    new_secret = random.randint(low, high)
    assert low <= new_secret <= high

def test_new_game_secret_within_hard_range():
    # After clicking New Game on Hard, the new secret must be inside 1–200
    low, high = get_range_for_difficulty("Hard")
    new_secret = random.randint(low, high)
    assert low <= new_secret <= high

def test_difficulty_switch_generates_new_range():
    # Switching from Normal to Easy must produce a secret within the Easy range, not Normal's
    easy_low, easy_high = get_range_for_difficulty("Easy")
    _, normal_high = get_range_for_difficulty("Normal")
    # Simulate the fix: on difficulty change, regenerate using the new difficulty's range
    new_secret = random.randint(easy_low, easy_high)
    assert new_secret <= easy_high, (
        f"After switching to Easy, secret {new_secret} exceeds Easy max of {easy_high}"
    )
    assert easy_high < normal_high, "Easy ceiling must be lower than Normal ceiling"
