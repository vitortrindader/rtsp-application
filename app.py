import paho.mqtt.client as mqtt
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

ecg_data = [0]          

def on_message(client, userdata, message):

    try:
        new_data = float(message.payload.decode())
        ecg_data.append(new_data)     

    except ValueError:
        print("Invalid data received.")

client = mqtt.Client()

client.on_message = on_message

client.connect("127.0.0.1", 1883)

client.loop_start()

topic = "ambulance/ecg"

client.subscribe(topic)

#--------------------------------------------------------------------

from pathlib import Path
import PIL
import streamlit as st
import settings
import helper

st.set_page_config(
    page_title="Ambulance Monitoring",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Ambulance Monitoring")

source_radio = 'RTSP'

if source_radio == settings.RTSP:
    helper.play_rtsp_stream_modified(ecg_data)

else:
    st.error("Please select a valid source type!")
