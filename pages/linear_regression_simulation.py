import streamlit as st

st.title("Problem")
st.write("A company wants your help. It has some data collected and wants to predict new data based on the data they are giving you. If you can get a coefficient of R^2 higher than 98% you are going to get a job at this company.")

st.title("Train the model")

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Set up parameters for the linear equation
m = 2  # slope
b = 5  # y-intercept
noise_level = 2.5  # small standard deviation of noise

# Generate x values (e.g., 100 points between 0 and 10)
x_values = np.linspace(0, 10, 100)

# Generate y values with small noise
noise = np.random.normal(0, noise_level, size=len(x_values))
y_values = m * x_values + b + noise

# Create the scatter plot
fig, ax = plt.subplots()
ax.scatter(x_values, y_values, color='blue')
# ax.plot(x_values, m * x_values + b, label='True Line', color='red')

# Label the axes
ax.set_xlabel('X')
ax.set_ylabel('Y')

# Show the plot in Streamlit
st.pyplot(fig)

lr_degree = st.number_input("Degree of linear regression", min_value=1, max_value=8)

st.title("Test the model")