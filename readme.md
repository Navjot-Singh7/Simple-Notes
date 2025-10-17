# 📝 Simple Notes

A clean, efficient note-taking app built with KivyMD and SQLite3. Create, edit, and manage your notes with a smooth, intuitive interface.

## ✨ Features

- **Create & Edit Notes** - Simple title-based note management
- **Auto-Save Timestamps** - Tracks when notes were created or modified
- **Unsaved Changes Protection** - Prevents accidental data loss when navigating away
- **Duplicate Prevention** - Ensures unique note titles
- **Dark Theme** - Easy on the eyes with Material Design
- **Offline Storage** - All data stored locally using SQLite3

## 🛠️ Tech Stack

- **Python 3** - Core programming language
- **KivyMD** - Material Design UI components
- **SQLite3** - Local database storage
- **DateTime** - Automatic timestamping

## 🚀 Installation

### Prerequisites
```bash
pip install kivymd
```

Running the Application

```bash
python main.py
```

📱 Usage

1. Create Note - Tap the + button and enter a title
2. Edit Note - Tap any note from the list to view/edit
3. Save Changes - Use the save button or navigate away (with confirmation)
4. Delete Note - Use the trash can button with confirmation
5. Auto-Save - Notes are automatically timestamped on creation and modification

🗃️ Database

The app uses SQLite3 with the following schema:

```sql
CREATE TABLE notes (
    title TEXT NOT NULL,
    content TEXT NOT NULL, 
    timestamp TEXT NOT NULL
)
```

🔧 Key Features

· Smart Navigation - Handles unsaved changes gracefully
· Efficient Queries - Fast note retrieval and updates
· Clean UI - Material Design with proper spacing
· Data Safety - Multiple confirmation dialogs for destructive actions