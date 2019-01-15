#include <Adafruit_NeoPixel.h> 
#ifdef __AVR__
  #include <avr/power.h>
#endif
// Which pin on the Arduino is connected to the NeoPixels? // On a Trinket or Gemma we suggest changing this to 1
#define PIN 7
// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS 4
// When we setup the NeoPixel library, we tell it how many pixels, and which pin to use to send signals. 
// Note that for older NeoPixel strips you might need to change the third parameter--see the strandtest 
// example for more information on possible values. 
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800); 

int delayval = 100; // delay for half a second 
int n=0;
int oldPixelnum=-1;

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
  // This is for Trinket 5V 16MHz, you can remove these three lines if you are not using a Trinket
#if defined (_AVR_ATtiny85_)
  if (F_CPU == 16000000) clock_prescale_set(clock_div_1);
#endif
  // End of trinket special code
  pixels.begin(); // This initializes the NeoPixel library.
}

void loop() {
  n=0;
  if(Serial.available()>0){
	  n=Serial.read();
	  Serial.print("ho letto: ");
	  Serial.println(n);
	  pixel(n);
	  sendPositionToNextion();
  }
  delay(delayval); // Delay for a period of time (in milliseconds).
}

void pixel(int num){    //funzione gestore dei pixel
  
  num=num-48;
  if (num>7){
    num=1;
  }
  // For a set of NeoPixels the first NeoPixel is 0, second is 1, all the way up to the count of pixels minus one.
  // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
  if(num != oldPixelnum)
  {
    pixels.setPixelColor(oldPixelnum, pixels.Color(0,0,0));
    pixels.setPixelColor(num, pixels.Color(90,0,0));
    oldPixelnum=num;
  }
  // Moderately bright green color.
  pixels.show(); // This sends the updated pixel color to the hardware.
}

void sendPositionToNextion(){
  String command = "t1.txt=\""+String(n-47)+"\"";
  Serial1.print(command);
  endNextionCommand();
}

void endNextionCommand(){
  Serial1.write(0xff);
  Serial1.write(0xff);
  Serial1.write(0xff);
}
