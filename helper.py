import streamlit as st
import cv2
import subprocess


def create_interface(st_frame, frame, ecg_data, prediction):

    number_1 = ecg_data[-1] if ecg_data else 0
    number_1 = round(number_1, 4)
    number_2 = prediction[-1] if prediction else 0
    if number_2 == 0:
        number_2 = "Normal"
    elif number_2 == 1:
        number_2 = "Supraventricular"
    elif number_2 == 2:
        number_2 = "Ventricular"
    elif number_2 == 3:
        number_2 = "Fusion"
    elif number_2 == 4:
        number_2 = "Unknown"

    # Logic to show prediction
    overlay = frame.copy()
    cv2.rectangle(overlay, (22, 22), (350, 100), (0, 0, 0), thickness=cv2.FILLED)
    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame, str(number_1), (65, 50), font, 1 * 0.7, (113, 244, 164), 1)
    cv2.putText(frame, "ECG", (25, 50), font, 1 * 0.4, (113, 244, 164), 1)  # ECG
    cv2.putText(frame, str(number_2), (110, 80), font, 1 * 0.7, (81, 249, 249), 1)
    cv2.putText(frame, "PREDICTION", (25, 80), font, 1 * 0.4, (81, 249, 249), 1)  # Prediction

    st_frame.image(frame,caption='inteface',channels="BGR",use_column_width=True)
    return frame


def play_rtsp_stream_modified(prediction, ecg_data):
    source_rtsp = st.sidebar.text_input("rtsp stream url:")
    st.sidebar.caption('Example URL: rtsp://admin:12345@192.168.1.210:554/Streaming/Channels/101')
    
    rtsp_output_url = st.sidebar.text_input("rtsp output url:")
    st.sidebar.caption('Example URL: rtsp://your_server_ip:554/live/stream')

    if st.sidebar.button('PLAY'):
        try:
            vid_cap = cv2.VideoCapture(source_rtsp)
            st_frame = st.empty()
            width, height = 640, 480
            fps = 60
            vid_cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            vid_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            vid_cap.set(cv2.CAP_PROP_FPS, fps)
            ffmpeg_cmd = [
                "ffmpeg",
                "-f", "rawvideo",
                "-pix_fmt", "bgr24",
                "-s", f"{width}x{height}",
                "-r", str(fps),
                "-i", "-",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-preset", "ultrafast",
                "-f", "rtsp",
                "-rtsp_transport", "tcp",
                rtsp_output_url
            ]
            
            ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

            while vid_cap.isOpened():
                success, imagem = vid_cap.read()
                image = cv2.resize(imagem, (640, 480))
                if success:
                    frame = create_interface(st_frame, image, ecg_data, prediction)
                    ffmpeg_process.stdin.write(frame.tobytes())
                else:
                    break

            vid_cap.release()
            ffmpeg_process.stdin.close()
            ffmpeg_process.wait()

        except Exception as e:
            vid_cap.release()
            st.sidebar.error("Error loading RTSP stream: " + str(e))

