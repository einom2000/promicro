// Serial test script
#include <Keyboard.h>
int buttonPin = 9;  // Set a button to any pin
int setPoint = 55;
String readString;

void setup()
{
  pinMode(buttonPin, INPUT); // Set the button as an input
  digitalWrite(buttonPin, HIGH); // Pull the button high
  Serial.begin(9600);  // initialize serial communications at 9600 bps
  Keyboard.begin();

}

void loop()
{
  if (digitalRead(buttonPin) == 0)
  {
    // serial read section
    while (Serial.available()) // this will be skipped if no data present, leading to
                             // the code sitting in the delay function below
    {
      delay(30);  //delay to allow buffer to fill
      if (Serial.available() > 0)
      {
        char c = Serial.read();  //gets one byte from serial buffer
        readString += c; //makes the string readString
       }
     }
     if (readString.length() >0)
     {
        char key_in = readString.charAt(0);
        Keyboard.write(key_in);
        Serial.print("Done!");
        //Serial.println(readString); //see what was received
        readString = "";
      }

     delay(500);
  }
}