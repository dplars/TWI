#include <FastLED.h>
#include <stdlib.h>

void startupLEDsTest();

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
int addr = 1;

// How many leds in your strip?
#define NUM_LEDS 15

// For led chips like WS2812, which have a data line, ground, and power, you just
// need to define DATA_PIN.  For led chipsets that are SPI based (four wires - data, clock,
// ground, and power), like the LPD8806 define both DATA_PIN and CLOCK_PIN
// Clock pin only needed for SPI based chipsets when not using hardware SPI
#define DATA_PIN1 D6
#define DATA_PIN2 D0
#define CLOCK_PIN D5

// Define the array of leds
CRGB leds[NUM_LEDS];
int nrled1 = 0;
int nrled2 = 0;
int brightness1 = 32;
int brightness2 = 32;
int ledmode1 = 1;
int ledmode2 = 1;
boolean verbose = true;
String ch = "";

int step = 0;

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

  FastLED.addLeds<APA102, DATA_PIN1, CLOCK_PIN, RGB>(leds, NUM_LEDS);  // BGR ordering is typical
  FastLED.addLeds<APA102, DATA_PIN2, CLOCK_PIN, RGB>(leds, NUM_LEDS);  // BGR ordering is typical
  FastLED.clear();
  FastLED.show();

  startupLEDsTest();
  
}
void loop()
{

  if (Serial.available()) {
    ch = Serial.readStringUntil('\n');
    
    
        String alpha, special, num; 
        for (int i=0; i<ch.length(); i++) 
        { 
            if (isdigit(ch[i])) {
                num += (ch[i]); 
            }
            else if((ch[i] >= 'A' && ch[i] <= 'Z') || 
                    (ch[i] >= 'a' && ch[i] <= 'z')) 
                alpha += (ch[i]); 
            else
                special += (ch[i]); 
        } 

        Serial.println(alpha);
        Serial.println(num);
        Serial.println(special);

        if (alpha == "brightnessA") {
          if(verbose) Serial.print("brightness A ");
          // als geen special is gezet, de waarde instellen.. anders de waarde verhogen met het getal bij + en verlagen bij -
          if(special == "") {
            // getal setten
            int value;
            value = num.toInt();
            brightness1 = value;
          }
          else if(special == "+") {
             int value;
             value = num.toInt();
            brightness1 += value;
          }
          else if(special == "-") {
             int value;
             value = num.toInt();
            brightness1 -= value;
          }
          else if(special == "_") {
             brightness1 = 0;
          }
          if(verbose) Serial.println(brightness1);
          FastLED.setBrightness(brightness1);
          FastLED.show();
        }
         if (alpha == "brightnessB") {
          if(verbose) Serial.print("brightness B ");
          // als geen special is gezet, de waarde instellen.. anders de waarde verhogen met het getal bij + en verlagen bij -
          if(special == "") {
            // getal setten
            int value;
            value = num.toInt();
            brightness2 = value;
          }
          else if(special == "+") {
             int value;
             value = num.toInt();
            brightness2 += value;
          }
          else if(special == "-") {
             int value;
             value = num.toInt();
            brightness2 -= value;
          }
          else if(special == "_") {
             brightness2 = 0;
          }
          if(verbose) Serial.println(brightness2);
          FastLED.setBrightness(brightness2);
          FastLED.show();
        }

         if (alpha == "nrledA") {
          if(verbose) Serial.print("nrled A ");
          // als geen special is gezet, de waarde instellen.. anders de waarde verhogen met het getal bij + en verlagen bij -
          if(special == "") {
            // getal setten
            int value;
            value = num.toInt();
            nrled1 = value;

            
          }
          else if(special == "+") {
             int value;
             value = num.toInt();
            nrled1 = value;
            ledmode1 = 1;
            
            leds[nrled1] = CRGB::Blue;
            FastLED.show();
          }
          else if(special == "-") {
             int value;
             value = num.toInt();
             nrled1 = value;
             ledmode1 = 0;

             leds[nrled1] = CRGB::Black;
             FastLED.show();
          }
          else if(special == "_") {
             fill_solid(leds, NUM_LEDS, CRGB(0,0,0));  // fill black
             nrled1 = 0;
             ledmode1 = 0;
          }
          if(verbose) Serial.println(nrled1);

          // leds aan of uit zetten
          if(ledmode1 == 1) {
              leds[nrled1] = CRGB::Blue;
          }
          else {
            leds[nrled1] = CRGB::Black;
          }
          FastLED.show();
        }
         if (alpha == "nrledB") {
          if(verbose) Serial.print("nrled B ");
          // als geen special is gezet, de waarde instellen.. anders de waarde verhogen met het getal bij + en verlagen bij -
          if(special == "") {
            // getal setten
            int value;
            value = num.toInt();
            nrled2 = value;

            
          }
          else if(special == "+") {
             int value;
             value = num.toInt();
            nrled2 = value;
            ledmode2 = 1;
            
            leds[nrled2] = CRGB::Blue;
            FastLED.show();
          }
          else if(special == "-") {
             int value;
             value = num.toInt();
             nrled2 = value;
             ledmode2 = 0;

             leds[nrled2] = CRGB::Black;
             FastLED.show();
          }
          else if(special == "_") {
             fill_solid(leds, NUM_LEDS, CRGB(0,0,0));  // fill black
             nrled2 = 0;
             ledmode2 = 0;
          }
          if(verbose) Serial.println(nrled2);

          // leds aan of uit zetten
          if(ledmode2 == 1) {
              leds[nrled2] = CRGB::Blue;
          }
          else {
            leds[nrled2] = CRGB::Black;
          }
          FastLED.show();
        }

       if (alpha == "step") {
        if(verbose) Serial.print("step ");
        // als geen special is gezet, de waarde instellen.. anders de waarde verhogen met het getal bij + en verlagen bij -
        if(special == "") {
          // getal setten
          int value;
          if(num != "") {
            step = num.toInt();
          }
          // anders gewoon step maken
         
        }
        else if(special == "+") {
           int value;
           value = num.toInt();
          step = value;
          //Serial.println("Links");
          digitalWrite(dirPin, HIGH);
        }
        else if(special == "-") {
          //Serial.println(num);
           int value;
           value = num.toInt();
          step = value;
          //Serial.println("Rechts");
          digitalWrite(dirPin, LOW);
        }
        else if(special == "_") {
           step = 0;
        }
        if(verbose) Serial.println(step);

        for(int s = 0; s < step; s++) {
          //Serial.println("Stap maken");
          digitalWrite(stepPin, HIGH);
          delayMicroseconds(1000);
          digitalWrite(stepPin, LOW);
          delayMicroseconds(1000);
        }
        
      }
        
        
        if(ch == "c+") {
          
          nrled1++;
          Serial.print("nrled = ");
          Serial.println(nrled1);
        }
        else if(ch == "c-") {
          
          nrled1--;
          Serial.print("nrled = ");
          Serial.println(nrled1);
        }
        else if(ch == "b+") {
          
          brightness1++;
          Serial.print("brightness1 = ");
          Serial.println(brightness1);
        }
        else if(ch == "b-") {
          
          brightness1--;
          Serial.print("brightness1 = ");
          Serial.println(brightness1);
        }
        else if(ch == "ledmode") {
          
          if (ledmode1 == 1) {
            ledmode1 = 0;
          }
          else {
            ledmode1 = 1;
          }
          Serial.print("ledmode1 = ");
          Serial.println(ledmode1);
        }
        else if(ch == "l") {
          Serial.println("links");
          digitalWrite(dirPin, HIGH);
        }
        else if(ch == "r") {
          Serial.println("Rechts");
          digitalWrite(dirPin, LOW);
        }
        else if(ch == "+") {
          Serial.println("Snelheid");
          Serial.println(snelheid);
          snelheid -= 10;
        }
        else if(ch == "-") {
          Serial.print("Snelheid");
          Serial.println(snelheid);
          snelheid += 10;
        }
        else if(ch == "s") {
          Serial.println("Stap maken");
          digitalWrite(stepPin, HIGH);
          delayMicroseconds(snelheid);
          digitalWrite(stepPin, LOW);
          delayMicroseconds(snelheid);
        }
        else if(ch == "q") {
          Serial.println("Stoppen");
          digitalWrite(ledPin1, LOW);
          digitalWrite(ledPin2, LOW);
          digitalWrite(ledPin3, LOW);
          for (int i = 0; i < NUM_LEDS; i++) {
            leds[i] = CRGB::Black;
            FastLED.show();
            FastLED.delay(100);
          }
          
          start = 0;
        }
        else if(ch == "v") {
          Serial.println("Verder doen");
          start = 1;
        }
        else if(ch == "1") {
          Serial.println("Led 1 omschakelen");
          if(led1 == 1) {
            led1 = 0;
            digitalWrite(ledPin1, LOW);
          }
          else {
            led1 = 1;
            digitalWrite(ledPin1, HIGH);
          }
        }
        else if(ch ==  "2") {
          Serial.println("Led 2 omschakelen");
          if(led2 == 1) {
            led2 = 0;
            digitalWrite(ledPin2, LOW);
          }
          else {
            led2 = 1;
            digitalWrite(ledPin2, HIGH);
          }
        }
        else if(ch == "3") {
          Serial.println("Led 3 omschakelen");
          if(led3 == 1) {
            led3 = 0;
            digitalWrite(ledPin3, LOW);
          }
          else {
            led3 = 1;
            digitalWrite(ledPin3, HIGH);
          }
        }
        else if(ch == "c") {
          Serial.println("Leds laten branden");
          FastLED.setBrightness(brightness1);
          fill_solid(leds, NUM_LEDS, CRGB(0,255,0));  // fill red
        }
        

          
        
      }
   

    if (start == 1) {
      //Serial.println("traag");
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(snelheid);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(snelheid);
    }

      /*// Turn the LED on
      FastLED.setBrightness(brightness);
      if(ledmode == 1) {
        leds[nrled] = CRGB::Blue;
        FastLED.show();
      }
      else {
        leds[nrled] = CRGB::Black;
        FastLED.show();
      }*/
      

}

void startupLEDsTest() {
  // startup blink test to confirm LEDs are working.
  FastLED.setBrightness(32);
  fill_solid(leds, NUM_LEDS, CRGB(255,0,0));  // fill red
  FastLED.show();
  delay(1000);
  fill_solid(leds, NUM_LEDS, CRGB(0,255,0));  // fill green
  FastLED.show();
  delay(1000);
  fill_solid(leds, NUM_LEDS, CRGB(0,0,255));  // fill blue
  FastLED.show();
  delay(1000);
  FastLED.clear();
  FastLED.show();
  FastLED.setBrightness(40);

} //end_startupLEDsTest
