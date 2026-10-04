
from flask import Flask, render_template, request, redirect, send_from_directory
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Folder for uploaded files
os.makedirs("uploads", exist_ok=True)

# Create database and table
db = sqlite3.connect("notes.db")

db.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    year TEXT,
    subject TEXT,
    filename TEXT
)
""")

db.commit()
db.close()


# Home page and upload notes
@app.route("/", methods=["GET", "POST"])
def home():
    db = sqlite3.connect("notes.db")

    if request.method == "POST":
        title = request.form["title"].strip()
        year = request.form["year"]
        subject = request.form["subject"].strip()
        file = request.files["file"]

        if not title or not subject or not file or not file.filename:
            db.close()
            return "Please fill in all fields and select a file.", 400

        filename = secure_filename(file.filename)

        if not filename:
            db.close()
            return "Invalid filename.", 400

        # Save the uploaded file with a unique name
        stored_name = os.urandom(8).hex() + "_" + filename
        file.save(os.path.join("uploads", stored_name))

        # Save note details in the database
        db.execute("""
            INSERT INTO notes (title, year, subject, filename)
            VALUES (?, ?, ?, ?)
        """, (title, year, subject, stored_name))

        db.commit()
        db.close()

        return redirect("/")

    # Search notes
    search = request.args.get("search", "")

    notes = db.execute("""
        SELECT * FROM notes
        WHERE title LIKE ?
           OR subject LIKE ?
           OR year LIKE ?
        ORDER BY id DESC
    """, (
        "%" + search + "%",
        "%" + search + "%",
        "%" + search + "%"
    )).fetchall()

    db.close()

    return render_template(
        "index.html",
        notes=notes,
        search=search
    )


# Download a note
@app.route("/uploads/<filename>")
def download_file(filename):
    return send_from_directory(
        "uploads", filename, as_attachment=True
    )


# Delete a note
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    db = sqlite3.connect("notes.db")

    note = db.execute(
        "SELECT filename FROM notes WHERE id = ?", (id,)
    ).fetchone()

    if note:
        path = os.path.join("uploads", note[0])

        if os.path.isfile(path):
            os.remove(path)

        db.execute("DELETE FROM notes WHERE id = ?", (id,))
        db.commit()

    db.close()

    return redirect("/")


# Run the website
if __name__ == "__main__":
    app.run(debug=True)