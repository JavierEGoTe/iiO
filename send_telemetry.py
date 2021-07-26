import random
import time
import json
#import sys
#import RPi.GPIO as GPIO

from azure.iot.device import IoTHubDeviceClient, Message

'''EMULATE_HX711=False

referenceUnit = 1

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711'''

CONNECTION_STRING = "HostName=input-data.azure-devices.net;DeviceId=receive-device;SharedAccessKey=h7td4i+hDdCvuExieCXZA/m1oFpjAUnHS2ahJkNpWGQ="

SILO = "silo 1"
CAPACIDAD_OCUPADA = 1000
GRANO = "Maiz"
CAPACIDAD_TOTAL = 1000
CAPACIDAD_RESTANTE = 0




def iothub_client_init():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_client_telemetry():
    
    try:
        client = iothub_client_init()
        print("IoT Hub Device sending periodic messages, press Ctrl-C to exit")
        capacidad_ocupada = CAPACIDAD_OCUPADA
        capacidad_total = CAPACIDAD_TOTAL
        silo = SILO
        grano = GRANO
        capacidad_restante = CAPACIDAD_RESTANTE
        llenado = False

        while True:
            

            if(capacidad_ocupada > 250 and llenado == False):
                capacidad_ocupada = capacidad_ocupada - random.randint(20,50)
                capacidad_restante = capacidad_total - capacidad_ocupada
                MSG_TXT = {"silo": silo, "capacidad_ocupada": capacidad_ocupada, "grano": grano, "capacidad_total": capacidad_total, "capacidad_restante": capacidad_restante}
                msg_txt_formatted = json.dumps(MSG_TXT)
                message = Message(msg_txt_formatted)

                print("Sending message: {}".format(message))
                client.send_message(message)
                print("Message successfully sent ")
                if((capacidad_ocupada - 50) < 250):
                    llenado = True
            elif(capacidad_ocupada < 950 and llenado == True):
                capacidad_ocupada = capacidad_ocupada + random.randint(200,250)
                capacidad_restante = capacidad_total - capacidad_ocupada
                MSG_TXT = {"silo": silo, "capacidad_ocupada": capacidad_ocupada, "grano": grano, "capacidad_total": capacidad_total, "capacidad_restante": capacidad_restante}
                msg_txt_formatted = json.dumps(MSG_TXT)
                message = Message(msg_txt_formatted)

                print("Sending message: {}".format(message))
                client.send_message(message)
                print("Message successfully sent ")
                if((capacidad_ocupada + 50) > 950):
                    llenado = False
                
            
            time.sleep(20)

    except KeyboardInterrupt:
        print("IoTHubClient stopped")

if __name__ == '__main__':
    print("Press Ctrl-C to exit")
    iothub_client_telemetry()

