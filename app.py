import streamlit as st
import random
import pandas as pd
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Growth Mindset Challenge",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Motivational quotes
MOTIVATIONAL_QUOTES = [
    "The only limit to our realization of tomorrow is our doubts of today. – Franklin D. Roosevelt",
    "You are never too old to set another goal or to dream a new dream. – C.S. Lewis",
    "Believe you can and you're halfway there. – Theodore Roosevelt",
    "It does not matter how slowly you go as long as you do not stop. – Confucius",
    "Success is not final, failure is not fatal: It is the courage to continue that counts. – Winston Churchill",
    "The only way to achieve the impossible is to believe it is possible. – Charles Kingsleigh",
    "Don't watch the clock; do what it does. Keep going. – Sam Levenson",
    "The future belongs to those who believe in the beauty of their dreams. – Eleanor Roosevelt",
    "The only person you are destined to become is the person you decide to be. – Ralph Waldo Emerson",
    "The secret of getting ahead is getting started. – Mark Twain"
]

# Initialize session state
if "goals" not in st.session_state:
    st.session_state.goals = []
if "progress_data" not in st.session_state:
    st.session_state.progress_data = {}
if "habits" not in st.session_state:
    st.session_state.habits = {}
if "points" not in st.session_state:
    st.session_state.points = 0
if "badges" not in st.session_state:
    st.session_state.badges = []
if "emotions" not in st.session_state:
    st.session_state.emotions = []

# Sidebar for user authentication and theme
with st.sidebar:
    st.title("Settings ⚙️")
    # Theme selector
    theme = st.selectbox("Choose Theme", ["Light", "Dark"])
    if theme == "Dark":
        st.markdown("<style>body {color: white; background-color: #0E1117;}</style>", unsafe_allow_html=True)
    # User authentication
    st.subheader("User Login 🔒")
    username = st.text_input("Enter your username:")
    if username:
        st.success(f"Welcome, {username}!")

# App title and description
st.title("Growth Mindset Challenge 🚀")
st.write("Track your goals, stay motivated, and achieve greatness!")

# Add a new goal
st.header("Add a New Goal ✍️")
new_goal = st.text_input("Enter your growth mindset goal:")
if st.button("Add Goal"):
    if new_goal:
        st.session_state.goals.append(new_goal)
        st.session_state.progress_data[new_goal] = []
        st.success(f"Goal added: '{new_goal}'")
    else:
        st.error("Please enter a goal.")

# Display motivational quote
st.header("Today's Motivational Quote 💪")
quote = random.choice(MOTIVATIONAL_QUOTES)
st.info(quote)

# Progress tracker for each goal
st.header("Track Your Progress 📊")
if st.session_state.goals:
    for goal in st.session_state.goals:
        st.subheader(f"Goal: {goal}")
        progress = st.slider(f"Update progress for '{goal}':", 0, 100, key=f"slider_{goal}")
        if st.button(f"Update Progress for '{goal}'", key=f"update_{goal}"):
            st.session_state.progress_data[goal].append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), progress))
            st.session_state.points += 10  # Award points for updating progress
            st.success(f"Progress for '{goal}' updated to {progress}%!")
        # Display progress chart
        if st.session_state.progress_data[goal]:
            progress_df = pd.DataFrame(st.session_state.progress_data[goal], columns=["Date", "Progress"])
            st.line_chart(progress_df.set_index("Date"))
        # Reset progress
        if st.button(f"Reset Progress for '{goal}'", key=f"reset_{goal}"):
            st.session_state.progress_data[goal] = []
            st.success(f"Progress for '{goal}' reset!")
else:
    st.warning("No goals added yet. Add a goal to get started!")

# Habit tracker
st.header("Habit Tracker 📅")
habit = st.text_input("Enter a habit you want to track:")
if st.button("Add Habit"):
    if habit:
        st.session_state.habits[habit] = []
        st.success(f"Habit added: '{habit}'")
    else:
        st.error("Please enter a habit.")
if st.session_state.habits:
    for habit, dates in st.session_state.habits.items():
        st.subheader(f"Habit: {habit}")
        if st.button(f"Mark '{habit}' as completed today", key=f"habit_{habit}"):
            st.session_state.habits[habit].append(datetime.now().strftime("%Y-%m-%d"))
            st.session_state.points += 5  # Award points for completing a habit
            st.success(f"'{habit}' marked as completed today!")
        st.write(f"Completed on: {', '.join(dates) if dates else 'Not completed yet'}")

# Achievement badges
st.header("Achievement Badges 🏆")
if st.session_state.points >= 50 and "50 Points" not in st.session_state.badges:
    st.session_state.badges.append("50 Points")
if st.session_state.points >= 100 and "100 Points" not in st.session_state.badges:
    st.session_state.badges.append("100 Points")
if st.session_state.badges:
    st.write("You've earned the following badges:")
    for badge in st.session_state.badges:
        st.success(f"🎉 {badge}")
else:
    st.warning("Earn points by updating progress and completing habits to unlock badges!")

# Emotion tracker
st.header("Emotion Tracker 😊")
emotion = st.selectbox("How are you feeling today?", ["😊 Happy", "😢 Sad", "😡 Angry", "😌 Calm", "😴 Tired"])
if st.button("Log Emotion"):
    st.session_state.emotions.append((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), emotion))
    st.success(f"Emotion logged: {emotion}")
if st.session_state.emotions:
    st.write("Your emotion history:")
    emotion_df = pd.DataFrame(st.session_state.emotions, columns=["Date", "Emotion"])
    st.write(emotion_df)

# Daily reminder
st.header("Set a Daily Reminder ⏰")
reminder_time = st.time_input("Set a reminder time:")
if st.button("Set Reminder"):
    st.success(f"Reminder set for {reminder_time}!")
    # Simulate a reminder (for demonstration purposes)
    with st.spinner("Waiting for reminder..."):
        time.sleep(5)  # Simulate a delay
        st.balloons()
        st.success("It's time to work on your goals!")

# Export progress data
st.header("Export Your Progress 📂")
if st.button("Export Progress as CSV"):
    if st.session_state.progress_data:
        all_data = []
        for goal, progress in st.session_state.progress_data.items():
            for entry in progress:
                all_data.append([goal, entry[0], entry[1]])
        export_df = pd.DataFrame(all_data, columns=["Goal", "Date", "Progress"])
        csv = export_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="growth_mindset_progress.csv",
            mime="text/csv"
        )
    else:
        st.warning("No progress data to export.")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using [Streamlit](https://streamlit.io)")