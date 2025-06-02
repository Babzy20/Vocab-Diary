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
        return None

    data = response.json()[0]

    definition = data["meanings"][0]["definitions"][0].get("definition", "Definition not found.")
    example = data["meanings"][0]["definitions"][0].get("example", "No example available.")
    ipa = data.get("phonetic", "")
    if not ipa:
        ipa = next((p.get("text", "") for p in data.get("phonetics", []) if "text" in p), "IPA not found.")
    audio_url = next((p.get("audio", "") for p in data.get("phonetics", []) if "audio" in p and p["audio"]), "")

    return {
        "Word": word,
        "Definition": definition,
        "Example Sentence": example,
        "IPA": ipa,
        "Audio URL": audio_url
    }

def create_word_doc(df):
    doc = Document()
    doc.add_heading('Vocabulary Diary', 0)

    table = doc.add_table(rows=1, cols=5)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Word'
    hdr_cells[1].text = 'Definition'
    hdr_cells[2].text = 'Example Sentence'
    hdr_cells[3].text = 'IPA'
    hdr_cells[4].text = 'Audio URL'

    for index, row in df.iterrows():
        word, definition, example, ipa, audio_url = row
        row_cells = table.add_row().cells
        row_cells[0].text = word
        row_cells[1].text = definition
        row_cells[2].text = example
        row_cells[3].text = ipa
        row_cells[4].text = f'<a href="{audio_url}">🔊 Listen</a>' if audio_url else "No audio"

    output = BytesIO()
    doc.save(output)
    return output.getvalue()

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

        # Word document download button
        doc_data = create_word_doc(df)
        st.download_button(
            label="Download as Word Document",
            data=doc_data,
            file_name='vocabulary_diary.docx',
            mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    else:
        st.warning("⚠️ No word details found. Please check your input.")


        return None

    data = response.json()[0]

    definition = data["meanings"][0]["definitions"][0].get("definition", "Definition not found.")
    example = data["meanings"][0]["definitions"][0].get("example", "No example available.")
    ipa = data.get("phonetic", "")
    if not ipa:
        ipa = next((p.get("text", "") for p in data.get("phonetics", []) if "text" in p), "IPA not found.")
    audio_url = next((p.get("audio", "") for p in data.get("phonetics", []) if "audio" in p and p["audio"]), "")

    return {
        "Word": word,
        "Definition": definition,
        "Example Sentence": example,
        "IPA": ipa,
        "Audio URL": audio_url
    }

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
    else:
        st.warning("⚠️ No word details found. Please check your input.")
