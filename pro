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
        else if (key_in <=57 )  // mouse move command
        {
          String str = readString;
          char str_array[str.length()+1];
          str.toCharArray(str_array, str.length()+1);
          char *p = strtok(str_array, ",");
          char *coordi[2];
          int i = 0;
          while (p != NULL)
          {
           coordi[i++] = p;
           p = strtok (NULL, ",");
          }
//          Keyboard.write(coordi[5]);
          Serial.print(coordi[1]);
          Serial.print(coordi[0]);
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