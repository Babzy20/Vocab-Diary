
import streamlit as st
import pandas as pd
import requests

def fetch_word_details(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        word_info = {
            "Word": word,
            "Part of Speech": data[0]['meanings'][0]['partOfSpeech'],
            "Pronunciation": data[0]['phonetics'][0]['text'] if data[0]['phonetics'] else '',
            "Audio Link": data[0]['phonetics'][0]['audio'] if data[0]['phonetics'] else '',
        }
        return word_info
    else:
        return None

st.title("Vocabulary Diary")

words_input = st.text_area("Enter words (comma, space, or newline separated):")

if st.button("Fetch Word Details"):
    words = [word.strip() for word in words_input.replace(',', ' ').split()]
    word_details = [fetch_word_details(word) for word in words if fetch_word_details(word)]

    if word_details:
        df = pd.DataFrame(word_details)
        st.write(df)
    else:
        st.write("No word details found.")
