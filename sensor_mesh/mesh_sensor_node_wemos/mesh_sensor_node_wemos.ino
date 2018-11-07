//************************************************************
// Sensor node code for wemos sensor
//
// 
// 
//
//
//************************************************************
#include <painlessMesh.h>
#include <painlessMeshSync.h>
#include <painlessScheduler.h>
#include <WEMOS_DHT12.h>


#define   MESH_PREFIX     "HakalaSensorNode"
#define   MESH_PASSWORD   "password"
#define   MESH_PORT       5555

void sendMessage() ;
painlessMesh  mesh;
Task taskSendMessage( TASK_SECOND * 600 , TASK_FOREVER, &sendMessage );

DHT12 dht12;
void sendMessage() {
    String msg = ";";
    if(dht12.get()==0){
      // Reading temperature or humidity takes about 250 milliseconds!
      // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
      float h = dht12.humidity;
      // Read temperature as Celsius (the default)
      float t = dht12.cTemp;
      
      msg += mesh.getNodeId();
      msg +=";H;" + String(h) + ";T;" + String(t) + ";\n";
    }
    else
    {
      String error_msg = "Failed to read from sensor, nodeid: ";
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

  mesh.scheduler.addTask( taskSendMessage );
  taskSendMessage.enable() ;
  Serial.printf("Setup Done");

}

void loop() {
  mesh.update();
  //Serial.printf("Setup Done");
}
