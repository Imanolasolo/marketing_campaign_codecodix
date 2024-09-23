from openai import OpenAI
import streamlit as st

# Layout: Logo and Title
col1, col2 = st.columns([1, 4])

with col1:
    st.image("logo.png")

with col2:    
    st.title("MarketingGPT with CodeCodix")

# Instructions section
with st.expander("Instructions"):
    st.write(''' 
             1.- Insert your API key below.

              If you don't have one, [click here to get your OpenAI API key](https://www.howtogeek.com/885918/how-to-get-an-openai-api-key/).

             2.- Tell us in the prompt area who you are and how we can help you with your marketing issues or doubts in your project.(Help in creating marketing campaings for your project, specific marketing questions, ...)

             3.- The chat will guide you in every aspect you need about marketing.
             ''')

# Input for user's API key
api_key = st.text_input("Enter your OpenAI API Key", type="password")

# Verify if the API key has been entered
if api_key:
    # Store API key in session state
    st.session_state.api_key = api_key

    # Initialize OpenAI client with the user's API key
    client = OpenAI(api_key=st.session_state.api_key)

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input for the user to enter their marketing-related prompt
    if prompt := st.chat_input("Tell us your requirements about marketing, we are here to help you!"):
        # Add user's prompt to session state messages
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user's message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response from OpenAI
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        
        # Add assistant's response to session state messages
        st.session_state.messages.append({"role": "assistant", "content": response})

else:
    st.warning("Please enter your OpenAI API Key to continue.")
