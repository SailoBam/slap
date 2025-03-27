async function sensorReadings(){
    response = await fetch('/api/sensorReadings');
    console.log(response)
    responseReadings = await response.json();
    console.log(responseReadings)
    return responseReadings
}

async function updateAll(){
    readings = await sensorReadings();
    for (const [sensorName, value] of Object.entries(readings)) {
        console.log(sensorName, value)
        document.getElementById(sensorName).textContent = value;
    }
}
// Update readings
setInterval(updateAll, 200);