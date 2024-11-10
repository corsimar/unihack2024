import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go
import tensorflow as tf
from tensorflow import keras

# Inițializăm starea aplicației pentru cercuri în fiecare coloană
if 'circles' not in st.session_state:
    st.session_state.circles = {
        0: [0.5],      # Coloană 1 cu un cerc inițial
        1: [0.5],      # Coloană 2 cu un cerc inițial
        2: [0.5, 0.5, 0.5]  # Coloană 3 cu trei cercuri inițiale
    }
    
if 'inputs' not in st.session_state:
    st.session_state.inputs = [1, 0, 0, 0, 0]

# Inițializăm starea valorilor pentru săgeți
if 'arrows' not in st.session_state:
    st.session_state.arrows = {
        (i, j): 1 for i in range(3) for j in range(3)  # Valorile săgeților (1 pentru toate)
    }

st.title("Problem")
st.write("There is a dataset with data about people's heights. There are the age, gender, parent height average, nutrition score and physical activity level values that you can train the model with. At the end you have to classify people in 3 classes using these values:")
st.markdown("- **class 0**: people with height under 170 cm")
st.markdown("- **class 1**: people with height between 170-185 cm")
st.markdown("- **class 2**: people with height above 185 cm")

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

data = generate_data(100)
st.title("Learn more about the data")
if st.button("Explore data"):
    st.write(data)
    pairplot = sns.pairplot(data)
    st.pyplot(pairplot)

# Funcție pentru a crea o figură cu toate cercurile și săgețile între coloane
def create_circle_figure(circles_by_column, arrows_values):
    # print(st.session_state.inputs)
    fig = go.Figure()

    colors = ["blue", "green", "red"]  # Câte o culoare diferită pentru fiecare coloană
    circle_positions = {0: [], 1: [], 2: []}  # Păstrăm pozițiile cercurilor pentru a trasa săgeți

    # Adăugăm cercurile din fiecare coloană pe grafic
    names = ["Age", "Gender", "Parent Height Average", "Nutrition Score", "Physical Acticity Level"]
    max_y_position = 10  # Poziția maximă de sus pe verticală
    for col_idx, circles in circles_by_column.items():
        # Calculăm offset-ul pentru alinierea cercurilor pe coloană
        y_offset = 2 if col_idx == 2 else 0  # Coloana 3 va fi centrată mai jos

        if col_idx == 0:
            #for i, radius in enumerate(circles):
            for i in range(len(st.session_state.inputs)):
                if st.session_state.inputs[i] == 0:
                    continue
                
                x = col_idx * 3  # Coloanele sunt distanțate orizontal
                y = max_y_position - i * 2 - y_offset  # Coloana 3 are un offset mai jos
                fig.add_trace(go.Scatter(
                    x=[x], y=[y], mode='markers+text', marker=dict(size=30, color=colors[col_idx]), text=names[i], textposition="middle left",
                    name=f"Circle {col_idx + 1}-{i + 1}", hoverinfo='skip'  # Dezactivăm hover pe cercuri
                ))
                circle_positions[col_idx].append((x, y))  # Salvăm poziția cercului
        else:
            class_texts = ["< 170 cm", "170-185 cm", "> 185 cm"]
            for i, radius in enumerate(circles):
                x = col_idx * 3  # Coloanele sunt distanțate orizontal
                y = max_y_position - i * 2 - y_offset  # Coloana 3 are un offset mai jos
                if col_idx == 2:
                    fig.add_trace(go.Scatter(
                        x=[x], y=[y], mode='markers+text', marker=dict(size=30, color=colors[col_idx]),
                        name=f"Circle {col_idx + 1}-{i + 1}", text=class_texts[i], textposition="middle right", hoverinfo='skip'  # Dezactivăm hover pe cercuri
                    ))
                else:
                    fig.add_trace(go.Scatter(
                        x=[x], y=[y], mode='markers+text', marker=dict(size=30, color=colors[col_idx]),
                        name=f"Circle {col_idx + 1}-{i + 1}", hoverinfo='skip'  # Dezactivăm hover pe cercuri
                    ))
                circle_positions[col_idx].append((x, y))  # Salvăm poziția cercului

    # Adăugăm săgeți între cercurile din coloana 1 și 2 și între coloana 2 și 3
    annotations = []
    for i, pos1 in enumerate(circle_positions[0]):  # Din fiecare cerc din coloana 1
        for j, pos2 in enumerate(circle_positions[1]):  # Către fiecare cerc din coloana 2
            x0, y0 = pos1
            x1, y1 = pos2
            # Plasăm doar un singur text la mijlocul săgeții
            mid_x = (x0 + x1) / 2
            mid_y = (y0 + y1) / 2
            annotations.append(dict(
                x=x1, y=y1, ax=x0, ay=y0,
                xref="x", yref="y", axref="x", ayref="y",
                showarrow=True, arrowhead=2, arrowsize=1,
                arrowcolor="white", 
                hovertext=f"Arrow Value: {arrows_values.get((i, j), 1)}",  # Textul care va apărea la hover
            ))

    for i, pos2 in enumerate(circle_positions[1]):  # Din fiecare cerc din coloana 2
        for j, pos3 in enumerate(circle_positions[2]):  # Către fiecare cerc din coloana 3
            x0, y0 = pos2
            x1, y1 = pos3
            # Plasăm doar un singur text la mijlocul săgeții
            mid_x = (x0 + x1) / 2
            mid_y = (y0 + y1) / 2
            annotations.append(dict(
                x=x1, y=y1, ax=x0, ay=y0,
                xref="x", yref="y", axref="x", ayref="y",
                showarrow=True, arrowhead=2, arrowsize=1,
                arrowcolor="white", 
                hovertext=f"Arrow Value: {arrows_values.get((i, j), 1)}",  # Textul care va apărea la hover
            ))

    # Adăugăm săgețile ca `annotations` la grafic
    fig.update_layout(
        annotations=annotations,
        xaxis=dict(range=[-1, 8]),
        yaxis=dict(range=[-1, max_y_position + 1]),
        showlegend=False,
    )

    return fig

st.title("Train the model")

# Interfața cu butoane pentru fiecare coloană
cols = st.columns(3)
for col_idx in range(3):
    if col_idx == 1:
        with cols[col_idx]:
            if col_idx < 2:
                if len(st.session_state.circles[col_idx]) < 5:
                    if st.button(f"Add neuron"):
                        st.session_state.circles[col_idx].append(0.5)  # Adaugă un cerc cu rază 0.5 în coloană
                        st.rerun()
                
                if len(st.session_state.circles[col_idx]) > 1:
                    if st.button(f"Remove neuron"):
                        st.session_state.circles[col_idx].pop()  # Elimină ultimul cerc din coloană
                        st.rerun()
                        
                point_number = len(st.session_state.circles[0])

# Creăm și afișăm graficul cu toate cercurile și săgețile
fig = create_circle_figure(st.session_state.circles, st.session_state.arrows)
st.plotly_chart(fig)

# # -------------------- Selectbox ----------------------
st.selectbox("Activation function (2nd layer):", ["relu", "tanh", "selu"])
st.selectbox("Optimizer:", ["adam", "sgd", "rmsprop"])

def attributes_checked():
    checked_attributes = 0
    
    if age_checkbox: 
        checked_attributes += 1
    if gen_checkbox:
        checked_attributes += 1
    if pha_checkbox:
        checked_attributes += 1
    if ns_checkbox:
        checked_attributes += 1
    if pal_checkbox:
        checked_attributes += 1
        
    return checked_attributes


names = ["Age", "Gender", "Parent Height Average", "Nutrition Score", "Physical Activity Level"]

def select_input(checkbox):
    if checkbox == "age":
        if not age_checkbox:
            st.session_state.circles[0].append(0.5)  # Adaugă un cerc cu rază 0.5 în coloană
            st.session_state.inputs[0] = 1
        else:
            st.session_state.inputs[0] = 0
            st.session_state.circles[0] = st.session_state.circles[0][1:] # Adaugă un cerc cu rază 0.5 în coloană
    if checkbox == "gender":
        if not gen_checkbox:
            st.session_state.circles[0].append(0.5)  # Adaugă un cerc cu rază 0.5 în coloană
            st.session_state.inputs[1] = 1
        else:
            st.session_state.inputs[1] = 0
            st.session_state.circles[0] = st.session_state.circles[0][:1] + st.session_state.circles[0][2:] # Adaugă un cerc cu rază 0.5 în coloană
    if checkbox == "pha":
        if not pha_checkbox:
            st.session_state.circles[0].append(0.5)  # Adaugă un cerc cu rază 0.5 în coloană
            st.session_state.inputs[2] = 1
        else:
            st.session_state.inputs[2] = 0
            st.session_state.circles[0] = st.session_state.circles[0][:2] + st.session_state.circles[0][3:] # Adaugă un cerc cu rază 0.5 în coloană
    if checkbox == "ns":
        if not ns_checkbox:
            st.session_state.circles[0].append(0.5)  # Adaugă un cerc cu rază 0.5 în coloană
            st.session_state.inputs[3] = 1
        else:
            st.session_state.inputs[3] = 0
            st.session_state.circles[0] = st.session_state.circles[0][:3] + st.session_state.circles[0][4:] # Adaugă un cerc cu rază 0.5 în coloană
    if checkbox == "pal": 
        if not pal_checkbox:
            st.session_state.circles[0].append(0.5)  # Adaugă un cerc cu rază 0.5 în coloană
            st.session_state.inputs[4] = 1
        else:
            st.session_state.inputs[4] = 0
            st.session_state.circles[0] = st.session_state.circles[0][:-1] # Adaugă un cerc cu rază 0.5 în coloană

age_checkbox = st.checkbox(names[0], value=True, on_change=lambda: select_input("age"))
gen_checkbox = st.checkbox(names[1], on_change=lambda: select_input("gender"))
pha_checkbox = st.checkbox(names[2], on_change=lambda: select_input("pha"))
ns_checkbox = st.checkbox(names[3], on_change=lambda: select_input("ns"))
pal_checkbox = st.checkbox(names[4], on_change=lambda: select_input("pal"))

if st.button("Train the model"):
    input_len = np.array(len(st.session_state.circles[0]))
    second_len = np.array(len(st.session_state.circles[1]))
    
    # model = keras.Sequential([
    #     keras.layers.Dense(second_len, input_shape=(input_len,), activation)
    # ])