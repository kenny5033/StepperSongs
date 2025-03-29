from tmc_driver.tmc_2209 import *
import RPi.GPIO as GPIO
import time

# TMC2209 config
UART_PORT = "/dev/serial0"
ENABLE_PIN = 21
MOTION_CONTROL_PIN0 = 16
MOTION_CONTROL_PIN1 = 20
PWM_PIN = 18

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

class StepperSongsDriver:
    def __init__(self) -> None:
        self.tmc = Tmc2209(
            TmcEnableControlPin(ENABLE_PIN),
            TmcMotionControlStepDir(MOTION_CONTROL_PIN0, MOTION_CONTROL_PIN1),
            TmcComUart(UART_PORT),
        )
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PWM_PIN, GPIO.OUT)
        self.pwm = GPIO.PWM(PWM_PIN, 1)  # initialize with dummy frequency
        self.pwm.start(0) # start with duty cycle of 0

    # TODO: this code needs to be refactored to use the TMC2209 driver
    def play_pwm_note(self, note: str, duration: float = 1.0) -> None:
        """Plays a note using PWM for the specified duration."""
        frequency = NOTE_FREQUENCIES.get(note)
        if not frequency:
            raise ValueError(f"Invalid note: {note}")

        print(f"Playing note: {note} ({frequency} Hz) for {duration} seconds")
        self.pwm.ChangeFrequency(frequency)
        self.pwm.ChangeDutyCycle(50)  # Set duty cycle to 50% for a square wave
        time.sleep(duration)
        self.pwm.ChangeDutyCycle(0)  # Stop the sound

    def cleanup(self):
        """Clean up GPIO and PWM resources."""
        self.pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    driver = StepperSongsDriver()

    try:
        driver.play_pwm_note("C", 1.0)
        driver.play_pwm_note("E", 1.0)
        driver.play_pwm_note("G", 1.0)
    except KeyboardInterrupt:
        print("Stopping driver...")
    finally:
        driver.cleanup()
