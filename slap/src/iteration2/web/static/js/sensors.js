async function sensorReadings(){
    response = await fetch('/api/sensorReadings');
    console.log(response)
    responseReadings = await response.json();
    console.log(responseReadings)
    return responseReadings
}

async function updateAll(){
    readings = await sensorReadings();
    for (const reading of readings) {
        console.log(reading)
        document.getElementById(reading.name).textContent = reading.value;
    }
}
// Update readings
setInterval(updateAll, 200);