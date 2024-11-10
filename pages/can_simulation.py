import streamlit as st
import numpy as np
import plotly.graph_objects as go
import utils

# Initialize session state for cylinder parameters
if "radius_visualise" not in st.session_state:
    st.session_state.radius_visualise = 1.0
if "height_visualise" not in st.session_state:
    st.session_state.height_visualise = 1.0
if "slider_min_value" not in st.session_state:
    st.session_state.slider_min_value = 1.0
if "slider_max_value" not in st.session_state:
    st.session_state.slider_max_value = 20.0
if "constraint" not in st.session_state:
    st.session_state.constraint = 330.0
if "radius" not in st.session_state:
    st.session_state.radius = 1.0
if "height" not in st.session_state:
    st.session_state.height = 5.0
if "title" not in st.session_state:
    st.session_state.title = f"Lateral area: {(2 * np.pi * st.session_state.radius_visualise + 2 * np.pi * st.session_state.radius_visualise * st.session_state.height_visualise):.2f} cm^2<br>Volume: {(np.pi * st.session_state.radius_visualise ** 2 * st.session_state.height_visualise):.2f} cm^3"

solution = [10, 20]
problem = "A company of juices needs your help. They want to sell juice at a capacity (volume) of 330mL. They wish to use as little material as possible to make the cans. Can you help them and optimize the minimum surface area needed to build such a can?" 

st.title("Problem")
st.write(problem)

st.title("Visualize the problem")

def update_height():
    st.session_state.height_visualise = height_slider
    st.session_state.title = f"Lateral area: {(2 * np.pi * st.session_state.radius_visualise + 2 * np.pi * st.session_state.radius_visualise * st.session_state.height_visualise):.2f} cm^2<br>Volume: {(np.pi * st.session_state.radius_visualise ** 2 * st.session_state.height_visualise):.2f} cm^3"
    
def update_radius():
    st.session_state.radius_visualise = radius_slider
    st.session_state.title = f"Lateral area: {(2 * np.pi * st.session_state.radius_visualise + 2 * np.pi * st.session_state.radius_visualise * st.session_state.height_visualise):.2f} cm^2<br>Volume: {(np.pi * st.session_state.radius_visualise ** 2 * st.session_state.height_visualise):.2f} cm^3"
    
radius_slider = st.slider("Radius", 1.0, 20.0, step=0.01, on_change=update_radius)
height_slider = st.slider("Height", 1.0, 20.0, step=0.01, on_change=update_height)

# Generate data for the cylinder with the updated parameters
z = np.linspace(0, st.session_state.height_visualise, 100)
theta = np.linspace(0, 2 * np.pi, 50)
theta_grid, z_grid = np.meshgrid(theta, z)
x_grid = st.session_state.radius_visualise * np.cos(theta_grid)
y_grid = st.session_state.radius_visualise * np.sin(theta_grid)

# Create the base circle (filled circle at z = 0)
theta_base = np.linspace(0, 2 * np.pi, 100)  # More points for smoothness
base_x = st.session_state.radius_visualise * np.cos(theta_base)
base_y = st.session_state.radius_visualise * np.sin(theta_base)
base_z = np.zeros_like(base_x)  # Z coordinates for the base at z = 0

# Create a mesh for the base
theta_base_grid, r_base_grid = np.meshgrid(theta_base, np.linspace(0, st.session_state.radius_visualise, 10))
base_x_grid = r_base_grid * np.cos(theta_base_grid)
base_y_grid = r_base_grid * np.sin(theta_base_grid)
base_z_grid = np.zeros_like(base_x_grid)

# Create the Plotly figure with updated parameters
fig = go.Figure(data=[
    # Cylinder surface
    go.Surface(
        x=x_grid, y=y_grid, z=z_grid, 
        colorscale="Viridis", opacity=0.7
    ),
    # Base as a filled circle at z = 0
    go.Surface(
        x=base_x_grid, y=base_y_grid, z=base_z_grid,
        colorscale="Viridis", opacity=1.0, showscale=False
    )
])

# Customize layout
fig.update_layout(
    title=st.session_state.title,
    scene=dict(
        xaxis_title="X",
        yaxis_title="Y",
        zaxis_title="Z",
    )
)

# Display the updated Plotly figure in a single container
plot_placeholder = st.empty()
plot_placeholder.plotly_chart(fig, use_container_width=True)

st.title("Give the solution")

# Render input fields for cylinder parameters
radius = np.float64(st.number_input("Enter Cylinder Radius", min_value=0.1, value=st.session_state.radius))
height = np.float64(st.number_input("Enter Cylinder Height", min_value=0.1, value=st.session_state.height))

# Button to update the cylinder parameters
if st.button("Submit"):
    # Update session state with new values
    st.session_state.radius = radius
    st.session_state.height = height
    
    if radius == solution[0] and height == solution[1]:
        st.success("Well done! You found the optimum values")
        st.balloons()
        utils.complete_experiment(st.session_state.experiment_id)
    else:
        st.error("These are not the optimum values")

if height_slider != st.session_state.height_visualise:
    update_radius()
    
if radius_slider != st.session_state.radius_visualise:
    update_height()
    
if st.button("Back to dashboard"):
            utils.reset_and_navigate('pages/student_dashboard.py')
    
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
                "It sounds like you're working on a problem involving minimizing the surface area of a cylinder with a given volume, and you want me to view nicely anything related to math, like formulas"
                "Let's break it down step by step. You mentioned a cylinder with a volume of 330 cm³. "
                "First, let's define the variables: let 'r' be the radius of the base and 'h' be the height of the cylinder. "
                "The volume of the cylinder is given by the formula: πr²h = 330 cm³. "
                "To minimize the surface area, we need to express the surface area A = 2πr² + 2πrh in terms of one variable and then find its minimum value. "
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
            response_placeholder.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

