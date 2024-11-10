import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_absolute_error, mean_squared_error
from openai import OpenAI
import utils

utils.restrict_access("student")


st.title("Problem")
st.write("A company wants your help. It has some data collected and wants to predict new data based on the data they are giving you. If you can get a coefficient of R^2 higher than 98% you are going to get a job at this company. To complete this experiment you have to get at least a value of 0.6 for R^2 for testing data.")

st.title("Train the model")
st.write("In order for your model to make predictions you have to train with some data provided by the company.")

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
    y_pred = lr.predict(X_train)
    
    st.metric(label="R² for training", value=f"{actual_training_r2:.4f}")
    st.metric(label="Mean Absolute Error (MAE)", value=f"{mean_absolute_error(data['y'], y_pred):.4f}")
    st.metric(label="Mean Squared Error (MSE)", value=f"{mean_squared_error(data['y'], y_pred):.4f}")

st.title("Test the model")
st.write("Testing data is some data that the model has never seen before.")

if st.button("Test the model"):
    # Generate test data
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
    
    noise = np.random.normal(0, noise_level, n_points)
    y_values = m1 * x1_values + m2 * x2_values + m3 * x3_values + m4 * x4_values + m5 * x4_values + b + noise
    
    test_data = pd.DataFrame({
        'x1': x1_values,
        'x2': x2_values,
        'x3': x3_values,
        'x4': x4_values,
        'x5': x5_values,
        'y': y_values
    })
    
    X_train = PolynomialFeatures(lr_degree, include_bias=False).fit_transform(np.array(data[selected_attribute]).reshape(-1, 1))
    lr = LinearRegression()
    lr.fit(X_train, data['y'])
    
    fig, ax = plt.subplots()
    plt.scatter(test_data[selected_attribute], test_data['y'])
    X_test = np.array(test_data[selected_attribute])
    x_linspace = np.linspace(np.min(X_test), np.max(X_test), 100).reshape(-1, 1)
    x = PolynomialFeatures(lr_degree, include_bias=False).fit_transform(x_linspace)
    plt.plot(x_linspace, np.dot(lr.coef_, x.T) + lr.intercept_, color='red')
    st.pyplot(fig)
    
    X_test = PolynomialFeatures(lr_degree, include_bias=False).fit_transform(np.array(test_data[selected_attribute]).reshape(-1, 1))
    actual_testing_r2 = lr.score(X_test, test_data['y'])
    y_pred = lr.predict(X_test)
    
    st.metric(label="R² for testing", value=f"{actual_testing_r2}")
    st.metric(label="Mean Absolute Error (MAE)", value=f"{mean_absolute_error(data['y'], y_pred):.4f}")
    st.metric(label="Mean Squared Error (MSE)", value=f"{mean_squared_error(data['y'], y_pred):.4f}")
    
    if actual_testing_r2 > 0.6:
        pass
    
st.markdown("---")
st.title("How can I improve my linear regression model?")

problem = "A company wants your help. It has some data collected and wants to predict new data based on the data they are giving you. If you can get a coefficient of R^2 higher than 98% you are going to get a job at this company."
what_to_solve= "Train the model to get the maximum R^2 you can at training before testing the model."
how_to_use="Choose a variable and the degree of the linear regression. Train the model and test it."


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
                "I will explain how to do this experiment, not the coding part."
                "Let's break it down step by step. The company has provided you with some data, and your task is to train a model to predict new data. "
                "To achieve this, you need to maximize the R² coefficient during training. "
                "Start by choosing a variable from the provided options and selecting the degree of the polynomial regression. "
                "Then, train the model using the selected variable and degree. "
                "After training, you can test the model with new data to see how well it performs. "
                "If you need further assistance, let me know where you are encountering problems in this process."
            )
        else:
            response_placeholder = st.empty()
            st.session_state.messages.append({"role": "system", "content": problem+" "+what_to_solve+" "+how_to_use})
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