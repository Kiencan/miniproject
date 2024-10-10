import streamlit as st

st.set_page_config(page_title="My Webpage", page_icon=":tada:", layout="wide")
st.sidebar.success("Select a page above.")
with st.container():
    st.subheader("Hello, my name is Kien :wave:")
    st.title("Welcome to my mini project!")

with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("What is this project?")
        st.write("##")
        st.write(
            """
            Using appropriate image processing methods to conceal the identities of objects in images. \n
            2 different methods are used:
            - Blurring faces: with a track bar to adjust the blurring levels.
            - Anonymize faces: replacing the faces with some icons.
            """
        )

st.write("---")
st.header("Which methods you want to choose?")
left, middle_left, middle_right, right = st.columns(4)

if middle_left.button("Blurring faces", type="primary"):
    st.switch_page("./pages/2_🎭_BlurringFace.py")

    
if middle_right.button("Anonymize faces", type="primary"):
    st.switch_page("./pages/3_🤖_AnonymizeFace.py")