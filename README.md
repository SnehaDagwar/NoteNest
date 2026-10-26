# 📚 NoteNest — Student Resource Hub

> **Your Notes. Your Nest.**  
> A lightweight web app for students to upload, search, and download study materials — all in one place.

---

## ✨ Features

- 📤 **Upload Study Materials** — Share notes, PDFs, slides, and more with a simple form
- 🔍 **Smart Search** — Search resources by title, subject, or academic year
- 📥 **Download Resources** — One-click download of any uploaded material
- 🗑️ **Delete Resources** — Remove outdated or unwanted files easily
- 📂 **Resource Library** — Browse all uploaded notes in a clean card layout
- 🎓 **Year-wise Filtering** — Organise resources from First Year to Fourth Year
- 🗄️ **Persistent Storage** — All data stored in a local SQLite database

---

## 🛠️ Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Backend    | Python · Flask                      |
| Frontend   | HTML · CSS (Vanilla)                |
| Templating | Jinja2                              |
| Database   | SQLite3                             |
| File Handling | Werkzeug `secure_filename`       |

---

## 📁 Project Structure

```
NoteNest/
├── app.py                  # Flask application — routes and logic
├── notes.db                # SQLite database (auto-created, git-ignored)
├── .gitignore              # Ignores venv, db, cache files
├── static/
│   └── style.css           # All styling for the app
├── templates/
│   └── index.html          # Main HTML template (Jinja2)
└── uploads/                # Uploaded files stored here (auto-created)
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/SnehaDagwar/NoteNest.git
cd NoteNest
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

**Activate it:**

- **Windows:**
  ```powershell
  venv\Scripts\activate
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

```bash
pip install flask werkzeug
```

### 4. Run the App

```bash
python app.py
```

The app will start in **debug mode** and be available at:

```
http://127.0.0.1:5000
```

---

## 📖 How to Use

### Uploading a Resource
1. Navigate to the **Upload Notes** section on the dashboard.
2. Fill in the **Resource Title**, select your **Academic Year**, and enter the **Subject**.
3. Choose a file (PDF, DOC, DOCX, PPT, PPTX, TXT, JPG, PNG, or ZIP).
4. Click **⬆ Upload Resource** — your file is now shared!

### Searching for Resources
1. Go to the **Study Resources** section.
2. Type any keyword into the search bar (title, subject, or year).
3. Click **Search** to filter results, or **Clear** to show all resources.

### Downloading a Resource
- Click the **⬇ Download** button on any resource card.

### Deleting a Resource
- Click the **🗑 Delete** button on a resource card.
- Confirm the deletion prompt — the file and its database entry are permanently removed.

---

## 📂 Supported File Types

| Extension | Description         |
|-----------|---------------------|
| `.pdf`    | PDF Document        |
| `.doc`    | Word Document       |
| `.docx`   | Word Document (new) |
| `.ppt`    | PowerPoint          |
| `.pptx`   | PowerPoint (new)    |
| `.txt`    | Plain Text          |
| `.jpg` / `.jpeg` | Image      |
| `.png`    | Image               |
| `.zip`    | Compressed Archive  |

---

## 🔒 Security Notes

- File names are sanitised using Werkzeug's `secure_filename` to prevent path traversal attacks.
- Each uploaded file is stored with a unique 8-byte random hex prefix to avoid filename conflicts.
- The `.gitignore` ensures the database (`notes.db`) and virtual environment are never committed.

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to the branch: `git push origin feat/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👩‍💻 Author

Made with ❤️ for students, by students.

**Sneha Dagwar** · [GitHub](https://github.com/SnehaDagwar)

---

> © 2026 NoteNest · *Your Notes. Your Nest.*
