#include <WiFi.h>

// WiFi credentials
const char* ssid = "Elite Group";                    //Enter your wifi hotspot ssid
const char* password =  "Spyvrat7";               //Enter your wifi hotspot password
const uint16_t port = 8002;
const char * host = "192.168.29.162";                   //Enter the ip address of your laptop after connecting it to wifi hotspot
volatile bool ismoving = false;

hw_timer_t *My_timer = NULL;

char incomingPacket[80];
WiFiClient client;

String msg = "0";

void setup(){
   
  Serial.begin(115200);                          //Serial to print data on Serial Monitor
  Serial1.begin(115200,SERIAL_8N1,33,32);        //Serial to transfer data between ESP and AVR. The Serial connection is inbuilt.
  
  
  //Connecting to wifi
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  }
 
  Serial.print("WiFi connected with IP: ");
  Serial.println(WiFi.localIP());

  //My_timer = timerBegin(0, 80, true);
  //timerAttachInterrupt(My_timer, &onTimer, true);
  //timerAlarmWrite(My_timer, 10000, true);
  //timerAlarmEnable(My_timer); //Just Enable
}

void loop() {

  if (!client.connect(host, port)) {
    Serial.println("Connection to host failed");
    delay(200);
    return;
  }
  
  while(1){
      msg = client.readStringUntil('\n');         //Read the message through the socket until new line char(\n)
      if (msg.length() == 0) {
        continue;
      }
      client.print("1");                          //Send an acknowledgement to host(laptop)
      client.flush();
      Serial.println(msg);                        //Print data on Serial monitor
      Serial1.println(msg);                       //Send data to AVR
      Serial1.flush();
    }
}
