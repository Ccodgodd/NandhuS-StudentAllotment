from flask import Flask, render_template, request, redirect, url_for
import json, os

app = Flask(__name__)

DATA_FILE = "data.json"


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

blocks = load_data()


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
    return render_template('index.html', blocks=blocks)

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

    save_data(blocks)
    return redirect(url_for('index'))

@app.route('/view/<block_name>')
def view_block(block_name):
    block = blocks.get(block_name, {})
    return render_template('view.html', block_name=block_name, students=block.get("students", []))

if __name__ == '__main__':
    app.run(debug=True)
