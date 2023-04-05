//************************************************************
// Gateway for the mesh sensor network
//
// 1. Receives messages
// 2. Prints them to serial port
//
//
//************************************************************
#include <painlessMesh.h>

#define   MESH_PREFIX     "HakalaSensorNode"
#define   MESH_PASSWORD   "password"
#define   MESH_PORT       5555

enum meshNodeType {
  MESH_GATEWAY = 1,
  MESH_WEMOS_DHT12_NODE= 2,
  MESH_DS18B20_NODE= 3,
  MESH_WEMOS_SHT3X_NODE= 4,
  MESH_UNKNOWN = 0
};

meshNodeType node_type = MESH_GATEWAY;
painlessMesh  mesh;


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

  node_type = MESH_GATEWAY;  

  mesh.onReceive(&receivedCallback);
  mesh.onNewConnection(&newConnectionCallback);
  mesh.onChangedConnections(&changedConnectionCallback);

  Serial.printf("Setup Done");

}

void loop() {
  mesh.update();
}
