import streamlit as st
from chatbot.bot import EnglishTeachingBot
from chatbot.database import DatabaseManager

# Configure the page to look like a mobile app
st.set_page_config(page_title="Karite Tutor", page_icon="🌺", layout="centered")

UI_TEXT = {
    "English": {
        "title": "🌺 Karite English Tutor",
        "nav_header": "Navigation",
        "btn_menu": "Menu",
        "btn_progress": "Check Progress",
        "review_header": "🔁 Review Topics",
        "instructions": "Type commands like `start`, `next`, or `quiz` in the chat, or switch to conversational mode to chat freely!",
        "chat_placeholder": "Type your message here...",
        "thinking": "Thinking...",
        "language_toggle": "Language / Gagana",
        "login_title": "🌺 Karite English Tutor – Login",
        "login_username": "Username",
        "login_password": "Password",
        "btn_login": "Login",
        "btn_register": "Register",
        "error_invalid": "❌ Invalid username or password.",
        "error_taken": "❌ Username already taken. Please choose another.",
        "success_register": "✅ Account created! Logging you in…",
    },
    "Samoan": {
        "title": "🌺 Karite Faiaoga Igilisi",
        "nav_header": "Fa'atautaiga (Navigation)",
        "btn_menu": "Lisi (Menu)",
        "btn_progress": "Siaki le Alualu i Luma (Progress)",
        "review_header": "🔁 Toe Iloilo Autu (Review Topics)",
        "instructions": "Ta'i i totonu upu e pei o le `start`, `next`, po'o le `quiz` i le talanoaga, pe fesuia'i i le tulaga fa'atalanoaga e talanoa saoloto ai!",
        "chat_placeholder": "Ta'i lau fe'au i'i...",
        "thinking": "Mafaufau...",
        "language_toggle": "Language / Gagana",
        "login_title": "🌺 Karite Faiaoga Igilisi – Ulufale",
        "login_username": "Igoa o le tagata fa'aoga",
        "login_password": "Upu fa'aagaga",
        "btn_login": "Ulufale (Login)",
        "btn_register": "Resitala (Register)",
        "error_invalid": "❌ Igoa po'o upu fa'aagaga sese.",
        "error_taken": "❌ O lo'o fa'aaogaina le igoa lea. Filifili se isi.",
        "success_register": "✅ Ua faia le tala! O lo'o ulufale oe…",
    }
}

# Initialize the database and login state
if "db" not in st.session_state:
    st.session_state.db = DatabaseManager()
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None
if "language" not in st.session_state:
    st.session_state.language = "English"


def _init_bot_for_user(username):
    """Create and store a bot instance loaded with the user's saved progress."""
    db = st.session_state.db
    saved_progress = db.get_progress(username)
    st.session_state.bot = EnglishTeachingBot(
        initial_progress=saved_progress if saved_progress else None,
        save_callback=lambda data: db.save_progress(username, data),
    )
    st.session_state.chat_history = [
        {"role": "assistant", "content": st.session_state.bot.greet()}
    ]


if st.session_state.logged_in_user:
    # ── Main application ────────────────────────────────────────────────
    # Ensure the bot is initialised (survives hot-reloads)
    if "bot" not in st.session_state:
        _init_bot_for_user(st.session_state.logged_in_user)

    lang = st.session_state.language

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
        
        # --- MISSING COURSE SELECTOR INJECTED HERE ---
        st.markdown("---")
        course_options = ["English", "Samoan"]
        st.session_state.target_course = st.radio(
            "Course / Kosi:", 
            options=course_options,
            index=0 if st.session_state.get("target_course", "English") == "English" else 1
        )
        
        # Sync the RAM to the Bot
        if "bot" in st.session_state:
            st.session_state.bot.ui_language = st.session_state.language
            st.session_state.bot.target_language = st.session_state.target_course

        st.markdown("---")
        st.header(UI_TEXT[lang]["nav_header"])
        if st.button(UI_TEXT[lang]["btn_menu"]):
            st.session_state.chat_history.append({"role": "user", "content": "Menu"})
            response = st.session_state.bot.handle("menu")
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()
        if st.button(UI_TEXT[lang]["btn_progress"]):
            st.session_state.chat_history.append({"role": "user", "content": "Check Progress"})
            response = st.session_state.bot.handle("progress")
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.rerun()
            
        # --- Endless Practice UI ---
        if "bot" in st.session_state:
            completed_topics = st.session_state.bot.progress.completed_topics_list()
            if completed_topics:
                st.markdown("---")
                st.subheader("🔁 Practice & Review")
                review_choice = st.selectbox("Select past topic to practice:", completed_topics)
                if st.button("Start Practice Loop"):
                    command = f"review {review_choice}"
                    st.session_state.chat_history.append({"role": "user", "content": f"Start Practice: {review_choice}"})
                    response = st.session_state.bot.handle(command)
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
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner(UI_TEXT[lang]["thinking"]):
                response = st.session_state.bot.handle(prompt)
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})

else:
    # ── Login / Register screen ─────────────────────────────────────────
    lang = st.session_state.language
    st.title(UI_TEXT[lang]["login_title"])

    with st.form("login_form"):
        username = st.text_input(UI_TEXT[lang]["login_username"])
        password = st.text_input(UI_TEXT[lang]["login_password"], type="password")
        col1, col2 = st.columns(2)
        login_clicked = col1.form_submit_button(UI_TEXT[lang]["btn_login"])
        register_clicked = col2.form_submit_button(UI_TEXT[lang]["btn_register"])

    if login_clicked:
        if not username or not password:
            st.error(UI_TEXT[lang]["error_invalid"])
        elif st.session_state.db.verify_user(username, password):
            st.session_state.logged_in_user = username
            _init_bot_for_user(username)
            st.rerun()
        else:
            st.error(UI_TEXT[lang]["error_invalid"])

    if register_clicked:
        if not username or not password:
            st.error(UI_TEXT[lang]["error_invalid"])
        elif st.session_state.db.register_user(username, password):
            st.success(UI_TEXT[lang]["success_register"])
            st.session_state.logged_in_user = username
            _init_bot_for_user(username)
            st.rerun()
        else:
            st.error(UI_TEXT[lang]["error_taken"])
