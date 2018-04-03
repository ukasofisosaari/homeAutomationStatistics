//************************************************************
// this is a simple example that uses the painlessMesh library
//
// 1. sends a silly message to every node on the mesh at a random time betweew 1 and 5 seconds
// 2. prints anything it recieves to Serial.print
//
//
//************************************************************
#include <painlessMesh.h>
#include <painlessMeshSync.h>
#include <painlessScheduler.h>
#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 4     // what digital pin the DHT22 is conected to
#define DHTTYPE DHT22   // there are multiple kinds of DHT sensors

#define   MESH_PREFIX     "HakalaSensorNode"
#define   MESH_PASSWORD   "password"
#define   MESH_PORT       5555

DHT dht(DHTPIN, DHTTYPE);

enum meshNodeType {
  MESH_GATEWAY = 1,
  MESH_DHT_NODE= 2,
  MESH_UNKNOWN = 0
};

meshNodeType node_type = MESH_UNKNOWN;
void sendMessage() ;
painlessMesh  mesh;
Task taskSendMessage( TASK_SECOND * 1 , TASK_FOREVER, &sendMessage );

void sendMessage() {
    String error_msg = "";
    // Reading temperature or humidity takes about 250 milliseconds!
    // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
    float h = dht.readHumidity();
    // Read temperature as Celsius (the default)
    float t = dht.readTemperature();

    // Check if any reads failed and exit early (to try again).
    if (isnan(h) || isnan(t) ) {
      error_msg = "Failed to read from sensor, nodeid: ";
    }

    
    String msg = ";";
    if(error_msg.length() == 0) {
      msg += mesh.getNodeId();
      msg +=";H;" + String(h) + ";T;" + String(t) + ";\n";
    }
    else {
      msg = mesh.getNodeId();
      msg += error_msg;
    }
  
    mesh.sendBroadcast( msg );
    
    Serial.printf(" Sent message;%s", msg.c_str());
    taskSendMessage.setInterval( random( TASK_SECOND * 1, TASK_SECOND * 5 ));
}




void receivedCallback( uint32_t from, String &msg ) {
  Serial.printf(";R;%u;msg;%s", from, msg.c_str());
}

void newConnectionCallback(uint32_t nodeId) {
    //Serial.printf("--> startHere: New Connection, nodeId = %u\n", nodeId);
}

void changedConnectionCallback() {
    //Serial.printf("Changed connections %s\n",mesh.subConnectionJson().c_str());
}

void nodeTimeAdjustedCallback(int32_t offset) {
    //Serial.printf("Adjusted time %u. Offset = %d\n", mesh.getNodeTime(),offset);
}

void setup() {
  Serial.begin(9600);

//mesh.setDebugMsgTypes( ERROR | MESH_STATUS | CONNECTION | SYNC | COMMUNICATION | GENERAL | MSG_TYPES | REMOTE ); // all types on
  mesh.setDebugMsgTypes( ERROR | STARTUP );  // set before init() so that you can see startup messages

  mesh.init( MESH_PREFIX, MESH_PASSWORD, MESH_PORT );
  mesh.onNodeTimeAdjusted(&nodeTimeAdjustedCallback);


  
  mesh.onReceive(&receivedCallback);
  mesh.onNewConnection(&newConnectionCallback);
  mesh.onChangedConnections(&changedConnectionCallback);


  node_type = MESH_DHT_NODE;
  mesh.scheduler.addTask( taskSendMessage );
  taskSendMessage.enable() ;
  Serial.printf("Setup Done");

}

void loop() {
  mesh.update();
  //Serial.printf("Setup Done");
}
