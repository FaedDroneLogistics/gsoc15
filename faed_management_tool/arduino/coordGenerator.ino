
#include <SPI.h>
#include <Ethernet.h>


// Enter a MAC address for your controller below.
// Newer Ethernet shields have a MAC address printed on a sticker on the shield
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
// if you don't want to use DNS (and reduce your sketch size)
// use the numeric IP instead of the name for the server:
//IPAddress server(74,125,232,128);  // numeric IP for Google (no DNS)

IPAddress server(172,26,17,106);  // numeric IP for Google (no DNS)

//char server[] = "www.google.com";    // name address for Google (using DNS)

// fill in your Domain Name Server address here:
IPAddress myDns(1, 1, 1, 1);

// Set the static IP address to use if the DHCP fails to assign
IPAddress ip(172,26,17,200);

// Initialize the Ethernet client library
// with the IP address and port of the server
// that you want to connect to (port 80 is default for HTTP):
EthernetClient client;



String lat;
String lng;
String getPath;

const int buttonPin = 7;     // the number of the pushbutton pin
const int ledPin =  13;      // the number of the LED pin

// variables will change:
int buttonState = 0;         // variable for reading the pushbutton status



void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  
  // initialize the LED pin as an output:
  pinMode(ledPin, OUTPUT);      
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT); 
  digitalWrite(buttonPin, HIGH);   

  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }

  // give the ethernet module time to boot up:
  delay(1000);
  // start the Ethernet connection using a fixed IP address and DNS server:
  Ethernet.begin(mac, ip, myDns);
  // print the Ethernet board/shield's IP address:
  Serial.print("My IP address: ");
  Serial.println(Ethernet.localIP());



}



void loop(){
  // read the state of the pushbutton value:
  buttonState = digitalRead(buttonPin);
  Serial.println(buttonState);
  // check if the pushbutton is pressed.
  // if it is, the buttonState is HIGH:
  if (buttonState == HIGH) {  
    // turn LED on:    
    digitalWrite(ledPin, HIGH);  
    

  } 
  else {
    // turn LED off:
    digitalWrite(ledPin, LOW); 
    lat = generateLat();
    lng = generateLng();

    Serial.println(lat + " - " + lng);

    getPath= "GET /incidence/?lat=" + lat + "&lng=" + lng +" HTTP/1.1";
    delay(1000);

    httpRequest(getPath);
 
    delay(1000);

    
  }
}


String generateLat(){
  
  String lleidaLat = "41.6";
  long randLat = random(5397, 26646);
  String randLatString = String(randLat);
  
  if ( randLatString.length() < 5){
    randLatString = "0"+randLatString;
  }
  
  lleidaLat = lleidaLat + randLatString;
  return lleidaLat;
}


String generateLng(){
  
  String lleidaLng = "0.6";
  long randLng = random(8994, 40554);
  String randLngString = String(randLng);
  
  if ( randLngString.length() < 5){
    randLngString = "0"+randLngString;
  }

  lleidaLng = lleidaLng + randLngString;
  return lleidaLng;
}



// this method makes a HTTP connection to the server:
void httpRequest(String url) {
  // close any connection before send a new request.
  // This will free the socket on the WiFi shield
  client.stop();
  
  // if there's a successful connection:
  if (client.connect(server, 8000)) {
    Serial.println("connecting...");
    // send the HTTP PUT request:
    client.println(url);
    client.println("Host: 172.26.17.246");
    client.println("Connection: close");
    client.println();

    // note the time that the connection was made:
    //lastConnectionTime = millis();
  }
  else {
    // if you couldn't make a connection:
    Serial.println("connection failed");
  }
}



