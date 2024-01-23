import paho.mqtt.client as mqtt
import settings
import helper
from keras.models import load_model
import numpy as np

loaded_model = load_model('best_model.h5')

ecg_data = [0]          
batch_size = 186
batches = []
prediction = []


def predict_single_input(model, input_data):
    input_data = np.reshape(input_data, (1, input_data.shape[0], 1))
    model_response = model.predict(input_data)
    predicted_class = np.argmax(model_response)
    return predicted_class


def process_batch(batch):
    input_array = np.array(batch)
    predicted_class = predict_single_input(loaded_model, input_array)
    prediction.append(predicted_class)


def on_message(client_, userdata, message):

    try:
        new_data = float(message.payload.decode())
        ecg_data.append(new_data)

        if len(ecg_data) >= batch_size:
            current_batch = ecg_data[-batch_size:]
            batches.append(current_batch)
            process_batch(current_batch)

    except ValueError:
        print("Invalid data received.")


client = mqtt.Client()

client.on_message = on_message

client.connect("192.168.15.26", 1883)

client.loop_start()

topic = "ambulance/ecg"

client.subscribe(topic)

source_radio = 'RTSP'

if source_radio == settings.RTSP:
    helper.play_rtsp_stream_modified(prediction, ecg_data)
