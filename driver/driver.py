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
    "C":  1047,
    "C#": 1109,
    "D":  1175,
    "D#": 1245,
    "E":  1319,
    "F":  1397,
    "F#": 1480,
    "G":  1568,
    "G#": 1661,
    "A":  1760,
    "A#": 1865,
    "B":  1976,
}

class Note:
    def __init__(self, note: str, duration: int):
        if note not in NOTE_FREQUENCIES:
            raise ValueError(f"Invalid note: {note}")

        self.frequency = NOTE_FREQUENCIES[note]
        self.duration = duration

    def to_bytes(self) -> None:
        return struct.pack('>HH', self.frequency, self.duration)
    
class Driver:
    def __init__(self, serial_port: str = SERIAL_PORT) -> None:
        if not os.path.exists(serial_port):
            raise FileNotFoundError(f"The serial port {serial_port} does not exist.")

        self.ser = serial.Serial(SERIAL_PORT, baudrate=9600, timeout=1)
    
    def __del__(self):
        if self.ser.is_open:
            self.ser.close()

    def send_note_via_serial(self, note: Note) -> None:
        try:
            self.ser.write(note.to_bytes())
        except serial.SerialException as e:
            print(f"Serial error: {e}")
