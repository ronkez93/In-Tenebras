#include <Adafruit_NeoPixel.h> 
#include <SPI.h>
#include <MFRC522.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif
// Which pin on the Arduino is connected to the NeoPixels? // On a Trinket or Gemma we suggest changing this to 1
#define SS_PIN 53
#define RST_PIN 5
#define LED_G 2 //define green LED pin
#define LED_R 4

#define PIN 7
// How many NeoPixels are attached to the Arduino?
#define NUMPIXELS 225
// When we setup the NeoPixel library, we tell it how many pixels, and which pin to use to send signals. 
// Note that for older NeoPixel strips you might need to change the third parameter--see the strandtest 
// example for more information on possible values. 
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800); 
MFRC522 mfrc522(SS_PIN, RST_PIN);

int delayval = 100; // delay for half a second 
int n=0;
int oldPixelnum=-1;
String inputString="";
int pixelcolor=0;
String color="";

void setup() {
  //rfid
  SPI.begin();
  mfrc522.PCD_Init();

  //serial and LCD
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
  char inputstring[200];
  String readed="";
  int buffindex=0;
  bool received=false;
  while(Serial.available()>0){
	  char letto=Serial.read();
   readed+=letto;
    if (letto!='\n'){
      inputstring[buffindex]=letto;
      buffindex++;
    }
    received=true;
  }
  //Serial.print(readed);
  bool lettonum=false;
  String num="";
  String pixcolor="";
  if (received){
    //Serial.println("im in");
    for (int i=0;i<buffindex;i++){ 
      if (inputstring[i] != ',' && !lettonum){
          num+=inputstring[i];
      }
      if (inputstring[i]==','){
        n=num.toInt();
        lettonum=true;
      }
      if (inputstring[i] != ';' && lettonum && inputstring[i] != ','){
        pixcolor+=inputstring[i];
      }
      if (inputstring[i] == ';'){
        pixelcolor=pixcolor.toInt();
        /*Serial.print("ho letto: ");
        Serial.println(n);
        Serial.print("colore: ");
        Serial.println(pixelcolor);*/
        pixel(n,pixelcolor);
        delay(100);
        num="";
        pixcolor="";
        lettonum=false;
      }
    }
    sendPositionToNextion();
  }
  rfid();
  delay(delayval); // Delay for a period of time (in milliseconds).
  ledoff();
}

void pixel(int num, int pc){    //funzione gestore dei pixel
  
  // For a set of NeoPixels the first NeoPixel is 0, second is 1, all the way up to the count of pixels minus one.
  // pixels.Color takes RGB values, from 0,0,0 up to 255,255,255

    switch (pc){
      case 4:
          pixels.setPixelColor(num, pixels.Color(40,0,0));
          break;
       case 3:
          pixels.setPixelColor(num, pixels.Color(150,0,0));
          break;
       case 1:
          pixels.setPixelColor(num, pixels.Color(0,60,120));
          break;
       case 0:
          pixels.setPixelColor(num, pixels.Color(180,160,120));
          break;
       case 5:
          for (int i=0;i<NUMPIXELS;i++){
            pixels.setPixelColor(i, pixels.Color(0,0,0));
          }
          break;
          case 2:
          pixels.setPixelColor(num, pixels.Color(180,0,120));
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

void rfid(){
  //Serial.println("dentro funz. rfid");
    // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent()) 
  {
    return;
  }
  //Serial.println("trovata carta");
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) 
  {
    return;
  }
  //Serial.println("scelta una");
  String content= "";
  byte letter;
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
     //Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
     //Serial.print(mfrc522.uid.uidByte[i], HEX);
     content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
     content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  content.toUpperCase();
  Serial.println(content);
  if (content.equals("04 27 84 EA E6 4C 81")) //change here the UID of the card/cards that you want to give access
  {
    Serial.write("1");
    //Serial.println("Item n.1 used");
    //Serial.println();
    //delay(500);
    //digitalWrite(LED_G, HIGH);
    //tone(BUZZER, 500);
    //delay(300);
    //noTone(BUZZER);
    //myServo.write(180);
    //delay(5000);
    //myServo.write(0);
    
  }
  else{
    if (content.equals("04 38 83 BA 90 5B 81")){
      Serial.write("2");
      //Serial.println("Item n.2 used");
      //digitalWrite(LED_R, HIGH);
      //tone(BUZZER, 300);
      //delay(1000);  
      //noTone(BUZZER);
    }
  }
}

void ledoff(){
  digitalWrite(LED_G, LOW);
  digitalWrite(LED_R, LOW);
}
