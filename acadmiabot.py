import streamlit as st
import random
from openai import OpenAI

# ==============================
# QUIZ DATA
# ==============================
QUIZ_BANK = {
    "Class 6": [
        ("What is the largest planet?", ["Earth", "Jupiter", "Mars", "Venus"], "Jupiter", "Jupiter is the largest planet."),
        ("Who invented the light bulb?", ["Newton", "Einstein", "Edison", "Tesla"], "Edison", "Thomas Edison invented it."),
    ],
    "Class 7": [
        ("What is H2O?", ["Oxygen", "Water", "Hydrogen", "Carbon"], "Water", "H2O is the chemical formula for water."),
        ("Fastest land animal?", ["Cheetah", "Tiger", "Leopard", "Horse"], "Cheetah", "Cheetah is the fastest land animal."),
    ],
}

PUZZLE_BANK = {
    "easy": [
        ("I speak without a mouth and hear without ears. What am I?", "An echo"),
        ("What has to be broken before you can use it?", "An egg"),
    ],
    "medium": [
        ("The more of me you take, the more you leave behind. What am I?", "Footsteps"),
        ("What goes up but never comes down?", "Your age"),
    ],
    "hard": [
        ("I have cities but no houses, I have mountains but no trees, I have water but no fish. What am I?", "A map"),
        ("What gets wetter as it dries?", "A towel"),
    ],
}

# ==============================
# APP UI
# ==============================
st.set_page_config(page_title="AcademiaBot", page_icon="🎓", layout="wide")
st.title("🎓 AcademiaBot")
st.write("Your Study Buddy: Quiz • Puzzles • Ask Anything (AI powered)")

mode = st.sidebar.radio("Choose Mode:", ["Quiz Mode", "Puzzle Mode", "AI Mode"])

# ==============================
# QUIZ MODE
# ==============================
if mode == "Quiz Mode":
    st.header("📝 Quiz Time!")
    grade = st.selectbox("Select Class", list(QUIZ_BANK.keys()))

    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0

    q, choices, ans, expl = random.choice(QUIZ_BANK[grade])
    st.subheader(q)
    choice = st.radio("Select your answer:", choices)

    if st.button("Submit Answer"):
        if choice == ans:
            st.success("✅ Correct! " + expl)
            st.session_state.quiz_score += 1
        else:
            st.error(f"❌ Wrong! Correct answer is {ans}. {expl}")
        st.info(f"Your score: {st.session_state.quiz_score}")

# ==============================
# PUZZLE MODE
# ==============================
elif mode == "Puzzle Mode":
    st.header("🧩 Puzzle Challenge")
    diff = st.selectbox("Select Difficulty", ["easy", "medium", "hard"])

    if "puzzle_score" not in st.session_state:
        st.session_state.puzzle_score = 0

    q, ans = random.choice(PUZZLE_BANK[diff])
    st.subheader(q)
    user_ans = st.text_input("Your Answer:")

    if st.button("Check Puzzle"):
        if user_ans.lower().strip() == ans.lower():
            st.success("✅ Correct!")
            st.session_state.puzzle_score += 1
        else:
            st.error(f"❌ Wrong! Correct answer: {ans}")
        st.info(f"Your puzzle score: {st.session_state.puzzle_score}")

# ==============================
# AI MODE
# ==============================
elif mode == "AI Mode":
    st.header("🤖 Ask AcademiaBot Anything!")

    api_key = st.text_input("Enter your OpenAI API Key:", type="password")
    question = st.text_area("Type your question:")

    if st.button("Get Answer"):
        if not api_key:
            st.error("Please enter your OpenAI API Key!")
        elif not question:
            st.warning("Please type a question.")
        else:
            try:
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": question}]
                )
                st.success(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")
