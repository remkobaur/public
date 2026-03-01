// Wi-Fi credentials setup:
// Keep credentials in MyWifiSettings.secret.h (ignored by git).
#include "MySettings.secret.h"

#ifndef WIFI_SSID
#error "WIFI_SSID is not defined. Please set it in MySettings.secret.h"
#endif

#ifndef WIFI_PASSWORD
#error "WIFI_PASSWORD is not defined. Please set it in MySettings.secret.h"
#endif

#ifndef OPEN_WEATHER_API_KEY
#error "OPEN_WEATHER_API_KEY is not defined. Please set it in MySettings.secret.h"
#endif

#ifndef OPEN_WEATHER_API_LOC
#error "OPEN_WEATHER_API_LOC is not defined. Please set it in MySettings.secret.h"
#endif

const char* ssid = WIFI_SSID;
const char* password = WIFI_PASSWORD;
const char* open_weather_api_key = OPEN_WEATHER_API_KEY;
const char* open_weather_api_loc = OPEN_WEATHER_API_LOC;