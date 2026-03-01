
boolean Button_pressed(int ID){
  boolean State = false;
  
  switch(ID){
    case 1: State = digitalRead(But_1)==LOW;break;
    case 2: State = digitalRead(But_2)==LOW;break;
    case 3: State = digitalRead(But_3)==LOW;break;
  }    
  
  if (State)
  {print_console("Button "+(String)ID+" pressed");return true;}
  else
  {return false;}
}

void init_IOs(){ // Initialize the output variables as outputs
  pinMode(But_1,INPUT);
  pinMode(But_2,INPUT);
  pinMode(But_3,INPUT);
  }
