#include <time.h>
int timezone = 1;
//boolean summertime = false;
int dst = 0;
int t_man = 0;

String  aktZeit  = "";

void time_synch(int timezone){
    //time setup
  configTime(timezone * 3600, 0, "pool.ntp.org", "time.nist.gov");
  print_console("\nWaiting for time");
  while (!time(nullptr)) {
    print_console(".");
    delay(1000);
  }
  print_console("");
}

void print_time(){
  //get time
  time_t now = time(nullptr);
  aktZeit = ctime(&now);
  Serial.println(aktZeit);
   }


tm* get_time(){
  //SRC: http://www.cplusplus.com/reference/ctime/gmtime/
  time_t rawtime;
  struct tm * T_struct;
  time ( &rawtime );
  T_struct = gmtime ( &rawtime );

  //time string
  aktZeit = ctime(&rawtime);
  
  return T_struct;
}

int get_time_mm(){
  tm* t_struct = get_time();
  int Minutes = t_struct->tm_hour*60 + t_struct->tm_min;  
  //"Time: "+(String)t_struct->tm_hour+":"+(String)t_struct->tm_min);
  
  return Minutes;
}

String leading_Zero(int I){
  if (I<10)
  {return "0"+(String)I;}
  else
  {return (String)I;}
}
String get_Str_Date(){
  tm* T= get_time();
  return leading_Zero(T->tm_mday)+"."+leading_Zero(T->tm_mon+1) +"."+leading_Zero(T->tm_year+1900);
}

String get_Str_Time(){
  tm* T= get_time();
  return leading_Zero(T->tm_hour)+":"+leading_Zero(T->tm_min)+":"+leading_Zero(T->tm_sec);
}

void init_Timer(){
  Serial.println(summertime);
  if (summertime == true)
  {time_synch(timezone+1);}
  else
  {time_synch(timezone);}
  print_time();
}
