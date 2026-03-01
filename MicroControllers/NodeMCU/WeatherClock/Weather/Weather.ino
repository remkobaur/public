/*********
  Remko Baur
  Date:       2018-09-07
  My IP:      http://192.168.178.32 
*********/

void print_console(String s)
{
  //Serial.println(s);  // uncomment for debugging with serial monitor
}

#define But_1 D7
#define But_2 D8
#define But_3 D6

#define menu_pages 4

boolean summertime = false;

//String IP = "192.168.178.26";
// Replace with your network credentials
#include "MySettings.h"

// Load Wi-Fi library
#include "myLib_WIFI.h"

// Load timer lib
#include "myLib_Timer.h"

// Load IO lib
#include "myLib_IOs.h"

// OLED library
#include "myLib_OLED.h"

// JSON - Weather
#include "myLib_Weather.h"

/*************** Setup *******************/
void setup() {
  init_IOs();
  init_WiFi();
  init_OLED();

  init_Timer();
  init_Weather();

  // read switch and set summer time flag
  if (Button_pressed(3) && (!summertime))
    { summertime = true;  
    init_Timer();}
  else if((!Button_pressed(3))&& (summertime))
    {summertime = false;
    init_Timer();}
    
}
/******************************************/ 
int ct = 0;
int Modus = 3;
/*************** Loop *******************/
void loop(){
  delay(1000);
//  print_console("Time: "+get_Str_Time()+"  --> "+get_time_mm()+" min");

  //disp_Weather((ct/2%num_days));
  //disp_Test1((ct/2%num_days));
    
  /*
  if (Button_pressed(1) && (Button_pressed(2)))
    {      
      int cnt=0;
      while (Button_pressed(1)&& Button_pressed(2))
      {
        cnt++;
        delay(1000);
        if (cnt == 5)
        {
          summertime = !summertime;
          init_Timer();
          break;
        }
      }
    }
  */
  
  // select next page by button click
  if (Button_pressed(1))
    { Modus = (Modus+1+menu_pages)%menu_pages;  disp_Mode();}      
 // else if(Button_pressed(2))
 //   { Modus = (Modus-1+menu_pages)%menu_pages;  disp_Mode();}      
    
  switch(Modus){
    case 0: disp_Current();break;
    case 1: disp_Weather((ct/2%num_days));break;
    case 2: disp_statistics();break;
    case 3: disp_clock();break;
  }
  /* Do each minute*/
  ct+=1;
  if ((ct%60)==0){    
    updateWeather(); // update weather data
    ct=0;
  }
}

void disp_Weather(int z){
  // z is index of the provided weather forecast list
  u8g2.firstPage();
  do {
   weather_printSymbol(weather[z]);
   //print_console(daytime[z].substring(0,8));
   //print_console(get_Str_Date());
   if (daytime[z].substring(0,2) == get_Str_Date().substring(0,2)){
    OLED_write(1,10,2,"today");
   }
   else{
    OLED_write(1,10,2,daytime[z].substring(0,8));
   }
   
   OLED_write(2,32,3,daytime[z].substring(16,23));
   //writeOled(1,0,daytime[z]);
   OLED_write(90,12,3,humidity[z]);
   OLED_write(90,32,3,temp[z]);
   } while ( u8g2.nextPage() );   
}

void disp_Current(){
  int z = 0;
  u8g2.firstPage();
  do {
   weather_printSymbol(weather[z]);
   OLED_write(1,10,2,get_Str_Date());
   //OLED_write(2,32,3,daytime[z].substring(16,23));
   OLED_write(2,32,3,get_Str_Time().substring(0,5));   
   OLED_write(90,12,3,humidity[z]);
   OLED_write(90,32,3,temp[z]);
   } while ( u8g2.nextPage() );   
}

void disp_statistics(){
  u8g2.firstPage();
  do {
  OLED_write( 5,30,2,temp_stat[0]);
  OLED_write(50,30,2,temp_stat[1]);
  OLED_write(95,30,2,temp_stat[2]);
  OLED_write(5,12,2,"act");
  OLED_write(40,12,2,"mean");
  OLED_write(95,12,2,"max");
  } while ( u8g2.nextPage() );   
}

void disp_clock(){
  u8g2.firstPage();
  do {
  //OLED_write(37,8,1,get_Str_Date());
  //OLED_write(25,32,6,get_Str_Time().substring(0,5)); 
  OLED_write(1,10,1,get_Str_Date().substring(0,2));
  OLED_write(1,25,1,get_Str_Date().substring(3,5));   
  OLED_write(25,32,7,get_Str_Time().substring(0,5));   
  } while ( u8g2.nextPage() );     
}

void disp_Mode(){
  String S;
  switch(Modus){
    case 0: S = "     aktuelles Wetter   ";break;
    case 1: S = "      Wettervorschau    ";break;
    case 2: S = "      Tagesstatistik    ";break;
    case 3: S = "              Uhr       ";break;
  }
  u8g2.firstPage();
  do {
    OLED_write(0,22,4,S);
   } while ( u8g2.nextPage() );   
  delay(1000);
}
