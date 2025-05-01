"""
This script initializes and runs the StepperSongs MQTT client.
Designed to be the entry point for the project.

Kenny Howes - kenneth.howes53@gmail.com
Omar Valdez - ov25@calvin.edu
"""

from client.stepper_songs_client import StepperSongsClient
from signal import pause
import os
from dotenv import load_dotenv
load_dotenv()

# MQTT constants
BROKER = "iot.cs.calvin.edu"
PORT = 1883
USERNAME = os.getenv("MQTT_USERNAME", "default_username")
PASSWORD = os.getenv("MQTT_PASSWORD", "default_password")


if __name__ == "__main__":
    # remove hardcoded client_id for random UUID
    client = StepperSongsClient(BROKER, PORT, USERNAME, PASSWORD, client_id="12345")

    try:
        client.run()
        print(f"Client ID: {client.getClientID()}")
        pause()
    except KeyboardInterrupt:
        print("Exiting...")
