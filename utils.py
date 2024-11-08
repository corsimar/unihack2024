import streamlit as st

def convert_objectid(doc):
    if '_id' in doc:
        doc['_id'] = str(doc['_id'])
    return doc

def reset_state():
    for key in st.session_state.keys():
        del st.session_state[key]

def reset_and_navigate(page):
    """
    Resets the given state and navigates to the specified page.
    
    Parameters:
    state (dict): The state dictionary to reset.
    page (str): The page to navigate to.
    """
    reset_state()
    st.switch_page(page)
