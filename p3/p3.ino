// Pin definitions for the LEDs
const int led1Pin = 13;
const int led2Pin = 12;
const int led3Pin = 11;

void setup() {
  // Set the LED pins as outputs
  pinMode(led1Pin, OUTPUT);
  pinMode(led2Pin, OUTPUT);
  pinMode(led3Pin, OUTPUT);

  // Initialize serial communication
  Serial.begin(9600);

  // Prompt user in Serial Monitor
  Serial.println("Type '1', '2', or '3' to turn on respective LED. Type '0' to turn off all LEDs.");
}

void loop() {
  // Check if data is available to read
  if (Serial.available() > 0) {
    // Read the incoming byte
    char command = Serial.read();

    // Process the command
    switch (command) {
      case '1':
        // Turn on LED 1
        digitalWrite(led1Pin, HIGH);
        digitalWrite(led2Pin, LOW);
        digitalWrite(led3Pin, LOW);
        break;

      case '2':
        // Turn on LED 2
        digitalWrite(led1Pin, LOW);
        digitalWrite(led2Pin, HIGH);
        digitalWrite(led3Pin, LOW);
        break;

      case '3':
        // Turn on LED 3
        digitalWrite(led1Pin, LOW);
        digitalWrite(led2Pin, LOW);
        digitalWrite(led3Pin, HIGH);
        break;

      case '0':
        // Turn off all LEDs
        digitalWrite(led1Pin, LOW);
        digitalWrite(led2Pin, LOW);
        digitalWrite(led3Pin, LOW);
        break;

      default:
        // Invalid command
        Serial.println("Invalid command. Type '1', '2', '3', or '0'.");
    }
  }
}
