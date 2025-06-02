import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import streamlit as st

def save_to_gsheet(word, definition, example, ipa, audio_url):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)

    sheet = client.open("Vocab Diary").sheet1
    row = [word, definition, example, ipa, audio_url, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    sheet.append_row(row)

    return word_info
    else:
        return None

st.title("Vocabulary Diary")

words_input = st.text_area("Enter words (comma, space, or newline separated):")

if st.button("Fetch Word Details"):
    save_to_gsheet(word, definition, example_sentence, ipa, audio_url)
    st.success("✅ Word saved to your Vocab Diary!")
    words = [word.strip() for word in words_input.replace(',', ' ').split()]
    word_details = [fetch_word_details(word) for word in words if fetch_word_details(word)]

    if word_details:
        df = pd.DataFrame(word_details)
        st.write(df)
    else:
        st.write("No word details found.")
Add Google Sheets integration
