import streamlit as st
import pandas as pd
import requests

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
