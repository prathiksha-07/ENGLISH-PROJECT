import streamlit as st
import textstat
import re
from collections import Counter

st.set_page_config(page_title="English Readability Checker", page_icon="📖")

st.title("📖 English Text Readability Level Checker")

st.write("Analyze your English text easily and check its readability level.")

# -------- TEXT INPUT --------

text = st.text_area("Enter your text here:")

# -------- FILE UPLOAD OPTION --------

uploaded_file = st.file_uploader("Or upload a text file", type=["txt"])

if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")
    st.text_area("Uploaded Text", text, height=200)

# -------- ANALYZE BUTTON --------

if st.button("Analyze Text"):

    if text.strip() == "":
        st.warning("Please enter text or upload a file.")
    
    else:

        flesch = textstat.flesch_reading_ease(text)

        # -------- SIMPLE READABILITY LEVEL --------

        st.subheader("📖 Simple Reading Level")

        if flesch >= 80:
            st.success("Very Easy – Suitable for children.")
        elif flesch >= 60:
            st.info("Easy – Suitable for most readers.")
        elif flesch >= 50:
            st.warning("Moderate – Suitable for high school students.")
        else:
            st.error("Difficult – Suitable for college or advanced readers.")

        # -------- TEXT DIFFICULTY COLOR INDICATOR --------

        st.subheader("🎯 Text Difficulty Indicator")

        if flesch >= 60:
            st.markdown("<h3 style='color:green;'>🟢 Easy to Read</h3>", unsafe_allow_html=True)
        elif flesch >= 30:
            st.markdown("<h3 style='color:orange;'>🟠 Medium Difficulty</h3>", unsafe_allow_html=True)
        else:
            st.markdown("<h3 style='color:red;'>🔴 Hard to Read</h3>", unsafe_allow_html=True)

        # -------- WORD COUNT --------

        words = text.split()
        word_count = len(words)
        st.write("Total Words:", word_count)

        # -------- SENTENCE COUNT --------

        sentences = re.split(r'[.!?]+', text)
        sentences = [s for s in sentences if s.strip() != ""]
        sentence_count = len(sentences)
        st.write("Total Sentences:", sentence_count)

        # -------- AVERAGE WORDS PER SENTENCE --------

        avg_words = word_count / sentence_count
        st.write("Average Words per Sentence:", round(avg_words,2))

        # -------- ESTIMATED READING TIME --------

        reading_time = word_count / 200
        st.write("Estimated Reading Time:", round(reading_time,2), "minutes")

        # -------- DIFFICULT WORDS --------

        st.subheader("⚠ Difficult Words")

        difficult_words = textstat.difficult_words_list(text)

        if len(difficult_words) == 0:
            st.success("No difficult words found.")
        else:
            for word in difficult_words:
                st.write(word)

        # -------- DIFFICULT WORDS HIGHLIGHTER --------

        st.subheader("🖍 Highlighted Difficult Words")

        highlighted_text = text

        for word in difficult_words:
            highlighted_text = re.sub(
                r'\b' + re.escape(word) + r'\b',
                f"<span style='background-color:yellow'>{word}</span>",
                highlighted_text,
                flags=re.IGNORECASE
            )

        st.markdown(highlighted_text, unsafe_allow_html=True)

        # -------- TOP FREQUENT WORDS --------

        st.subheader("📊 Top Frequent Words")

        clean_words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        common_words = Counter(clean_words).most_common(5)

        for word, count in common_words:
            st.write(f"{word} : {count} times")

        # -------- LONG SENTENCE DETECTOR --------

        st.subheader("📏 Long Sentence Detector")

        long_sentences = []

        for sentence in sentences:
            if len(sentence.split()) > 20:
                long_sentences.append(sentence)

        if len(long_sentences) == 0:
            st.success("No long sentences detected.")
        else:
            for s in long_sentences:
                st.warning(s.strip())

        # -------- PARAGRAPH COUNTER --------

        st.subheader("📑 Paragraph Counter")

        paragraphs = [p for p in text.split("\n") if p.strip() != ""]
        st.write("Total Paragraphs:", len(paragraphs))

        # -------- TEXT IMPROVEMENT SUGGESTIONS --------

        st.subheader("💡 Text Improvement Suggestions")

        if avg_words > 20:
            st.write("• Try shortening long sentences to improve readability.")

        if len(difficult_words) > 5:
            st.write("• Consider replacing difficult words with simpler alternatives.")

        if word_count > 300:
            st.write("• Consider splitting the text into smaller paragraphs.")

        if len(long_sentences) > 0:
            st.write("• Some sentences are too long. Breaking them into shorter ones may help.")

        if avg_words <= 20 and len(difficult_words) <= 5:
            st.success("Your text readability looks good!")

        # ================= NEW INNOVATIVE FEATURES =================

        # -------- READABILITY PROGRESS BAR --------

        st.subheader("📊 Readability Progress")

        progress_value = int(min(max(flesch,0),100))
        st.progress(progress_value)

        # -------- READING SPEED CATEGORY --------

        st.subheader("⚡ Reading Speed Category")

        if reading_time < 1:
            st.success("⚡ Quick Read")
        elif reading_time < 3:
            st.info("📖 Medium Length Read")
        else:
            st.warning("📚 Long Read")

        # -------- PASSIVE VOICE DETECTOR --------

        st.subheader("🗣 Passive Voice Detector")

        passive_words = ["was", "were", "is", "are", "been", "being"]

        passive_sentences = []

        for s in sentences:
            for word in passive_words:
                if f" {word} " in s.lower():
                    passive_sentences.append(s.strip())
                    break

        if len(passive_sentences) == 0:
            st.success("No passive voice sentences detected.")
        else:
            for s in passive_sentences:
                st.write(s)

        # -------- QUESTION SENTENCE DETECTOR --------

        st.subheader("❓ Question Sentence Detector")

        questions = re.findall(r'[^.?!]*\?', text)

        if len(questions) == 0:
            st.success("No questions found in the text.")
        else:
            for q in questions:
                st.write(q.strip())

        # -------- TEXT COMPLEXITY SCORE --------

        st.subheader("🎯 Text Complexity Score")

        complexity = (len(difficult_words) / word_count) * 100

        st.write("Complexity Score:", round(complexity,2), "%")

        st.progress(int(min(complexity,100)))

        # -------- DOWNLOAD REPORT --------

        st.subheader("⬇ Download Analysis Report")

        report = f"""
Text Analysis Report

Total Words: {word_count}
Total Sentences: {sentence_count}
Average Words per Sentence: {round(avg_words,2)}
Reading Time: {round(reading_time,2)} minutes
Paragraphs: {len(paragraphs)}
Difficult Words: {len(difficult_words)}
Complexity Score: {round(complexity,2)}%
"""

        st.download_button(
            label="Download Report",
            data=report,
            file_name="text_analysis_report.txt",
            mime="text/plain"
        )
        # ================= EXTRA INNOVATIVE FEATURES =================

        # -------- WRITING STYLE ANALYZER --------

        st.subheader("✍ Writing Style Analyzer")

        long_sentence_count = len(long_sentences)

        if long_sentence_count == 0 and len(difficult_words) <= 3:
            st.success("Your writing style is Simple and Clear.")
        elif long_sentence_count <= 2 and len(difficult_words) <= 7:
            st.info("Your writing style is Balanced and Informative.")
        else:
            st.warning("Your writing style is Complex and Academic.")

        # -------- SENTENCE LENGTH VISUALIZATION --------

        st.subheader("📊 Sentence Length Visualization")

        short_sent = 0
        medium_sent = 0
        long_sent = 0

        for s in sentences:
            length = len(s.split())

            if length <= 8:
                short_sent += 1
            elif length <= 15:
                medium_sent += 1
            else:
                long_sent += 1

        st.write("Short Sentences:", short_sent)
        st.write("Medium Sentences:", medium_sent)
        st.write("Long Sentences:", long_sent)

        st.progress(min((short_sent + medium_sent + long_sent) / 10,1.0))

        # -------- VOCABULARY RICHNESS INDICATOR --------

        st.subheader("🧠 Vocabulary Richness Indicator")

        unique_words = set(clean_words)
        vocab_richness = len(unique_words) / word_count

        st.write("Unique Words:", len(unique_words))
        st.write("Vocabulary Richness Score:", round(vocab_richness,2))

        richness_percent = int(vocab_richness * 100)
        st.progress(min(richness_percent,100))

        if vocab_richness > 0.6:
            st.success("Excellent vocabulary diversity.")
        elif vocab_richness > 0.4:
            st.info("Moderate vocabulary diversity.")
        else:
            st.warning("Vocabulary repetition detected. Try using more varied words.")