import streamlit as st
import random
import utility

#UI code
def homepage():
    st.title(":blue[Spellex]! 🐝")
    st.text("Hello this is a mini project i am trying to make!!! This is meant to help improve spelling.")
    
    difficulty = st.selectbox(
    "What is your preferred difficulty?",
    ("Super Easy", "Easy", "Medium","Hard","Very Hard","Extreme"),
    index = None,
    placeholder = "Select one...")
    
    st.session_state.difficulty = difficulty

    deny = True
    if difficulty != None: deny = False

    if st.button("Start!",icon="📝",icon_position="right",disabled = deny ,type="primary"):
        st.session_state.screen = "question"
        st.session_state.word_data = None
        st.rerun()

def question():
    difficulty = st.session_state.difficulty
    data = utility.get_ref_table(difficulty)

    #Checks if the current rerun has a word selected
    if st.session_state.word_data == None:
        index = random.randint(0,data[1] - 1)
        word = data[0][index]
        word_data = utility.get_word_detail(word)

        st.session_state.word_data = word_data

    word_data = st.session_state.word_data

    st.title(f"Spell the word!")
    st.text(word_data['sentence'])
    st.audio(None) #word_data['audio']
    
    ans, button = st.columns([3, 1])
    st.session_state.answer = ans.text_input("Spelling?").lower()

    button.space()
    if button.button("Submit",type = "primary"):
        st.session_state.screen = 'ans_check'
        st.rerun()

def ans_check():
    if st.session_state.answer == st.session_state.word_data['word']:
        st.title(":green[You got it correct!!!]")
        st.text(f"You spelled {st.session_state.word_data['word']} correctly!!")
        st.balloons()

    else:
        st.title("Oh no, its wrong...")
        st.text(f"This is the correct spelling: {st.session_state.word_data['word']}")

    col1, col2 = st.columns(2)

    if col1.button("Homepage"):
        st.session_state.screen = 'homepage'
        st.session_state.word_data = None
        st.rerun()

    if col2.button("Continue",type = "primary"):
        st.session_state.screen = 'question'
        st.session_state.word_data = None
        st.rerun()
 

def error_page():
    st.title("Error? 😵‍💫")
    
    if st.button("Return"):
        st.session_state.screen = "homepage"
        st.rerun()

#Will be accessible once I have done the moderation system
def add_word(): 
    
    with st.form('add'):
        word = st.text_input("Word")
        
        difficulty = st.selectbox(
        "Difficulty",
        ("Super Easy", "Easy", "Medium","Hard","Very Hard","Extreme"),
        index = None,
        placeholder = "Select one...")

        description = st.text_area("description")

        submit = st.form_submit_button('add')

    if submit:
        word_detail = {
        "word": word,
        "audio": "empty",
        "sentence": description,
        "difficulty": difficulty
        }

        utility.add_data(word, difficulty, word_detail)
        st.balloons()

#Main loop and initial session state declaration
def main():
    if 'session' not in st.session_state:
        st.session_state["session"] = 'created'
        st.session_state['screen'] = 'homepage'
        st.session_state['difficulty'] = None
        st.session_state['word_data'] = None
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

#Since Streamlit works by looping code every rerun there is no loops here
main()