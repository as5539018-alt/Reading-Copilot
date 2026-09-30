import sqlite3
from datetime import date

class HistoryService:
    def __init__(self, database_path="C:/Users/HP/Documents/reading project/database/reading_copilot.db"):
        self.database_path=database_path
        self._create_table()
    def _create_table(self):
        with sqlite3.connect(self.database_path) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT NOT NULL,
                    context_before TEXT,
                    context_after TEXT,
                    explanation TEXT NOT NULL,
                    created_date TEXT NOT NULL
                )
            """)
            connection.execute("""
                CREATE INDEX IF NOT EXISTS idx_history_date_id
                ON history (created_date DESC, id DESC)
            """)
            
    def save(self, word, context, explanation):
        before=context.get("before", "") if context else ""
        after = context.get("after", "") if context else ""
        created_date = date.today().isoformat()
    
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.execute("""
                INSERT INTO history(
                    word,
                    context_before,
                    context_after,
                    explanation,
                    created_date
                )
                VALUES (?, ?, ?, ?, ?)
    
            """, (
                    word,
                    before,
                    after,
                    explanation,
                    created_date
            )
            )
            connection.commit()
            return cursor.lastrowid
    def get_all(self):
        #offset = (page-1)*100
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.execute("""
                SELECT
                    id,
                    word,
                    context_before,
                    context_after,
                    explanation,
                    created_date
                FROM history
                ORDER BY created_date DESC, id DESC
            """)
            rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "word": row[1],
                "context['before']": row[2],
                "context['after']": row[3],
                "explanation": row[4],
                "date": row[5]
            }
            for row in rows
        ]
    def search(self, quest):
        quest = quest.strip()
        if not quest:
            return self.get_all()
        pattern = f"%{quest}%"
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.execute("""
                SELECT
                    id,
                    word,
                    context_before,
                    context_after,
                    explanation,
                    created_date
                FROM history
                WHERE
                    word LIKE ?
                    OR explanation LIKE ?
                    OR context_before LIKE ?
                    OR context_after LIKE ?
                ORDER BY created_date DESC, id DESC
            """, (
                    pattern,
                    pattern,
                    pattern,
                    pattern
            ))
            rows=cursor.fetchall()
        return[
            {
                "id":row[0],
                "word":row[1],
                "context['before']": row[2],
                "context['after']": row[3],
                "explanation":row[4],
                "date":row[5]
            }
            for row in rows
        ]
    def delete(self, history_id):
        with sqlite3.connect(self.database_path) as connection:
            connection.execute("""
                DELETE FROM history
                WHERE id = ?                
            """, (history_id,)
            )
            connection.commit()
    def clear_all(self):
        with sqlite3.connect(self.database_path) as connection:
            connection.execute("""DELETE FROM history""")
            connection.commit()
    def get_by_id(self, history_id):
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.execute("""
                SELECT
                    id,
                    word,
                    context_before,
                    context_after,
                    explanation,
                    created_date
                FROM history
                WHERE id = ?
            """, (history_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return{
                "id":row[0],
                "word":row[1],
                "context['before']":row[2],
                "context['after]": row[3],
                "explanation":row[4],
                "date":row[5]
            }
