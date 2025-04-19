#########
# This file bridges the Python client to the Arduino driver
# over serial
#########
import struct
import serial
import os

SERIAL_PORT = "/dev/ttyACM0"  # serial port of the arduino

# frequency (hz) by note
NOTE_FREQUENCIES: list[int] = {
    "C":  1912,
    "C#": 1805,
    "D":  1703,
    "D#": 1607,
    "E":  1517,
    "F":  1431,
    "F#": 1351,
    "G":  1275,
    "G#": 1203,
    "A":  1136,
    "A#": 1072,
    "B":  1012,
}

class Note:
    def __init__(self, note: str, duration: int):
        if note not in NOTE_FREQUENCIES:
            raise ValueError(f"Invalid note: {note}")

        self.frequency = NOTE_FREQUENCIES[note]
        self.duration = duration

    def to_bytes(self) -> None:
        return struct.pack('>HH', self.frequency, self.duration)

def send_note_via_serial(note, serial_port: str = SERIAL_PORT) -> None:
    if not os.path.exists(serial_port):
        raise FileNotFoundError(f"The serial port {serial_port} does not exist.")

    with serial.Serial(serial_port, 9600, timeout=1) as ser:
        ser.write(note.to_bytes())
