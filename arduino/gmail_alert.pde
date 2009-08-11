/*
physical-gmail-alert is a arduino script that physically alert the arrival of gmails 
Copyright (C) 2008  laboratorio (info@laboratorio.us)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

int led1Pin = 13;
int led2Pin = 12;
int led3Pin = 11;

int incomingByte;

void setup() {
 Serial.begin(9600);
 pinMode(led1Pin, OUTPUT);
 pinMode(led2Pin, OUTPUT);
 pinMode(led3Pin, OUTPUT);
}

void loop() {
  
 if (Serial.available() > 0) {
   
   incomingByte = Serial.read();
   
   if (incomingByte == 'H') {
     ledBlink(HIGH);  
   }
   
   delay(500);
   ledBlink(LOW);

 }
 
}

void ledBlink(int mode) {
  digitalWrite(led1Pin, mode);
  digitalWrite(led2Pin, mode);
  digitalWrite(led3Pin, mode);
}