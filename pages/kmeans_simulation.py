import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

st.title("Problem")
st.write("The marketing HR of a company needs your help. They have a set of clients and would like to classify them in 3 categories in order to understand better their needs. Do you think you can help them?")

st.title("Try to cluster the clients yourself")

# Set random seed for reproducibility
np.random.seed(0)

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

# # Number of buttons per row
# buttons_per_row = 10
# total_buttons = 30

# # Create 9 columns (since 45 / 5 = 9 rows)
# cols = st.columns(buttons_per_row)

# # Loop to create 45 buttons in total
# for i in range(total_buttons):
#     col = cols[i % buttons_per_row]  # Distribute buttons across columns
#     if col.button(f"P{i + 1}"):
#         update_color(i)
        
if 'colors' not in st.session_state:
    st.session_state.colors = ['gray'] * len(data['Age'])  # Initial colors set to blue

# Create the Plotly scatter plot
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=data['Age'], y=data['Salary'], mode='markers+text',
    marker=dict(color=st.session_state.colors, size=12),
    text=[f'{i+1}' for i in range(len(data['Age']))],
    textposition='bottom center',  # Position the text directly under each point
    hoverinfo='text',
))

fig.update_layout(
    xaxis_title="Age",  # Label for x-axis
    yaxis_title="Annual Salary",  # Label for y-axis
)

if "button_number" not in st.session_state:
    st.session_state.button_number = 0
if 'button_text' not in st.session_state:
    st.session_state.button_text = f"P{st.session_state.button_number + 1}" # Initial text is P1 (the first point)
    
cols = st.columns(3)
if cols[0].button("Previous point"):
    if st.session_state.button_number > 0:
        st.session_state.button_number -= 1
    st.session_state.button_text = f"P{st.session_state.button_number + 1}"
    
    st.rerun()

if cols[1].button(st.session_state.button_text):
    update_color(st.session_state.button_number)
    st.rerun()

if cols[2].button("Next button"):
    if st.session_state.button_number < 30:
        st.session_state.button_number += 1
    st.session_state.button_text = f"P{st.session_state.button_number + 1}"
    
    st.rerun()

# Display the plot
st.plotly_chart(fig)

st.title("Use KMeans to cluster")

# Button to show labels and cluster centers
if st.button('Run KMeans'):
    # Number of clusters (you can change this as needed)
    n_clusters = 3

    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(data)

    # Get the cluster labels for each point
    labels = kmeans.labels_

    # Get the coordinates of the cluster centers
    centers = kmeans.cluster_centers_

    # Create the Plotly scatter plot with labels and cluster centers
    fig = go.Figure()

    # Plot the data points, color them by their cluster label
    fig.add_trace(go.Scatter(
        x=data['Age'], y=data['Salary'], mode='markers',  # Plot points as markers with text
        marker=dict(color=labels, size=12, colorscale='Viridis'),
        text=[f'{i}' for i in range(len(data['Age']))],  # Text for each point (index)
        textposition='bottom center',  # Position the text under each point
        hoverinfo='text',
        showlegend=False
    ))
    
    fig.update_layout(
        xaxis_title="Age",  # Label for x-axis
        yaxis_title="Annual Salary",  # Label for y-axis
    )


    # Plot the cluster centers
    fig.add_trace(go.Scatter(
        x=centers[:, 0], y=centers[:, 1], mode='markers', 
        marker=dict(symbol='circle', size=12, color='red'),
        name='Cluster Centers',
    ))

    # Display the plot with labels and cluster centers
    st.plotly_chart(fig)
    
st.markdown("---")

st.title("Do you want to know how KMeans works?")
st.button("Ask AI")