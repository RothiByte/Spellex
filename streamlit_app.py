import streamlit as st
import json
import random

@st.cache_data(ttl=60)
def sample_data():
    return json.load(open("Sample_data.json","r"))

def homepage():
    st.title(":blue[Spellex]! 🐝")
    st.text("Hello this is a mini project i am trying to make!!! This is meant to help improve spelling.")
    
    diffculty = st.selectbox(
    "What is your preffered difficulty?",
    ("Super Easy", "Easy", "Medium","Hard","Very Hard","Extreme"),
    index = None,
    placeholder = "Select one...")
    
    st.session_state.diffculty = diffculty

    deny = True
    if diffculty != None: deny = False

    if st.button("Start!",icon="📝",icon_position="right",disabled = deny ,type="primary"):
        st.session_state.screen = "question"
        st.session_state.word_obj = None
        st.rerun()

def question():
    data = sample_data()

    if st.session_state.word_obj == None:
        while True:
            word_obj = random.choice(data)
            
            if word_obj['difficulty'] == st.session_state.diffculty:
                break
        
        st.session_state.word_obj = word_obj

    word_obj = st.session_state.word_obj

    st.title(f"Spell the word: {word_obj['word']}")
    st.text(word_obj['sentence'])
    st.audio(None) #word_obj['audio']
    
    ans, button = st.columns([3, 1])
    st.session_state.answer = ans.text_input("Spelling?").lower()

    button.space()
    if button.button("Submit",type = "primary"):
        st.session_state.screen = 'ans_check'
        st.rerun()

def ans_check():
    if st.session_state.answer == st.session_state.word_obj['word']:
        st.title(":green[You got it correct!!!]")
        st.text(f"You spelled {st.session_state.word_obj['word']} correctly!!")
        st.balloons()

    else:
        st.title("Oh no, its wrong...")
        st.text(f"This is the correct spelling: {st.session_state.word_obj['word']}")

    col1, col2 = st.columns(2)

    if col1.button("Homepage"):
        st.session_state.screen = 'homepage'
        st.session_state.word_obj = None
        st.rerun()

    if col2.button("Continue",type = "primary"):
        st.session_state.screen = 'question'
        st.session_state.word_obj = None
        st.rerun()
 

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
        st.session_state['word_obj'] = None
        st.session_state['answer'] = None

    screen = st.session_state.screen

    if screen == 'homepage':
        homepage()
    elif screen == 'question':
        question()
    elif screen == 'ans_check':
        ans_check()
    else:
        error_page()

main()