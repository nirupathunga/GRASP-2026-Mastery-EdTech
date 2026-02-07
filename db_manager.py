import sqlite3

DB_NAME = "mastery_data.sqlite"

def update_db(topic_id, status="mastered"):
    """Records that a student has mastered a specific topic."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create the table if it doesn't exist yet
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS topic_status (
            topic_id TEXT PRIMARY KEY,
            status TEXT,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Update or Insert the status
    cursor.execute('''
        INSERT INTO topic_status (topic_id, status) 
        VALUES (?, ?)
        ON CONFLICT(topic_id) DO UPDATE SET status=excluded.status
    ''', (topic_id, status))
    
    conn.commit()
    conn.close()
    print(f"✅ Database Updated: {topic_id} is now {status}")