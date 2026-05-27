import sqlite3
from llm_parser import ExtractedFile

DB_NAME = "social_router.db"

def initialize_database():
    conn = sqlite3.connect(DB_NAME)
    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_number INTEGER,
            name TEXT,
            doc_number TEXT,
            email TEXT,
            location TEXT,
            area TEXT,
            company TEXT
        )
        """)
        conn.commit()
        print("[*] Database schema verified.")
    except sqlite3.Error as e:
        print(f"[!] Database Initialization Error: {e}")
    finally:
        conn.close()

def save_to_database(doc: ExtractedFile):
    conn = sqlite3.connect(DB_NAME)
    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO requests (id_number, name, doc_number, email, location, area, company)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (
            doc.id_number, 
            doc.name, 
            doc.doc_number, 
            doc.email, 
            doc.location, 
            doc.area, 
            doc.company
        ))
        conn.commit()
        print(f"[*] Record for '{doc.name}' committed to disk successfully.")
    except sqlite3.Error as e:
        print(f"[!] Database Write Error: {e}")
    finally:
        conn.close()
