import hashlib
import streamlit as st
from elevenlabs.client import ElevenLabs
from supabase import create_client

#Creates a supaClient object to access supabase tables
@st.cache_resource #Prevents duplicates due to multiple users 
def connect():
    SP_URL = st.secrets.Supabase.URL
    SP_KEY = st.secrets.Supabase.KEY
    TTS_KEY = st.secrets.Elevenlabs.KEY
    return create_client(SP_URL,SP_KEY), ElevenLabs(api_key=TTS_KEY)

#Gets a reference table depending on the difficulty 
@st.cache_data(ttl=3600)
def get_ref_table(difficulty):
    diffList = ["Super Easy", "Easy", "Medium","Hard","Very Hard","Extreme"]
    diffNum = diffList.index(difficulty)
    response = supaClient.table("Word_Table").select("Word").eq("Difficulty",diffNum).execute()
    
    wordList = []
    length = 0

    #API output was messy so I reconstructed it in a more code friendly way
    for data in response.data:
        wordList.append(data["Word"])
        length += 1
    
    return wordList, length

@st.cache_data(ttl=120)
def get_word_detail(word):
    response = supaClient.table("Word_Table").select("Word_details").eq("Word",word).execute()

    return response.data[0]["Word_details"]

def add_data(word, difficulty, word_detail):
    diffList = ["Super Easy", "Easy", "Medium","Hard","Very Hard","Extreme"]
    diffNum = diffList.index(difficulty)
    
    supaClient.table("Word_Table").insert([
        {
            "Word": word,
            "Difficulty": diffNum,
            "Word_details": word_detail
        }
    ]).execute()

@st.cache_data
def get_word_sound(word_data):

    request = supaClient.storage.from_("Audio").exists(f"Audio/{word_data["difficulty"]}/{word_data["word"]}.mp3")
    if request == True:
        request = supaClient.storage.from_("Audio").download(f"Audio/{word_data["difficulty"]}/{word_data["word"]}.mp3")
        return request
    else:
        sentence = word_data['sentence']
        listSentence = sentence.split("<word>")
        listSentence.insert(1,word_data["word"])
        listSentence.insert(0,word_data["word"])
        listSentence.insert(1,",")
        sentence = "".join(listSentence) 
        
        response = b"".join(TTSclient.text_to_speech.convert(
            voice_id="bIHbv24MWmeRgasZH58o",
            text=sentence,
            voice_settings={"speed": 0.91},
            output_format="mp3_44100_128"
        ))

        request = supaClient.storage.from_("Audio").upload(f"Audio/{word_data["difficulty"]}/{word_data["word"]}.mp3",response)
        return response

def hashpass(string):
    out = hashlib.sha3_512(string.encode()).hexdigest()
    return out

class user:
    username = None
    id = None
    trust = None 
    banned = False
    #User data to be added

    def password_check(self,username,password):
        
        if username == None:
            username = self.username

        response = supaClient.table("users").select("hashpass").eq("username",username).execute()
        hashValue = hashpass(password)
        print(response)
        return hashValue == response.data[0]['hashpass']
    
    def userExists(self,username):
        response = supaClient.table("users").select("username").eq("Username",username).execute()
        #to be completed

    def login(self,username,password):

        if self.password_check(username,password):

            self.username = username
            response = supaClient.table("users").select("id","trust","banned").eq("username",username).execute()
            data = response.data[0]

            self.id = data['id']
            self.trust = data['trust']
            self.banned = data['banned']

            return True
        
        else:
            return False
    
    def logout(self):
        self.username = None
        self.id = None
        self.trust = None 
        self.banned = False

    def change_password(self):
        pass

    def change_username(self):
        pass

    def trust_user(self):
        pass

    def ban_user(self):
        pass

    def isbanned(self):
        pass

    def delete_user(self,password):
        
        if self.password_check(None,password):
            
            response = supaClient.table("users").delete().eq("username",self.username).execute()
            print(response)

            return True
        
        else:
            return False

    def create_user(self,username,password,trust = None):
        hashValue = hashpass(password)
        supaClient.table("users").insert({
            
            "username":username,
            "trust":trust,
            "hashpass":hashValue
        }).execute()

    '''
    def update_userdata(self):
        pass
    
    '''

    
#Auto runs the connect function
supaClient, TTSclient = connect()