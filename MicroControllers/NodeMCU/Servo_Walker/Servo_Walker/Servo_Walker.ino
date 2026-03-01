//ref: https://www.esp8266learning.com/pca9685-led-controller-and-esp8266-example.php
#include <Wire.h>
#include "Adafruit_PWMServoDriver.h"

#define PWM_LEG_FRONT_LEFT  0
#define PWM_LEG_FRONT_RIGHT 3
#define PWM_LEG_REAR_LEFT   4
#define PWM_LEG_REAR_RIGHT  7

#define IO_LED 12
#define IO_SW  14
 
#define PWM_VALUE_MIN  800
#define PWM_VALUE_MAX 4000

// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

int _mode = 0;
int led_counter=0;
bool led_state = false;
float _angle=0;
float _speed = 3;

void setup() {
  Serial.begin(9600);
  pinMode(IO_SW, INPUT);
  pinMode(IO_LED, OUTPUT);
  Serial.println("Walking Monster");
  pwm.begin();
  pwm.setPWMFreq(400);  // This is the maximum PWM frequency
    
  // save I2C bitrate
  //uint8_t twbrbackup = TWBR;
  // must be changed after calling Wire.begin() (inside pwm.begin())
  //TWBR = 12; // upgrade to 400KHz!
}
void wave()
{
    // Drive each PWM in a 'wave'
  for (uint16_t i=0; i<4096; i += 8) 
  {
    for (uint8_t pwmnum=0; pwmnum < 16; pwmnum++) 
    {
      pwm.setPWM(pwmnum, 0, (i + (4096/16)*pwmnum) % 4096 );
    }
  }
}

void set_leg_angle(uint8_t pin_num,float angle, bool inverted)
{
  if (inverted)
  {
    angle = -1.0*angle;
  }
  uint16_t pwm_val= (uint16_t)(((int)(angle+90) * (PWM_VALUE_MAX-PWM_VALUE_MIN) / 180) +  PWM_VALUE_MIN);
  pwm.setPWM(pin_num, 0, pwm_val );
}

void stand()
{
  int angle = 0;
  set_leg_angle(PWM_LEG_FRONT_LEFT ,angle,true);
  set_leg_angle(PWM_LEG_REAR_LEFT  ,angle,true);
  set_leg_angle(PWM_LEG_FRONT_RIGHT,angle,false);  
  set_leg_angle(PWM_LEG_REAR_RIGHT ,angle,false);
}

void walk()
{
  for (float angle=-30.0; angle<=30.0; angle += 30.0) 
  {
    set_leg_angle(PWM_LEG_FRONT_LEFT ,angle,false);
    set_leg_angle(PWM_LEG_FRONT_RIGHT,angle,true);
    set_leg_angle(PWM_LEG_REAR_LEFT  ,angle,false);
    set_leg_angle(PWM_LEG_REAR_RIGHT ,angle,true);
    Serial.print("angle: ");
    Serial.println(angle);
    delay(300);
  }  
}

void set_leg_angle2(uint8_t pin_num,float angle, bool inverted,int offset)
{
  if (angle>360)
  {
    angle-= round(angle/360.0)*360;
  }
  if (inverted)
  {
    angle = -1.0*angle;
  }  
  int servo_ag = (int)(sin(angle*PI/180.0) * 30.0) +90+offset;
  //Serial.print("angle: ");
  //Serial.println(servo_ag);
  uint16_t pwm_val= (uint16_t)(( servo_ag * (PWM_VALUE_MAX-PWM_VALUE_MIN) / 180) +  PWM_VALUE_MIN);
  pwm.setPWM(pin_num, 0, pwm_val );
}
void walk2()
{
  _angle = _angle + _speed*1.0;
  if (_angle>360)
  {
    _angle-= round(_angle/360.0)*360;
  }
  set_leg_angle2(PWM_LEG_FRONT_LEFT ,_angle+00.0,false,20);
  set_leg_angle2(PWM_LEG_FRONT_RIGHT,_angle+090.0,true,-20);
  set_leg_angle2(PWM_LEG_REAR_LEFT  ,_angle+180.0,false,-20);
  set_leg_angle2(PWM_LEG_REAR_RIGHT ,_angle+270.0,true,20);
//  Serial.print("angle: ");
//  Serial.println(_angle);
  delay(10);
}

void led_blink()
{
  if (led_counter % 300 == 0)
  {
    led_state = ! led_state;
    led_counter = 0;
  }
  digitalWrite(IO_LED,led_state);
  led_counter++;
}


void loop() {
  //wave();
  if (digitalRead(IO_SW))
  {
    _mode = (_mode+1)%2;
    delay(500);
    led_blink();
    switch(_mode)
    {
      case 0: // stand    
        Serial.println("Change Mode --> STAND"); 
        break;
      case 1: // walk
        Serial.println("Change Mode --> WALK");  
        digitalWrite(IO_LED,true);      
        break;
      default:
        break;
      }
  }
  switch(_mode)
  {
    case 0: // stand    
      led_blink();
      stand();
      break;
    case 1: // walk
      //walk();
      walk2();
      break;
    default:
      break;
  }  
  
  
}
