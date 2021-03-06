// Serial test script
#include <Keyboard.h>
#include <AbsMouse.h>
int buttonPin = 9;  // Set a button to any pin
int setPoint = 55;
String readString;

void setup()
{
  pinMode(buttonPin, INPUT); // Set the button as an input
  digitalWrite(buttonPin, HIGH); // Pull the button high
  AbsMouse.init(2560, 1440);
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
     if (readString.length() > 0)
     {
        char key_in = readString.charAt(0);
        if (key_in == 's')
        {
          Keyboard.write((char) 32);  //(char) 32
          Serial.print("Done!");
          readString = "";
        }
        else if (key_in == 'M' )  // mouse move command  or cuold be less than 57 to trigger the mouse
        {
          int commaIndex = readString.indexOf(',');
          String positionX = readString.substring(1, commaIndex);
          String positionY = readString.substring(commaIndex + 1);
          int x = atoi(positionX.c_str());
          int y = atoi(positionY.c_str());
          AbsMouse.move(x, y);
          Serial.print("Done!");
          readString ="";
        }
        else
        {
          Keyboard.write(key_in); // other key command
          Serial.print("Done!");
          //Serial.println(readString); //see what was received
          readString = "";
         }
      }

     delay(500);
  }
}