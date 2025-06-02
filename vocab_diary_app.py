import streamlit as st
import pandas as pd
import requests
from io import BytesIO

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
        st.write(df)
        st.success("✅ Words fetched successfully!")

        # Create Excel file in memory
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Vocabulary')
            writer.save()
            processed_data = output.getvalue()

        st.download_button(
            label="Download as Excel",
            data=processed_data,
            file_name='vocabulary_diary.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    else:
        st.warning("⚠️ No word details found. Please check your input.")
