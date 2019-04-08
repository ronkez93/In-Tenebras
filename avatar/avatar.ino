#include <Wire.h>
#include <I2Cdev.h>
#include <MPU6050.h>
#include <SPI.h>
//#include <nRF24L01.h>
#include <RF24.h>
MPU6050 accelgyro;
#define MPU 0x68 //I2C address

//variabili sensore temperatura
#define PIN_LM35 A1

//variabili giroscopio
double ax, ay, az;
double gx, gy, gz;

//variabili battito cardiaco
unsigned long old=0;
unsigned long now=0;
double freq=0;
double  diff;
int valori[25];
int count =0;
float media=0;
int lastRead=0;
bool tempo=true;
int countNumRead=0;
int SAMPLES=25;
float stDev=0;
int *sam; 
float temp=0;
int minTemp=0;
int minBattito=0;
int Pitch, Roll;
int acceleration=0;

//variabili microfono
int soundDetectedPin = 10; // Use Pin 10 as our Input
int soundDetectedVal = HIGH; // This is where we record our Sound Measurement
boolean bAlarm = false;
unsigned long lastSoundDetectTime;
int soundAlarmTime = 500;

RF24 radio(9, 10);


// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  old=millis();
  pinMode (soundDetectedPin, INPUT) ;
  Wire.begin();
  accelgyro.initialize();
  //start radio
  radio.begin();
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(0x76);
  radio.openWritingPipe(0xF0F0F0F0E1LL);
  const uint64_t pipe = (0xE8E8F0F0E1LL);
  radio.openReadingPipe(1, pipe);
  radio.enableDynamicPayloads();
  radio.powerUp();
}

// the loop routine runs over and over again forever:
void loop() {
  if(media==0){
    battito();
    temperatura();
  }  
  else{
    radio.startListening();
    Serial.println("Starting loop. Radio on.");
    char receivedMessage[32] = {0};
    if(radio.available()){
      radio.read(receivedMessage, sizeof(receivedMessage));
      Serial.println(receivedMessage);
      Serial.println("Turning off the radio.");
      radio.stopListening();
      String stringMessage(receivedMessage);
      int scelta = stringMessage.toInt();
      const char text[8];
      switch(scelta){
        case 0:
          itoa((int)minBattito,text,10);
          radio.write(text, sizeof(text));
          Serial.println("battito minimo inviato");
        break;
        case 1:
          itoa((int)minTemp,text,10);
          radio.write(text, sizeof(text));
          Serial.println("temperatura minima inviata");
        break;
        case 2:
          itoa((int)media,text,10);
          radio.write(text, sizeof(text));
          Serial.println("battito attuale inviato");
        break;
        case 3:
          itoa((int)temperatura,text,10);
          radio.write(text, sizeof(text));
          Serial.println("temperatura attuale inviato");
        break;
        case 4:
          itoa((int)Roll,text,10);
          radio.write(text, sizeof(text));
          Serial.println("roll inviato");
        break;
        case 5:
          itoa((int)Pitch,text,10);
          radio.write(text, sizeof(text));
          Serial.println("pitch inviato");
        break;
        case 6: 
          itoa((int)acceleration,text,10);
          radio.write(text, sizeof(text));
          Serial.print("accelerazione maggiore inviata");
        }
    }
  }
//  microfono();
  
  delay(100);  
}
void temperatura(){
  int valore = analogRead(PIN_LM35);
  //float mV = valore / 1023.0 * 5000;
  //float temperatura = mV / 10;
  temp = valore / 2.046;
  Serial.print("Temp.: ");
  Serial.print(temp);
  Serial.println("°C");
  if ((int)temp<minTemp){
    minTemp=temp;
  }
}

void giroscopio(){
  FunctionsMPU();
  Roll = FunctionsPitchRoll(ax, ay, az);   //Calcolo angolo Roll
  Pitch = FunctionsPitchRoll(ax, ay, az);  //Calcolo angolo Pitch
 
  Roll = map(Roll, -180, 180, 0, 359);
  Pitch = map(Pitch, -180, 180, 359, 0);
  if (abs(ax)> abs(ay) && abs(ax)>abs(az)){
    acceleration=abs(ax)/16384;   //acceleration in Gs
  }
  if (abs(ay)> abs(ax) && abs(ay)>abs(az)){
    acceleration=abs(ay)/16384;   //acceleration in Gs
  }
  if (abs(az)> abs(ay) && abs(az)>abs(ax)){
    acceleration=abs(az)/16384;   //acceleration in Gs
  }
  /*accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  Serial.print("a/g:\t");
  Serial.print(ax); Serial.print("\t");
  Serial.print(ay); Serial.print("\t");
  Serial.print(az); Serial.print("\t");
  Serial.print(gx); Serial.print("\t");
  Serial.print(gy); Serial.print("\t");
  Serial.println(gz);*/
}

double FunctionsPitchRoll(double A, double B, double C){ //angolo giroscopio
  double DatoA, DatoB, Value;
  DatoA = A;
  DatoB = (B*B) + (C*C);
  DatoB = sqrt(DatoB);
  
  Value = atan2(DatoA, DatoB);
  Value = Value * 180/3.14;
  
  return (int)Value;
}
 
//Funzione per l'acquisizione degli assi X,Y,Z del MPU6050
void FunctionsMPU(){
  Wire.beginTransmission(MPU);
  Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(MPU,6,true);  // request a total of 14 registers
  ax=Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)     
  ay=Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  az=Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  double Tmp;
  Tmp=Wire.read()<<8|Wire.read();  // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
  gx=Wire.read()<<8|Wire.read();  // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
  gy=Wire.read()<<8|Wire.read();  // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
  gz=Wire.read()<<8|Wire.read();  // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
}

/*void microfono(){
  soundDetectedVal = digitalRead (soundDetectedPin) ; // read the sound alarm time
  if (soundDetectedVal == LOW) // If we hear a sound
  {
    lastSoundDetectTime = millis(); // record the time of the sound alarm
    // The following is so you don't scroll on the output screen
    if (!bAlarm){
      Serial.println("LOUD, LOUD");
      bAlarm = true;
    }
  }
  else
  {
    if( (millis()-lastSoundDetectTime) > soundAlarmTime  &&  bAlarm){
      Serial.println("quiet");
      bAlarm = false;
    }
  }
}*/

void battito(){
  // read the input on analog pin 0:
  int sensorValue = analogRead(A0);
  // print out the value you read:
  if(sensorValue-lastRead>=0 ){//sto salendo, quindi battito
    lastRead=sensorValue;
    tempo=true;
  }
  else{
    if(tempo){
      tempo=false;
      lastRead=sensorValue;
      now=millis();
      diff=(double)(now-old);
      freq=(double)60/((diff)/(double)1000);
      if (freq>55 && freq < 120){ 
        if(stDev==0){
          valori[count]=freq;
          count ++;
          if (countNumRead==0){
            countNumRead++;
            sam=(int*)malloc(countNumRead*sizeof(double));
            sam[countNumRead-1]=freq;
          }
          else{
            countNumRead++;
            sam=(int*)realloc(sam,countNumRead*sizeof(double));
            sam[countNumRead-1]=freq;
          }
        }
        else{
          if(media+stDev>freq && freq>media-stDev){
            valori[count]=freq;
            count ++;
            if (countNumRead==0){
            countNumRead++;
            sam=(int*)malloc(countNumRead*sizeof(double));
            sam[countNumRead-1]=freq;
            }
            else{
              countNumRead++;
              sam=(int*)realloc(sam,countNumRead*sizeof(double));
              sam[countNumRead-1]=freq;
            }
          }
          else{
            if (countNumRead==0){
            countNumRead++;
            sam=(int*)malloc(countNumRead*sizeof(double));
            sam[countNumRead-1]=freq;
            }
            else{
              countNumRead++;
              sam=(int*)realloc(sam,countNumRead*sizeof(double));
              sam[countNumRead-1]=freq;
            }
          }
        }
        if (count == SAMPLES){
          media=0;
          count=0;
          for(int i=0;i<countNumRead;i++){
            Serial.print(sam[i]);
            Serial.print("\t");
          }
          Serial.println("\t");
          for( int i=0;i<SAMPLES;i++){
            media+=valori[i];
          }
          media/=SAMPLES;
          stdDev();
          countNumRead=0;
          free(sam);
          if (media<minBattito)
            minBattito=media;
        }
      }
      old=now;
    }      
  }        // delay in between reads for stability
}

void stdDev(){
  float sampleSum = 0;
  for(int i = 0; i < countNumRead; i++) {
    sampleSum += float(sam[i]);
  }
  float meanSample = sampleSum/float(SAMPLES);

  // HOW TO FIND STANDARD DEVIATION
  // STEP 1, FIND THE MEAN. (We Just did.)

  // STEP 2, sum the squares of the differences from the mean

  float sqDevSum = 0.0;

  for(int i = 0; i < SAMPLES; i++) {
    // pow(x, 2) is x squared.
    sqDevSum += pow((meanSample - float(valori[i])), 2);
  }

  // STEP 3, FIND THE MEAN OF THAT
  // STEP 4, TAKE THE SQUARE ROOT OF THAT

  stDev = sqrt(sqDevSum/float(SAMPLES));
}
