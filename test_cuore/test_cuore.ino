/*
  AnalogReadSerial
  Reads an analog input on pin 0, prints the result to the serial monitor.
  Graphical representation is available using serial plotter (Tools > Serial Plotter menu)
  Attach the center pin of a potentiometer to pin A0, and the outside pins to +5V and ground.

  This example code is in the public domain.
*/
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
// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  old=millis();
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input on analog pin 0:
  int sensorValue = analogRead(A1);
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
        Serial.print(count);
        Serial.print("\t");
        Serial.print(stDev);
        Serial.print("\t");
        Serial.print(media);
        Serial.print("\t");
        Serial.print(freq);
        Serial.println("\t"); 
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
        }
      }
      old=now;
    }      
  }
  delay(100);        // delay in between reads for stability
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
