//************************************************************
// Sensor node with DS18B20 temperature sensor
//
// 1. Reads temperature sensor
// 2. Sends it to mesh network
//
//
//************************************************************
#include <painlessMesh.h>
#include <OneWire.h>
#include <DallasTemperature.h>

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

void sendMessage() ;
meshNodeType node_type = MESH_DS18B20_NODE;
Scheduler userScheduler;
painlessMesh  mesh;
Task taskSendMessage( TASK_SECOND * 600 , TASK_FOREVER, &sendMessage );

// GPIO where the DS18B20 is connected to
const int oneWireBus = 4;     

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(oneWireBus);

// Pass our oneWire reference to Dallas Temperature sensor 
DallasTemperature sensors(&oneWire);

void sendMessage() {
    String msg = ";";
    sensors.requestTemperatures(); 
    float temperatureC = sensors.getTempCByIndex(0);
      
    msg += mesh.getNodeId();
    msg +=";H;NO_HUMIDITY;T;" + String(temperatureC) + ";\n";
    
  
    mesh.sendBroadcast( msg );
    
    Serial.printf(" Sent message;%s", msg.c_str());
    taskSendMessage.setInterval( random( TASK_SECOND * 1, TASK_SECOND * 5 ));
}

void receivedCallback( uint32_t from, String &msg ) {
  //Serial.printf(";R;%u;msg;%s", from, msg.c_str());
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

  mesh.init( MESH_PREFIX, MESH_PASSWORD, &userScheduler, MESH_PORT );
  mesh.onNodeTimeAdjusted(&nodeTimeAdjustedCallback);


  
  mesh.onReceive(&receivedCallback);
  mesh.onNewConnection(&newConnectionCallback);
  mesh.onChangedConnections(&changedConnectionCallback);

  userScheduler.addTask( taskSendMessage );
  taskSendMessage.enable() ;
  Serial.printf("Setup Done");

}

void loop() {
  mesh.update();
  //Serial.printf("Setup Done");
}
