// Define physical pin connections
const int trigPin = 9;
const int echoPin = 10;

// Variables for calculation
long duration;
int distance;

void setup() {
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT);  // Sets the echoPin as an Input
  Serial.begin(9600);       // Starts serial communication at 9600 baud rate
}

void loop() {
  // Clear the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  
  // Send a 10 microsecond ultrasonic pulse
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Read the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  
  // Calculate the distance (Speed of sound is 0.034 cm/microsecond)
  distance = duration * 0.034 / 2;
  
  // Print the distance to the Serial Port
  Serial.println(distance);
  
  // Delay 100 milliseconds before the next reading to prevent buffer overload
  delay(100);
}
