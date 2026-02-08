#ifndef myTypes_h
#define myTypes_h

#include <WString.h>

typedef struct {
  int t_start_hh[Max_Entries];
  int t_start_mm[Max_Entries];
  int t_dur_on[Max_Entries];
  int t_start_min[Max_Entries];
  int t_manual;
} configData_t;

/*
// Types 'byte' und 'word' doesn't work!
typedef struct {
  int valid;                        // 0=no configuration, 1=valid configuration
  char SSID[31];                    // SSID of WiFi
  char password[31];                // Password of WiFi
  int  useMQTT;                     // 0=Don't use, 1=use MQTT
  char MQTTHost[31];                // Ip address or hostname of MQTT broker
  char MQTTPort[11];                // Port of MQTT broker
  char MQTTpubCH0[61];              // MQTT publish CH0 topic
  char MQTTpubCH1[61];              // MQTT publish CH1 topic
  char MQTTsubCH0[61];              // MQTT subscribe CH0 topic
  char MQTTsubCH1[61];              // MQTT subscripe CH1 topic
  int useCH0;                       // 0=Don't use, 1=use channel 0
  int useCH1;                       // 0=Don't use, 1=use channel 1
} configData_t;
*/
#endif