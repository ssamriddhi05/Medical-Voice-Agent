import streamlit as st

from medical_agent import ask_medical_agent
from speech import save_audio, speech_to_text
# from speech import record_audio, speech_to_text
from tts import text_to_speech


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="MediVoice AI",
    page_icon="🩺",
    layout="centered"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* ================================
   MAIN APP
================================ */

.stApp {
    background-color: #f5f7fb;
    color: #1f2937;
}

.block-container {
    max-width: 850px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* ================================
   TEXT
================================ */

h1, h2, h3, h4, h5, h6 {
    color: #111827 !important;
}

p, span, label {
    color: #1f2937 !important;
}


/* ================================
   HEADER
================================ */

.header {
    text-align: center;
    padding: 15px;
}

.logo {
    font-size: 55px;
}

.title {
    font-size: 42px;
    font-weight: 700;
    color: #111827 !important;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 18px;
    color: #4b5563 !important;
}


/* ================================
   STATUS
================================ */

.status {
    display: inline-block;
    background-color: #dcfce7;
    color: #166534 !important;
    padding: 8px 18px;
    border-radius: 20px;
    font-weight: 600;
}


/* ================================
   CARDS
================================ */

.card {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 18px;
    margin-top: 20px;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.06);
}

.card h3 {
    color: #111827 !important;
}


/* ================================
   USER MESSAGE
================================ */

.user-message {
    background-color: #eaf2ff;
    color: #1e3a8a !important;
    padding: 18px;
    border-radius: 15px;
    margin-top: 10px;
    font-size: 16px;
}

.user-message * {
    color: #1e3a8a !important;
}


/* ================================
   AI MESSAGE
================================ */

.ai-message {
    background-color: #ecfdf5;
    color: #064e3b !important;
    padding: 20px;
    border-radius: 15px;
    margin-top: 10px;
    font-size: 16px;
    line-height: 1.6;
}

.ai-message * {
    color: #064e3b !important;
}


/* ================================
   TEXT AREA
================================ */

.stTextArea textarea {
    background-color: #ffffff !important;
    color: #111827 !important;
    border: 1px solid #d1d5db !important;
    border-radius: 12px !important;
    font-size: 16px !important;
}

.stTextArea textarea::placeholder {
    color: #6b7280 !important;
}


/* ================================
   BUTTONS
================================ */

.stButton > button {
    background-color: #2563eb;
    color: white !important;
    border: none;
    border-radius: 12px;
    padding: 12px;
    font-size: 16px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #1d4ed8;
    color: white !important;
}


/* ================================
   DISCLAIMER
================================ */

.disclaimer {
    font-size: 13px;
    color: #6b7280 !important;
    text-align: center;
    margin-top: 30px;
}

.disclaimer * {
    color: #6b7280 !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="header">

<div class="logo">
🩺
</div>

<div class="title">
MediVoice AI
</div>

<div class="subtitle">
Your AI-powered Medical Information Assistant
</div>

<br>

<div class="status">
● Online
</div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# INTRODUCTION
# =========================================================

st.markdown("""
<div class="card">

<h3>👋 Welcome to MediVoice AI</h3>

<p>
Ask your medical question using your voice or type it manually.
Our AI agent will provide general medical information.
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# INPUT METHOD
# =========================================================

st.markdown("""
<div class="card">

<h3>💬 How would you like to ask?</h3>

</div>
""", unsafe_allow_html=True)


input_method = st.radio(
    "",
    [
        "⌨️ Type my question",
        "🎙️ Speak my question"
    ],
    horizontal=True
)


# =========================================================
# WRITTEN QUESTION
# =========================================================

if input_method == "⌨️ Type my question":

    st.markdown("""
    <div class="card">

    <h3>⌨️ Write your question</h3>

    </div>
    """, unsafe_allow_html=True)

    question = st.text_area(
        "Medical Question",
        placeholder=(
            "Example: What are the common symptoms of dehydration?"
        ),
        height=130,
        label_visibility="collapsed"
    )

    if st.button(
        "🩺 Ask Medical Assistant",
        use_container_width=True
    ):

        if not question.strip():

            st.warning(
                "Please enter a question first."
            )

        else:

            # =============================================
            # USER QUESTION
            # =============================================

            st.markdown("""
            <div class="card">

            <h3>🗣️ Your Question</h3>

            </div>
            """, unsafe_allow_html=True)

            st.markdown(
                f"""
                <div class="user-message">
                {question}
                </div>
                """,
                unsafe_allow_html=True
            )


            # =============================================
            # MEDICAL AGENT
            # =============================================

            with st.spinner(
                "🧠 Medical AI is thinking..."
            ):

                answer = ask_medical_agent(question)


            # =============================================
            # AI RESPONSE
            # =============================================

            st.markdown("""
            <div class="card">

            <h3>🩺 Medical Assistant</h3>

            </div>
            """, unsafe_allow_html=True)

            st.markdown(
                f"""
                <div class="ai-message">
                {answer}
                </div>
                """,
                unsafe_allow_html=True
            )


            # =============================================
            # TEXT TO SPEECH
            # =============================================

            try:

                with st.spinner(
                    "🔊 Generating voice response..."
                ):

                    audio_bytes = text_to_speech(answer)


                st.markdown("""
                <div class="card">

                <h3>🔊 Listen to Response</h3>

                </div>
                """, unsafe_allow_html=True)


                st.audio(
                    audio_bytes,
                    format="audio/mpeg"
                )


            except Exception as e:

                st.error(
                    f"Voice generation failed: {str(e)}"
                )

                print(
                    "TTS ERROR:",
                    str(e)
                )


# =========================================================
# VOICE QUESTION
# =========================================================

else:

    st.markdown("""
    <div class="card">

    <h3>🎙️ Speak your question</h3>

    <p>
    Record your medical question using your microphone.
    </p>

    </div>
    """, unsafe_allow_html=True)


    # =====================================================
    # BROWSER AUDIO RECORDER
    # =====================================================

    audio_data = st.audio_input(
        "🎙️ Record your medical question"
    )


    if audio_data is not None:

        st.success("✅ Recording completed!")

        # Play recorded audio
        st.audio(
            audio_data,
            format="audio/wav"
        )


        # =================================================
        # SAVE AUDIO
        # =================================================

        with st.spinner(
            "🔄 Understanding your speech..."
        ):

            audio_file = save_audio(
                audio_data.getvalue()
            )


            question = speech_to_text(
                audio_file
            )


        if question:

            # =============================================
            # TRANSCRIBED QUESTION
            # =============================================

            st.markdown("""
            <div class="card">

            <h3>🗣️ You said</h3>

            </div>
            """, unsafe_allow_html=True)

            st.markdown(
                f"""
                <div class="user-message">
                {question}
                </div>
                """,
                unsafe_allow_html=True
            )


            # =============================================
            # MEDICAL AGENT
            # =============================================

            with st.spinner(
                "🧠 Medical AI is thinking..."
            ):

                answer = ask_medical_agent(
                    question
                )


            # =============================================
            # AI RESPONSE
            # =============================================

            st.markdown("""
            <div class="card">

            <h3>🩺 Medical Assistant</h3>

            </div>
            """, unsafe_allow_html=True)

            st.markdown(
                f"""
                <div class="ai-message">
                {answer}
                </div>
                """,
                unsafe_allow_html=True
            )


            # =============================================
            # TEXT TO SPEECH
            # =============================================

            try:

                with st.spinner(
                    "🔊 Generating voice response..."
                ):

                    audio_bytes = text_to_speech(
                        answer
                    )


                st.markdown("""
                <div class="card">

                <h3>🔊 Listen to Response</h3>

                </div>
                """, unsafe_allow_html=True)


                st.audio(
                    audio_bytes,
                    format="audio/mpeg"
                )


            except Exception as e:

                st.error(
                    f"Voice generation failed: {str(e)}"
                )

                print(
                    "TTS ERROR:",
                    str(e)
                )
                
# =========================================================
# DISCLAIMER
# =========================================================

st.markdown("""
<div class="disclaimer">

⚠️ MediVoice AI provides general educational information
and is not a replacement for a qualified healthcare professional.

For emergencies or serious symptoms, seek immediate
professional medical care.

</div>
""", unsafe_allow_html=True)
