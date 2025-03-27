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



function updateHeading(a){
    console.log("update Heading: ", a)
    line = document.getElementById("actual")
    line.setAttribute("transform", `rotate(${a}, 100, 100)`);

}

function updateTarget(a){
    console.log("update Target: ", a)
    line = document.getElementById("target")
    line.setAttribute("transform", `rotate(${a}, 100, 100)`);

}

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

async function systemStatus(){
    response = await fetch('/api/systemStatus');
    console.log(response)
    sysStatus = await response.json();
    console.log(sysStatus.status)
    console.log(sysStatus)
    button = document.getElementById('loggingButton')
    setButtonStatus(sysStatus)
}


async function sensorReadings(){
    response = await fetch('/api/sensorReadings');
    console.log(response)
    sensorReadings = await response.json();
    console.log(sensorReadings)
}


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
}

async function toggleLogging(){
    response = await fetch('/api/toggleLogging');
    
    logging_status = await response.json();
    console.log(logging_status.status)
    button = document.getElementById('loggingButton')
    setButtonStatus(logging_status)
}

async function startPilot(){
    response = await fetch('/api/startPilot');
    console.log(response)
}

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

async function stopPilot(){
    response = await fetch('/api/stopPilot');
    console.log(response)
}


async function updateAll(){
    updateCompass();
    systemStatus();
}
// Update readings
setInterval(updateAll, 200);