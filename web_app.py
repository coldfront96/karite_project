import streamlit as st
from chatbot.bot import EnglishTeachingBot

# Configure the page to look like a mobile app
st.set_page_config(page_title="Karite Tutor", page_icon="🌺", layout="centered")

st.title("🌺 Karite English Tutor")

# Initialize the Bot in the session state so it remembers progress between clicks
if "bot" not in st.session_state:
    st.session_state.bot = EnglishTeachingBot(save_path=".progress.json")
    st.session_state.chat_history = [
        {"role": "assistant", "content": st.session_state.bot.greet()}
    ]

# Render the sidebar for visual controls
with st.sidebar:
    st.header("Navigation")
    if st.button("Menu"):
        response = st.session_state.bot.handle("menu")
        st.session_state.chat_history.append({"role": "assistant", "content": response})
    if st.button("Check Progress"):
        response = st.session_state.bot.handle("progress")
        st.session_state.chat_history.append({"role": "assistant", "content": response})
    st.markdown("---")
    st.markdown("Type commands like `start`, `next`, or `quiz` in the chat, or switch to conversational mode to chat freely!")

# Render the chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process through our existing AI/Logic bridge
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.bot.handle(prompt)
            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
