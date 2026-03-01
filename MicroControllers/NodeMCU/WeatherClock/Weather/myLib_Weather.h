//myLib_Weather
#include <ArduinoJson.h> 

String W_API_key = open_weather_api_key;
String W_API_loc = open_weather_api_loc; 

WiFiClient client; 

int status = WL_IDLE_STATUS; 
char W_API_server[] = "api.openweathermap.org";  

#define num_days 8

String humidity[num_days];
String pressure[num_days];
String temp[num_days];
String temp_min[num_days];
String temp_max[num_days];
String clouds[num_days];
String weather[num_days];
String daytime[num_days];

String temp_stat[3];

String str_transfer(String S){
 return S;
}

String get_weather_Str(int z){
  String S= daytime[z]+": "+weather[z]+ ", Clouds: " +clouds[z]+", pressure: "+pressure[z]+", humidity:"+humidity[z]+", temp:"+temp_min[z]+" - "+temp_max[z];
  print_console(S);
  return S;
}

int mean_temp(){
  int sum=0;
  for(int i=0;i<num_days;i++){
    sum += temp[i].substring(0,3).toInt();
  }
  return sum/num_days;
}

int max_temp(){
  int Max=temp[0].substring(0,3).toInt();
  for(int i=0;i<num_days;i++){
    if (Max < temp[i].substring(0,3).toInt())
    {Max = temp[i].substring(0,3).toInt(); }
  }
  return Max;
}


void getWeather() { 
  //http://api.openweathermap.org/data/2.5/forecast?q=wolfsburg,DE&cnt=3&appid=083fd066dd85af6d33e7716ce677f973
  //String "http://api.openweathermap.org/data/2.5/forecast?q="+W_API_loc+"&cnt=3&appid="+W_API_key;
 print_console("\nStarting connection to server..."); 
 print_console("WiFi.status=" + (String)WiFi.status());
 print_console("IP=" + WiFi.localIP().toString() + ", RSSI=" + (String)WiFi.RSSI());

 if (WiFi.status() != WL_CONNECTED) {
   print_console("WiFi is not connected. Abort weather request.");
   return;
 }

 IPAddress weather_ip;
 bool dns_ok = WiFi.hostByName(W_API_server, weather_ip);
 print_console("DNS ok=" + (String)dns_ok + ", hostIP=" + weather_ip.toString());

 if (!dns_ok) {
   print_console("DNS resolution failed");
   return;
 }

 client.stop();
 // if you get a connection, report back via serial: 
 //api.openweathermap.org/data/2.5/forecast/daily?id=524901
 if (client.connect(weather_ip, 80)) { 
   print_console("connected to server");
   // Make a HTTP request: 
   client.print("GET /data/2.5/forecast?"); 
   //client.print("GET /data/2.5/forecast/daily?"); 
   client.print("q="+W_API_loc); 
   client.print("&appid="+W_API_key); 
   client.print("&mode=json"); 
   client.print("&cnt="+(String)num_days); 
   //client.print("&cnt=3"); 
   client.println("&units=metric"); 
   client.println("Host: api.openweathermap.org"); 
   client.println("Connection: close"); 
   client.println(); 
 } else { 
   print_console("unable to connect"); 
 } 

 delay(1000);
 String line = ""; 
 
 int z;
 switch(2){
 case 1:   
    while (client.connected()) { 
     line = client.readStringUntil('\n'); 
     print_console(line); 
    };
    break;
  case 2: 
    while (client.connected()) { 
       line = client.readStringUntil('\n'); 
       print_console(line); 
       print_console(" -- parsingValues"); 
       //create a json buffer where to store the json data 
       //StaticJsonBuffer<2800> jsonBuffer;   
       DynamicJsonBuffer jsonBuffer(10000);
       JsonObject& root = jsonBuffer.parseObject(line); 
       if (!root.success()) { 
         print_console(" -- parseObject() failed"); 
         return; 
       } 
       //else{Serial.println("Json - read line");}
      delay(100);
     //get the data from the json tree
     //{"cod":"200","message":0.0072,"cnt":2,"list":[{"dt":1536181200,"main":{"temp":15.58,"temp_min":15.58,"temp_max":16,"pressure":1015.67,"sea_level":1030.38,"grnd_level":1015.67,"humidity":78,"temp_kf":-0.41},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}],"clouds":{"all":0},"wind":{"speed":3.56,"deg":63.0014},"rain":{},"sys":{"pod":"n"},"dt_txt":"2018-09-05 21:00:00"},{"dt":1536192000,"main":{"temp":13.79,"temp_min":13.79,"temp_max":14.1,"pressure":1015.21,"sea_level":1029.89,"grnd_level":1015.21,"humidity":84,"temp_kf":-0.31},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}],"clouds":{"all":0},"wind":{"speed":3.22,"deg":78.0046},"rain":{},"sys":{"pod":"n"},"dt_txt":"2018-09-06 00:00:00"}],"city":{"id":2806654,"name":"Wolfsburg","coord":{"lat":52.4206,"lon":10.7862},"country":"DE","population":123064}}
     //humidity pressure temp_min temp_max clouds rain
     for(z=0;z<num_days;z++){
      temp[z]     = str_transfer(root["list"][z]["main"]["temp"]);
      temp_min[z] = str_transfer(root["list"][z]["main"]["temp_min"]);
      temp_max[z] = str_transfer(root["list"][z]["main"]["temp_max"]);
      humidity[z] = str_transfer(root["list"][z]["main"]["humidity"]);
      pressure[z] = str_transfer(root["list"][z]["main"]["pressure"]);
      clouds[z] = str_transfer(root["list"][z]["clouds"]["all"]);
      weather[z] = str_transfer(root["list"][z]["weather"][0]["description"]); 
      daytime[z] = str_transfer(root["list"][z]["dt_txt"]); 
      //
      temp    [z]= (String)temp[z].toInt();
      temp_min[z]= (String)temp_min[z].toInt();
      temp_max[z]= (String)temp_max[z].toInt();
      //
      pressure[z] = pressure[z] +"hPa";
      humidity[z] = humidity[z] +"%";
      clouds[z]   = clouds[z] +"%";
      temp[z]     = temp[z]+"°C";
      temp_min[z] = temp_min[z]+"°C";
      temp_max[z] = temp_max[z]+"°C";
      daytime[z]  = daytime[z].substring(8,10)+"-"+daytime[z].substring(5,7)+"-"+daytime[z].substring(2,4)+"        "+daytime[z].substring(11,16) ;
      get_weather_Str(z);      
     }      
   }
   break;
 }
 temp_stat[0] = (String)temp[0];
 temp_stat[1] = (String)mean_temp() + "°C";
 temp_stat[2] = (String)max_temp() + "°C";
}
/* 
String* get_weather_Str2(int z){
  String S[3];
  S[0]= daytime[z];
  S[1]= weather[z];
  S[2]= temp_min[z];
  print_console(S[0]+" , "+S[1]+" , "+S[2]+" , ");
  return S;
}*/
#include<string.h>

String S1;
/*
void disp_Weather(int z){
  u8g2.firstPage();
  do {
    writeOled(1,0,daytime[z]);
    //writeOled(1,0,daytime[z];
    writeOled(2,0,weather[z]);
    writeOled(3,0,temp_min[z]+" oC");
   } while ( u8g2.nextPage() );   
}
*/
void draw_raindrop(int x,int y,int r){
  u8g2.drawDisc(x,y,r);
  u8g2.drawTriangle(x-r,y, x,y-r-r, x+r,y);
}

void draw_rain(int x,int y,int r){
  int d = r+2;
  draw_raindrop(x-d,y-d,r);
  draw_raindrop(x,y+d,r);
  draw_raindrop(x+d,y-d,r);
}

void draw_sun(int x,int y){
  int r = 6;
  int l = 5;
  
  u8g2.drawDisc(x,y,r); 
  for(float ag=-PI;ag<PI;ag+=PI/4){
  
  u8g2.drawLine(x+((r+1)*cos(ag)), y+((r+1)*sin(ag)), x+((r+l)*cos(ag)), y+((r+l)*sin(ag)));
  }  
}

void draw_cloud(int x,int y){
  int r = 4;
  int d = 6;
  for(int z = -1;z<2;z++){
    u8g2.drawDisc(x+z*d,y+d/2,r);
    if (z<1){
      u8g2.drawDisc(x+z*d+d/2,y-d/2,r);
    } 
  }
}

void weather_printSymbol(String descript){
  int x=70;
  int y=22;
  if (descript.equals("clear sky"))
   {draw_sun(x,y);}
   else if (descript.equals("few clouds"))
   {draw_cloud(x,y);}
   else if (descript.equals("scattered clouds"))
   {draw_cloud(x,y);}
   else if (descript.equals("broken clouds"))
   {draw_cloud(x,y);}
   else if (descript.equals("overcast clouds"))
   {draw_cloud(x,y);}
   else if (descript.equals("light rain"))
   {draw_rain(x,y,2);}
   else if (descript.equals("moderate rain"))
   {draw_rain(x,y,3);}
   else 
   {print_console("missing weather type: "+descript);}
  }

void updateWeather(void){
  tm* T;
  T = get_time();
    if ((T->tm_hour%3)==0 && T->tm_min == 0)
    { 
      getWeather();
    }
}


void init_Weather(void){
  getWeather();
  }
