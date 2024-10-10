from pathlib import Path
import streamlit as st
import numpy as np
from PIL import Image
import cv2
from image_processing import blurring
import tempfile


if st.button("Back to main page"):
    st.switch_page("./1_😎_Homepage.py")

st.title("Blurring Faces")
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
        blur_level = st.slider('Blurring levels', 0, 100)
        submit = st.form_submit_button('Submit', help="Click to processing!")

    st.subheader("Your result here:")
    if submit:
        img_array = blurring(img_array, blur_level, detector_backend='retinaface')
        st.image(img_array, caption="Blur image", use_column_width=True)

if choice == "video":
    st.subheader("Upload your video here:")
    video_file = st.file_uploader("Upload a video", type=["mp4"])
    show_file = st.empty()
    if not video_file:
        show_file.info("Please upload a video file: {}".format(" ".join(["mp4"])))

    with st.form("my_form"):
        blur_level = st.slider('Blurring levels', 0, 100)
        submit = st.form_submit_button('Submit', help="Click to processing!")
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
            frame = blurring(frame, blur_level=50, detector_backend='ssd')
            stframe.image(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    
if choice == "webcam":
    if st.button("Turn on your camera!"):

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