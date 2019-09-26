void setup()  {
 
 Serial.begin(9600); //Start serial communication boud rate at 9600
 pinMode(5,INPUT); //Pin 5 as signal input
 
}
void loop()  {
 while(1)  {
   delay(500);
   if(digitalRead(5)==LOW)  { 
    // If no signal print collision detected
     Serial.println("Collision Detected.");
   }
   else  {
     // If signal detected print collision detected
     Serial.println("No Collision Detected.");
   }
 }
}