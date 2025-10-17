import sqlite3

class NoteDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("notes.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_note(self, title, content, timestamp):
        self.cursor.execute('''
            INSERT INTO notes (title, content, timestamp) VALUES (?, ?, ?)
        ''', (title, content, timestamp))
        self.conn.commit()

    def get_all_notes(self):
        self.cursor.execute('SELECT * FROM notes ORDER BY timestamp DESC')
        return self.cursor.fetchall()

    def update_note(self, title, content, timestamp):
        self.cursor.execute('''
            UPDATE notes SET content = ?, timestamp = ? WHERE title= ?
        ''', (content, timestamp, title))
        self.conn.commit()

    def delete_note(self, title):
        self.cursor.execute('DELETE FROM notes WHERE title = ?', (title,))
        self.conn.commit()
    
    def get_specific_note(self, title):
        self.cursor.execute('SELECT * FROM notes WHERE title = ?', (title,))
        note = self.cursor.fetchone()
        return note

print(NoteDatabase().get_all_notes())  # For testing purposes
#NoteDatabase().delete_note("my note1")