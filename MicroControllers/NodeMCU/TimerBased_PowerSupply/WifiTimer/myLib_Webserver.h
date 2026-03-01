// Load Wi-Fi library
//#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

// Replace with your network credentials
#include "MyWifiSettings.h"
//const char* ssid     = "REPLACE_WITH_YOUR_SSID";
//const char* password = "REPLACE_WITH_YOUR_PASSWORD";

// Set web server port number to 80
ESP8266WebServer server ( 80 );

// Variable to store the HTTP request
String header;


// Auxiliar variables to store the current output state
boolean State_Button1 = false;
boolean State_Button2 = false;
boolean Times_a_day = 1;

int act_ID = 0;
int html_scale = 2;//1.3

String html_print(String S){
  return (S+"\n");
  }

String create_NumberInput(String Tag,String Label, int Val,int Max){
  String page="";
  page += html_print("         <div class='inline'>");
  page += html_print("            <label for='"+Tag+"'>"+Label+":</label>");
  page += html_print("            <form action='http://"+IP+"/' method='POST'>");
  page += html_print("               <input type='number' name='"+Tag+"' id='"+Tag+"' placeholder='1' value='"+(String)Val+"' step='1' min='0' max='"+(String)Max+"' <='' input=''>");
  page += html_print("            </form>");
  page += html_print("         </div>");
/*
  cmd += "<div style='float:left;margin-right:40px;'>";
  cmd +=   "<label  for='"+Tag+"'>"+Label+":</label>";
  cmd +=   "<form action='/' method='POST'><input type='number' name='"+Tag+"' id='"+Tag+"' placeholder='1' value='"+Val+"' step='1' min='0' max='"+(String)Max+"' </input></form>";
  //cmd +=   "<input type='number' name='"+Tag+"' id='"+Tag+"' placeholder='1' value='"+Val+"' step='1' min='0' max='"+(String)Max+"' </input>";
  cmd += "</div>";
*/
  return page;
}

String create_NumDropDown(String Tag,String Label, int Val,int Max){
  String page="";
  page += html_print("         <div class='inline'>");
  page += html_print("            <label for='num_ID'>"+Label+":</label>");
  page += html_print("            <form action='http://"+IP+"/' method='POST'>");
  page += html_print("            <!--<input type='number' name='"+Tag+"' id='"+Tag+"' placeholder='1' value='"+(String)Val+"' step='1' min='0' max='"+(String)Max+"' <='' input=''>-->");
  page += html_print("            <select name='"+Tag+"'>");
  for (int z=0;z<Max_Entries;z++){
    page += html_print("              <option value='"+(String)z+"'>"+(String)z+"</option>");
  }
  page += html_print("            </select>");
  page += html_print("            </form>");
  page += html_print("         </div>");
  return page;
  }    
String create_Button(String Tag,String Text,String Style,int Val){
  String page="";
  page += html_print("         <div class='inline'>");
  page += html_print("            <label for='"+Tag+"'><font color='#FFFFFF'>_</font>   </label>");
  page += html_print("            <form action='http://"+IP+"/' method='POST'>");
  page += html_print("               <button class='button fat "+Style+"' type='button submit' name='"+Tag+"' id='"+Tag+"' value='"+(String)Val+"'>"+Text+"</button>");
  page += html_print("            </form>");
  page += html_print("         </div>");
  return page;
  }
 
String getPage(){
  String page = "";
  page += html_print("<html>");
  page += html_print("  <head>");
  page += html_print("      <meta http-equiv='Content-Type' content='text/html; charset=windows-1252'>");
  page += html_print("      <meta http-equiv='refresh' content='60' name='viewport'>");
  page += html_print("      <script src='./Zeitschaltuhr_files/jquery.min.js.Download'></script>");
  page += html_print("      <script src='./Zeitschaltuhr_files/bootstrap.min.js.Download'></script>");
  page += html_print("      <title>Timer Switch</title>");
  page += html_print("      <style>");
  page += html_print("      html{width:400px; height:100%;  }");
  page += html_print("      body{width:400px; height:100%; align:center; transform: scale("+(String)html_scale+"); transform-origin: 0 0};");
  page += html_print("      .button {border: none; color: black; padding: 5px; text-align: center; text-decoration: none; display: inline-block;");
  page += html_print("          font-size: 12px; margin: 1px 1px; cursor: pointer; border-radius:5px; }  ");
  page += html_print("      .on  {background-color: #56DB05;} /* Green*/");
  page += html_print("      .off {background-color: #FA2D01;} /* Red*/");
  page += html_print("      .inline {float:left;margin-left:10px;margin-right:10px;}");
  page += html_print("      .fat {font-weight:bold}");
  page += html_print("      .text1 {background-color:#4444FF; color:white;font-size: 16px;margin: 2px 2px;font-weight:bold;border-radius:5px;}");
  page += html_print("      .text9 {background-color:white  ;  color:black;font-size: 30px;font-weight:bold;border-radius:5px;}");
  page += html_print("      .text2 {color:#4444FF;}");
  page += html_print("      .text3 {color:#A4A4A4;font-size: 12px;} /* grey comment   margin-bottom:1px; padding: 5px;*/");
  page += html_print("      .table1{border-collapse:collapse; text-align:center;padding: 2px;border: 1px solid black;width:100%;}");
  page += html_print("      .table2{border-collapse:collapse; text-align:center;padding: 2px;border: 0;width:100%;}");
  page += html_print("      .table3{border-collapse:collapse; text-align:left;padding: 25px 2px 2px 25px;border: 0;width:100%;}");
  page += html_print("      .table1 th{font-weight:bold;background-color: #ddd;}");
  page += html_print("      </style>");
  page += html_print("   </head>");
  //page += html_print("   <body style='height:100px; width:500px; transform: scale(1.3);transform-origin: 0 0;'>");
  page += html_print("   <body>");
  page += html_print("");
  page += html_print("   <div style='margin-left:10px;'>");
  page += html_print("   <!-- Title Author server time-->");
  page += html_print("      <table class = 'table2'  cellpadding ='5px'>");
  page += html_print("      <!-- <tr><td margin-right='40'>-->");
  page += html_print("         <tr><td><span class='text9'>Timer Switch</span>");
  page += html_print("         </td></tr><tr><td><!-- &emsp;&emsp;-->");
  page += html_print("         <span class='text3'>R. Baur  &lt;10.08.2018&gt;</span> </td></tr>");
  page += html_print("         <tr><td><span class='text1'>&ensp; Time:&ensp; </span> &emsp; <span class='text2'> "+aktZeit+" </span></td></tr>");
  page += html_print("      </table>");
  page += html_print("      <br>");
  page += html_print("");
  page += html_print("      <!-- Time Table: Schedulinng -->");
  page += html_print("      <table class = 'table1' border='1'>");
  page += html_print("         <thead>");
  page += html_print("            <tr class='fat'>");
  page += html_print("            <th>ID</th><th>Hour</th><th>Minute</th><th>Duration</th></tr>");
  page += html_print("         </thead>");
  page += html_print("         <tbody>");
   for (int z=0;z<Max_Entries;z++){
      page +=html_print("            <tr><td>"+(String)z+"</td><td>"+(String)cfg.t_start_hh[z]+"</td><td>"+(String)cfg.t_start_mm[z]+"</td><td>"+(String)cfg.t_dur_on[z]+"</td></tr>"); 
    }
  page += html_print("         </tbody>");
  page += html_print("      </table> <br>");
  page += html_print("      <table class='table1'><tr><td>");
  page += html_print("         <!-- numerical inputs-->");
  //page +=       create_NumDropDown("num_ID","ID",act_ID,Max_Entries-1);
  page +=       create_NumberInput("num_ID","ID",act_ID,Max_Entries-1);
  page +=       create_NumberInput("num_hh","hh",cfg.t_start_hh[act_ID],24);
  page +=       create_NumberInput("num_mm","mm",cfg.t_start_mm[act_ID],60);
  page +=       create_NumberInput("num_dur","dur",cfg.t_dur_on[act_ID],10);
  page +=       create_NumberInput("num_t_man","t_manual",cfg.t_manual,10);
  page += html_print("<br>");
  page += html_print("         <!-- submit button that updates EEPROM -->");
  page +=       create_Button("but_update","update","",1);
  page += html_print("     </td></tr>");
  page += html_print("     </table>");
  page += html_print("");
  page += html_print("      <br style='clear:both;'>");
  page += html_print("      <br>");
  page += html_print("      <!-- On/Off buttons for Switch -->");
  page += html_print("      <table text-align='center'><tr><td>");
  page += html_print("         <div class='inline'>");
  if (Switch_is_on())
  {page += html_print("               <label>Switch is</label> <b>ON</b> ");}
  else
  {page += html_print("               <label>Switch is</label> <b>OFF</b> ");}
  //page += html_print("               <label>Schalter ist</label> <b>AUS</b> &ensp;soilMoisturePercent: "+(String)soilMoisturePercent+"%");
  page += html_print("         </div>");
  page += html_print("         </td><td>");
  page +=       create_Button("B1","ON","on",1);
  page += html_print("         </td></tr><tr><td>");
  if (waterLevelOk)
    {page += html_print("               <label>Water level: </label> <b>Okay</b>");}
  else
    {page += html_print("               <label>Water level: </label> <b>empty !!!</b>");}
  page += html_print("         </td><td>");
  page +=       create_Button("B1","OFF","off",0);
  
  page += html_print("         </td></tr>");  
  page += html_print("      </table>");
  page += html_print("      <br style='clear:both;'>");
  page += html_print("");
  page += html_print("      <!-- Log-Table -->");
  page += html_print("      <table class = 'table3' border='1'>");
  page += html_print("         <thead>");
  page += html_print("            <tr class='fat'>");
  page += html_print("            <th>Log file</th></tr>");
  page += html_print("         </thead>");
  page += html_print("         <tbody>");
   for (int z=0;z<Log_length;z++){
      int id = ((Log_length+Log_id-1-z)%Log_length);
      page +=html_print("            <tr><td> &emsp;&emsp;"+Log[id]+" </td></tr>"); 
    }
  page += html_print("         </tbody>");
  page += html_print("      </table> <br>");
  page += html_print("   </div>");
  page +=       create_NumberInput("num_scale","Scale",html_scale,2);
  page += html_print("   </body>");
  page += html_print("</html>");
  return page;

}


/**
 * @brief Handle on/off actions from the web UI for the primary switch.
 *
 * @param is_on true to switch on, false to switch off.
 */
void handleB1(boolean is_on) {
  print_console("Button 1 is pressed"); 
  if (is_on){Switch_on();}
  else      {Switch_off();}
  Log_write("Manual");
  server.send ( 200, "text/html", getPage() );
}

/**
 * @brief Read an integer parameter from the server request.
 *
 * Returns 0 if the argument is missing or empty.
 */
int server_getInt(String Arg){
  int val;
  String arg = server.arg(Arg);
  if (arg.length() != 0) val = arg.toInt();
  print_console((String)val);
  return val;
}

void handleRoot(){ 
  if ( server.hasArg("B1") ) {
    if (server_getInt("B1")==1)
      {handleB1(true);}
    else
      {handleB1(false);}
  } else if(server.hasArg("num_ID")){
    print_console(server.arg("num_ID"));
    act_ID = server_getInt("num_ID");
  } else if(server.hasArg("num_mm")){
    print_console(server.arg("num_mm"));
    cfg.t_start_mm[act_ID] = server_getInt("num_mm");
  } else if(server.hasArg("num_hh")){
    print_console(server.arg("num_hh"));
    cfg.t_start_hh[act_ID] = server_getInt("num_hh");
  } else if(server.hasArg("num_dur")){
    print_console(server.arg("num_dur"));
    cfg.t_dur_on[act_ID] = server_getInt("num_dur");
  } else if(server.hasArg("num_t_man")){
    print_console(server.arg("num_t_man"));
    cfg.t_manual = server_getInt("num_t_man"); 
    } else if(server.hasArg("num_scale")){
    print_console(server.arg("num_scale"));
    html_scale = server_getInt("num_scale");
  } else if(server.hasArg("but_update")){
    print_console("update scheduling table (EEPROM)");
    update_start_min();
    saveConfig();
    /*
    cfg.t_start_hh[ID] = server.arg("num_hh");
    cfg.t_start_mm[ID] = (int)server.arg("num_mm");
    cfg.t_dur_on[ID] = (int)server.arg("num_dur");
    cfg.t_start_mm[ID] = (int)server.arg("num_hh")*60+(int)server.arg("num_mm");
    */
  }else {
    //server.send ( 200, "text/html", getPage() );
    print_console("Server --> unknown arg");
  }  
  server.send ( 200, "text/html", getPage() );
}

void init_WiFi(){
  Serial.begin(115200); 
  // Connect to Wi-Fi network with SSID and password
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  // Print local IP address and start web server
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  server.on ( "/", handleRoot );
  
  server.begin();
  }
    
void exec_WebServer(){
    server.handleClient();
}
    
