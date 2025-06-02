import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
import requests

st.write("Secrets loaded:", "gcp_service_account" in st.secrets)

def fetch_word_details(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)

    if response.status_code != 200:
        return None
    data = response.json()[0]

    # Get definition
    definition = data["meanings"][0]["definitions"][0].get("definition", "Definition not found.")

    # Get example sentence
    example = data["meanings"][0]["definitions"][0].get("example", "No example available.")

    # Get IPA
    ipa = data.get("phonetic", "")
    if not ipa:
        ipa = next((p.get("text", "") for p in data.get("phonetics", []) if "text" in p), "IPA not found.")

    # Get audio URL
    audio_url = next((p.get("audio", "") for p in data.get("phonetics", []) if "audio" in p and p["audio"]), "")

    return {
        "Word": word,
        "Definition": definition,
        "Example Sentence": example,
        "IPA": ipa,
        "Audio URL": audio_url
    }

def save_to_gsheet(word, definition, example, ipa, audio_url):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)

    sheet = client.open("Vocab Diary").sheet1
    row = [word, definition, example, ipa, audio_url, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    sheet.append_row(row)

st.title("Vocabulary Diary")

words_input = st.text_area("Enter words (comma, space, or newline separated):")

if st.button("Fetch Word Details"):
    words = [word.strip() for word in words_input.replace(',', ' ').split()]
    word_details = []

    for word in words:
        details = fetch_word_details(word)
        if details:
            word_details.append(details)
            save_to_gsheet(
                word=details["Word"],
                definition=details["Definition"],
                example=details["Example Sentence"],
                ipa=details["IPA"],
                audio_url=details["Audio URL"]
            )

    if word_details:
        df = pd.DataFrame(word_details)
        st.write(df)
        st.success("✅ Words saved to your Vocab Diary!")
    else:
        st.warning("⚠️ No word details found. Please check your input.")

