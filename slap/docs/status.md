# Technical Solution

## 1. Boat Simulation Model
    Simple motion dynamics example - working
    Simple boat dynamics example - 
TODO: 

    Create boat dynamic maths
    Code boat simulator module (this must genertate heading as a function of time in response to rudder angle)
    
## 2. PID Controller
    PID Module - working
    Tester which runs it with the rocket simulation - working
TODO:

    Run PID module against boat dynamics
## 3. Web App
    Basic web server with PUSH, PUT, POST functions - Not Working
    Basic HTML page with javascript button - Working
    Can serve a file - Working
TODO:

    Fix basic web server (experiment 2) (404 Error with gettime and changeangle pages)
    Design iteration 2 of web page - This will include current direction, set direction, up and down button, start / stop button, record button
    Design iteration 3 of web app - This will include all bells and whistles

## 4. NMEA Reader
    NMEA Writer (Angle) - working
    NMEA Writer (Position) - working
    NMEA Test (Angle, Position) - working

## 5. Database
TODO:

    Finalise database design 
    Create database initialisation script
    Finish database service layer (slapStore)

## 6. Cloud Interface (For Database)
TODO:

    Decide on which cloud service to use e.g strava etc
    Create rest service
    Create Tests
    Develop upload code

## 7. Application Framework
    Created basic threading tests inlcuding using a simple web server one thread (without PID) - Working
TODO:

    Create worker threads for PID and seperated web server (fix webserver EXP 2 first : 3 TODO)
    Intergrate the PID boat simulator into a multi-threaded application
    Intergrate PID output to drive servo motor

## X. Motor Driver
TODO:

    Investigate basics of servo motor control
    Buy suitable motor and controller
    Build basic 3D printed mount
    Write motor driver Code
    

# Write Up topics

## 8. User Requirements
(Write Up) TODO:

    Generate set of interview questions to discover user requirements
    Develop a set of user stories
    Develop use cases from user stories

## 9. Write Up
TODO:

    Investigate the best report structure (May be provided)
    Read the AQA guidance on project write up
    Read provided examples
    Identify key things to feature in write up
    Restructure project files
    

## 10. Planning
TODO:

    Read submission deadlines
    Write simple plan to complete work

