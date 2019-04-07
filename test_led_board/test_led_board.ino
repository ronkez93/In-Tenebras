#include <Adafruit_NeoPixel.h>
 
#define PIN      7
#define N_LEDS 225
 
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(N_LEDS, PIN, NEO_GRB + NEO_KHZ800);
 
void setup() {
  pixels.begin();
}
 
void loop() {
  chase(pixels.Color(50, 0, 0)); // Red
  chase(pixels.Color(0, 50, 0)); // Green
  chase(pixels.Color(0, 0, 50)); // Blue
}
 
static void chase(uint32_t c) {
  for(uint16_t i=0; i<pixels.numPixels()+4; i++) {
      pixels.setPixelColor(i  , c); // Draw new pixel
      pixels.setPixelColor(i-4, 0); // Erase pixel a few steps back
      pixels.show();
      delay(25);
  }
}
