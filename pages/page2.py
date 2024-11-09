import streamlit as st
import plotly.graph_objects as go

# Inițializăm starea aplicației pentru cercuri în fiecare coloană
if 'circles' not in st.session_state:
    st.session_state.circles = {
        0: [0.5],      # Coloană 1 cu un cerc inițial
        1: [0.5],      # Coloană 2 cu un cerc inițial
        2: [0.5, 0.5, 0.5]  # Coloană 3 cu trei cercuri inițiale
    }

# Inițializăm starea valorilor pentru săgeți
if 'arrows' not in st.session_state:
    st.session_state.arrows = {
        (i, j): 1 for i in range(3) for j in range(3)  # Valorile săgeților (1 pentru toate)
    }

# Funcție pentru a crea o figură cu toate cercurile și săgețile între coloane
def create_circle_figure(circles_by_column, arrows_values):
    fig = go.Figure()

    colors = ["blue", "green", "red"]  # Câte o culoare diferită pentru fiecare coloană
    circle_positions = {0: [], 1: [], 2: []}  # Păstrăm pozițiile cercurilor pentru a trasa săgeți

    # Adăugăm cercurile din fiecare coloană pe grafic
    max_y_position = 10  # Poziția maximă de sus pe verticală
    for col_idx, circles in circles_by_column.items():
        # Calculăm offset-ul pentru alinierea cercurilor pe coloană
        y_offset = 4 if col_idx == 2 else 0  # Coloana 3 va fi centrată mai jos

        for i, radius in enumerate(circles):
            x = col_idx * 3  # Coloanele sunt distanțate orizontal
            y = max_y_position - i * 2 - y_offset  # Coloana 3 are un offset mai jos
            fig.add_trace(go.Scatter(
                x=[x], y=[y], mode='markers', marker=dict(size=30, color=colors[col_idx]),
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
        title="Cercuri și Săgeți Interactiv",
        xaxis=dict(range=[-1, 8]),
        yaxis=dict(range=[-1, max_y_position + 1]),
        showlegend=False,
        title_x=0.5,
        title_y=0.95
    )

    # if st.button("Show value"):
    #     for i, pos1 in enumerate(circle_positions[0]):  # Din fiecare cerc din coloana 1
    #         for j, pos2 in enumerate(circle_positions[1]):  # Către fiecare cerc din coloana 2
    #             st.write(f"{arrows_values.get((i, j), random(1, 10))}")

    return fig

# Interfața cu butoane pentru fiecare coloană
cols = st.columns(3)
for col_idx in range(3):
    with cols[col_idx]:
        if col_idx < 2:  # Butoane doar pentru primele două coloane
            # Butoane de adăugare și ștergere
            if len(st.session_state.circles[col_idx]) < 5:
                if st.button(f"Add Circle to Column {col_idx + 1}"):
                    st.session_state.circles[col_idx].append(0.5)  # Adaugă un cerc cu rază 0.5 în coloană
                    st.rerun()
            
            if len(st.session_state.circles[col_idx]) > 1:
                if st.button(f"Remove Circle from Column {col_idx + 1}"):
                    st.session_state.circles[col_idx].pop()  # Elimină ultimul cerc din coloană
                    st.rerun()

# Creăm și afișăm graficul cu toate cercurile și săgețile
fig = create_circle_figure(st.session_state.circles, st.session_state.arrows)
st.plotly_chart(fig)

# -------------------- Selectbox ----------------------
index1 = 0
index2 = 0
options = [f"{i}" for i in range(1, 13)]
pos1 = st.selectbox("Beginning point", options, index=index1)
pos2 = st.selectbox("End point", options, index=index2)





st.write(f"{pos1}, {pos2}")