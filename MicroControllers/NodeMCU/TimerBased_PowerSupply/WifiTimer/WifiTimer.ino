/*********
  Remko Baur
  Date: 06.08.2018
  My IP: http://192.168.178.26  (Zeitschaltung)
  WifiTimer - Timer-based WiFi power supply controller
*********/

#define Max_Entries 3

#define RELAY1_PIN D0
#define RELAY2_PIN D1
#define BUTTON_PIN D6
#define LEVEL_SWITCH_PIN D5
#define LED D4

String IP = "192.168.178.26";

void print_console(String s)
{
  /**
   * @brief Print a message to the console if console output is enabled.
   *
   * Wrapper around Serial.println() kept to easily enable/disable
   * console output across the project.
   */
  //Serial.println(s);
  }
void print_debug(String s)
{
  /**
   * @brief Print a debug message when debug output is enabled.
   *
   * This function intentionally mirrors `print_console()` and can be
   * enabled/disabled centrally.
   */
  //Serial.println(s);
  }
#include "myLib_PersistentVars.h"
/*************** timer & schedule *******************/
// Load timer lib
#include "myLib_Timer.h"

#include "myLib_IOs.h"

// Load Wi-Fi library
#include "myLib_Webserver.h"

 
/*************** Setup *******************/
void setup() {
  /**
   * @brief Arduino setup routine.
   *
   * Initializes IO, Wi-Fi, time synchronization and loads configuration
   * from persistent storage.
   */
  init_IOs();
  init_WiFi();
  time_synch(timezone);
  print_time();

  for(int zz=0;zz<Log_length;zz++){Log[zz]="---";}
  // load setting from EEPROM or save it the first time
  /*
  if (false){
    //eraseConfig();
    for (int z =0;z<Max_Entries;z++)
    {
      cfg.t_start_hh[z] = 13;
      cfg.t_start_mm[z] = 30;
      cfg.t_dur_on[z] = 6;// [min]
      cfg.t_manual = 6;
      set_start_min(z,7,30);
    }  
    saveConfig();
  }
  */
  loadConfig();
}
/*************** Loop *******************/
boolean trigger;
boolean act_check;
boolean old_check = false;
int Timer_status;

void loop(){
  /**
   * @brief Main program loop.
   *
   * Handles scheduling, manual button events and runs the webserver
   * request handler. Runs periodically with a short delay.
   */
  delay(500);
//  print_time();
  tm* T = get_time();
  //Serial.println("Time: "+aktZeit +"  --> "+get_time_mm()+" min");

  act_check = check_time();
  trigger = (act_check && !old_check); // rising edge
 
  if  (isButtonPressed())
  {
    if(Switch_is_on())
    { //Abort 
      Switch_off();
      Timer_stop();
      Log_write("Extern");
    }
    else // start timer
    {
      Timer_status = my_Timer(cfg.t_manual,true);
      Switch_on();
      Log_write("Extern");
    }    
  }
  else if (trigger)
  { 
    // start timer
    Timer_status = my_Timer(0,true);
  }
  else // check timer and update Timer_Status
  {
    Timer_status = my_Timer(0,false);
  }
    
  // Timer actions
  switch (Timer_status){
    case 0:                 break;
    case 1:  Switch_on();   break;
    case 2:  Switch_off();  break;
  }

  if ( (Timer_status == 1 && trigger) ||  (Timer_status == 2)) //(Timer_status == 2 && old_check))
  { Log_write("Auto"); }  

  old_check = act_check; 
  
  // check water level
  isLevelOk();

//  is_soil_dry();
  
  //Webserver
  exec_WebServer();
}
