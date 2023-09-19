# First
import openai , dotenv , os
import streamlit as st
from audio_recorder_streamlit import audio_recorder as st_audio_recorder
from streamlit_chat import message
dotenv.load_dotenv()

openai_api_key = os.environ.get("OPENAI_API")
openai.api_key = openai_api_key

image_path = "static/img/0.png"
style = """
<style>
        img {
            border-radius: 10%;
            width:70%;
        }
        .stAudioRecorder .stAudioRecorder-controls::before {
        display: flex;
        justify-content: center;
    }
</style>
"""

with st.sidebar:
    st.title("Alita - The AI ChatBot",anchor="center")
    st.image(image_path, caption="Hey I am Alita , Start talk with me",use_column_width=True)
    col1,col2,col3 = st.columns(3)
    with col2:
        recorded_audio = st_audio_recorder(key="audio_recorder",text='',neutral_color="#ffffff")
    '''
    * Hey there, My name is Alita
    * I can Talk with you
    * I can Generates image for you
    * I am eager to hear your voice
    * Start to talk with me :)

    Powered by <p Codesperfect
    '''
st.session_state.setdefault('past',[])
st.session_state.setdefault('generated',[])
st.session_state.setdefault('isVoice',False)
st.markdown(style,unsafe_allow_html=True)
st.title("Chat,Talk and Generate Images")

chat_placeholder = st.empty()
with chat_placeholder.container(): 
    i =  len(st.session_state['generated']) -1   
    
    if i >= 0:
        message(st.session_state['past'][i],is_user=True, key=f"{i}_user")
        message(
                    st.session_state['generated'][i]['data'], 
                    key=f"{i}", 
                    allow_html=True,
                    is_table=True if st.session_state['generated'][i]['type']=='table' else False
                )

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": os.environ.get("GENE")}]
    st.chat_message("Alita").write("Hey i am Alita, You can chat with me and you can speak with me.")

if recorded_audio != None:
        st.session_state["isVoice"] = True
        with open("out.mp3","wb") as f:
            f.write(recorded_audio)
            recorded_audio = None
        with open("out.mp3","rb") as f:
            try:
                transcribe = openai.Audio.transcribe("whisper-1", f)
                prompt = transcribe['text']
                if len(st.session_state.messages) > 1:
                    st.chat_message("Alita").write(st.session_state.messages[-2]['content'])
                st.session_state.messages.append({"role": "user", "content": prompt})
                message(st.session_state.messages[-1]['content'],is_user=True)
                response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
                msg = response.choices[0].message
                if msg['content'][0:11] == "THISISDALLE":
                    message("Generating ...",is_user=False,allow_html=True)
                    PROMPT = msg['content'][12:]
                    response = openai.Image.create(
                        prompt=PROMPT,
                        n=1,
                        size="256x256"
                    )
                    img_path = response["data"][0]["url"]
                    toshow = f'<img width="100%" height="200" src="{img_path}"/>'
                    message(toshow,is_user=False,allow_html=True)
                    message(f"This is image for '{PROMPT}'",is_user=False,allow_html=True)
                else:
                    message(msg['content'],is_user=False,allow_html=True)
                st.session_state.messages.append(msg)
            except:
                st.chat_message("Alita").write("Difficult to understand")

prom = st.chat_input(placeholder="Your message",key='inp')
if prom:

    if not st.session_state["isVoice"]:
        if len(st.session_state.messages) > 1:
            st.chat_message("Alita").write(st.session_state.messages[-2]['content'])
        st.session_state.messages.append({"role": "user", "content": prom})
        message(st.session_state.messages[-1]['content'],is_user=True)
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg = response.choices[0].message
        if msg['content'][0:11] == "THISISDALLE":
            message("Generating ...",is_user=False,allow_html=True)
            PROMPT = msg['content'][12:]
            response = openai.Image.create(
                        prompt=PROMPT,
                        n=1,
                        size="256x256"
                    )
            img_path = response["data"][0]["url"]
            toshow = f'<img width="100%" height="200" src="{img_path}"/>'
            message(toshow,is_user=False,allow_html=True)
            message(f"This is image for '{PROMPT}'",is_user=False,allow_html=True)
        else:
            message(msg['content'],is_user=False,allow_html=True)
        st.session_state.messages.append(msg)
    st.session_state["isVoice"] = False
