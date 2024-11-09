from openai import OpenAI
import streamlit as st

st.title("ChatGPT-like clone")

client = OpenAI()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if "box" in prompt.lower() and "surface area" in prompt.lower():
            response = (
                "It sounds like you're working on a problem involving maximizing the volume of a box with a given surface area. "
                "Let's break it down step by step. You mentioned a box with a square base and a maximum surface area of 500 cm². "
                "First, let's define the variables: let 'x' be the side length of the square base and 'h' be the height of the box. "
                "The surface area of the box is given by the formula: 2x² + 4xh = 500 cm². "
                "To maximize the volume, we need to express the volume V = x²h in terms of one variable and then find its maximum value. "
                "Where did you encounter problems in this process?"
            )
        else:
            response_placeholder = st.empty()
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)
            response_placeholder.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})