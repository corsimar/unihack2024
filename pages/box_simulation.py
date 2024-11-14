import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

import utils
utils.restrict_access("student")

import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Box Simulation", page_icon="📄", initial_sidebar_state="collapsed", layout='wide')
st.markdown(
    """
<style>
    [data-testid="stBaseButton-headerNoPadding"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)
hide_streamlit_style = """
<style>
.stAppHeader {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
solution = [4, 6]
problem = "A company of delivery need your help. They want to send packages and set that they want to use a maximum of 500cm^2 for the surface area of this box. Can you help them build this box that has s square base such that at the end the box has the maximum volume possible for this surface area."

# -------------------- Problem --------------------
st.title("Problem")
st.write(problem)

# Initialize session state for width and height if not already set
if "width" not in st.session_state:
    st.session_state.width = 2.00
if "height" not in st.session_state:
    st.session_state.height = 5.00
if 'slider_height' not in st.session_state:
    st.session_state.slider_height = 10.00  # Valoare inițială a slider-ului
if 'slider_width' not in st.session_state:
    st.session_state.slider_width = 7.32  # Valoare inițială a slider-ului
if "title" not in st.session_state:
    st.session_state.title= f"Lateral area is {(2 * st.session_state.slider_width ** 2 + 4 * st.session_state.slider_width * st.session_state.slider_height):.2f} cm^2 <br>Volume is {(st.session_state.slider_width * st.session_state.slider_width * st.session_state.slider_height):.2f} cm^3"

# def update_curr_width():
#     current_width = width_slider
#     return current_width
# def update_curr_height():
#     return height_slider

# -------------------- A little help --------------------
st.title("Visualize the problem")
st.write("Play with the sliders to estimate what are the answers")
# def update_slider_width():
#     st.session_state.slider_width = (-2*height_slider + np.sqrt(2*height_input**2 + 1000)) / 2 

# def update_slider_height():
#     st.session_state.slider_height = (250 - width_slider**2)/(2*width_slider)

width_slider = st.slider("Width", 1.00, 20.00)
height_slider = st.slider("Height", 1.00, 20.00)

st.session_state.title= f"Lateral area is {(2 * width_slider ** 2 + 4 * width_slider * height_slider):.2f} cm^2 <br>Volume is {(width_slider * width_slider * height_slider):.2f} cm^3"

# -------------------- 3D cube --------------------
# Define the vertices of the parallelepiped
x = [0, width_slider, width_slider, 0, 0, width_slider, width_slider, 0]
y = [0, 0, width_slider, width_slider, 0, 0, width_slider, width_slider]
z = [0, 0, 0, 0, height_slider, height_slider, height_slider, height_slider]

# Define the surfaces (each list defines a rectangular face)
faces = [
    [0, 1, 2, 3],  # Bottom face
    [4, 5, 6, 7],  # Top face
    [0, 1, 5, 4],  # Side face 1
    [2, 3, 7, 6],  # Side face 2
    [1, 2, 6, 5],  # Side face 3
    [0, 3, 7, 4],  # Side face 4
]

# Create the 3D figure
fig = go.Figure()

# Plot each face of the parallelepiped
for face in faces:
    x_face = [x[vertex] for vertex in face]
    y_face = [y[vertex] for vertex in face]
    z_face = [z[vertex] for vertex in face]
    x_face.append(x[face[0]])  # Close the loop
    y_face.append(y[face[0]])
    z_face.append(z[face[0]])
    fig.add_trace(go.Scatter3d(
        x=x_face, y=y_face, z=z_face, 
        mode='lines+markers', marker=dict(size=2),
        line=dict(color='blue', width=4),
        showlegend=False
    ))

# Customize layout
fig.update_layout(
    title= st.session_state.title,
    scene=dict(
        xaxis_title="X",
        yaxis_title="Y",
        zaxis_title="Z",
        aspectmode="manual",
        aspectratio=dict(x=width_slider/height_slider, y=width_slider/height_slider, z=1),
    )
)

# Display the Plotly figure in Streamlit
plot_placeholder = st.empty()
plot_placeholder.plotly_chart(fig, use_container_width=True)

# -------------------- Give solution --------------------
st.title("Give the solution")
st.write("Write down your solutions")
width_input = np.float64(st.text_input("Width", value=st.session_state.width))
height_input = np.float64(st.text_input("Height", value=st.session_state.height))
submit_button = st.button("Submit")

# Button to update the parallelepiped
if submit_button:
    # Ensure inputs are converted to numeric types
    try:
         # Update session state with new values
        st.session_state.width = float(width_input)
        st.session_state.height = float(height_input)
    except ValueError:
        st.error("Please enter valid numeric values for both height and width.")
    if st.session_state.width == solution[0] and st.session_state.height == solution[1]:
        st.success("Excellent!")
        st.button("Next")
        #st.session_state.title = f"Volume is {(st.session_state.width * st.session_state.width * st.session_state.height):.2f} cm^3"
    else:
        st.error("Not correct :(")

st.markdown("---")

# -------------------- Explanation --------------------
st.title("Are you having troubles?")
from openai import OpenAI
import streamlit as st

# Set a maximum height for the chat input area
st.markdown(
    """
    <style>
    .stTextInput, .stButton, .stTextArea {
        max-height: 300px;
        overflow-y: auto;
    }
    .stChatMessage {
        max-height: 500px;
        overflow-y: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)


client = OpenAI()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

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
        st.session_state.messages.append({"role": "system", "content": problem})
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
        #response_placeholder.markdown(response)
    
    # Display the assistant's response
    with st.chat_message("assistant"):
        st.markdown(response)

    # Append the assistant's response to the session state messages
    st.session_state.messages.append({"role": "assistant", "content": response})