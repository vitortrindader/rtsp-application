import paho.mqtt.client as mqtt
import time
import neurokit2 as nk
import matplotlib.pyplot as plt

# ECG ------------------------

data = nk.data("bio_eventrelated_100hz")

processed_data, info = nk.bio_process(ecg=data["ECG"], rsp=data["RSP"], eda=data["EDA"], sampling_rate=100)


# MQTT ------------------------

def on_publish(client, userdata, mid):
    return

def on_message(client, userdata, message):
    return

client = mqtt.Client()

client.on_publish = on_publish
client.on_message = on_message

client.connect("127.0.0.1", 1883)

client.loop_start()

topic = "ambulance/ecg"
message = ""
client.publish(topic, message)

client.subscribe(topic)

cont=0

try:
    while True:
        message = processed_data['ECG_Clean'][cont]
        client.publish(topic, message)
        print(f"Published message to topic '{topic}': {message}")
        time.sleep(0.0167)  # Adjust the interval (in seconds) between messages as needed

                
        cont+=1  
        if cont >= 15000:
            cont = 0           
        
except KeyboardInterrupt:
    print("Exiting...")
    client.disconnect()
    client.loop_stop()
