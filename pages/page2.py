import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.title("Problem")
st.write("The marketing HR of a company needs your help. They have a set of clients and would like to classify them in categories in order to understand better their needs. Do you think you can help them?")

import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic data for 3 clusters: Age and Salary
cluster_1_age = np.random.normal(loc=25, scale=5, size=10)  # Younger customers (age around 25)
cluster_1_salary = np.random.normal(loc=30000, scale=5000, size=10)  # Lower salary (~30k)

cluster_2_age = np.random.normal(loc=40, scale=7, size=10)  # Middle-aged customers (age around 40)
cluster_2_salary = np.random.normal(loc=50000, scale=10000, size=10)  # Mid-range salary (~50k)

cluster_3_age = np.random.normal(loc=60, scale=8, size=10)  # Older customers (age around 60)
cluster_3_salary = np.random.normal(loc=70000, scale=12000, size=10)  # Higher salary (~70k)

# Combine all data
ages = np.concatenate([cluster_1_age, cluster_2_age, cluster_3_age])
salaries = np.concatenate([cluster_1_salary, cluster_2_salary, cluster_3_salary])

# Create a DataFrame for the data
data = pd.DataFrame({
    'Age': ages,
    'Salary': salaries
})

if 'colors' not in st.session_state:
    st.session_state.colors = ['gray'] * len(data['Age'])  # Initial colors set to gray

# Function to update the color of a specific point
def update_color(index):
    if st.session_state.colors[index] == 'gray':
        st.session_state.colors[index] = 'red'
    elif st.session_state.colors[index] == 'red':
        st.session_state.colors[index] = 'blue'
    elif st.session_state.colors[index] == 'blue':
        st.session_state.colors[index] = 'green'
    elif st.session_state.colors[index] == 'green':
        st.session_state.colors[index] = 'gray'

if "button_number" not in st.session_state:
    st.session_state.button_number = 0
if 'button_text' not in st.session_state:
    st.session_state.button_text = f"P{st.session_state.button_number + 1}" # Initial text is P1 (the first point)
    
cols = st.columns(3)
if cols[0].button("Previous point"):
    if st.session_state.button_number > 0:
        st.session_state.button_number -= 1
    st.session_state.button_text = f"P{st.session_state.button_number + 1}"

if cols[1].button(st.session_state.button_text):
        update_color(st.session_state.button_number)

if cols[2].button("Next button"):
    if st.session_state.button_number < 30:
        st.session_state.button_number += 1
    st.session_state.button_text = f"P{st.session_state.button_number + 1}"

# Create the Plotly scatter plot
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=data['Age'], y=data['Salary'], mode='markers+text',
    marker=dict(color=st.session_state.colors, size=12),
    text=[f'{i+1}' for i in range(len(data['Age']))],
    textposition='bottom center',  # Position the text directly under each point
    hoverinfo='text',
))

# Display the plot
st.plotly_chart(fig)