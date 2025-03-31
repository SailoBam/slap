# Design


## Overall System Design




| Inputs | Processes | Storage | Outputs |
| --- | --- | --- | --- |
| Destination<br><br>Manual angle adjustment<br><br>Sensor inputs (Wind, Tide...) | Angle calculation<br><br>Calculate adjustment needed | Log files of each passage stored on a cloud database | Rudder movement<br><br>Visual updates on screen (angle, speed, etc) |

## Modular Design

The system will be split into multiple smaller modules, a webserver running micro-python on an Arduino (or similar) will host a file system to store the user interface.

The client (Phone) will run the interface and send requests the webserver upon button press. The client will also be sending a �rest call� to update the GUI constantly over Wi-Fi.

The user interface will be written in JavaScript with React to run a HTML web application.

A separate PID module will be running custom code which preforms the main feedback loop, the webserver will communicate to this module to execute manual changes by sending a set point position.

\*React- JavaScript framework to write apps


## Form/Navigation Design



### Data Dictionary

Primary Sensor Data

GPS will be used to get positional data about the boat and its location relative to the desired destination using its longitude and latitude. GPS will also be used to determine approximate speed and direction using the standard NMEA format. Speed and direction will be stored as a decimal value

A Motion Sensor will be used to report information about the boat's movement and by extension the seas condition. It will possess a decimal value for each axis.

Log files will include many different data types, such as time (integer) and distance (integer) and error value which will be stored as a decimal value (float)

Data Collection

Current Time will be stored for each reading of each sensor.

The destination will be retrieved from the user and stored as a longitude and latitude coordinate (integers).

Actual course will be stored as a change in longitude and latitude (integers).

Desired course will be stored as a change in longitude and latitude (integers) from start position to desired destination.

Actuator value will be stored as an integer value.

| Data | Format | Description |
| --- | --- | --- |
| Coordinate | Array, Integer | 2 Integer values for longitude and latitude |
| Speed | Float | Value of speed in knots |
| Wind | Float | Value of wind speed in knots |
| Time | Time | Time at read |
| Motion Sensor | Float | Value of motion sensor as a decimal |
| Actuator value | Integer | The value sent to the motor for steering after processing |
| Distance | Float | Value of distance in nautical miles |

Database

| Field Name | Data Type | Description |
| --- | --- | --- |
| **boatID** | int | ID of boat |
| boatName | varchar(50) | Name of boat |
| boatModel | varchar(50) | Model of boat |
| proportionalGain | float | PID gain |
| integralGain | float | PID gain |
| differentialGain | float | PID gain |

| Field Name | Data Type | Description |
| --- | --- | --- |
| **tripID** | int | ID number of trip |
| boatID | int | ID of associated boat |
| sensorID | int | ID of associated sensor |
| dateStarted | date | Date started trip |
| dateFinished | date | Date completed trip |
| timeStarted | time | The time that the trip began |
| timeFinished | time | The time the trip finished |
| timeTaken | time | Time taken for trip |
| distanceTravelled | float | Distance travelled in trip |

| Field Name | Data Type | Description |
| --- | --- | --- |
| **sensorId** | int | ID of sensor |
| boatId | int | ID of associated boat |
| sensorName | Varchar(50) | Name of sensor |
| dataType | string | Type of data sensor reads |

| Field Name | Data Type | Description |
| --- | --- | --- |
| **sensorId** | int | ID of sensor |
| tripId | int | ID of associated trip |
| data | float | Data the sensor is reading |
| timeStamp | time | Time of reading |

## Data Validation

Input data from the user will not need to be validated as the only inputs are buttons of which have a predetermined function.

## Database Design

## Algorithms

## Interface Design

Central value gives the angle of the heading in degrees between 0 and 359. Speed is given in knots at the top left with the time in the top right. Central at the bottom is a set button which begins the program which will try to keep the boat on course, this will also start the elapsed running time and will begin to count. The stop button will cancel the program and will reset the timer. Manual adjustments can be made with the buttons at the bottom, allowing for both fine and broad adjustments. The map button gives access to the map interface.
## Security

The system will not be able to be accessed by other devices as it is local to the boat, this means that a security system will not be necessary

## Testing Strategy