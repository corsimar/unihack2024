import streamlit as st
import utils
from streamlit_extras.stylable_container import stylable_container 

#utils.restrict_access('professor')

with stylable_container(
    key="body",
    css_styles="""
    .stMainBlockContainer {
    background: white;
}
    """
    ):
    # Create a button at the top right
    col1, col2, col3 = st.columns([6.5, 2, 1.5])
    # Create a top bar with the name RevoLearn on the left and profile on the right
    with col2:
        if st.button("Create Lesson"):
            utils.reset_and_navigate("pages/lesson_editor.py")
    with col3:
        if st.button("Logout"):
            st.session_state.role = ""
            utils.reset_and_navigate("pages/login.py")

    if(st.session_state.get("lessons") is None):
        st.session_state["lessons"] = utils.get_lessons_dashboard()

    # Display the lessons with borders, icons, and progress
    st.markdown("""
        <style>
        html, body {
            background: linear-gradient(to bottom, #f0f0f0, #ffffff);
        }
        .lesson {
            font-size: 18px;
            border-radius: 5px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 10px;
            padding: 10px;
            border: 1px solid #ddd;
            transition: all 0.3s;
        }
        .lesson:hover {
            border: 4px solid white;
            box-shadow: 0px 0px 10px rgba(76, 175, 80, 0.5);
        }
        .lesson img {
            width: 100%;
            height: auto;
            border-radius: 5px;
        }
        .lesson-title {
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin-top: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown('<h2 class="header-text">Your Lessons</h2>', unsafe_allow_html=True)
    for lesson in st.session_state["lessons"]:
        with stylable_container(
            key="green_button",
            css_styles="""
                button {
                    color: white;
                    border-radius: 6px;
                    line-height: 25px;
                    display: flex;
                    justify-content: flex-start;
                    padding-left: 10px; /* Optional: Adds padding on the left side */
                }
                .st-emotion-cache-3lmqu2 e1nzilvr5 {
                    background-color: #4caf50;
                    color: white;
                    border-radius: 6px;
                    display: flex;
                    justify-content: flex-start;
                    padding-left: 10px; /* Optional */
                }
                """,
        ):
            @st.dialog("Preview Content")
            def preview_dialog(content):
                st.write(content)
                
            buttoncol1, buttoncol2 = st.columns([7.4,2.6])
            with buttoncol1:
                st.button(lesson['title'], use_container_width=True)
            with buttoncol2:
                innerButtonCol1, innerButtonCol2 = st.columns(2)
                with innerButtonCol1:
                    if st.button("Preview", key=f"preview{lesson['title']}"):
                        preview_dialog(lesson['content'])

                with innerButtonCol2:
                    if st.button("Delete", key=f"delete{lesson['title']}"):
                        utils.remove_lesson(lesson['_id'])
                        st.session_state["lessons"] = utils.get_lessons_dashboard()
                        st.rerun()
                    
                    