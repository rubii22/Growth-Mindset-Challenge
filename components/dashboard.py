import streamlit as st
import json
import os
import numpy as np
import matplotlib.pyplot as plt

DATA_FILE = "data/journal_data.json"

# 📂 Load Journal Data
def load_journal_data():
    """ Load user journal data from JSON file """
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# 📊 **Dashboard Page**
def dashboard_page(user_data):
    """ Dashboard with key mindset tracking statistics """

    # 🌟 Stylish Heading
    st.markdown("""
        <h1 style='text-align: center; color: #2196F3;'>📈 Mindset Evolution Dashboard</h1>
        <hr style='border: 2px solid #2196F3; border-radius: 5px;'>
    """, unsafe_allow_html=True)
    
    st.write("### 🚀 Track your growth and see how your mindset has evolved over time!")

    # ✅ Fetch user entries
    reflections = user_data.get("entries", [])

    if not reflections:
        st.warning("⚠️ No journal entries found. Start writing in the **Daily Journal** to generate insights!")
        return

    # 📊 Extract Key Data
    mindset_scores = [entry["mindset_score"] for entry in reflections]
    dates = [entry["date"] for entry in reflections]

    avg_score = round(np.mean(mindset_scores), 2) if mindset_scores else 0
    total_entries = len(reflections)

    # 🎯 Display Key Metrics
    st.markdown("""
        <h3>📊 Key Statistics</h3>
        <hr style='border: 1.5px solid #FFC107; border-radius: 5px;'>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("📖 Total Journal Entries", total_entries)

    with col2:
        st.metric("🧠 Average Mindset Score", f"{avg_score}%")

    # 📉 Mindset Trend Graph
    st.markdown("""
        <h3>📈 Mindset Score Over Time</h3>
        <hr style='border: 1.5px solid #4CAF50; border-radius: 5px;'>
    """, unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(dates, mindset_scores, marker="o", linestyle="-", color="green", label="Mindset Score")
    ax.set_xlabel("Date")
    ax.set_ylabel("Mindset Score (%)")
    ax.set_title("Your Mindset Progress")
    ax.legend()
    ax.grid(True)
    plt.xticks(rotation=45)

    st.pyplot(fig)

    # 📥 **Save Graph as PNG**
    fig.savefig("mindset_progress.png")
    with open("mindset_progress.png", "rb") as file:
        st.download_button(label="📥 Download Graph", data=file, file_name="mindset_progress.png", mime="image/png")

    # 📌 Mood Breakdown Pie Chart
    st.markdown("""
        <h3>🎭 Mood Breakdown</h3>
        <hr style='border: 1.5px solid #F44336; border-radius: 5px;'>
    """, unsafe_allow_html=True)

    positive = sum(1 for score in mindset_scores if score > 75)
    neutral = sum(1 for score in mindset_scores if 50 <= score <= 75)
    negative = sum(1 for score in mindset_scores if score < 50)

    fig, ax = plt.subplots()
    ax.pie([positive, neutral, negative], labels=["😊 Positive", "🙂 Neutral", "😟 Negative"], autopct="%1.1f%%", colors=["#4CAF50", "#FFC107", "#F44336"])
    ax.set_title("Your Emotional Trends")

    st.pyplot(fig)
