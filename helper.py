from ultralytics import YOLO
import time
import streamlit as st
import numpy as np
import cv2
from pytube import YouTube
import settings
import subprocess

def create_interface(st_frame, frame,ecg_data):

    number_1 = ecg_data[-1] if ecg_data else 0
    number_2 = 2
    number_3 = 3

    height, width, _ = frame.shape

    p1 = int(height / 28.33)
    p2_w = int(width / 3.55)
    p2_h = int(height / 2.05)

    overlay = frame.copy()

    cv2.rectangle(overlay, (p1, p1), (p2_w, p2_h), (0, 0, 0), thickness=cv2.FILLED)

    cv2.addWeighted(overlay, 0.55, frame, 0.45, 0, frame)

    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 1.5
    font_thickness = 3

    p_w = int(width / 7.73)
    p_h = int(height / 5.37)

    text_1 = "HR"
    text_color_1 = (113, 244, 164)
    cv2.putText(frame, str(number_1), (p_w, p_h), font, font_scale, text_color_1, font_thickness)
    p_w1 = p_w - 40
    cv2.putText(frame, text_1, (p_w1, p_h), font, font_scale * 0.4, text_color_1, 1)

    text_2 = "SpO2"
    text_color_2 = (81, 249, 249)
    p_h2 = p_h + 60
    cv2.putText(frame, str(number_2), (p_w, p_h2), font, font_scale, text_color_2, font_thickness)
    p_w2 = p_w - 60
    cv2.putText(frame, text_2, (p_w2, p_h2), font, font_scale * 0.4, text_color_2, 1)

    text_3 = "etCO2"
    text_color_3 = (220, 246, 77)
    p_h3 = p_h2 + 60
    cv2.putText(frame, str(number_3), (p_w, p_h3), font, font_scale, text_color_3, font_thickness)
    p_w3 = p_w - 60
    cv2.putText(frame, text_3, (p_w3, p_h3), font, font_scale * 0.4, text_color_3, 1)


    st_frame.image(frame,caption='inteface',channels="BGR",use_column_width=True)
    return frame


def play_rtsp_stream_modified(ecg_data):
    source_rtsp = st.sidebar.text_input("rtsp stream url:")
    st.sidebar.caption('Example URL: rtsp://admin:12345@192.168.1.210:554/Streaming/Channels/101')
    
    rtsp_output_url = st.sidebar.text_input("rtsp output url:")
    st.sidebar.caption('Example URL: rtsp://your_server_ip:554/live/stream')

    if st.sidebar.button('Detect Objects'):
        try:
            vid_cap = cv2.VideoCapture(source_rtsp)
            st_frame = st.empty()
            width, height = 640, 480
            fps = 30
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
                success, image = vid_cap.read()
                if success:
                    frame = create_interface(st_frame, image, ecg_data)
                    ffmpeg_process.stdin.write(frame.tobytes())
                else:
                    break

            vid_cap.release()
            ffmpeg_process.stdin.close()
            ffmpeg_process.wait()

        except Exception as e:
            vid_cap.release()
            st.sidebar.error("Error loading RTSP stream: " + str(e))

