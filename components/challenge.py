import streamlit as st
import random
import json
import os
from datetime import datetime

DATA_FILE = "data/challenge_responses.json"
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

def load_responses():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_response(challenge, response):
    responses = load_responses()
    responses.append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "challenge": challenge,
        "response": response
    })
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(responses, file, indent=4)

challenges = [
    "🚀 Learn something new today and teach it to someone.",
    "📖 Read one chapter of a new book.",
    "💬 Have a deep conversation with someone.",
    "💡 Write down 3 things you are grateful for.",
    "🌿 Take a 10-minute mindfulness session.",
    "🎨 Create something (a drawing, a blog post, or a small project).",
    "🏋️‍♂️ Exercise for 15 minutes and stay active.",
    "🎯 Set a goal for the day and complete it."
]

quotes = [
    "🌟 **Believe you can, and you're halfway there.** – Theodore Roosevelt",
    "🚀 **Small steps lead to big changes. Keep going!**",
    "🔥 **Discipline is choosing between what you want now and what you want most.**",
    "💡 **Your future is created by what you do today, not tomorrow.**"
]

def challenge_page():
    st.markdown("""
    <h1 style='text-align: center; color: #FF5733;'>🌱 Growth Challenge of the Day</h1>
    <p style='text-align: center; font-size: 18px;'>Step out of your comfort zone and take on today's challenge! 🚀</p>
    <hr style='border: 2px solid #FFA07A;'>
    """, unsafe_allow_html=True)
    
    if "current_challenge" not in st.session_state:
        st.session_state.current_challenge = None
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎲 Generate Challenge", help="Click to get a new challenge", use_container_width=True):
            st.session_state.current_challenge = random.choice(challenges)
    
    if st.session_state.current_challenge:
        st.success(f"🔹 **Your Challenge:** {st.session_state.current_challenge}")
    
    st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)
    response = st.text_area("✏️ How did you complete this challenge? What did you learn?", "", height=150)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💾 Save Response", help="Click to save your reflection", use_container_width=True):
            if response.strip():
                save_response(st.session_state.current_challenge, response)
                st.success("✅ Your reflection has been saved!")
                st.session_state.current_challenge = None
            else:
                st.warning("⚠ Please write something before saving.")
    
    st.markdown("<hr style='border: 2px solid #FFA07A;'>", unsafe_allow_html=True)
    st.subheader("📜 Your Past Challenge Reflections")
    past_responses = load_responses()
    
    if past_responses:
        for resp in past_responses[::-1]:
            with st.expander(f"📅 {resp['date']} - {resp['challenge']}"):
                st.markdown(f"<div style='background-color: #f9f9f9; padding: 15px; border-radius: 10px; font-size: 16px;'>{resp['response']}</div>", unsafe_allow_html=True)
    else:
        st.info("No past reflections yet. Start your journey today! 🚀")
    
    st.sidebar.markdown("""
    <h3 style='text-align: center; color: #FF5733;'>💭 Today's Motivation</h3>
    """, unsafe_allow_html=True)
    st.sidebar.success(random.choice(quotes))

if __name__ == "__main__":
    challenge_page()
