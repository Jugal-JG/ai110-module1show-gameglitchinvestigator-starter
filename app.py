import random
import streamlit as st
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# BUG 1 FIX (range persists on difficulty switch): The page loads with Normal (index=1) by
# default, setting the secret in 1–100. Switching to Easy never regenerated the secret,
# so out-of-range values persisted. AI (Claude) identified the missing difficulty-change
# detection and suggested comparing session_state.difficulty to the current selection.
# Also flagged that the hint text was hardcoded "1 and 100" — fixed below using {low}/{high}.
# Collaborated with Claude Agent mode; we reviewed the diff and confirmed the reset logic.
if st.session_state.get("difficulty") != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 1
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []

st.subheader("Make a guess")

# FIXED: Was hardcoded "1 and 100" — now uses {low} and {high} from get_range_for_difficulty
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    # BUG 3 FIX: New Game only reset attempts + secret, leaving status/score/history unchanged.
    # After a win/loss, status stayed "won"/"lost" so st.stop() fired on the very next rerun,
    # making it impossible to play again without a full page refresh.
    # AI (Claude) traced the st.stop() call and identified the 3 missing state resets.
    # We verified by playing to a win, clicking New Game, and confirming the game restarted.
    # Collaborated with Claude Agent mode; changes reviewed in the diff before accepting.
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.score = 0
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        # FIXED: On even attempts the secret was cast to str, causing string comparison.
        # e.g. check_guess(12, "7") → "12" < "7" alphabetically → wrong "Too Low" result.
        # Secret must always stay an int for correct numeric comparison.
        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        # CHALLENGE 4: Color-coded hints + Hot/Cold proximity emoji
        if show_hint:
            distance = abs(guess_int - st.session_state.secret)
            if distance == 0:
                proximity = "🎯 Exact!"
            elif distance <= 5:
                proximity = "🔥 Very Hot!"
            elif distance <= 15:
                proximity = "🌡️ Warm"
            elif distance <= 30:
                proximity = "🧊 Cold"
            else:
                proximity = "❄️ Freezing!"

            if outcome == "Too High":
                st.error(f"{message}  |  {proximity}")
            elif outcome == "Too Low":
                st.warning(f"{message}  |  {proximity}")

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

# CHALLENGE 4: Session summary table — shows all guesses with outcome per attempt
if st.session_state.history:
    st.divider()
    st.subheader("📊 Guess History")
    rows = []
    for i, g in enumerate(st.session_state.history):
        if isinstance(g, int):
            distance = abs(g - st.session_state.secret)
            if distance == 0:
                result = "✅ Correct!"
            elif g > st.session_state.secret:
                result = "📉 Too High"
            else:
                result = "📈 Too Low"
            rows.append({"Attempt": i + 1, "Guess": g, "Result": result, "Distance": distance})
        else:
            rows.append({"Attempt": i + 1, "Guess": str(g), "Result": "❌ Invalid", "Distance": "—"})
    st.table(rows)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
