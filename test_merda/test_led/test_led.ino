#include <Adafruit_NeoPixel.h> 
#include <SPI.h>
//#include <MFRC522.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif
// Which pin on the Arduino is connected to the NeoPixels? // On a Trinket or Gemma we suggest changing this to 1

#define PIN 7
/*#define SS_PIN 53
#define RST_PIN 5
#define LED_G 2 //define green LED pin
#define LED_R 4 //define red LED
MFRC522 mfrc522(SS_PIN, RST_PIN);*/

// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS 8
// When we setup the NeoPixel library, we tell it how many pixels, and which pin to use to send signals. 
// Note that for older NeoPixel strips you might need to change the third parameter--see the strandtest 
// example for more information on possible values. 
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800); 

int delayval = 100; // delay for half a second 
int n=0;
int pos = 0;

void setup() {
  Serial.begin(9600);
  // This is for Trinket 5V 16MHz, you can remove these three lines if you are not using a Trinket
#if defined (_AVR_ATtiny85_)
  if (F_CPU == 16000000) clock_prescale_set(clock_div_1);
#endif
  // End of trinket special code
  pixels.begin(); // This initializes the NeoPixel library.
  
  /*SPI.begin();      // Initiate  SPI bus
  mfrc522.PCD_Init();   // Initiate MFRC522
  //myServo.attach(3); //servo pin
  //myServo.write(0); //servo start position
  pinMode(LED_G, OUTPUT);
  pinMode(LED_R, OUTPUT);
  //pinMode(BUZZER, OUTPUT);
  //noTone(BUZZER);
  Serial.println("Put your card to the reader...");
  Serial.println();*/
}

void loop() {
  n=0;
  n=Serial.read();
  n=n-48;
  pos = n;
  sendTextToNextion();
  if (n>7){
    n=1;
  }
  /*// For a set of NeoPixels the first NeoPixel is 0, second is 1, all the way up to the count of pixels minus one.
  // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255
  pixels.setPixelColor(n, pixels.Color(90,0,0)); // Moderately bright green color.
  pixels.show(); // This sends the updated pixel color to the hardware.
  delay(delayval); // Delay for a period of time (in milliseconds).

  // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent()) 
  {
    return;
  }
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) 
  {
    return;
  }
  //Show UID on serial monitor
  Serial.print("UID tag :");
  String content= "";
  byte letter;
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
     Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
     Serial.print(mfrc522.uid.uidByte[i], HEX);
     content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  Serial.println();
  Serial.print("Message : ");
  content.toUpperCase();
  if (content.substring(1) == "69 B4 DB 56") //change here the UID of the card/cards that you want to give access
  {
    Serial.println("Item n.1 used");
    Serial.println();
    delay(500);
    digitalWrite(LED_G, HIGH);
    //tone(BUZZER, 500);
    //delay(300);
    //noTone(BUZZER);
    //myServo.write(180);
    delay(5000);
    //myServo.write(0);
    digitalWrite(LED_G, LOW);
  }
 
 else   {
    Serial.println("Item n.2 used");
    digitalWrite(LED_R, HIGH);
    //tone(BUZZER, 300);
    delay(1000);
    digitalWrite(LED_R, LOW);
    //noTone(BUZZER);*/
  }
}

void sendTextToNextion()
{
  String command = "t1.txt=\""+String(pos)+"\"";
  Serial.print(command);
  endNextionCommand();
}

void endNextionCommand()
{
  Serial.write(0xff);
  Serial.write(0xff);
  Serial.write(0xff);
}
