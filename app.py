
from flask import Flask, render_template, request, redirect, send_from_directory, abort
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
DATABASE = os.path.join(app.root_path, "notes.db")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Create database and table
db = sqlite3.connect(DATABASE)

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


# Home page, upload notes and search
@app.route("/", methods=["GET", "POST"])
def home():

    db = sqlite3.connect(DATABASE)

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

        stored_name = os.urandom(8).hex() + "_" + filename

        file.save(os.path.join(UPLOAD_FOLDER, stored_name))

        db.execute("""
            INSERT INTO notes (title, year, subject, filename)
            VALUES (?, ?, ?, ?)
        """, (title, year, subject, stored_name))

        db.commit()
        db.close()

        return redirect("/#notes-section")

    search = request.args.get("search", "").strip()

    if search:

        keyword = f"%{search.lower()}%"

        notes = db.execute("""
            SELECT * FROM notes
            WHERE LOWER(TRIM(title)) LIKE ?
               OR LOWER(TRIM(subject)) LIKE ?
               OR LOWER(TRIM(year)) LIKE ?
            ORDER BY id DESC
        """, (keyword, keyword, keyword)).fetchall()

    else:

        notes = db.execute("""
            SELECT * FROM notes
            ORDER BY id DESC
        """).fetchall()

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
        UPLOAD_FOLDER,
        filename,
        as_attachment=True
    )


# Preview PDF inside the browser
@app.route("/preview/<int:id>")
def preview_file(id):

    db = sqlite3.connect(DATABASE)

    note = db.execute(
        "SELECT filename FROM notes WHERE id = ?",
        (id,)
    ).fetchone()

    db.close()

    if not note:
        abort(404)

    filename = note[0]

    if not filename.lower().endswith(".pdf"):
        abort(404)

    return send_from_directory(
        UPLOAD_FOLDER,
        filename,
        mimetype="application/pdf",
        as_attachment=False
    )


# Delete a note
@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):

    db = sqlite3.connect(DATABASE)

    note = db.execute(
        "SELECT filename FROM notes WHERE id = ?",
        (id,)
    ).fetchone()

    if note:

        path = os.path.join(UPLOAD_FOLDER, note[0])

        if os.path.isfile(path):
            os.remove(path)

        db.execute(
            "DELETE FROM notes WHERE id = ?",
            (id,)
        )

        db.commit()

    db.close()

    return redirect("/#notes-section")


# Run the website
if __name__ == "__main__":
    app.run(debug=True)
