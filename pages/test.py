import streamlit as st
import numpy as np
import pandas as pd

# Set up parameters for the linear equation
m1, m2, m3 = 2, -3, 1  # Slopes for each attribute (x1, x2, x3)
b = 5  # y-intercept
noise_level = 1  # Standard deviation of noise

# Generate random values for x1, x2, and x3 (e.g., 100 points each)
n_points = 100
x1_values = np.random.uniform(0, 10, n_points)
x2_values = np.random.uniform(0, 10, n_points)
x3_values = np.random.uniform(0, 10, n_points)

# Calculate target variable y based on a linear combination of x1, x2, x3 with noise
noise = np.random.normal(0, noise_level, n_points)
y_values = m1 * x1_values + m2 * x2_values + m3 * x3_values + b + noise

# Create a DataFrame to hold the data
data = pd.DataFrame({
    'x1': x1_values,
    'x2': x2_values,
    'x3': x3_values,
    'y': y_values
})

# Show the first few rows of the dataset in Streamlit
st.write(data)  # Display the full DataFrame in Streamlit

# Optional: You can also show the first few rows for a quick preview
# st.write(data.head())  # Displays only the first few rows
