import streamlit as st
import pandas as pd

st.set_page_config(page_title="Leaderboard", page_icon="📄", initial_sidebar_state="collapsed", layout='wide')
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

# Sample data
data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Brian', 'Fiona', 'George', 'Hannah', 'Ian'],
    'Score': [95, 85, 75, 65, 55, 45, 35, 25, 15, 5]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Sort the DataFrame by Score in descending order
df = df.sort_values(by='Score', ascending=False)

# Display the leaderboard

# Create columns
col1, col2, col3, col4 = st.columns([1,2,2,1])

# Display data in columns
with col2:
    st.markdown("<h2 style='text-align: center;'> Name</h2>", unsafe_allow_html=True)
    for name in df['Name']:
        if df.index[df['Name'] == name][0] % 2 == 0:
            st.markdown(f"<div style='text-align: center;'>{name}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background-color: gray; text-align: center;'>{name}</div>", unsafe_allow_html=True)

with col3:
    st.markdown("<h2 style='text-align: center;'> XP Points</h2>", unsafe_allow_html=True)
    for i, score in enumerate(df['Score']):
        if i % 2 == 0:
            st.markdown(f"<div style='text-align: center;'>{score}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align:center; background-color: gray;'>{score}</div>", unsafe_allow_html=True)
            
