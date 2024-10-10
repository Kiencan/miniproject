from deepface import DeepFace
import cv2
import os


def blurring(img, blur_level, detector_backend):
    detected_face = DeepFace.extract_faces(img_path=img, detector_backend=detector_backend, enforce_detection=False)
    face_data = []
    for i in range(len(detected_face)):
        face_data.append(detected_face[i]['facial_area'])
        x1 = face_data[i].get('x')
        y1 = face_data[i].get('y')
        width = face_data[i].get('w')
        height = face_data[i].get('h')

        img[y1:y1 + height, x1:x1 + width] = cv2.blur(img[y1:y1 + height, x1:x1 + width], (blur_level, blur_level))
 
    return img

def icon_face(img, img_icon, detector_backend):
    detected_face = DeepFace.extract_faces(img_path=img, detector_backend=detector_backend, enforce_detection=False)
    face_data = []
    for i in range(len(detected_face)):
        face_data.append(detected_face[i]['facial_area'])
        x1 = face_data[i].get('x')
        y1 = face_data[i].get('y')
        width = face_data[i].get('w')
        height = face_data[i].get('h')

        img_icon = cv2.resize(img_icon, (max(width, height), max(width, height)))
        img[y1:y1 + max(height, width), x1:x1 + max(height, width)] = img_icon
 
    return img



def detect_faces(mode, input_source, blur_level):
    # Handle image mode
    if mode == "image":
        img = cv2.imread(input_source)
        img = blurring(img, blur_level, detector_backend='retinaface')
    
        # cv2.imshow('Face Detection - Image', img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return img

    # Handle video mode
    elif mode == "video":
        cap = cv2.VideoCapture(input_source)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frameRate = int(cap.get(cv2.CAP_PROP_FPS))
        # output_path = os.path.join(output_folder, "output.mp4")

        fourccCode = cv2.VideoWriter_fourcc(*'mp4v')
        videoFileName = "output.mp4"
        videoDimension = (frame_width, frame_height)
        out = cv2.VideoWriter(videoFileName, fourccCode, frameRate, videoDimension)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            frame = img_processing(frame, blur_level=blur_level,detector_backend='ssd')
            out.write(frame)

            # cv2.imshow('Face Detection - Video', frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break

        cap.release()
        cv2.destroyAllWindows()

    # Handle webcam mode
    elif mode == "webcam":
        cap = cv2.VideoCapture(0)  # Use '0' for webcam
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = img_processing(frame, detector_backend='ssd')

            cv2.imshow('Face Detection - Webcam', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

# Example usage:
# For image mode
# img = cv2.imread("./input/anh1.jpg")
# blur_img = detect_faces("image", blur_level=10, img=img)
# cv2.imshow('Face Detection - Image', blur_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# For video mode
# detect_faces("video", './input/video1.mp4')

# For webcam mode
# detect_faces("webcam", None)