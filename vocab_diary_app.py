import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import streamlit as st
import pandas as pd

# You need to define this function or import it if it's in another file
def fetch_word_details(word):
    # Placeholder: Replace this with your actual logic to fetch word details
    return {
        "Word": word,
        "Definition": "Sample definition",
        "Example Sentence": "This is an example sentence.",
        "IPA": "/ˈsæmpəl/",
        "Audio URL": "https://example.com/audio.mp3"
    }
import requests

def fetch_word_details(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()[0]

    # Get definition
    try:
        definition = data["meanings"][0]["definitions"][0]["definition"]
    except (IndexError, KeyError):
        definition = "Definition not found."

    # Get example sentence
    try:
        example = data["meanings"][0]["definitions"][0].get("example", "No example available.")
    except (IndexError, KeyError):
        example = "No example available."

    # Get IPA
    try:
        ipa = data.get("phonetic", "IPA not found.")
    except KeyError:
        ipa = "IPA not found."

    # Get audio URL
    try:
        audio_url = data["phonetics"][0].get("audio", "")
    except (IndexError, KeyError):
        audio_url = ""

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
        st.warning("No word details found.")
