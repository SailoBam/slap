# Technical Solution

## 1. Boat Simulation Model
    Simple motion dynamics example - working
    Simple boat dynamics example - 
    boat dymanic maths - (almost done)
    Code boat simulator module (this must genertate heading as a function of time in response to rudder angle)
TODO: 


    
## 2. PID Controller
    PID Module - working
    Tester which runs it with the rocket simulation - working
    Run PID module against boat dynamics
TODO:
    Add gain setting linked to the accelerometer
   
## 3. Web App
    Basic web server with PUSH, PUT, POST functions -Working
    Basic HTML page with javascript button - Working
    Can serve a file - Working
    Design iteration 0 of web page - Includes current direction, set direction, up and down button - Working
    Basic web app with images and rotation svg according to angle - working
    Design iteration 1 of web app - This will include all bells and whistles including start/stop, record buttons, time

TODO:
    Add error message bar
    Add sensors config page
    Add sensors readout page
    Increase compass size
    add gps fix indicator
    Choose sim mode
    add map view button in trips page
    move common javascript to common file

## 4. NMEA Reader
    NMEA Writer (Angle) - working
    NMEA Writer (Position) - working
    NMEA Test (Angle, Position) - working

## 5. Database
    basic database function library - working
    basic database design drawing - complete
    Create database initialisation script
TODO:

    Finalise database design 
    fix sensors table
    add required functions
    add sensor plugin code#
    logger needs to write all sensor values to the log with link to sensors table
    Finish database service layer (slapStore)

## 6. Cloud Interface (For Database)
    Decide on which cloud service to use e.g strava etc
    Create rest service
    Create Tests
    Develop upload code

TODO:
    Add sensor values to the waypoints as additional metadata

## 7. Application Framework
    Created basic threading tests inlcuding using a simple web server one thread (without PID) - Working
    Create worker threads for PID and seperated web server
    Intergrate the PID boat simulator into a multi-threaded application
    Intergrate PID output to drive servo motor
TODO:


## X. Motor Driver
    Investigate basics of servo motor control
    Buy suitable motor and controller
    Write motor driver Code
TODO:

   

    

# Write Up topics

## 8. User Requirements
Generate set of interview questions to discover user requirements

(Write Up) TODO:
    Develop a set of user stories
    Develop use cases from user stories

## 9. Write Up
TODO:
    Write up Pid tuning
    Investigate the best report structure (May be provided)
    Read the AQA guidance on project write up
    Read provided examples
    Identify key things to feature in write up
    Restructure project files
    
### Technical Solution
TODO:
    Intro including all techniques used against marking criteria
    review all code, clean up add comments + exception handling

### Evaluation
TODO:
    Develop form for feedback
    send to nick
    deploy app and make available 
    describe conditional imports to run on pi and dev on windows

### Testing
TODO:
    add more unittests for more complex areas
    add UI tests
    add a test which shows motor jitter
    PID Algorithm plot

### Design
TODO:
    Collect relevant citations to:
        Flask stuff
        service interface pattern
        threading
        hardware control
        inheritance
        (think of any more)

### Analysis
TODO:
    Update current document using mark scheme as reference

### Maths
TODO:
    Update maths for full write up with differential equation
    Choppy Boat RMS


## 10. Planning
TODO:

    Read submission deadlines
    Write simple plan to complete work

