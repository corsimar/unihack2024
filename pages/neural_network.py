import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.graph_objects as go
from tensorflow.keras.callbacks import LambdaCallback
from tensorflow import keras
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import utils

#utils.restrict_access("student")


st.set_page_config(page_title="Neural Network", page_icon="📄", initial_sidebar_state="collapsed", layout='wide')
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
st.write("In order to complete the experiment you have to get at least 60% accuracy at training.")

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
activation_fc = st.selectbox("Activation function (2nd layer):", ["relu", "tanh", "selu"])
optimizer = st.selectbox("Optimizer:", ["adam", "sgd", "rmsprop"])
epochs = st.number_input("Epochs", min_value=1, max_value=100)

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

if st.button("Train and test the model"):
    input_len = np.array(len(st.session_state.circles[0]))
    second_len = np.array(len(st.session_state.circles[1]))
    
    model = keras.Sequential([
        keras.layers.Dense(second_len, input_shape=(input_len,), activation=activation_fc),
        keras.layers.Dense(3, activation='sigmoid')
    ])
    
    model.compile(
        optimizer=optimizer,
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    def streamlit_callback(epoch, logs):
        loss = logs['loss']
        accuracy = logs['accuracy']
        st.write(f'Epoch {epoch + 1}: Loss = {loss:.4f}, Accuracy = {accuracy:.4f}')

    # LambdaCallback to use in Keras training
    streamlit_cb = LambdaCallback(on_epoch_end=lambda epoch, logs: streamlit_callback(epoch, logs))

    st.write("Training model...")
    
    X_train = data.drop('Height', axis='columns')
    
    attributes = []
    if age_checkbox:
        attributes.append("Age")
    if gen_checkbox:
        attributes.append("Gender")
    if pha_checkbox:
        attributes.append("Parent_Height_Avg")
    if ns_checkbox:
        attributes.append("Nutrition_Score")
    if pal_checkbox:
        attributes.append("Physical_Activity_Level")
    
    X = X_train[attributes]
    y = data['Height']
    y = np.where(y < 170, 0, 
                     np.where((170 <= y) & (y <= 185), 1, 2))
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, random_state=0)
    
    X_train = np.array(X_train).reshape(-1, input_len)
    X_test = np.array(X_test).reshape(-1, input_len)
    y_train = np.array(y_train).reshape(-1)
    y_test = np.array(y_test).reshape(-1)
    
    print(X_train.shape, y_train.shape)

    history = model.fit(X_train, y_train, epochs=epochs, callbacks=[streamlit_cb])
    
    # Assuming you have already trained your model and have the 'history' object
    accuracy = history.history['accuracy']
    loss = history.history['loss']

    # Create a figure with 1 row and 2 columns (horizontal layout)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Plot Accuracy on the first subplot (left side)
    ax1.plot(range(1, len(accuracy) + 1), accuracy, label='Accuracy', color='orange')
    ax1.set_title('Accuracy Over Epochs')
    ax1.set_xlabel('Epochs')
    ax1.set_ylabel('Accuracy')
    ax1.grid(True)
    ax1.legend()

    # Plot Loss on the second subplot (right side)
    ax2.plot(range(1, len(loss) + 1), loss, label='Loss', color='blue')
    ax2.set_title('Loss Over Epochs')
    ax2.set_xlabel('Epochs')
    ax2.set_ylabel('Loss')
    ax2.grid(True)
    ax2.legend()

    # Display the plot in Streamlit
    st.pyplot(fig)
    
    y_predicted = model.predict(X_test)
    y_predicted = np.argmax(y_predicted, axis=1)
    
    accuracy = np.sum(y_predicted == y_test) / len(y_predicted)
    
    st.write(f"### Test training accuracy: {accuracy:.2f}")
    
    if accuracy >= 0.6:
        st.success("Well done! You found the optimum values")
        st.balloons()
        utils.complete_experiment(st.session_state.experiment_id)
        
if st.button("Back to dashboard"):
        utils.reset_and_navigate('pages/student_dashboard.py')
        

st.markdown("---")
st.title("How can I improve my neural network?")


from openai import OpenAI

problem = """
giving this problem: There is a dataset with data about people's heights. There are the age, gender, parent height average, nutrition score and physical activity level values that you can train the model with. At the end you have to classify people in 3 classes using these values:

class 0: people with height under 170 cm
class 1: people with height between 170-185 cm
class 2: people with height above 185 cm, note that a student can explore the data, can add more neurons, and can select an activation function, an optimizer and number of epochs. After that he can select the attributes(neurons in first layer). After that he trains and test the model with a button. 
In order to complete the experiment you have to get at least 60% accuracy at training.
I won't use any code to solve this problem, I'll just guide the student through the process.
"""
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
                "I'll guide you through this height classification experiment! Let's break down each step to help you train a model and reach that 60% training accuracy. "
            "You have a dataset with features like age, gender, parent height average, nutrition score, and physical activity level, which you'll use to predict height classes:\n"
            "- Class 0: height under 170 cm\n"
            "- Class 1: height between 170-185 cm\n"
            "- Class 2: height above 185 cm.\n"
            "\n"
            "Here's a step-by-step process:\n"
            "1. **Data Exploration**: Start by exploring the dataset to understand the distributions and relationships between features like age, nutrition, and physical activity. This can help you decide which features might be most important.\n"
            "2. **Model Configuration**: Select the number of neurons for the first layer, which will form the base of your neural network. You can add more layers and adjust the neurons to improve the model’s ability to learn.\n"
            "3. **Activation Function and Optimizer**: Choose an activation function (e.g., ReLU or sigmoid) for each layer. Try different optimizers like Adam or SGD to improve training.\n"
            "4. **Training and Epochs**: Set the number of epochs (training iterations) for the model. Generally, more epochs give the model more chances to learn patterns in the data.\n"
            "5. **Train and Test the Model**: After configuring the model, use the button to train it on your data and get a sense of its performance.\n"
            "\n"
            "To pass this experiment, aim for at least 60% accuracy. If you need further help with specific configurations or if your model’s accuracy isn’t improving, I’m here to guide you through fine-tuning!"
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