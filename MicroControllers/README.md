# Micro Controller Projects

## NodeMCU

- [Timer based Power Supply with Web Server Configuration](NodeMCU/TimerBased_PowerSupply/Documentation.md)
- [Servo-based walker build with LEGO Technic](NodeMCU/Servo_Walker/Documentation.md)

## Secrets setup (Wi-Fi)

To avoid committing Wi-Fi credentials to git, keep them in a local file:

1. Create secrete config file `NodeMCU/TimerBased_PowerSupply/WifiTimer/MyWifiSettings.secret.h`
2. Set your credentials in that local file:
	- `#define WIFI_SSID "..."`
	- `#define WIFI_PASSWORD "..."`
3. Commit as usual. `MyWifiSettings.secret.h` is ignored via `.gitignore`.

