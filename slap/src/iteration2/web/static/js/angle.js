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

async function toggleLogging(){
    response = await fetch('/api/toggleLogging');
    
    logging_status = await response.json();
    console.log(logging_status.status)
    button = document.getElementById('loggingButton')
    if (logging_status.status) {
        console.log("set to STOP")
        button.textContent = "STOP"
        button.style.backgroundColor = "red"
    }
    else {
        console.log("set to START")
        button.textContent = "START"
        button.style.backgroundColor = "green"
    }
}
// Initial load
updateCompass();

// Update readings
setInterval(updateCompass, 200);