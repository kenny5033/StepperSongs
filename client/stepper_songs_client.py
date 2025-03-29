import paho.mqtt.client as mqtt
from uuid import uuid4
from signal import pause
import sys
import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../driver"))) # add driver directory to path
# from driver import StepperSongsDriver
import re

# MQTT constants
BROKER = "test.mosquitto.org"
PORT = 1883

class StepperSongsClient:
    def __init__(self, broker: str, port: str, client_id: str = None) -> None:
        # generate a 6-character client code, if not provided
        self.CLIENT_ID = client_id if client_id else str(uuid4().hex[:6])
        self.TOPIC = f"Stepper Songs/client{self.CLIENT_ID}"

        # Create an MQTT client instance, ensure on latest version
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

        # Assign the callback functions
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Connect to the broker
        self.client.connect(broker, port, 60)

        # self.driver = StepperSongsDriver()
        self.note_regex = re.compile(r"[A-G]#?")

    # cb for when the client connects to the broker
    def on_connect(self, client, userdata, flags, rc, properties) -> None:
        if rc == 0:
            print("Connected to broker")
            client.subscribe(self.TOPIC)
        else:
            print(f"Failed to connect, return code {rc}")

    # cb for when a message is received
    def on_message(self, client, userdata, msg) -> None:
        note: str = str(msg.payload.decode()).upper()

        if not self.note_regex.match(note):
            self.client.publish("Invalid note")
            return
        
        # self.driver.play_note(note)
        print(f"Playing note: {note}")

    def run(self) -> None:
        self.client.loop_start() # starts in separate thread
    
    def stop(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()
    
    def getClientID(self) -> str:
        return self.CLIENT_ID

if __name__ == "__main__":
    client = StepperSongsClient(BROKER, PORT, client_id="12345")

    try:
        client.run()
        print(f"Client ID: {client.getClientID()}")
        pause()
    except KeyboardInterrupt:
        print("Disconnecting from broker...")
    finally:
        client.stop()
