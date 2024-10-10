import streamlit as st
import numpy as np
from PIL import Image
import cv2
from image_processing import icon_face
import tempfile

if st.button("Back to main page"):
    st.switch_page("./1_😎_Homepage.py")
st.title("Anonymize Faces")

menu = ["image", "video", "webcam"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "image":
    st.subheader("Upload your image here:")
    # Upload file
    img_file_buffer = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    show_file = st.empty()
    # Show info if no file is uploaded
    if not img_file_buffer:
        show_file.info("Please upload an image file: {}".format(" ".join(["jpg", "jpeg", "png"])))

    # Read and show image
    if img_file_buffer is not None:
        image = Image.open(img_file_buffer)
        img_array = np.array(image)
        st.image(img_array, caption="Origin Image", use_column_width=True)

    # Track bar and submit button
    with st.form("my_form"):
        option = st.selectbox(
            "Which icon do you prefer?",
            ("😀", "😂", "😈", "😍"),
        )
        if option == "😀":
            icon_img = cv2.imread("./input/face_grinning_icon.png", cv2.IMREAD_UNCHANGED)
            icon_img = cv2.cvtColor(icon_img, cv2.COLOR_BGR2RGB)
        elif option == "😂:":
            icon_img = cv2.imread("./input/face_joy_icon.png")
            icon_img = cv2.cvtColor(icon_img, cv2.COLOR_BGR2RGB)
        elif option == "😈":
            icon_img = cv2.imread("./input/smiling_imp_icon.png")
            icon_img = cv2.cvtColor(icon_img, cv2.COLOR_BGR2RGB)
        elif option == "😍":
            icon_img = cv2.imread("./input/heart_eyes_icon.png")
            icon_img = cv2.cvtColor(icon_img, cv2.COLOR_BGR2RGB)

        submit = st.form_submit_button('Submit', help="Click to processing!")

    st.subheader("Your result here:")
    if submit:
        img_array = icon_face(img_array, icon_img, detector_backend='retinaface')
        st.image(img_array, caption="Blur image", use_column_width=True)

if choice == "video":
    st.subheader("Upload your video here:")
    video_file = st.file_uploader("Upload a video", type=["mp4"])
    show_file = st.empty()
    if not video_file:
        show_file.info("Please upload a video file: {}".format(" ".join(["mp4"])))

    with st.form("my_form"):
        option = st.selectbox(
            "Which icon do you prefer?",
            ("😀", "😂", "😈", "😍"),
        )
        if option == "😀":
            icon_img = cv2.imread("./input/face_grinning_icon.png", cv2.IMREAD_UNCHANGED)
            icon_img = cv2.cvtColor(icon_img, cv2.COLOR_BGR2RGB)
        elif option == "😂:":
            icon_img = cv2.imread("./input/face_joy_icon.png")
            icon_img = cv2.cvtColor(icon_img, cv2.COLOR_BGR2RGB)
        elif option == "😈":
            icon_img = cv2.imread("./input/smiling_imp_icon.png")
            icon_img = cv2.cvtColor(icon_img, cv2.COLOR_BGR2RGB)
        elif option == "😍":
            icon_img = cv2.imread("./input/heart_eyes_icon.png")
            icon_img = cv2.cvtColor(icon_img, cv2.COLOR_BGR2RGB)
            
        submit = st.form_submit_button('Submit', help="Click to processing!")

    st.subheader("Your result here:")
    if submit:
        tfile = tempfile.NamedTemporaryFile(delete=False) 
        if video_file is not None:
            tfile.write(video_file.read())

        cap = cv2.VideoCapture(tfile.name)
        stframe = st.empty()

        while cap.isOpened():
            ret, frame = cap.read()
            # if frame is read correctly ret is True
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = icon_face(frame, icon_img, detector_backend='ssd')
            stframe.image(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    
if choice == "webcam":
    if st.button("Turn on your camera!"):
        with st.form("my_form"):
            option = st.selectbox(
                "Which icon do you prefer?",
                ("😀", "😂", "😈", "😍"),
            )
            if option == "😀":
                icon_img = cv2.imread("./input/face_grinning_icon.png", cv2.IMREAD_UNCHANGED)
                icon_img = cv2.cvtColor(icon_img, cv2.COLOR_BGR2RGB)
            elif option == "😂:":
                icon_img = cv2.imread("./input/face_joy_icon.png")
                icon_img = cv2.cvtColor(icon_img, cv2.COLOR_BGR2RGB)
            elif option == "😈":
                icon_img = cv2.imread("./input/smiling_imp_icon.png")
                icon_img = cv2.cvtColor(icon_img, cv2.COLOR_BGR2RGB)
            elif option == "😍":
                icon_img = cv2.imread("./input/heart_eyes_icon.png")
                icon_img = cv2.cvtColor(icon_img, cv2.COLOR_BGR2RGB)

        stframe = st.empty()
        cap = cv2.VideoCapture(0)
        while True:
            blur_level = st.slider('Blurring levels', 0, 100)
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = blurring(frame, blur_level=blur_level, detector_backend='ssd')
            stframe.image(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()