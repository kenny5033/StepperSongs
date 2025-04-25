/*
inspiration taken from
Make Music With Stepper Motors! By Whiteshadow11 https://www.instructables.com/Make-Music-With-Stepper-Motors/
*/

// Define Pins
#define STEP_PIN 4 
#define DIR_PIN 3

#define SERIAL_BAUD 9600
#define SERIAL_READ_DELAY 100

typedef struct {
  uint16_t frequency;
  uint16_t duration;
} Note;

// serial communication setup
// note returned by value, shouldn't need to worry about heapspace
// note is fairly small (2 bytes), so it should be fine
Note receiveNote(bool block) {
  // wait until the two bytes are ready
  while (true) {
    if (Serial.available() >= sizeof(Note)) {
      Note receivedNote;
      receivedNote.frequency = (Serial.read() << 8) | Serial.read();
      receivedNote.duration = (Serial.read() << 8) | Serial.read();
      return receivedNote;
    } else if (!block) {
      return (Note){0, 0};
    }
    delay(SERIAL_READ_DELAY);
  }
}

bool dir=0;

// pause beats for different songs
int pause1 = 300;
int pause2=180;

int tempo=120; // bpm

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

inline void pause(int beats){
  delay(floor(beats/100)*tempo);
}
