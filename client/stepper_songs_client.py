import paho.mqtt.client as mqtt
from uuid import uuid4
import re
from queue import Queue
from driver.driver import Driver, Note

class StepperSongsClient:
    '''
    A client that connects to an MQTT broker and listens for notes to play.
    Notes will be queued and sent to the driver for playback.
    '''

    def __init__(self, broker: str, port: str, username: str, password: str, client_id: str = None) -> None:
        # generate a 6-character client code, if not provided
        self.CLIENT_ID = client_id if client_id else str(uuid4().hex[:6])
        self.TOPIC = f"Stepper Songs/client{self.CLIENT_ID}"

        # Create an MQTT client instance, ensure on latest version
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

        # Assign the callback functions
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Connect to the broker
        self.client.username_pw_set(username, password=password)
        self.client.connect(broker, port, 60)

        # setup driver related variables
        self.driver = Driver()
        self.note_regex = re.compile(r"[A-G]#?")
        self.notes_queue: Queue[Note] = Queue()
    
    def __del__(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()

    # cb for when the client connects to the broker
    def on_connect(self, client, userdata, flags, rc, properties) -> None:
        if rc == 0:
            print("Connected to broker")
            client.subscribe(self.TOPIC)
        else:
            print(f"Failed to connect, return code {rc}")

    # cb for when a message is received
    def on_message(self, client, userdata, msg) -> None:
        recieved: str = str(msg.payload.decode()).upper()
        info = recieved.split("--")
        if len(info) != 2:
            self.client.publish("Invalid message format")
            return
        
        note = info[0]
        duration = info[1]
        if not duration.isdigit():
            self.client.publish("Invalid duration")
            return
        
        duration = int(duration)
        if duration <= 0:
            self.client.publish("Invalid duration")
            return

        if not self.note_regex.match(note):
            self.client.publish("Invalid note")
            return
        
        new_note = Note(note, duration)
        self.notes_queue.put(new_note)
        print(f"Received note: {note} for {duration} milliseconds")

    def run(self) -> None:
        self.client.loop_start()  # starts in separate thread

        # continually send notes to the driver
        while True:
            next_note = self.notes_queue.get(block=True)
            try:
                self.driver.send_note_via_serial(next_note)
                print(f"Playing note at frequency {next_note.frequency} HZ for {next_note.duration} milliseconds")
                print(f"Current queue length: {self.notes_queue.qsize()}")
            except Exception as e:
                print(e)

    def getClientID(self) -> str:
        return self.CLIENT_ID
