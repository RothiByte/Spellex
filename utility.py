import streamlit as st
from supabase import create_client

#Creates a client object to access supabase tables
@st.cache_resource #Prevents duplicates due to multiple users 
def connect():
    global client

    URL = st.secrets.Supabase.URL
    KEY = st.secrets.Supabase.KEY
    client = create_client(URL,KEY)

#Gets a reference table depending on the difficulty 
@st.cache_data(ttl=3600)
def get_ref_table(difficulty):
    diffList = ["Super Easy", "Easy", "Medium","Hard","Very Hard","Extreme"]
    diffNum = diffList.index(difficulty)
    response = client.table("Word_Table").select("Word").eq("Difficulty",diffNum).execute()
    
    wordList = []
    length = 0

    #API output was messy so I reconstructed it in a more code friendly way
    for data in response.data:
        wordList.append(data["Word"])
        length += 1
    
    return wordList, length

@st.cache_data(ttl=120)
def get_word_detail(word):
    response = client.table("Word_Table").select("Word_details").eq("Word",word).execute()

    return response.data[0]["Word_details"]


def add_data(word, difficulty, word_detail):
    diffList = ["Super Easy", "Easy", "Medium","Hard","Very Hard","Extreme"]
    diffNum = diffList.index(difficulty)
    
    client.table("Word_Table").insert([
        {
            "Word": word,
            "Difficulty": diffNum,
            "Word_details": word_detail
        }
    ]).execute()

#Used to hash the password in the future development
def hash(string):
    #To be built
    return string

#Auto runs the connect function
connect()