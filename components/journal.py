import streamlit as st
import json
import os
from datetime import datetime
from textblob import TextBlob

DATA_FILE = "data/journal_data.json"

# 📂 Function to Load Journal Data
def load_journal():
    """ Load journal entries from JSON file """
    if not os.path.exists(DATA_FILE):
        return {"entries": []}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"entries": []}

# 💾 Function to Save Journal Data
def save_journal(data):
    """ Save journal entries to JSON file """
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

# 📝 **Optimized Journal Page**
def journal_page(user_data, journal_data, username, save_journal_data):
    """ Journal Entry Page for a Specific User """
    
    st.markdown(
        """
        <h1 style='text-align: center; color: #4CAF50;'>📖 Mindset Journal</h1>
        <p style='text-align: center; font-size: 18px; color: white;'>
            Reflect on your day and track your emotional growth! 🌱
        </p>
        <hr style="border: 1px solid #4CAF50;">
        """,
        unsafe_allow_html=True,
    )

    # ✅ Fetch user's journal entries
    reflections = user_data.get("entries", [])

    # 📂 Sidebar - Display All Entries
    with st.sidebar:
        st.markdown("<h3>📅 Past Reflections</h3>", unsafe_allow_html=True)
        if reflections:
            for ref in reflections[::-1]:  # Show latest first
                with st.expander(f"📅 {ref['date']}"):
                    st.write(f"📝 **Entry:** {ref['entry']}")
                    st.progress(ref["mindset_score"] / 100)  # Visual progress bar
        else:
            st.warning("No reflections yet. Start journaling today! ✍️")

    # 🌟 UI Improvements: Column Layout
    col1, col2 = st.columns([2, 1])

    # 📝 Journal Entry Form (Left Side)
    with col1:
        st.markdown("<h3>✍️ Write a New Reflection</h3>", unsafe_allow_html=True)
        with st.form("journal_entry", clear_on_submit=True):
            date = datetime.now().strftime("%Y-%m-%d")
            entry = st.text_area("📝 **Write your thoughts here...**", height=150, placeholder="How was your day?")
            submitted = st.form_submit_button("💾 **Save Reflection**", use_container_width=True)

            if submitted and entry.strip():
                sentiment = TextBlob(entry).sentiment.polarity
                mindset_score = round((sentiment + 1) * 50, 2)  # Normalize score (0-100)

                # 🔹 Add entry to user's data
                reflections.append({"date": date, "entry": entry, "mindset_score": mindset_score})

                # 🔄 Update journal data and save it
                user_data["entries"] = reflections
                journal_data[username] = user_data
                save_journal_data(journal_data)

                st.success("✅ Reflection saved successfully!")
                st.rerun()

    # 📊 Mindset Insights (Right Side)
    with col2:
        st.markdown("<h3>📊 Mindset Insights</h3>", unsafe_allow_html=True)
        if reflections:
            last_entry = reflections[-1]
            st.markdown(f"**📅 Last Reflection Date:** `{last_entry['date']}`")
            st.markdown(f"**🧠 Mindset Score:** `{last_entry['mindset_score']}%`")
            st.progress(last_entry["mindset_score"] / 100)

            # 🎯 Sentiment Interpretation with Icons
            if last_entry["mindset_score"] > 75:
                st.success("😊 **You're in a great mindset! Keep up the positive energy!**")
            elif last_entry["mindset_score"] > 50:
                st.info("🙂 **You're doing well! Keep reflecting and growing!**")
            else:
                st.warning("😟 **You might need a little positivity boost. Try gratitude journaling!**")

    # 🎨 **Stylish Footer**
    st.markdown(
        """
        <hr style="border: 1px solid #ddd;">
        <p style="text-align:center; color:gray; font-size:14px;">
            🌿 **Keep reflecting, keep growing!** 
        </p>
        """,
        unsafe_allow_html=True,
    )
