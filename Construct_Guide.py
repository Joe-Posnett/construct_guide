import streamlit as st
from openai import OpenAI
from PIL import Image
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
from llama_index import SimpleDirectoryReader
import os

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Load data and create index
@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the ConstGuide knowledge base - hang tight!"):
        reader = SimpleDirectoryReader(input_dir="/Users/joeposnett/Desktop/streamlit_data", recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", embed_model='local', temperature=0.5, system_prompt="you are an expert on the Streamlit Python library and your job is to answer technical questions. Assume that all questions are related to the Streamlit Python Library. Do not hallucinate features"))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context) 
        return index

index = load_data()

# Setting up a session state (chat history) variable and selecting the GPT model to use.
if "openai_model" not in st.session_state:
    GPT_MODEL = "gpt-3.5-turbo"
    st.session_state["openai_model"] = GPT_MODEL

with st.chat_message(name="assistant", avatar="\U0001F477"):
    st.write("My name is Site-based Sam and I will be your AI construction helper")

# Initialising the chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Displaying chat messages from history on app re-run
for message in st.session_state.messages:
    role = message["role"]
    avatar = "\U0001F477" if role == "assistant" else None
    with st.chat_message(role, avatar=avatar):
        st.markdown(message["content"])

# Reacting to user input
if prompt := st.chat_input("How can I help?"):
    # Displaying user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Adding user message to chat history (session state variable)
    st.session_state.messages.append({"role": "user", "content": prompt})

# Creating a chat message container for the assistant
with st.chat_message("assistant", avatar="\U0001F477"):
    message_placeholder = st.empty()
    full_response = ""
    # Call the OpenAI API and pass the model and conversation history
    for response in client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True
    ):
        # Convert the dictionary response to a string
        response_text = response.choices[0].message.content
        full_response += response_text
        message_placeholder.markdown(full_response + "| ")

    message_placeholder.markdown(full_response)
    # Add ChatGPT response to the messages in the session state 
    st.session_state.messages.append({"role": "assistant", "content": full_response})
                                            
    

