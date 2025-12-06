from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)

# CORRECT! Using data.json
DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}  # Return empty dict if file doesn't exist

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Load existing data when app starts
blocks = load_data()

# If blocks is empty, initialize with your blocks
if not blocks:  # Only if data.json is empty or doesn't exist
    blocks = {
        "Learning Centre 1": {"total_classrooms": 3, "students": []},
        "Learning Centre 2": {"total_classrooms": 3, "students": []},
        "Kalataranga": {"total_classrooms": 3, "students": []},
        "Alliance School of Applied Engineering": {"total_classrooms": 3, "students": []},
        "Alliance School of Law": {"total_classrooms": 3, "students": []},
    }
    save_data(blocks)  # Save initial structure

def assign_class(block_name):
    count = len(blocks[block_name]["students"])
    if count < 50:
        return "A"
    elif count < 100:
        return "B"
    else:
        return "C"

@app.route('/')
def index():
    total_students = sum(len(block["students"]) for block in blocks.values())
    return render_template('index.html', blocks=blocks, total_students=total_students)

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    course = request.form['course']
    block_name = request.form['block']

    class_name = assign_class(block_name)
    blocks[block_name]["students"].append({
        "name": name,
        "course": course,
        "class": class_name
    })

    save_data(blocks)  # Save to data.json
    return redirect(url_for('index'))

@app.route('/view/<block_name>')
def view_block(block_name):
    block = blocks.get(block_name, {})
    return render_template('view.html', block_name=block_name, students=block.get("students", []))

if __name__ == '__main__':
    app.run(debug=True)
