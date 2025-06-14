import sqlite3
from config import DB_NAME

# ---------- INITIALIZE DATABASE ----------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Users Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            last_active INTEGER
        )
    ''')

    # Videos Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            thumbnail TEXT,
            duration INTEGER,
            link TEXT,
            actions TEXT,
            method TEXT, -- 'link' or 'manual'
            instructions TEXT,
            status TEXT DEFAULT 'pending',
            assigned_to INTEGER DEFAULT NULL,
            proof TEXT DEFAULT NULL,
            verified_by_owner INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Reports Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id INTEGER,
            reported_by INTEGER,
            reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

# ---------- USER OPERATIONS ----------
def add_user(user_id, username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, username, last_active) VALUES (?, ?, strftime('%s','now'))", (user_id, username))
    conn.commit()
    conn.close()

def update_last_active(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE users SET last_active = strftime('%s','now') WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

# ---------- VIDEO OPERATIONS ----------
def get_user_videos(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM videos WHERE user_id = ?", (user_id,))
    videos = c.fetchall()
    conn.close()
    return videos

def add_video(user_id, title, thumbnail, duration, link, actions, method, instructions):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO videos (user_id, title, thumbnail, duration, link, actions, method, instructions)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, title, thumbnail, duration, link, actions, method, instructions))
    conn.commit()
    conn.close()

def remove_video(video_id, user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM videos WHERE id = ? AND user_id = ?", (video_id, user_id))
    conn.commit()
    conn.close()

# ---------- MATCHING & PROOF ----------
def assign_video_to_user(video_id, user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE videos SET assigned_to = ? WHERE id = ?", (user_id, video_id))
    conn.commit()
    conn.close()

def submit_proof(video_id, proof_link):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE videos SET proof = ?, status = 'proof_submitted' WHERE id = ?", (proof_link, video_id))
    conn.commit()
    conn.close()

def verify_proof(video_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE videos SET verified_by_owner = 1, status = 'completed' WHERE id = ?", (video_id,))
    conn.commit()
    conn.close()

def get_pending_tasks(exclude_user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM videos WHERE user_id != ? AND status = 'pending' LIMIT 1", (exclude_user_id,))
    video = c.fetchone()
    conn.close()
    return video

# ---------- REPORT SYSTEM ----------
def add_report(video_id, reported_by, reason):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO reports (video_id, reported_by, reason)
        VALUES (?, ?, ?)
    ''', (video_id, reported_by, reason))
    conn.commit()
    conn.close()

def get_pending_reports():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM reports ORDER BY created_at DESC")
    reports = c.fetchall()
    conn.close()
    return reports

# ---------- VIDEO LIMIT PER USER ----------
def get_video_count(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM videos WHERE user_id = ?", (user_id,))
    count = c.fetchone()[0]
    conn.close()
    return count
