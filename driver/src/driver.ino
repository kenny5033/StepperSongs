/*
Arduino Program
---------------
This sketch receives musical notes via serial communication and plays them
on a stepper motor using the DRV8825 driver.

Inspiration taken from
Make Music With Stepper Motors! By Whiteshadow11 https://www.instructables.com/Make-Music-With-Stepper-Motors/

Kenny Howes - kenneth.howes53@gmail.com
Omar Valdez - ov25@calvin.edu
*/

// define Pins
#define STEP_PIN 4 
#define DIR_PIN 3


/* SERIAL COMMS */
#define SERIAL_BAUD 9600
#define SERIAL_READ_DELAY 100

typedef struct {
  uint16_t frequency;
  uint16_t duration;
} Note;

// note is fairly small (4 bytes), so it is stack allocated
// and returned by value
Note receiveNote(bool block) {
  // wait until the bytes are ready
  while (true) {
    if (Serial.available() >= sizeof(Note)) {
      Note receivedNote;
      // read in two-byte chunks
      receivedNote.frequency = (Serial.read() << 8) | Serial.read();
      receivedNote.duration = (Serial.read() << 8) | Serial.read();
      return receivedNote;
    } else if (!block) {
      return (Note){0, 0};
    }

    delay(SERIAL_READ_DELAY);
  }
}

void listenToSerial() {
  while (true) {
    Note n = receiveNote(true);
    Serial.println("Received note");
    Serial.print("Frequency: ");
    Serial.print(n.frequency);
    Serial.print(" Duration: ");
    Serial.println(n.duration);
    if (n.frequency == 0 && n.duration == 0) {
      Serial.println("No note received");
      continue;
    }
    playNote(&n);
  }
}
/* END SERIAL COMMS */

bool dir=0;
int tempo=120; // bpm

void setup() {
  // Step and Direction pins, DRV8825 has 2 other pins set to high (5V) directly from source
  // Other Drivers need to have different pin sets ups but still use STEP and DIR in the same methond
  // Will stick with DRV8825 drivers since they produce the least amount of non-needed noise
  pinMode(STEP_PIN,OUTPUT); 
  pinMode(DIR_PIN,OUTPUT);

  // Set the pins to low
  digitalWrite(STEP_PIN, LOW);
  digitalWrite(DIR_PIN, LOW);

  Serial.begin(SERIAL_BAUD);
}

void loop() {
  // to handle serial comms
  listenToSerial();
}

uint16_t lastFreq = 0;
void note(int freq, long dur) {
  if (freq <= 0) return; // Ignore invalid frequencies

  int delay = 1000000 / freq; // Calculate delay in microseconds for the given frequency

  // Swap direction if frequency is different
  // helps gives a more satisfying sound
  if (freq != lastFreq) {
    lastFreq = freq;
    dir = !dir;
  }
  digitalWrite(DIR_PIN, dir);

  // Calculate the number of steps to take
  long steps = (dur * 1000L) / (2 * delay);

  for (long i = 0; i < steps; i++) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(delay);
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(delay);
  }

  digitalWrite(STEP_PIN, LOW); // Ensure the step pin is low after the last step
}

inline void playNote(Note* noteToPlay) {
  note((int)noteToPlay->frequency, (int)noteToPlay->duration);
}

/* can be used to write songs directly into the arduino code */
inline void pause(int beats){
  delay(floor(beats/100)*tempo);
}
