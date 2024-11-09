import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Function to generate synthetic data
def generate_data(n_samples):
    np.random.seed(42)
    age = np.random.randint(0, 19, n_samples)
    gender = np.random.choice([0, 1], n_samples)
    parent_height_avg = np.random.normal(170, 10, n_samples)
    nutrition_score = np.random.uniform(0.5, 1, n_samples)
    physical_activity_level = np.random.uniform(0, 1, n_samples)

    data = pd.DataFrame({
        "Age": age,
        "Gender": gender,
        "Parent_Height_Avg": parent_height_avg,
        "Nutrition_Score": nutrition_score,
        "Physical_Activity_Level": physical_activity_level
    })

    # Gender-specific height adjustment (use np.where for element-wise comparison)
    gender_height_adjustment = np.where(gender == 0, 7, 6)  # 7 for male, 6 for female

    # Generate height using a formula with some weights and noise
    data["Height"] = (
        50 + 
        5 * age + 
        gender_height_adjustment +  
        0.5 * parent_height_avg + 
        10 * nutrition_score + 
        3 * physical_activity_level + 
        np.random.normal(0, 5, n_samples)  # Adding some noise
    )

    return data

# Streamlit app setup
st.title("Synthetic Height Prediction Dataset")

# Generate and display the data
data = generate_data(100)
st.write("Generated Synthetic Data", data)