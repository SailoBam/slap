// Functions for reacting to button presses


function changeValue(c) {
    const url = '/addDirection'; 
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
            updateLine(data.angle)
        })
        .catch(error => {
            console.error("Error:", error);
            document.getElementById("angle").textContent = 
                "Error: " + error.message;
        });
}

function setValue(c) {
    const url = '/setDirection'; 
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
            updateLine(data.angle)
        })
        .catch(error => {
            console.error("Error:", error);
            document.getElementById("angle").textContent = 
                "Error: " + error.message;
        });
    }

function updateLine(a){
    console.log("update Line: ", a)
    line = document.getElementById("line")
    line.setAttribute("transform", `rotate(${a}, 100, 100)`);

}
