
import streamlit as st
import ollama

# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="AI Mock Interview Assistant",
    page_icon="🎯",
    layout="wide"
)

# -----------------------------------
# SESSION STATE
# -----------------------------------

if "question" not in st.session_state:
    st.session_state.question = ""

if "history" not in st.session_state:
    st.session_state.history = []

if "started" not in st.session_state:
    st.session_state.started = False

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("Interview Settings")

role = st.sidebar.selectbox(
    "Select Job Role",
    [
        "AI Engineer",
        "Machine Learning Engineer",
        "Data Analyst",
        "Python Developer",
        "Software Developer"
    ]
)

difficulty = st.sidebar.selectbox(
    "Interview Difficulty",
    ["Beginner", "Intermediate", "Advanced"]
)

if st.sidebar.button("Start New Interview"):
    st.session_state.history = []
    st.session_state.question = ""
    st.session_state.started = True

# -----------------------------------
# AI FUNCTION
# -----------------------------------

def ask_ai(prompt):

    response = ollama.chat(
        model="llama3.2:1b",
        messages=[
            {
                "role": "system",
                "content": """
                You are an experienced technical interviewer.

                Generate relevant interview questions.
                Evaluate candidate answers fairly.
                Give a score out of 10.
                Explain strengths and weaknesses.
                Suggest an improved answer.
                Use simple and clear English.
                """
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


# -----------------------------------
# MAIN APPLICATION
# -----------------------------------

st.title("🎯 AI Mock Interview Assistant")

st.write(
    "Practice technical interviews with an AI interviewer."
)

st.info(
    f"Selected Role: {role} | Difficulty: {difficulty}"
)

# -----------------------------------
# START INTERVIEW
# -----------------------------------

if st.button("Generate Interview Question"):

    with st.spinner("AI is preparing your question..."):

        try:

            prompt = f"""
            Generate ONE interview question for a fresher.

            Job Role: {role}
            Difficulty: {difficulty}

            Give only one clear question.
            Do not give the answer.
            """

            question = ask_ai(prompt)

            st.session_state.question = question
            st.session_state.started = True

        except Exception as error:
            st.error(f"AI Error: {error}")


# -----------------------------------
# DISPLAY QUESTION
# -----------------------------------

if st.session_state.question:

    st.subheader("📝 Interview Question")

    st.write(st.session_state.question)

    answer = st.text_area(
        "Enter your answer:",
        height=150,
        key="candidate_answer"
    )

    if st.button("Submit Answer"):

        if not answer.strip():

            st.warning("Please enter your answer.")

        else:

            with st.spinner("AI is evaluating your answer..."):

                try:

                    prompt = f"""
                    Job Role: {role}

                    Interview Question:
                    {st.session_state.question}

                    Candidate Answer:
                    {answer}

                    Evaluate this answer.

                    Provide:
                    1. Score out of 10.
                    2. What the candidate did well.
                    3. What needs improvement.
                    4. A better sample answer.

                    Be encouraging and suitable for a fresher.
                    """

                    feedback = ask_ai(prompt)

                    st.session_state.history.append({
                        "question": st.session_state.question,
                        "answer": answer,
                        "feedback": feedback
                    })

                    st.subheader("📊 AI Evaluation")
                    st.markdown(feedback)

                    st.success("Your answer has been evaluated!")

                except Exception as error:

                    st.error(f"AI Evaluation Error: {error}")


# -----------------------------------
# NEXT QUESTION
# -----------------------------------

if st.button("Next Interview Question"):

    with st.spinner("Generating next question..."):

        try:

            previous_questions = [
                item["question"]
                for item in st.session_state.history
            ]

            prompt = f"""
            Generate ONE new interview question.

            Job Role: {role}
            Difficulty: {difficulty}

            Avoid repeating these questions:
            {previous_questions}

            Return only the question.
            """

            st.session_state.question = ask_ai(prompt)

            # Clear previous answer input
            if "candidate_answer" in st.session_state:
                del st.session_state["candidate_answer"]

        except Exception as error:

            st.error(f"AI Error: {error}")


# -----------------------------------
# INTERVIEW HISTORY
# -----------------------------------

st.divider()

st.subheader("📚 Interview History")

if st.session_state.history:

    for index, item in enumerate(
        st.session_state.history, start=1
    ):

        with st.expander(f"Question {index}"):

            st.write("Question:", item["question"])

            st.write("Your Answer:", item["answer"])

            st.markdown(item["feedback"])

else:

    st.info("Your interview history will appear here.")
