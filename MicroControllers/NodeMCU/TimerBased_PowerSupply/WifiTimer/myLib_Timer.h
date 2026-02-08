#include <time.h>
int timezone = 2;
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

/**
 * @brief Print the current time to Serial and update `aktZeit`.
 */
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
  //Serial.println("Time: "+(String)t_struct->tm_hour+":"+(String)t_struct->tm_min);
  
  return Minutes;
}

//boolean check_time(int* t_start_min,int* t_dur_on){
/**
 * @brief Check whether current time falls within any configured timers.
 *
 * Iterates through `cfg` scheduling entries and returns true if the
 * current minute-of-day is within any scheduled interval.
 *
 * @return true when any timer is active, false otherwise.
 */
boolean check_time(){
  int T = get_time_mm();
  //Serial.println(cfg.t_start_min[0]-T);
  for(int z =0;z<Max_Entries;z++){
    if (T>= cfg.t_start_min[z] && T<= (cfg.t_start_min[z] + cfg.t_dur_on[z]))
	 {return true;}
  }
  return false;
}

int Timer_t_end;
boolean Timer_isRunning = false;

/**
 * @brief Start or evaluate the software timer.
 *
 * When `b_start` is true the timer will be started using either the
 * provided `t_manual` minutes or the current schedule. When false the
 * function evaluates timer state and returns status codes.
 *
 * @param t_manual manual minutes to run when starting (0 = use schedule)
 * @param b_start  true to start the timer, false to evaluate
 * @return 0 = idle, 1 = started/active, 2 = finished
 */
int my_Timer(int t_manual,boolean b_start)  {
  int T = get_time_mm();
  // get end time
  if (b_start){
    if (t_manual != 0)
    {
      Timer_t_end = t_manual + T;      
    }
    else
    {      
      for(int z =0;z<Max_Entries;z++){
        if (T>= cfg.t_start_min[z] && T<= (cfg.t_start_min[z] + cfg.t_dur_on[z]))
          { Timer_t_end = cfg.t_start_min[z] +cfg.t_dur_on[z]; 
            break;
          }    
      }      
    }
    Timer_isRunning = true;
    return 1;
  }

  // control timer
  if ( Timer_isRunning && (T<Timer_t_end) )
  {print_console("Active Timer: "+(String)(Timer_t_end-T)+" min remains");  }
  else if(Timer_isRunning && (T>=Timer_t_end))
  { Timer_isRunning =false;
    return 2; 
  }
  else 
  {return 0;}
}  

void Timer_stop(){
  Timer_isRunning =false;
}

void set_start_min(int id,int hh,int mm){
if (id<0 || id>=3){return;}
  cfg.t_start_min[id] = hh*60+mm;
  cfg.t_start_hh[id]=hh;
  cfg.t_start_mm[id]=mm;
  }

void update_start_min(void){
  for(int id =0;id<Max_Entries;id++){
    cfg.t_start_min[id] = cfg.t_start_hh[id]*60+cfg.t_start_mm[id];
  }
}

/*  Log-File */
#define Log_length 5
String Log[Log_length];
int Log_id = 0;

void Log_write(String Status){
  get_time();
  if (digitalRead(RELAY1_PIN)==HIGH)
  {Log[Log_id] = aktZeit + ": OFF - " +Status;}
  else
  {Log[Log_id] = aktZeit + ": ON&ensp;   - " +Status;}
  Log_id = (Log_id+1)%Log_length;
  }
