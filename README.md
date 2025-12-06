
---

# 🏫 Classroom Allotment System — Flask + Bootstrap

A web-based **Classroom Allotment System** built using **Flask (Python)** and **Bootstrap 5**, designed to efficiently assign students to classrooms across different academic blocks at **Alliance University**.

Developed with a clean and responsive UI, this app simplifies student management and classroom assignments for universities.

---

## 👨‍💻 Project Creators

* **Nandhu S**
* **Fiyanshu Singh**

---

## 🚀 Features

✅ Automatic classroom assignment (A, B, C) based on student count
✅ Add and view students per academic block
✅ Clean Bootstrap-based UI with responsive layout
✅ Gradient background and university-style theme
✅ Simple Flask backend for easy data handling

---

## 🛠️ Technologies Used

| Component  | Technology                   |
| ---------- | ---------------------------- |
| Backend    | Flask (Python)               |
| Frontend   | HTML, CSS, Bootstrap 5       |
| Templating | Jinja2                       |
| Styling    | Custom CSS + Bootstrap Theme |

---

## 📂 Project Structure

```
📦 Classroom-Allotment
│
├── app.py
├── static/
│   └── style.css
├── templates/
│   ├── index.html
│   └── view.html
└── README.md
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/<repo-name>.git
   cd <repo-name>
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows → venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install flask
   ```

4. **Run the application**

   ```bash
   python app.py
   ```

5. **Open in browser**

   ```
   http://127.0.0.1:5000/
   ```

---

## 🧠 How It Works

* The app contains predefined **blocks** (e.g., Learning Centre 1, Kalataranga, etc.).
* When a student is added, the system automatically assigns them to a class (A, B, or C) based on how many students are already registered in that block.
* Each block can be viewed to see the list of assigned students.

---

## 🌈 UI Highlights

* University-themed blue design
* Soft gradient background
* Responsive layout for all devices
* Clean forms and tables with hover effects

---

## 🧾 Future Enhancements

* Admin dashboard with class statistics using **Chart.js**
* Database integration (MySQL / SQLite) for persistent storage
* User authentication for admin login

---

## 🏁 License

This project is open-source and free to use under the **MIT License**.

---

