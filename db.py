import sqlite3

database_name: str = "monzo_tokens.db"
def create_table_if_not_exists():
    try:
        with sqlite3.connect(database_name) as conn:
            print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tokens (
                access_token text NOT NULL, 
                refresh_token text NOT NULL, 
                expiry DATE INTEGER NULL
            )
            """)   
            conn.commit()
    except sqlite3.OperationalError as e:
        print(e)

def insert_access_token(access_token: str, refresh_token: str, expiry: int):
    try:
        with sqlite3.connect(database_name) as conn:
            print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO tokens (access_token, refresh_token, expiry) VALUES(?,?,?)
            """,(access_token, refresh_token, expiry))   
            conn.commit()
    except sqlite3.OperationalError as e:
        print(e)

def fetch_access_token() -> tuple[str, str, int]:
    try:
        with sqlite3.connect(database_name) as conn:
            print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM tokens LIMIT 1""")  
            response = cursor.fetchone()
            return response
    except sqlite3.OperationalError as e:
        print(e)
    
def drop_expired_access_token():
    try:
        print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")
        with sqlite3.connect(database_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""DELETE FROM tokens""")   
            conn.commit()
    except sqlite3.OperationalError as e:
        print(e)