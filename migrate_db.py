"""
OptiLearn AI — Database Migration Script
Adds new columns (options, correct_option, selected_option) to existing DB
without losing any existing data.
"""
import sqlite3
import os
import sys

DB_PATH = os.path.join("data", "optilearn.db")

if not os.path.exists(DB_PATH):
    print(f"[ERROR] Database not found at: {DB_PATH}")
    sys.exit(1)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

def column_exists(table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    cols = [row[1] for row in cursor.fetchall()]
    return column in cols

migrations = [
    ("questions", "options", "TEXT"),
    ("questions", "correct_option", "VARCHAR(1)"),
    ("quiz_responses", "selected_option", "VARCHAR(1)"),
]

applied = 0
for table, col, col_type in migrations:
    if not column_exists(table, col):
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {col} {col_type}")
        print(f"[OK] Added column '{col}' to table '{table}'")
        applied += 1
    else:
        print(f"[--] Column '{col}' already exists in '{table}' — skipping")

conn.commit()
conn.close()

print(f"\n[OK] Migration complete — {applied} column(s) added.")
