// Define pin connections & motor's steps per revolution
const int dirPin = D8;
const int stepPin = D7;
const int ledPin3 = D3;
const int ledPin2 = D2;
const int ledPin1 = D1;
const int stepsPerRevolution = 200;
int snelheid = 2000;
int start = 0;
int led1 = 0;
int led2= 0;
int led3 = 0;

void setup()
{
  Serial.begin(9600);
  // Declare pins as Outputs
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(ledPin3, OUTPUT);
  // Set motor direction clockwise
  digitalWrite(dirPin, HIGH);
  digitalWrite(ledPin1, LOW);
  digitalWrite(ledPin2, LOW);
  digitalWrite(ledPin3, LOW);
  
  
}
void loop()
{

  if (Serial.available()) {
    char ch = Serial.read();
      switch(ch) {
        case 'l':
          Serial.println("links");
          digitalWrite(dirPin, HIGH);
          break;
        case 'r':
          Serial.println("Rechts");
          digitalWrite(dirPin, LOW);
          break;
        case '+':
          Serial.println("Snelheid");
          Serial.println(snelheid);
          snelheid -= 10;
          break;
        case '-':
          Serial.print("Snelheid");
          Serial.println(snelheid);
          snelheid += 10;
          break;
        case 's':
          Serial.println("Stap maken");
          digitalWrite(stepPin, HIGH);
          delayMicroseconds(snelheid);
          digitalWrite(stepPin, LOW);
          delayMicroseconds(snelheid);
          break;
        case 'q':
          Serial.println("Stoppen");
          digitalWrite(ledPin1, LOW);
          digitalWrite(ledPin2, LOW);
          digitalWrite(ledPin3, LOW);
          start = 0;
          break;
        case 'v':
          Serial.println("Verder doen");
          start = 1;
          break;
        case '1':
          Serial.println("Led 1 omschakelen");
          if(led1 == 1) {
            led1 = 0;
            digitalWrite(ledPin1, LOW);
          }
          else {
            led1 = 1;
            digitalWrite(ledPin1, HIGH);
          }
          break;
        case '2':
          Serial.println("Led 2 omschakelen");
          if(led2 == 1) {
            led2 = 0;
            digitalWrite(ledPin2, LOW);
          }
          else {
            led2 = 1;
            digitalWrite(ledPin2, HIGH);
          }
          break;
        case '3':
          Serial.println("Led 3 omschakelen");
          if(led3 == 1) {
            led3 = 0;
            digitalWrite(ledPin3, LOW);
          }
          else {
            led3 = 1;
            digitalWrite(ledPin3, HIGH);
          }
          break;
        
      }
   }

    if (start == 1) {
      //Serial.println("traag");
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(snelheid);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(snelheid);
    }
  
}
