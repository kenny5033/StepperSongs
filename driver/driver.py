#########
# This file bridges the Python client to the Arduino driver
# over serial
#########
import struct
import serial
import os

SERIAL_PORT = "/dev/ttyUSB0"  # serial port of the arduino

# frequency (hz) by note
NOTE_FREQUENCIES = {
    "C": 261.63,
    "C#": 277.18,
    "D": 293.66,
    "D#": 311.13,
    "E": 329.63,
    "F": 349.23,
    "F#": 369.99,
    "G": 392.00,
    "G#": 415.30,
    "A": 440.00,
    "A#": 466.16,
    "B": 493.88,
}

class Note:
    def __init__(self, note: str, duration: int):
        if note not in NOTE_FREQUENCIES:
            raise ValueError(f"Invalid note: {note}")

        self.frequency = NOTE_FREQUENCIES[note]
        self.duration = duration

    def to_bytes(self) -> None:
        return struct.pack('BB', self.frequency, self.duration)

def send_note_via_serial(note, serial_port: str = SERIAL_PORT) -> None:
    if not os.path.exists(serial_port):
        raise FileNotFoundError(f"The serial port {serial_port} does not exist.")

    with serial.Serial(serial_port, 9600, timeout=1) as ser:
        ser.write(note.to_bytes())
