import streamlit as st
import json
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# File Path
DATA_FILE = "data/journal_data.json"

def load_journal_data():
    """ Load user journal data from JSON file """
    if not os.path.exists(DATA_FILE):
        return {}
    
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def insights_page(user_data):
    """ Display journal insights including average mindset score and trends """
    
    # 🌟 **Enhanced Heading UI**
    st.markdown(
        """
        <h2 style='text-align: center; color: #FF5722;'>📊 Mindset Insights</h2>
        <hr style='border: 2px solid #FF5722; margin-top: -10px;'>
        """,
        unsafe_allow_html=True,
    )
    
    # 📝 **Introduction**
    st.markdown(
        """
        <p style='text-align:center; font-size:18px; color:white;'>
        🧠 Track your emotional progress and analyze your mindset trends over time!
        </p>
        <hr style='border: 1px dashed #FF9800;'>
        """,
        unsafe_allow_html=True,
    )
    
    reflections = user_data.get("entries", [])
    if not reflections:
        st.warning("⚠️ No journal entries found. Start writing in the **Daily Journal** to generate insights!")
        return
    
    mindset_scores = [entry["mindset_score"] for entry in reflections]
    dates = [entry["date"] for entry in reflections]
    
    avg_score = round(np.mean(mindset_scores), 2) if mindset_scores else 0
    min_score = min(mindset_scores) if mindset_scores else 0
    max_score = max(mindset_scores) if mindset_scores else 0
    
    # 📊 **Overall Statistics**
    st.subheader("📈 Overall Mindset Statistics")
    st.markdown("<hr style='border: 1px solid #FF9800;'>", unsafe_allow_html=True)

    st.markdown(f"**🔹 Average Score:** {avg_score}%")
    st.markdown(f"**🔻 Lowest Score:** {min_score}%")
    st.markdown(f"**🔺 Highest Score:** {max_score}%")
    
    st.markdown("<hr style='border: 1px dashed #FF9800;'>", unsafe_allow_html=True)
    
    # 📉 **Mindset Score Trend Chart**
    st.subheader("📊 Mindset Score Over Time")
    st.markdown("<hr style='border: 1px solid #FF9800;'>", unsafe_allow_html=True)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=dates, y=mindset_scores, marker="o", color="royalblue", linewidth=2, ax=ax)
    ax.fill_between(dates, mindset_scores, color="skyblue", alpha=0.3)
    ax.set_xlabel("Date", fontsize=12, fontweight="bold")
    ax.set_ylabel("Mindset Score (%)", fontsize=12, fontweight="bold")
    ax.set_title("Mindset Progress Over Time", fontsize=14, fontweight="bold", color="darkblue")
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.6)
    
    st.pyplot(fig)
    
    st.markdown("<hr style='border: 1px dashed #FF9800;'>", unsafe_allow_html=True)
    
    # 📅 **Recent Journal Entries**
    st.subheader("📅 Recent Journal Entries")
    st.markdown("<hr style='border: 1px solid #FF9800;'>", unsafe_allow_html=True)
    
    for entry in reflections[-5:][::-1]:
        with st.expander(f"📅 {entry['date']}", expanded=False):
            st.write(f"📝 {entry['entry']}")
            st.progress(entry["mindset_score"] / 100)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
