from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd

app = Flask(__name__)

EXCEL_FILE = "data.xlsx"
BLOCKS_SHEET = "Blocks"

DEFAULT_BLOCKS = {
    "Learning Centre 1": {"total_classrooms": 3},
    "Learning Centre 2": {"total_classrooms": 3},
    "Kalataranga": {"total_classrooms": 3},
    "Alliance School of Applied Engineering": {"total_classrooms": 3},
    "Alliance School of Law": {"total_classrooms": 3}
}


def initialize_excel():
    """Create Excel file with default structure if it doesn't exist"""
    if not os.path.exists(EXCEL_FILE):
       
        blocks_df = pd.DataFrame({
            'Block Name': list(DEFAULT_BLOCKS.keys()),
            'Total Classrooms': [DEFAULT_BLOCKS[b]['total_classrooms'] for b in DEFAULT_BLOCKS.keys()]
        })
        
        
        students_df = pd.DataFrame(columns=['Block', 'Name', 'Roll', 'Course', 'Year', 'Section', 'Class'])
        
        with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
            blocks_df.to_excel(writer, sheet_name=BLOCKS_SHEET, index=False)
            students_df.to_excel(writer, sheet_name='Students', index=False)


def load_data():
    """Load data from Excel file and return blocks dictionary"""
    initialize_excel()
    
    try:
      
        blocks_df = pd.read_excel(EXCEL_FILE, sheet_name=BLOCKS_SHEET)
        blocks = {}
        
        for _, row in blocks_df.iterrows():
            block_name = row['Block Name']
            blocks[block_name] = {
                "total_classrooms": int(row['Total Classrooms']),
                "students": []
            }
        
        
        try:
            students_df = pd.read_excel(EXCEL_FILE, sheet_name='Students')
            
           
            if not students_df.empty:
                for _, row in students_df.iterrows():
                    block_name = str(row['Block'])
                    if block_name in blocks:
                        student = {
                            "name": str(row['Name']) if pd.notna(row['Name']) else '',
                            "roll": str(row['Roll']) if pd.notna(row['Roll']) else '',
                            "course": str(row['Course']) if pd.notna(row['Course']) else '',
                            "year": str(row['Year']) if pd.notna(row['Year']) else '',
                            "section": str(row['Section']) if pd.notna(row['Section']) else '',
                            "class": str(row['Class']) if pd.notna(row['Class']) else ''
                        }
                        blocks[block_name]["students"].append(student)
        except Exception as e:
            print(f"Error reading students sheet: {e}")
        
        return blocks
    except Exception as e:
        print(f"Error loading data: {e}")
       
        result = {}
        for block_name, block_data in DEFAULT_BLOCKS.items():
            result[block_name] = {**block_data, "students": []}
        return result


def save_data(blocks):
    """Save data to Excel file"""
    try:
        
        blocks_data = []
        for block_name, block_info in blocks.items():
            blocks_data.append({
                'Block Name': block_name,
                'Total Classrooms': block_info.get('total_classrooms', 3)
            })
        blocks_df = pd.DataFrame(blocks_data)
        
        
        students_data = []
        for block_name, block_info in blocks.items():
            for student in block_info.get('students', []):
                students_data.append({
                    'Block': block_name,
                    'Name': student.get('name', ''),
                    'Roll': student.get('roll', ''),
                    'Course': student.get('course', ''),
                    'Year': student.get('year', ''),
                    'Section': student.get('section', ''),
                    'Class': student.get('class', '')
                })
        students_df = pd.DataFrame(students_data)
        
        # Write to Excel
        with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
            blocks_df.to_excel(writer, sheet_name=BLOCKS_SHEET, index=False)
            students_df.to_excel(writer, sheet_name='Students', index=False)
    except Exception as e:
        print(f"Error saving data: {e}")

def assign_class(block_name, blocks_data):
    if block_name not in blocks_data:
        return "A"
    
    students = blocks_data[block_name].get("students", [])
    count = len(students)
    
    if count < 50:
        return "A"
    elif count < 100:
        return "B"
    else:
        return "C"

@app.route('/')
def index():
    blocks = load_data()
    return render_template('index.html', blocks=blocks)

@app.route('/add_student', methods=['POST'])
def add_student():
    
    blocks = load_data()
    
    name = request.form.get('name', '')
    roll = request.form.get('roll', '')
    course = request.form.get('course', '')
    year = request.form.get('year', '')
    section = request.form.get('section', '')
    block_name = request.form.get('block', '')

    if not block_name or block_name not in blocks:
        return redirect(url_for('index'))

  
    if "students" not in blocks[block_name]:
        blocks[block_name]["students"] = []

    class_name = assign_class(block_name, blocks)
    blocks[block_name]["students"].append({
        "name": name,
        "roll": roll,
        "course": course,
        "year": year,
        "section": section,
        "class": class_name
    })

    save_data(blocks)
    return redirect(url_for('index'))

@app.route('/view/<block_name>')
def view_block(block_name):
    
    blocks = load_data()
    
    if block_name not in blocks:
        return redirect(url_for('index'))
    
    block = blocks.get(block_name, {})
    students = block.get("students", [])
    return render_template('view.html', block_name=block_name, students=students)
@app.route('/delete_student/<block_name>/<roll>')
def delete_student(block_name, roll):
    blocks = load_data()

    if block_name in blocks:
        students = blocks[block_name]["students"]
        updated_students = [s for s in students if s.get("roll") != roll]
        blocks[block_name]["students"] = updated_students

        save_data(blocks)

    return redirect(url_for('view_block', block_name=block_name))


if __name__ == '__main__':
    app.run(debug=True, port=2000)
