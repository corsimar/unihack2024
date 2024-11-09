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
    with col1:
        st.markdown('<h2 class="header-text">Your Lessons</h2>', unsafe_allow_html=True)
    with col2:
        with stylable_container(
            key="create_lesson",
            css_styles=""" 
            button {
                margin-top: 20px;
                color: black;
                background-color: white;
            }
            button:hover {
                border: 1px transparent black;
            }
            """,
        ):
            if st.button("Create Lesson"):
                utils.reset_and_navigate("pages/lesson_editor.py")
    with col3:
        with stylable_container(
            key="logout",
            css_styles=""" 
            button {
                margin-top: 20px;
                color: white;
                background-color: red;
            }
            button:hover {
                border: 1px transparent black;
            }
            """,
        ):
            if st.button("Logout"):
                utils.logout()

    if(st.session_state.get("lessons") is None):
        with st.spinner('Loading all lessons...'):
            st.session_state["lessons"] = utils.get_lessons_dashboard()

    # Display the lessons with borders, icons, and progress
    st.markdown("""
        <style>
        html, body {
            background: linear-gradient(to bottom, #f0f0f0, #ffffff);
        }
        .lesson {
            font-size: 18px;
            margin0: 10px;
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

    if len(st.session_state["lessons"]) == 0:
        with stylable_container(
            css_styles="""
            img {
                 display: block;
  margin-right: auto;
    margin-left: 80%;
    margin-top: 10%;
            filter: brightness(0) invert(0.6);}
            .noLessons {
                text-align: center;
                font-size: 20px;
                font-weight: bold;
                color: gray;
            }
            """,
            key="no_lessons"
        ):
            st.image("https://cdn-icons-png.freepik.com/256/1466/1466623.png?semt=ais_hybrid")
            st.write('<div class="noLessons">You have no lessons yet. Click the "Create Lesson" button to get started.</div>', unsafe_allow_html=True)
    for lesson in st.session_state["lessons"]:
        with stylable_container(
            key="lesson_button",
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
                    
                    