import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# Adjust the parameters for stronger correlation
m1, m2, m3, m4, m5 = -2, -3, 8, 2, 1  # Higher absolute values for stronger influence on y
b = 10  # Adjusted y-intercept
noise_level = 0.3  # Reduced noise for a clearer relationship

np.random.seed(0)

# Generate random values for x1, x2, and x3
n_points = 100
max_value = 10
x1_values = np.random.uniform(0, max_value, n_points)
x2_values = np.random.uniform(0, max_value, n_points)
x3_values = np.random.uniform(0, max_value, n_points)
x4_values = np.random.uniform(0, max_value, n_points)
x5_values = np.random.uniform(0, max_value, n_points)

x1_values += np.random.normal(0, 1, n_points)
x2_values += np.random.normal(0, 1, n_points)
x3_values += np.random.normal(0, 1, n_points)
x4_values += np.random.normal(0, 1, n_points)
x5_values += np.random.normal(0, 1, n_points)

# Calculate y with reduced noise and increased weights
noise = np.random.normal(0, noise_level, n_points)
y_values = m1 * x1_values + m2 * x2_values + m3 * x3_values + m4 * x4_values + m5 * x4_values + b + noise

# Create a DataFrame to hold the data
data = pd.DataFrame({
    'x1': x1_values,
    'x2': x2_values,
    'x3': x3_values,
    'x4': x4_values,
    'x5': x5_values,
    'y': y_values
})

# Show the dataset in Streamlit
st.title("Visualise data")
st.write(data)

# Calculate and display the correlation matrix
corr_matrix = data.corr()

# Plot the correlation matrix as a heatmap
fig, ax = plt.subplots()
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax)

# Show the correlation matrix plot in Streamlit
st.write("### Visualise how correlated the columns are to y")

if st.button("Plot correlation matrix"):
    st.pyplot(fig)
    
st.title("Train the model")
st.write("One of the ways to measure how good predictions your model is going to make is the R^2 coefficient. Try to get the maximum R^2 you can at training before testing the model.")

options = ['x1', 'x2', 'x3', 'x4', 'x5']
selected_attribute = st.select_slider("Choose a variable:", options=options)

lr_degree = st.number_input("Select the degree of the linear regression", min_value=1)

if st.button("Train the model"):
    # Generate test data
    x_values = np.random.uniform(0, 10, n_points)
    y_values = m1 * x_values + m2 * x_values + m3 * x_values + m4 * x_values + m5 * x_values + b + noise
    
    test_data = pd.DataFrame({
        "x": x_values,
        "y": y_values
    })

    X_train = PolynomialFeatures(lr_degree, include_bias=False).fit_transform(np.array(data[selected_attribute]).reshape(-1, 1))
    lr = LinearRegression()
    lr.fit(X_train, data['y'])
    
    fig, ax = plt.subplots()
    plt.scatter(X_train[:, 0], data['y'])
    x_linspace = np.linspace(np.min(X_train[:, 0]), np.max(X_train[:, 0]), 100).reshape(-1, 1)
    x = PolynomialFeatures(lr_degree, include_bias=False).fit_transform(x_linspace)
    plt.plot(x_linspace, np.dot(lr.coef_, x.T) + lr.intercept_, color='red')
    st.pyplot(fig)
    
    actual_training_r2 = lr.score(X_train, data['y'])
    st.metric(label="R² for training", value=f"{actual_training_r2}")
    # st.write(lr.score(np.array(test_data['x']).reshape(-1, 1), test_data['y']))

st.title("Test the model")