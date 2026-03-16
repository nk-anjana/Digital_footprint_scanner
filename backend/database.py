import pymysql
import json
import logging
from contextlib import contextmanager
from passlib.context import CryptContext
from backend.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

# Setup logging for database errors
logger = logging.getLogger("osint_api")

# Configuration pulled from central config
DB_CONFIG = {
    "host": DB_HOST,
    "port": DB_PORT,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": DB_NAME,
    "cursorclass": pymysql.cursors.DictCursor,
}

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Helper Utilities ---

def hash_password(plain: str) -> str:
    """Hashes a plain-text password."""
    return _pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    """Verifies a password against its hash."""
    return _pwd_context.verify(plain, hashed)

@contextmanager
def get_db_cursor():
    """
    Context manager that ensures connections are ALWAYS closed, 
    preventing 'Too many connections' errors.
    """
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Database error: {e}")
        raise e
    finally:
        conn.close()

def init_db():
    """Initializes the database schema if it doesn't exist."""
    with get_db_cursor() as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                hashed_password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                scan_id VARCHAR(255) PRIMARY KEY,
                owner VARCHAR(255) NOT NULL,
                email VARCHAR(255) NULL,
                username VARCHAR(255) NULL,
                domain VARCHAR(255) NULL,
                status VARCHAR(50),
                findings JSON,
                risk_score INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (owner) REFERENCES users(username) ON DELETE CASCADE
            )
        """)

# --- Authentication Logic ---

def get_user(username: str) -> dict:
    """Fetches a user record by username."""
    with get_db_cursor() as c:
        c.execute("SELECT * FROM users WHERE username = %s", (username,))
        return c.fetchone()

def create_user(username: str, password: str) -> None:
    """Registers a new user."""
    hashed = hash_password(password)
    with get_db_cursor() as c:
        c.execute(
            "INSERT INTO users (username, hashed_password) VALUES (%s, %s)",
            (username, hashed),
        )

# --- Scan Logic ---

def create_scan_entry(scan_id: str, owner: str, email: str = None, username: str = None, domain: str = None) -> None:
    """Initializes a scan record. Values not provided are stored as NULL."""
    with get_db_cursor() as c:
        c.execute(
            """
            INSERT INTO scans 
                (scan_id, owner, email, username, domain, status, findings, risk_score)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (scan_id, owner, email, username, domain, "Running", json.dumps([]), 0),
        )

def update_scan_result(scan_id: str, findings: list, risk_score: int) -> None:
    """Updates the scan entry with results from the Celery worker."""
    with get_db_cursor() as c:
        c.execute(
            """
            UPDATE scans
            SET status = %s, findings = %s, risk_score = %s
            WHERE scan_id = %s
            """,
            ("Completed", json.dumps(findings), risk_score, scan_id),
        )

def get_scan_result(scan_id: str) -> dict:
    """Retrieves full scan results, safely parsing the JSON findings."""
    with get_db_cursor() as c:
        c.execute("SELECT * FROM scans WHERE scan_id = %s", (scan_id,))
        row = c.fetchone()
        if row and isinstance(row.get("findings"), str):
            row["findings"] = json.loads(row["findings"])
        return row

def get_scans_by_owner(owner: str, limit: int = 20, offset: int = 0) -> list:
    """Paginated list of scans for a specific user."""
    with get_db_cursor() as c:
        c.execute(
            """
            SELECT scan_id, email, username, domain, status, risk_score, created_at
            FROM scans WHERE owner = %s
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
            """,
            (owner, limit, offset),
        )
        return c.fetchall()

def delete_scan(scan_id: str, owner: str) -> bool:
    """Deletes a scan if the owner matches."""
    with get_db_cursor() as c:
        c.execute(
            "DELETE FROM scans WHERE scan_id = %s AND owner = %s",
            (scan_id, owner),
        )
        # Access the cursor rowcount through the context manager's inner logic
        return c.rowcount > 0