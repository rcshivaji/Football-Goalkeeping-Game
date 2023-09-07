from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Store the user's shooting history
user_shooting_history = []

# Add a variable to store the CPU goalkeeper's predicted direction
cpu_predicted_direction = None

# Implement CPU goalkeeper behavior (random dive for demonstration)
def cpu_goalkeeper_behavior():
    return random.choice(['left', 'center', 'right'])

# Implement a basic prediction algorithm (Maximum in last 10 approach)
def predict_user_direction():
    if len(user_shooting_history)<10:
        return cpu_goalkeeper_behavior()
    direction_counts = {}
    for d in user_shooting_history[-10:]:
        if d in direction_counts:
            direction_counts[d] += 1
        else:
            direction_counts[d] = 1

    # Get the direction with the highest count
    predicted_direction = max(direction_counts, key=direction_counts.get)

    return predicted_direction

# Pattern prediction algorithm :o 


@app.route('/')
def game():
    return render_template('game.html')

@app.route('/shoot', methods=['POST'])
def handle_shoot():
    direction = request.json.get('direction')

    # Add the user's shot direction to the history
    user_shooting_history.append(direction)

    # Update the CPU goalkeeper's predicted direction
    global cpu_predicted_direction
    cpu_predicted_direction = predict_user_direction()

    # Implement CPU goalkeeper behavior
    cpu_direction = cpu_goalkeeper_behavior()
    print(direction, cpu_predicted_direction)

    # Check if the CPU's prediction is correct
    #is_prediction_correct = direction == cpu_predicted_direction
    if direction == cpu_predicted_direction:
        is_prediction_correct = True
    else:
        is_prediction_correct = False
    print("£££",is_prediction_correct,type(is_prediction_correct))

    response_data = {
        'cpu_direction': cpu_predicted_direction,
        'user_direction': direction,
        'is_prediction_correct': is_prediction_correct
    }

    return jsonify(response_data)

@app.route('/update_prediction', methods=['POST'])
def update_prediction():
    user_direction = request.json.get('user_direction')
    # Add the user's direction to the shooting history
    user_shooting_history.append(user_direction)
    # Calculate the new prediction based on updated data
    updated_prediction = predict_user_direction()
    return jsonify({'updated_prediction': updated_prediction})

if __name__ == "__main__":
    app.run(debug=True)
