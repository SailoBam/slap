// Functions for reacting to button presses


function changeValue(c) {
    const url = '/api/addDirection'; 
    console.log("Inside changeValue", c);

    fetch(url, {
        method: "PUT",
        headers: {
            "Content-Type": "text/plain"  // Changed from text/html
        }, 
        body: c.toString()  // Send the raw value instead of JSON.stringify
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Received response:", data);
            document.getElementById("angle").textContent = data.angle;
            updateTarget(data.angle)
        })
        .catch(error => {
            console.error("Error:", error);
            document.getElementById("angle").textContent = 
                "Error: " + error.message;
        });
}

function setValue(c) {
    const url = '/api/setDirection'; 
    console.log("Inside changeValue", c);

    fetch(url, {
        method: "PUT",
        headers: {
            "Content-Type": "text/plain"  // Changed from text/html
        },
        body: c.toString()  // Send the raw value instead of JSON.stringify
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Received response:", data);
            document.getElementById("angle").textContent = data.angle;
        })
        .catch(error => {
            console.error("Error:", error);
            document.getElementById("angle").textContent = 
                "Error: " + error.message;
        });
    }

// The updatePointer functions below first find the SVG element with the id of the pointer (e.g actual, target, tiller)
// Then it updates the SVG elements using the rotate function

// Update the compass pointer for the current heading
function updateHeading(a){
    console.log("update Heading: ", a)
    line = document.getElementById("actual")
    line.setAttribute("transform", `rotate(${a}, 100, 100)`);

}

// Update the compass pointer for the target heading
function updateTarget(a){
    console.log("update Target: ", a)
    line = document.getElementById("target")
    line.setAttribute("transform", `rotate(${a}, 100, 100)`);

}

// Update the compass pointer for the tiller angle
function updateTiller(a){
    console.log("update Target: ", a)
    line = document.getElementById("tiller")
    line.setAttribute("transform", `rotate(${a}, 100, 100)`);
}

// Update the compass
async function updateCompass() {
    response = await fetch('/api/headings');
    console.log(response)
    readings = await response.json();
    updateTarget(readings.target)
    updateHeading(readings.actual)
    updateTiller(readings.tiller)
    
}

// Update the system status
async function systemStatus(){
    response = await fetch('/api/systemStatus');
    console.log(response)
    sysStatus = await response.json();
    console.log(sysStatus.status)
    console.log(sysStatus)
    button = document.getElementById('loggingButton')
    setButtonStatus(sysStatus)
}

// Update the sensor readings
async function sensorReadings(){
    response = await fetch('/api/sensorReadings');
    console.log(response)
    sensorReadings = await response.json();
    console.log(sensorReadings)
}

// Update the button status
function setButtonStatus(sysStatus){
    button = document.getElementById('loggingButton')
    if (sysStatus.status) {
        button.textContent = "END"
        button.style.backgroundColor = "red"
    }
    else{
        button.textContent = "LOG"
        button.style.backgroundColor = "green"
    }
    buttonStart = document.getElementById('startPilotButton')
    buttonStop = document.getElementById('stopPilotButton')
    if (sysStatus.pilotRunning) {
        buttonStart.disabled = true;    
        buttonStop.disabled = false;
    }
    else{
        buttonStart.disabled = false;
        buttonStop.disabled = true;
    }
    buttonSim = document.getElementById('simulateButton')
    if (sysStatus.simRunning) {
        buttonSim.textContent = "STOP SIMULATION"
        buttonSim.style.backgroundColor = "red"
    }
    else{
        buttonSim.textContent = "START SIMULATION"
        buttonSim.style.backgroundColor = "green"
    }
}

// Toggle logging
async function toggleLogging(){
    response = await fetch('/api/toggleLogging');
    
    logging_status = await response.json();
    console.log(logging_status.status)
    button = document.getElementById('loggingButton')
    setButtonStatus(logging_status)
}

// Start the pilot
async function startPilot(){
    response = await fetch('/api/startPilot');
    console.log(response)
}

// Toggle simulation
async function toggleSimulation() {
    fetch('/api/toggleSimulation', {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Stop the pilot
async function stopPilot(){
    response = await fetch('/api/stopPilot');
    console.log(response)
}

// Update all the readings
async function updateAll(){
    updateCompass();
    systemStatus();
}

// Update readings every 200ms
setInterval(updateAll, 200);