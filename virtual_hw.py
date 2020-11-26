import time
import json
import psutil
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("bakecode")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("127.0.0.1", 1883, 60)

    while True:
        client.loop()
        
        cpu_percent: float = psutil.cpu_percent()
        mem_percent = psutil.virtual_memory().percent
        battery = psutil.sensors_battery().percent
        plugged = psutil.sensors_battery().power_plugged
        disk_usage = psutil.disk_usage('/').percent
        swap_usage = psutil.swap_memory().percent

        message = {
            "CPU": cpu_percent,
            "Memory": mem_percent,
            "Battery": battery,
            "AC Power": plugged,
            "Storage": disk_usage,
            "Swap": swap_usage,
        }


        packet = {
            "source": "virtualHW",
            "destinations": ["bakecode"],
            "message": json.dumps(message),
        }

        publish.single("bakecode", json.dumps(packet), hostname="127.0.0.1")
                
        time.sleep(1)




