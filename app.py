
import json
import streamlit as st
import ollama

st.set_page_config(
    page_title="Communicate AI",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

MODEL = "llama3.2:1b"

# -------------------- DESIGN --------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f8f7ff 0%, #f4f7ff 55%, #fff8fc 100%);
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e9e7f5;
    }

    .hero {
        padding: 32px;
        border-radius: 24px;
        background: linear-gradient(120deg, #44318d, #7160ce, #a18bdf);
        color: white;
        margin-bottom: 24px;
    }

    .hero h1 {
        color: white;
        font-size: 38px;
        margin-bottom: 10px;
    }

    .hero p {
        color: #f2edff;
        font-size: 16px;
    }

    .feature-card {
        background: white;
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #ece9f8;
        min-height: 135px;
        margin-bottom: 12px;
    }

    .feature-card h4 {
        color: #43317f;
        margin-bottom: 8px;
    }

    .feature-card p {
        color: #6d6b7b;
        font-size: 14px;
    }

    div[data-testid="stTextArea"] textarea {
        border-radius: 14px;
        border: 1px solid #ddd7f3;
        background: white;
    }

    .section-heading {
        color: #302452;
        font-size: 23px;
        font-weight: 700;
        margin: 12px 0;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(100deg, #5944b5, #8069db);
        border: none;
        color: white;
        border-radius: 12px;
        min-height: 46px;
        font-weight: 600;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #ece9f8;
        padding: 16px;
        border-radius: 15px;
    }
</style>
""", unsafe_allow_html=True)


# -------------------- AI FUNCTIONS --------------------
def call_ollama(prompt, system_message=None, json_mode=False):
    messages = []

    if system_message:
        messages.append({
            "role": "system",
            "content": system_message
        })

    messages.append({
        "role": "user",
        "content": prompt
    })

    arguments = {
        "model": MODEL,
        "messages": messages,
        "options": {
            "temperature": 0.2,
            "num_predict": 500
        }
    }

    if json_mode:
        arguments["format"] = "json"

    response = ollama.chat(**arguments)
    return response["message"]["content"].strip()


def get_instruction(mode, tone):
    instructions = {
        "Improve Tone": f"Rewrite the text in a {tone.lower()} tone.",
        "Correct Grammar": "Correct grammar, spelling and punctuation.",
        "Improve Clarity": "Make the message clear, natural and easy to understand.",
        "Make It Shorter": "Make the message concise without losing important meaning.",
        "Expand My Message": "Expand the message naturally without inventing facts.",
        "Improve Vocabulary": "Improve vocabulary while keeping the language natural.",
        "Write an Email": f"Convert this into a well-structured {tone.lower()} email.",
        "Prepare an Interview Answer": (
            "Improve this as a clear, structured interview answer. "
            "Do not invent personal experiences or achievements."
        )
    }
    return instructions[mode]


def analyze_communication(text):
    prompt = f"""
Evaluate this written message fairly from 0 to 100 for:
clarity, grammar, politeness, professionalism and conciseness.

Understand informal language and common idioms in context.
For example, "crack an interview" means succeed in an interview.
Scores are estimates, not objective measurements.

Return only JSON in this format:
{{
  "clarity": 80,
  "grammar": 80,
  "politeness": 80,
  "professionalism": 80,
  "conciseness": 80,
  "strengths": ["Specific strength", "Another strength"],
  "improvements": ["Practical suggestion", "Another suggestion"]
}}

Use integer scores from 0 to 100.
Give two or three strengths and suggestions.

Message:
{text}
"""

    result = call_ollama(
        prompt,
        system_message="You are a fair communication coach. Return valid JSON only.",
        json_mode=True
    )

    report = json.loads(result)
    metrics = [
        "clarity", "grammar", "politeness",
        "professionalism", "conciseness"
    ]

    for key in metrics:
        value = report.get(key)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("The AI returned an invalid score.")
        if not 0 <= value <= 100:
            raise ValueError("The AI returned a score outside 0–100.")
        report[key] = round(value)

    for key in ["strengths", "improvements"]:
        if not isinstance(report.get(key), list):
            report[key] = []

    report["overall"] = round(
        sum(report[key] for key in metrics) / len(metrics)
    )
    return report


# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.markdown("## 💬 Communicate AI")
    st.caption("Your personal communication coach")
    st.divider()

    mode = st.selectbox(
        "Choose a tool",
        [
            "Improve Tone",
            "Correct Grammar",
            "Improve Clarity",
            "Make It Shorter",
            "Expand My Message",
            "Improve Vocabulary",
            "Write an Email",
            "Prepare an Interview Answer",
            "Communication Quality Score"
        ]
    )

    tone = st.selectbox(
        "Preferred tone",
        ["Professional", "Polite", "Friendly", "Confident", "Natural", "Academic"]
    )

    st.divider()
    st.markdown("**Powered by**")
    st.caption("Python · Streamlit · Local Ollama")
    st.caption("Your text is processed using your local model.")


# -------------------- HERO --------------------
st.markdown("""
<div class="hero">
    <h1>Say it better. Be understood. ✨</h1>
    <p>Your AI-powered writing and communication workspace.</p>
    <p>Improve your words, strengthen your confidence, and communicate with clarity.</p>
</div>
""", unsafe_allow_html=True)


# -------------------- FEATURE CARDS --------------------
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="feature-card">
        <h4>✍️ Write better</h4>
        <p>Improve grammar, tone, vocabulary and clarity.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="feature-card">
        <h4>🎯 Speak confidently</h4>
        <p>Prepare professional messages and interview answers.</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="feature-card">
        <h4>📊 Understand your writing</h4>
        <p>Evaluate communication quality and discover areas to improve.</p>
    </div>
    """, unsafe_allow_html=True)


# -------------------- INPUT --------------------
st.markdown('<div class="section-heading">✍️ Your message</div>',
            unsafe_allow_html=True)

text = st.text_area(
    "Enter text to improve",
    placeholder="Example: Hello sir, I will not be able to attend today's meeting because I have an appointment.",
    height=180,
    label_visibility="collapsed"
)

if text.strip():
    col1, col2 = st.columns(2)
    col1.caption(f"📝 {len(text.split())} words")
    col2.caption(f"🔤 {len(text)} characters")


# -------------------- RUN ACTION --------------------
button_label = (
    "📊 Analyze communication"
    if mode == "Communication Quality Score"
    else "✨ Improve my communication"
)

if st.button(button_label, type="primary", use_container_width=True):
    if not text.strip():
        st.warning("Please enter a message first.")

    else:
        try:
            with st.spinner("Your AI communication coach is working..."):

                if mode == "Communication Quality Score":
                    report = analyze_communication(text)

                    st.divider()
                    st.markdown("## 📊 Your communication report")

                    st.metric("Overall quality score", f'{report["overall"]}/100')
                    st.progress(report["overall"] / 100)

                    labels = {
                        "clarity": "Clarity",
                        "grammar": "Grammar",
                        "politeness": "Politeness",
                        "professionalism": "Professionalism",
                        "conciseness": "Conciseness"
                    }

                    columns = st.columns(5)

                    for column, (key, label) in zip(columns, labels.items()):
                        with column:
                            st.metric(label, f'{report[key]}/100')
                            st.progress(report[key] / 100)

                    left, right = st.columns(2)

                    with left:
                        st.markdown("### ✅ Your strengths")
                        for item in report["strengths"]:
                            st.markdown(f"- {item}")

                    with right:
                        st.markdown("### 💡 Areas to improve")
                        for item in report["improvements"]:
                            st.markdown(f"- {item}")

                    st.caption(
                        "Scores are AI-generated estimates and should be "
                        "used as guidance, not as an objective test."
                    )

                else:
                    prompt = f"""
Task: {get_instruction(mode, tone)}

Rewrite the user's message while preserving its intended meaning.
Understand common idioms in context. "Crack an interview" commonly
means succeed in an interview.
Do not invent personal facts or achievements.
Return only the improved message.

Original message:
{text}
"""

                    result = call_ollama(
                        prompt,
                        system_message=(
                            "You are a helpful writing coach. "
                            "Understand harmless expressions in context."
                        )
                    )

                    st.divider()
                    st.markdown("## ✨ Your improved message")

                    left, right = st.columns(2)

                    with left:
                        st.markdown("### Original")
                        st.text_area(
                            "Original text",
                            value=text,
                            height=220,
                            disabled=True
                        )

                    with right:
                        st.markdown("### Improved")
                        st.text_area(
                            "Improved text",
                            value=result,
                            height=220,
                            key="improved_result"
                        )

                    st.download_button(
                        "⬇️ Download improved text",
                        data=result,
                        file_name="improved_message.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                    with st.expander("📘 Explain the improvements"):
                        explanation = call_ollama(
                            f"""
Compare the original and improved text.
Explain up to three important changes in simple English.
Do not invent changes.

Original: {text}
Improved: {result}
""",
                            system_message="You explain writing improvements accurately."
                        )
                        st.write(explanation)

        except json.JSONDecodeError:
            st.error("The AI returned an invalid report. Please try again.")

        except Exception as error:
            st.error(
                "Something went wrong. Check that Ollama is running "
                "and the llama3.2:1b model is installed."
            )
            with st.expander("Technical details"):
                st.code(str(error))


# -------------------- FOOTER --------------------
st.divider()
st.caption(
    "Communicate AI · Built with Python, Streamlit and Ollama · "
    "Local AI communication assistance"
)
