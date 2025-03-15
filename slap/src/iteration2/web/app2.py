from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

app = Flask(__name__)

def load_data():
    with open('data.json', 'r') as f:
        return json.load(f)

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', people=data['people'])

@app.route('/edit/<int:id>', methods=['GET'])
def edit(id):
    data = load_data()
    person = next((p for p in data['people'] if p['id'] == id), None)
    if person:
        return render_template('edit.html', person=person)
    return redirect(url_for('index'))

@app.route('/save', methods=['POST'])
def save():
    data = load_data()
    person_id = int(request.form['id'])
    updated_person = {
        'id': person_id,
        'name': request.form['name'],
        'dob': request.form['dob'],
        'job': request.form['job']
    }
    
    data['people'] = [updated_person if p['id'] == person_id else p for p in data['people']]
    save_data(data)
    return redirect(url_for('index'))

@app.route('/select/<int:id>', methods=['POST'])
def select(id):
    # This route will be called via AJAX when a row is selected
    return jsonify({'message': f'Selected person with ID: {id}'})

if __name__ == '__main__':
    app.run(debug=True) 