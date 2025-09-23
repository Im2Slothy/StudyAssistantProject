int ledPin = 8; 

void setup() {
    pinMode(ledPin, OUTPUT);    
    Serial.begin(9600);
}

void loop() {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');

        if (command == "light") {
            for (int i = 0; i < 5; i++) {
                digitalWrite(ledPin, HIGH);
                delay(500);
                digitalWrite(ledPin, LOW);
                delay(500);
            }
        }
    }
}
