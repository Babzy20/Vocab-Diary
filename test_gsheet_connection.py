import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.title("🔐 Google Sheets Connection Test")

# Step 1: Check if secret is loaded
if "gcp_service_account" in st.secrets:
    st.success("✅ Secret 'gcp_service_account' is loaded.")
else:
    st.error("❌ Secret 'gcp_service_account' is missing.")
    st.stop()

# Step 2: Try connecting to Google Sheets
try:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)

    # Try opening a known spreadsheet
    sheet = client.open("Your Google Sheet Name").sheet1  # Replace with your actual sheet name
    st.success("✅ Successfully connected to Google Sheets!")
    st.write("📄 First row of the sheet:", sheet.row_values(1))
except Exception as e:
    st.error(f"❌ Failed to connect to Google Sheets: {e}")
