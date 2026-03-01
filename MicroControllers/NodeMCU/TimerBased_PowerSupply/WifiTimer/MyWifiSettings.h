// Wi-Fi credentials setup:
// Keep credentials in MyWifiSettings.secret.h (ignored by git).
#include "MyWifiSettings.secret.h"

#ifndef WIFI_SSID
#error "WIFI_SSID is not defined. Please set it in MyWifiSettings.secret.h"
#endif

#ifndef WIFI_PASSWORD
#error "WIFI_PASSWORD is not defined. Please set it in MyWifiSettings.secret.h"
#endif

const char* ssid = WIFI_SSID;
const char* password = WIFI_PASSWORD;
