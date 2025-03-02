import streamlit as st
from components.journal import journal_page
from components.insights import insights_page
from components.challenge import challenge_page
from components.dashboard import dashboard_page
import random
import json
import os

DATA_FILE = "data/journal_data.json"  # File to store users' progress

# 💡 Custom Styling
st.set_page_config(
    page_title="Mindset Evolution Tracker",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ✅ Step 1: Ask for the user's name
if "username" not in st.session_state:
    st.session_state.username = None

if st.session_state.username is None:
    st.markdown("""
        <h1 style="text-align: center; color: #2E86C1;">🚀 Welcome to Mindset Evolution Tracker!</h1>
        <p style="text-align: center; font-size:18px; color: white">
        Unlock your potential, track progress, and grow daily! 🌱
        </p>
        <div style="border-bottom: 3px solid #2E86C1; width: 50%; margin: auto;"></div>
    """, unsafe_allow_html=True)

    username_input = st.text_input("👤 **Enter Your Name:**", placeholder="Type your name here...")

    if username_input:
        st.session_state.username = username_input
        st.success(f"🎉 Welcome, {st.session_state.username}! Let's get started 🚀")
        st.rerun()
    else:
        st.stop()

# 📂 Function to Load All Journal Data
def load_journal_data():
    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}

# 📂 Function to Save Journal Data
def save_journal_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

# 📥 Load existing journal data
journal_data = load_journal_data()

# 👤 Get the current user's data (or create empty if not found)
user_data = journal_data.get(st.session_state.username, {"entries": []})
journal_data[st.session_state.username] = user_data
save_journal_data(journal_data)

# 🎯 Sidebar Menu
st.sidebar.markdown("""
    <h2 style="color: #2E86C1; text-align: center;"> 🌍 Mindset Navigator</h2>
    <div style="border-bottom: 3px solid #2E86C1; width: 70%; margin: auto;"></div>
""", unsafe_allow_html=True)

menu = ["📖 Daily Journal", "📊 Insights", "💡 Growth Challenges", "📈 Dashboard"]
choice = st.sidebar.radio(" ", menu)

# 📜 Display list of all active users
st.sidebar.markdown("<h3 style='color: #2E86C1;'>📜 Active Users</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<div style='border-bottom: 1px solid #ddd;'></div>", unsafe_allow_html=True)

for user in journal_data.keys():
    st.sidebar.markdown(f"- ✅ {user}")

st.sidebar.markdown("<div style='border-bottom: 1px solid #ddd;'></div>", unsafe_allow_html=True)

# 🌟 Motivational Quote of the Day
quotes = [
    "💡 Believe in yourself and all that you are!",
    "🌱 Every day is a chance to grow!",
    "🚀 Small steps lead to big achievements!",
    "🔥 Stay consistent, progress will follow!"
]
st.sidebar.markdown(f"💬 **Quote of the Day:** *{random.choice(quotes)}*")
st.sidebar.markdown("<div style='border-bottom: 1px solid #ddd;'></div>", unsafe_allow_html=True)

# 🔄 Routing to Different Pages (Pass User Data)
if choice == "📖 Daily Journal":
    journal_page(user_data, journal_data, st.session_state.username, save_journal_data)
elif choice == "📊 Insights":
    insights_page(user_data)
elif choice == "💡 Growth Challenges":
    challenge_page()
elif choice == "📈 Dashboard":
    dashboard_page(user_data)
