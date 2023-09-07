// Function to handle shooting
function shoot(direction) {
    // Send the user's chosen direction to the server
    fetch('/shoot', {
        method: 'POST',
        body: JSON.stringify({ direction: direction }),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        // Display the CPU goalkeeper's prediction
        displayPrediction(data.cpu_direction);
        displayPrediction(data.user_direction);

        // Check if the CPU's prediction was correct and update the display
        if (data.is_prediction_correct) {
            displayPrediction(`Correct! CPU predicted: ${data.cpu_direction}`);
        } else {
            displayPrediction(`Incorrect. CPU predicted: ${data.cpu_direction}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to display CPU goalkeeper's prediction
function displayPrediction(prediction) {
    const predictedDirectionSpan = document.getElementById('predicted-direction');
    predictedDirectionSpan.textContent = prediction;
}

// Event listeners for shooting buttons
document.getElementById('shoot-left').addEventListener('click', () => shoot('left'));
document.getElementById('shoot-center').addEventListener('click', () => shoot('center'));
document.getElementById('shoot-right').addEventListener('click', () => shoot('right'));
