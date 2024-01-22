rtsp-application
1. Inicializando os servidores RTSP
   1.1. INPUT : docker run --rm -it -e RTSP_PROTOCOLS=tcp -p 8554:8554 -p 1935:1935 aler9/rtsp-simple-server 
   1.2. OUTPUT: docker run --rm -it -e RTSP_PROTOCOLS=tcp -p 9554:8554 -p 2935:1935 aler9/rtsp-simple-server
2. Inicializando o servidor MQTT
   2.1. Mosquitto: mosquitto_sub -h localhost -t /ambulance/ecg
   2.2. Envio dos dados: python3 mqtt.py
3. Inicializando a stream de video do input
   3.1. python3 teste.py
4. Inicializando a app 
   4.1. streamlit run app.py
5. Com o app aberto coloca as URL de input e output dos servidores RTSP
