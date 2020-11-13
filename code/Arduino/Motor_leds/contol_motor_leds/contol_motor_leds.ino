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
#define NUM_LEDS_PER_STRIP 15
#define NUM_STRIPS 2

// For led chips like WS2812, which have a data line, ground, and power, you just
// need to define DATA_PIN.  For led chipsets that are SPI based (four wires - data, clock,
// ground, and power), like the LPD8806 define both DATA_PIN and CLOCK_PIN
// Clock pin only needed for SPI based chipsets when not using hardware SPI
#define DATA_PIN1 D6
#define DATA_PIN2 D4
#define CLOCK_PIN D5

// Define the array of leds
CRGB leds[NUM_STRIPS][NUM_LEDS_PER_STRIP];
int nrled = 0;
int brightness = 32;
int ledmode = 1;
boolean verbose = false;
String ch = "";

int value = 0;
int volgnummer = 0;

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

  FastLED.addLeds<APA102, DATA_PIN1, CLOCK_PIN, RGB>(leds[0], NUM_LEDS_PER_STRIP);  // BGR ordering is typical
  FastLED.addLeds<APA102, DATA_PIN2, CLOCK_PIN, RGB>(leds[1], NUM_LEDS_PER_STRIP);  // BGR ordering is typical
  FastLED.clear();
  FastLED.show();

  startupLEDsTest();

  // set serial timeout at 10 miliseconds so 10 bytes of information can be transferred at 9600 baud
  Serial.setTimeout(10);
  
}
void loop()
{
  
  if (Serial.available()) {
    ch = Serial.readStringUntil('/');  // \n isn't detected
    //ch = Serial.readString();   // stops reading after 10 miliseconds
        String alpha, special, num; 
        for (int i=0; i<ch.length(); i++) 
        { 
            if (isdigit(ch[i])) {
                num += (ch[i]); 
            }
            else if(ch[i] >= 'a' && ch[i] <= 'z')
                alpha += (ch[i]); 
            else if(ch[i] >= 'A' && ch[i] <= 'Z') {
                switch(ch[i]) {
                  case 'A':
                    volgnummer = 0;
                    break;
                  case 'B':
                    volgnummer = 1;
                    break;
                }  
            }
            else
                special += (ch[i]); 
        } 

        if(verbose) Serial.println(alpha);
        if(verbose) Serial.println(num);
        if(verbose) Serial.println(special);
        if(verbose) Serial.println(volgnummer);
        
        if (alpha == "startupleds") {
          startupLEDsTest();
        }
        
        if (alpha == "brightness") {
          if(verbose) Serial.print("brightness");
          // als geen special is gezet, de waarde instellen.. anders de waarde verhogen met het getal bij + en verlagen bij -
          if(special == "") {
            // getal setten
            brightness = num.toInt();
          }
          else if(special == "+") {
            brightness += num.toInt();
          }
          else if(special == "-") {
            brightness -= num.toInt();
          }
          else if(special == "_") {
             brightness = 0;
          }
          if(verbose) Serial.println(brightness);
          FastLED.setBrightness(brightness);
          //FastLED.show();
        }

        if(alpha == "allon") {
          fill_solid(leds[0], NUM_LEDS_PER_STRIP, CRGB(255,255,255));  // fill White
          fill_solid(leds[1], NUM_LEDS_PER_STRIP, CRGB(255,255,255));  // fill White
          //FastLED.show();
        }
        if (alpha == "alloff") {
          fill_solid(leds[0], NUM_LEDS_PER_STRIP, CRGB(0,0,0));  // fill Black
          fill_solid(leds[1], NUM_LEDS_PER_STRIP, CRGB(0,0,0));  // fill Black
          //FastLED.show();
        }

       if (alpha == "nrled") {
            if(verbose) Serial.print("nrled ");
            // als geen special is gezet, de waarde instellen.. anders de waarde verhogen met het getal bij + en verlagen bij -
            if(special == "") {
              // getal setten
              nrled = num.toInt();
            }
            else if(special == "+") {
              nrled = num.toInt();
              ledmode = 1;
              leds[volgnummer][nrled] = CRGB::Blue;
            }
            else if(special == "-") {
               nrled = num.toInt();
               ledmode = 0;
               leds[volgnummer][nrled] = CRGB::Black;
            }
            else if(special == "_") {
               fill_solid(leds[volgnummer], NUM_LEDS_PER_STRIP, CRGB(0,0,0));  // fill black
               nrled = 0;
               ledmode = 0;
            }
            if(verbose) Serial.println(nrled);
      
            // leds aan of uit zetten
            if(ledmode == 1) {
                leds[volgnummer][nrled] = CRGB::Blue;
            }
            else {
              leds[volgnummer][nrled] = CRGB::Black;
            }
            //FastLED.show();
      }

      if (alpha == "nrleds") {
            if(verbose) Serial.print("nrleds ");
            // als geen special is gezet, de waarde instellen.. anders de waarde verhogen met het getal bij + en verlagen bij -
            if(special == "") {
              // getal setten
              nrled = num.toInt();
            }
            else if(special == "+") {
              nrled = num.toInt();
              ledmode = 1;
              leds[0][nrled] = CRGB::Blue;
              leds[1][nrled] = CRGB::Blue;
            }
            else if(special == "-") {
               nrled = num.toInt();
               ledmode = 0;
               leds[0][nrled] = CRGB::Black;
               leds[1][nrled] = CRGB::Black;
            }
            else if(special == "_") {
               fill_solid(leds[0], NUM_LEDS_PER_STRIP, CRGB(0,0,0));  // fill black
               fill_solid(leds[1], NUM_LEDS_PER_STRIP, CRGB(0,0,0));  // fill black
               nrled = 0;
               ledmode = 0;
            }
            if(verbose) Serial.println(nrled);
  
            // leds aan of uit zetten
            if(ledmode == 1) {
                leds[0][nrled] = CRGB::Blue;
                leds[1][nrled] = CRGB::Blue;
            }
            else {
              leds[0][nrled] = CRGB::Black;
              leds[1][nrled] = CRGB::Black;
            }
            //FastLED.show();
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
            step = num.toInt();
            //Serial.println("Links");
            digitalWrite(dirPin, HIGH);
          }
          else if(special == "-") {
            //Serial.println(num);
            step = num.toInt();
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
       
        if(ch == "q") {
          Serial.println("Stoppen");
          digitalWrite(ledPin1, LOW);
          digitalWrite(ledPin2, LOW);
          digitalWrite(ledPin3, LOW);
          fill_solid(leds[0], NUM_LEDS_PER_STRIP, CRGB(0,0,0));  // fill Black
          fill_solid(leds[1], NUM_LEDS_PER_STRIP, CRGB(0,0,0));  // fill Black
          //FastLED.show();
          start = 0;
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
      

      // send changes to ledstrip
      FastLED.show();
  }

}

void startupLEDsTest() {
  // startup blink test to confirm LEDs are working.

  FastLED.setBrightness(32);
  fill_solid(leds[0], NUM_LEDS_PER_STRIP, CRGB(255,0,0));  // fill red
  FastLED.show();
  delay(1000);
  fill_solid(leds[0], NUM_LEDS_PER_STRIP, CRGB(0,255,0));  // fill green
  FastLED.show();
  delay(1000);
  fill_solid(leds[0], NUM_LEDS_PER_STRIP, CRGB(0,0,255));  // fill blue
  FastLED.show();
  delay(1000);
  FastLED.clear();
  FastLED.show();
  FastLED.setBrightness(40);

   FastLED.setBrightness(32);
  fill_solid(leds[1], NUM_LEDS_PER_STRIP, CRGB(255,0,0));  // fill red
  FastLED.show();
  delay(1000);
  fill_solid(leds[1], NUM_LEDS_PER_STRIP, CRGB(0,255,0));  // fill green
  FastLED.show();
  delay(1000);
  fill_solid(leds[1], NUM_LEDS_PER_STRIP, CRGB(0,0,255));  // fill blue
  FastLED.show();
  delay(1000);
  FastLED.clear();
  FastLED.show();
  FastLED.setBrightness(40);

} //end_startupLEDsTest
