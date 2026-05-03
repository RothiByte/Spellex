import streamlit as st

def homepage():
    st.title(":blue[Spellex]! 🐝")
    st.text("Hello this is a mini project i am trying to make!!! This is meant to help improve spelling.")
    
    diffculty = st.selectbox(
    "What is your preffered difficulty?",
    ("Super Easy", "Easy", "Medium","Hard","Very Hard","Extreme"),
    index = None,
    placeholder = "Select one..."
    )
    st.session_state.diffculty = diffculty

    deny = True
    if diffculty != None: deny = False

    if st.button("Start!",icon="📝",icon_position="right",disabled = deny ,type="primary"):
        st.session_state.screen = "question"
        st.rerun()

def question():
    st.title("<sample>")
    st.text("<phonetics>, <sample sentence>")
    st.audio(None)
    st.text_input("Spelling?")

def error_page():
    st.title("Error? 😵‍💫")
    
    if st.button("Return"):
        st.session_state.screen = "homepage"
        st.rerun()

def main():
    if 'session' not in st.session_state:
        st.session_state["session"] = 'created'
        st.session_state['screen'] = 'homepage'
        st.session_state['diffculty'] = None

    screen = st.session_state.screen

    if screen == 'homepage':
        homepage()
    elif screen == 'question':
        question()
    else:
        error_page()

main()