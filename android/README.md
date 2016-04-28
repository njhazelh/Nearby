README - Nearby Android application

Built targeting API 15 with compatibility up through Marshmallow. Considered stable for now.
Extra dependencies (included in Gradle build): OkHttp, GSON

Features:
- Enables Bluetooth discoverability and scans surrounding area
- Reports other signed-up users who were recently nearby
- Allows account creation and modification
- Allows registration of device MAC address and reporting of all nearby MAC addresses

Things to watch for in the future:
- 6.0+ requires location access to scan BT
- Marshmallow removed official support for getting hardware MAC address; a hack
  was introduced to work around this, but that loophole may be closed in Android N
  
To start reading the code, start in MainActivity and BTDeviceFragment, then work 
your way through the settings activities/API requests (w/associated async tasks).
