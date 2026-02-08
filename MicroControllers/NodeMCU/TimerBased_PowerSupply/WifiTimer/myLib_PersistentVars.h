//********************************************************
//SRC: https://forum.arduino.cc/index.php?topic=410516.0

#include <EEPROM.h>

#include "myTypes.h"

#define cfgStart 1234

configData_t cfg;

void eraseConfig() {
  // Reset EEPROM bytes to '0' for the length of the data structure
  EEPROM.begin(4095);
  for (int i = cfgStart ; i < sizeof(cfg) ; i++) {
    EEPROM.write(i, 0);
  }
  delay(200);
  EEPROM.commit();
  EEPROM.end();
}

void saveConfig() {
  eraseConfig();
  
  // Save configuration from RAM into EEPROM
  EEPROM.begin(4095);
  EEPROM.put( cfgStart, cfg );
  delay(200);
  EEPROM.commit();                      // Only needed for ESP8266 to get data written
  EEPROM.end();                         // Free RAM copy of structure
}

void loadConfig() {
  // Loads configuration from EEPROM into RAM
  EEPROM.begin(4095);
  EEPROM.get( cfgStart, cfg );
  EEPROM.end();
}

