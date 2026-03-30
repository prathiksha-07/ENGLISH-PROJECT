import streamlit as st
import textstat
from PyPDF2 import PdfReader

# -------------------------------
# Page Setup
# -------------------------------
st.set_page_config(page_title="Smart Readability Checker", page_icon="✨")

# -------------------------------
# Styling
# -------------------------------
st.markdown("""
<style>
.title {
    text-align: center;
    font-size: 35px;
    font-weight: bold;
    color: white;
    background: linear-gradient(to right, #4facfe, #00f2fe);
    padding: 10px;
    border-radius: 10px;
}

.box {
    padding: 15px;
    border-radius: 10px;
    margin-top: 10px;
    font-size: 18px;
}

.easy {background-color: #d4edda; color: #155724;}
.medium {background-color: #fff3cd; color: #856404;}
.hard {background-color: #f8d7da; color: #721c24;}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Title
# -------------------------------
st.markdown('<div class="title">✨ Smart Readability Checker ✨</div>', unsafe_allow_html=True)

# -------------------------------
# File Upload
# -------------------------------
uploaded_file = st.file_uploader("📂 Upload a TXT or PDF file", type=["txt", "pdf"])

text = ""

if uploaded_file is not None:
    if uploaded_file.type == "text/plain":
        text = uploaded_file.read().decode("utf-8")

    elif uploaded_file.type == "application/pdf":
        pdf = PdfReader(uploaded_file)
        for page in pdf.pages:
            text += page.extract_text()

# -------------------------------
# Manual Input
# -------------------------------

text_input = st.text_area("✍️ Enter your text:", height=150)

# -------------------------------
# Simplify Function
# -------------------------------

def simplify_text(text):
    replacements = {
        "utilize": "use",
        "assistance": "help",
        "individuals": "people",
        "numerous": "many",
        "facilitate": "help",
        "demonstrate": "show",
        "approximately": "about",
        "commence": "start",
        "terminate": "end",
        "comprehension": "understanding"
    }

    words = text.split()
    new_words = []

    for word in words:
        clean = word.lower().strip(".,!?")
        if clean in replacements:
            new_words.append(replacements[clean])
        else:
            new_words.append(word)

    return " ".join(new_words)

# -------------------------------
# Suggestions
# -------------------------------
def get_tips(text, score):
    tips = []

    if len(text.split()) > 20:
        tips.append("✂️ Try shorter sentences")

    if score < 50:
        tips.append("📘 Use simpler words")

    if "," in text:
        tips.append("🪶 Avoid too many commas")

    if len(text) > 120:
        tips.append("📏 Break into smaller sentences")

    if not tips:
        tips.append("✅ Your text is already simple!")

    return tips

def highlight_difficult_words(text):
    words = text.split()
    difficult = []

    # simple rule: long words = difficult
    for w in words:
        clean = w.strip(".,!?")
        if len(clean) > 7:  # you can adjust
            difficult.append(clean)

    highlighted_text = text

    for word in difficult:
        highlighted_text = highlighted_text.replace(
            word,
            f"<span style='color:red; font-weight:bold'>{word}</span>"
        )

    return highlighted_text, difficult

def active_to_passive(sentence):
    words = sentence.split()

    if len(words) < 3:
        return "Conversion not possible"

    subject = words[0]
    verb = words[1]
    obj = " ".join(words[2:])

    verb_map = {
        "wrote": "written",
        "eats": "eaten",
        "makes": "made",
        "builds": "built",
        "reads": "read",
        "creates": "created"
    }

    if verb in verb_map:
        return f"{obj} was {verb_map[verb]} by {subject}"
    else:
        return "Conversion not available"
    
def passive_to_active(sentence):
    words = sentence.split()

    if "by" not in words:
        return "Conversion not possible"

    try:
        by_index = words.index("by")

        obj = words[0]  # first word (object)
        subject = words[by_index + 1]  # after 'by'
        verb = words[2]  # past participle

        # simple reverse verb map
        verb_map = {
            "written": "wrote",
            "eaten": "eats",
            "made": "makes",
            "built": "builds",
            "read": "reads",
            "created": "creates"
        }

        if verb in verb_map:
            return f"{subject} {verb_map[verb]} {obj}"
        else:
            return "Conversion not available"

    except:
        return "Conversion not possible"

def statement_to_question(text):
    words = text.split()

    if len(words) < 2:
        return "Cannot convert"

    helping_verbs = ["is", "are", "was", "were", "can", "will", "should"]

    if words[1] in helping_verbs:
        return f"{words[1].capitalize()} {words[0]} {' '.join(words[2:])}?"
    else:
        return "Conversion not available"
    
def positive_to_negative(text):
    words = text.split()

    if "not" in words:
        return "Already negative"

    if len(words) > 1:
        return words[0] + " " + words[1] + " not " + " ".join(words[2:])
    else:
        return "Conversion not possible"

if st.button("🔄 Convert to Passive"):
    result = active_to_passive(text_input)
    st.write(result)

if st.button("🔁 Convert to Active"):
    result_active = passive_to_active(text_input)
    st.write(text_input)

if st.button("❓ Convert to Question"):
    q = statement_to_question(text_input)
    st.subheader("Question Form")
    st.write(q)

if st.button("➖ Convert to Negative"):
    neg = positive_to_negative(text_input)
    st.subheader("Negative Form")
    st.write(neg)

# -------------------------------
# Button
# -------------------------------
if st.button("🚀 Check Readability"):


    if text_input.strip() == "":
        st.warning("Please enter or upload text!")
    else:
        score = textstat.flesch_reading_ease(text_input)

        meter = int(min(max(score, 0), 100) / 10)

        st.subheader("📊 Readability Meter")

        st.write("🟩" * meter + "⬜" * (10 - meter))
        st.write(f"Score: {round(score,2)}")

        if score >= 70:
            level = "Easy 😊"
            cls = "easy"
        elif score >= 40:
            level = "Medium 😐"
            cls = "medium"
        else:
            level = "Hard 😵"
            cls = "hard"

        simple = simplify_text(text_input)
        tips = get_tips(text_input, score)

        # Highlight
        highlighted, difficult_words = highlight_difficult_words(text_input)

        # OUTPUT
        st.markdown(f'<div class="box {cls}">📊 Score: {round(score,2)} <br> 🎯 Level: {level}</div>', unsafe_allow_html=True)

        st.subheader("✨ Simpler Version")
        st.write(simple)

        st.subheader("🔍 Difficult Words Highlighted")
        st.markdown(highlighted, unsafe_allow_html=True)

        st.subheader("📌 Difficult Words List")
        st.write(", ".join(set(difficult_words)) if difficult_words else "No difficult words 🎉")

        st.subheader("💡 Suggestions")
        for tip in tips:
            st.write(tip)

        # ✅ CORRECT INDENTATION HERE
        result_text = f"""READABILITY RESULT

Score: {round(score,2)}
Level: {level}

Simplified Sentence:
{simple}

Difficult Words:
{", ".join(set(difficult_words))}

Suggestions:
{chr(10).join(tips)}
"""


        # ---------------- DOWNLOAD BUTTON ----------------
        st.download_button(
    label="⬇️ Download Result",
    data=result_text,
    file_name="readability_result.txt",
    mime="text/plain",
    key="download1"   # ✅ ADD THIS LINE
)
        

# Footer
st.markdown("---")