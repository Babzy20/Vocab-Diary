import streamlit as st
import pandas as pd
import requests
from docx import Document
from io import BytesIO

# Enable wide layout
st.set_page_config(layout="wide")

st.title("Vocabulary Diary")

def fetch_word_details(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)

    if response.status_code != 200:
        return {
            "Word": word,
            "Definition": "Definition not found.",
            "Example Sentence": "No example available.",
            "IPA": "IPA not found.",
            "Audio URL": ""
        }

    try:
        data = response.json()[0]
        definition = data["meanings"][0]["definitions"][0].get("definition", "Definition not found.")
        example = data["meanings"][0]["definitions"][0].get("example", "No example available.")
        ipa = data.get("phonetic", "")
        if not ipa:
            ipa = next((p.get("text", "") for p in data.get("phonetics", []) if "text" in p), "IPA not found.")
        audio_url = next((p.get("audio", "") for p in data.get("phonetics", []) if "audio" in p and p["audio"]), "")
    except Exception:
        return {
            "Word": word,
            "Definition": "Definition not found.",
            "Example Sentence": "No example available.",
            "IPA": "IPA not found.",
            "Audio URL": ""
        }

    return {
        "Word": word,
        "Definition": definition,
        "Example Sentence": example,
        "IPA": ipa,
        "Audio URL": audio_url
    }

def create_word_document(df):
    doc = Document()
    doc.add_heading('Vocabulary Diary', 0)

    for index, row in df.iterrows():
        doc.add_heading(row['Word'], level=1)
        doc.add_paragraph(f"Definition: {row['Definition']}")
        doc.add_paragraph(f"Example Sentence: {row['Example Sentence']}")
        doc.add_paragraph(f"IPA: {row['IPA']}")
        if row['Audio URL']:
            doc.add_paragraph(f"Audio URL: {row['Audio URL']}")

    byte_io = BytesIO()
    doc.save(byte_io)
    byte_io.seek(0)
    return byte_io

words_input = st.text_area("Enter words (comma, space, or newline separated):")

if st.button("Fetch Word Details"):
    words = [word.strip() for word in words_input.replace(',', ' ').split()]
    word_details = []

    for word in words:
        details = fetch_word_details(word)
        if details:
            word_details.append(details)

    if word_details:
        df = pd.DataFrame(word_details)

        # Make audio links clickable
        df["Audio URL"] = df["Audio URL"].apply(
            lambda url: f'<a href="{url}" target="_blank">🔊 Listen</a>' if url else "No audio"
        )

        # Display the table with clickable links
        st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
        st.success("✅ Words fetched successfully!")

        # CSV download button
        st.download_button(
            label="Download as CSV",
            data=pd.DataFrame(word_details).to_csv(index=False),
            file_name='vocabulary_diary.csv',
            mime='text/csv'
        )

        # Word document download button
        word_doc = create_word_document(pd.DataFrame(word_details))
        st.download_button(
            label="Download as Word Document",
            data=word_doc,
            file_name='vocabulary_diary.docx',
            mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    else:
        st.warning("⚠️ No word details found. Please check your input.")
