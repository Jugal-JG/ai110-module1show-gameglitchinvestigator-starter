def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        # BUG 1 FIX: Hard was returning 1–50, which is easier than Normal's 1–100.
        # AI (Claude) identified the inverted range logic and suggested 1–200 to make Hard
        # genuinely harder. We verified by comparing all three ranges side-by-side.
        # Refactored from app.py into logic_utils.py using Claude Agent mode.
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        # BUG 2 FIX: Hint messages were completely backwards — "Too High" said "Go HIGHER!"
        # and "Too Low" said "Go LOWER!", giving players the opposite direction every time.
        # AI (Claude) spotted the swap and corrected both return values. We verified by
        # manually tracing: if guess(80) > secret(50), player must go LOWER, not higher.
        # Refactored from app.py into logic_utils.py using Claude Agent mode.
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        # BUG 2 FIX (string fallback): Same swapped-message bug existed in the TypeError
        # branch where the secret was cast to str. AI caught this secondary occurrence too.
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
