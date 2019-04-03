//Send.ino

#include<SPI.h>
#include<RF24.h>

// ce, csn pins
RF24 radio(7, 8);
#define heartPin A0

void setup(void){
  radio.begin();
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(0x76);
  radio.openWritingPipe(0xF0F0F0F0E1LL);
  radio.enableDynamicPayloads();
  radio.powerUp();
  Serial.begin(115200);
}

void loop(void){
    const char text[] = "Hello World is awesome";
    radio.write(&text, sizeof(text));
    int heartValue = analogRead(heartPin);
    Serial.println(heartValue);
    delay(20);

}
