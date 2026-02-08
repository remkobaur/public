
/**
 * @brief Turn both relays off and turn the status LED off.
 *
 * This sets the relay pins to the inactive state (HIGH) and clears
 * the LED output.
 */
void Switch_off(){
  digitalWrite(RELAY1_PIN, HIGH);
  digitalWrite(RELAY2_PIN, HIGH);
  digitalWrite(LED, LOW);
}

/**
 * @brief Turn both relays on and set the status LED on.
 *
 * This sets the relay pins to the active state (LOW) and sets
 * the LED output.
 */
void Switch_on(){
  digitalWrite(RELAY1_PIN, LOW);
  digitalWrite(RELAY2_PIN, LOW);
  digitalWrite(LED, HIGH);
}

/**
 * @brief Query whether the switch (relay) is currently on.
 *
 * @return true if relay1 is active (LOW), false otherwise.
 */
boolean Switch_is_on(){
  if (digitalRead(RELAY1_PIN)==LOW)
  {return true;}
  else
  {return false;}
}

/**
 * @brief Last measured soil moisture percentage.
 *
 * This value is updated by `is_soil_dry()`.
 */
int soilMoisturePercent;

/**
 * @brief Read the analog soil moisture sensor and update the cached value.
 *
 * Reads analog pin A0, computes a percentage and stores it in
 * `soilMoisturePercent`. Note: the function does not return a boolean
 * despite its historical name; it merely updates the cached value.
 */
void is_soil_dry(){
  int val = analogRead(A0);
  soilMoisturePercent = (((1024-val)*100)/1024)*100/60;
  print_debug("soilMoisturePercent: "+(String)soilMoisturePercent+"%");
}


/**
 * @brief Cached water level status.
 *
 * true means water level is OK; false means low/empty.
 */
boolean waterLevelOk;

/**
 * @brief Check the water level switch and perform safety actions.
 *
 * Reads the `LEVEL_SWITCH_PIN` and updates `waterLevelOk`. If the
 * level is low and the switch is currently on, this function will turn
 * the switch off and write a log entry. Also toggles the LED when
 * level is low to draw attention.
 *
 * @return the boolean water level state (true = OK, false = low)
 */
boolean isLevelOk(){
  waterLevelOk = (digitalRead(LEVEL_SWITCH_PIN)==LOW);
  print_debug("Level: "+(String)waterLevelOk);
  if ((waterLevelOk==false) && Switch_is_on())
  {Switch_off();Log_write("noWater");}
  if (waterLevelOk==false)
  {digitalWrite(LED,! digitalRead(LED));/*toggle LED*/}
  return waterLevelOk;
}


/**
 * @brief Debounced read of the user button.
 *
 * Returns true when the button is pressed (active LOW). This function
 * blocks while the button remains pressed to avoid multiple triggers
 * and includes a small post-release delay for debouncing.
 *
 * @return true if button was pressed, false otherwise.
 */
boolean isButtonPressed(){
  boolean IN;
  if (LOW==digitalRead(BUTTON_PIN))
  {IN = true;
  print_debug("Button: "+(String)IN);
  while(LOW == digitalRead(BUTTON_PIN)){}
  delay(100);
  }
  else
  {IN = false;}
  
  return IN;
}

/**
 * @brief Initialize IO pins and perform an initial sensor read.
 *
 * Configures relay outputs, LED and input pins, then reads the
 * water-level and soil sensors once. Finally sets outputs to the
 * default (off) state.
 */
void init_IOs(){ // Initialize the output variables as outputs
  //pinMode(LED, OUTPUT);
  pinMode(RELAY1_PIN,OUTPUT);
  pinMode(RELAY2_PIN,OUTPUT);
  pinMode(LED,OUTPUT);
  pinMode(LEVEL_SWITCH_PIN,INPUT);
  pinMode(BUTTON_PIN,INPUT);

  isLevelOk();

  is_soil_dry();
  // Set outputs to LOW
  Switch_off();
  }
