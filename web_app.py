import streamlit as st
from chatbot.bot import EnglishTeachingBot

# Configure the page to look like a mobile app
st.set_page_config(page_title="Karite Tutor", page_icon="🌺", layout="centered")

UI_TEXT = {
    "English": {
        "title": "🌺 Karite English Tutor",
        "nav_header": "Navigation",
        "btn_menu": "Menu",
        "btn_progress": "Check Progress",
        "instructions": "Type commands like `start`, `next`, or `quiz` in the chat, or switch to conversational mode to chat freely!",
        "chat_placeholder": "Type your message here...",
        "thinking": "Thinking...",
        "language_toggle": "Language / Gagana"
    },
    "Samoan": {
        "title": "🌺 Karite Faiaoga Igilisi",
        "nav_header": "Fa'atautaiga (Navigation)",
        "btn_menu": "Lisi (Menu)",
        "btn_progress": "Siaki le Alualu i Luma (Progress)",
        "instructions": "Ta'i i totonu upu e pei o le `start`, `next`, po'o le `quiz` i le talanoaga, pe fesuia'i i le tulaga fa'atalanoaga e talanoa saoloto ai!",
        "chat_placeholder": "Ta'i lau fe'au i'i...",
        "thinking": "Mafaufau...",
        "language_toggle": "Language / Gagana"
    }
}

# Initialize the Bot in the session state so it remembers progress between clicks
if "bot" not in st.session_state:
    st.session_state.bot = EnglishTeachingBot(save_path=".progress.json")
    st.session_state.chat_history = [
        {"role": "assistant", "content": st.session_state.bot.greet()}
    ]
if "language" not in st.session_state:
    st.session_state.language = "English"

# Render the sidebar for visual controls
with st.sidebar:
    languages = list(UI_TEXT.keys())
    st.selectbox(
        UI_TEXT["English"]["language_toggle"],
        options=languages,
        index=languages.index(st.session_state.language),
        key="language",
    )
    lang = st.session_state.language
    st.markdown("---")
    st.header(UI_TEXT[lang]["nav_header"])
    if st.button(UI_TEXT[lang]["btn_menu"]):
        response = st.session_state.bot.handle("menu")
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()
    if st.button(UI_TEXT[lang]["btn_progress"]):
        response = st.session_state.bot.handle("progress")
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()
    st.markdown("---")
    st.markdown(UI_TEXT[lang]["instructions"])

st.title(UI_TEXT[lang]["title"])

# Render the chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input(UI_TEXT[lang]["chat_placeholder"]):
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process through our existing AI/Logic bridge
    with st.chat_message("assistant"):
        with st.spinner(UI_TEXT[lang]["thinking"]):
            response = st.session_state.bot.handle(prompt)
            st.markdown(response)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
