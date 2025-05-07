import sqlite3
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """Initialize the SQLite database."""
    try:
        db_path = Path(__file__).parent.parent / "candidates.db"
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY,
                name TEXT,
                resume_text TEXT,
                skills TEXT,
                experience INTEGER,
                qualifications TEXT,
                match_score REAL,
                job_id TEXT
            )
        """)
        conn.commit()
        logger.info("Database initialized.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
    finally:
        conn.close()

def store_candidate(name, resume_text, skills, experience, qualifications, match_score, job_id):
    """
    Store candidate data in the database.

    Args:
        name (str): Candidate name or filename.
        resume_text (str): Resume text.
        skills (list): List of skills.
        experience (int): Years of experience.
        qualifications (list): List of qualifications.
        match_score (float): Match score.
        job_id (str): Job identifier.
    """
    try:
        conn = sqlite3.connect(Path(__file__).parent.parent / "candidates.db")
        c = conn.cursor()
        c.execute(
            """
            INSERT INTO candidates (name, resume_text, skills, experience, qualifications, match_score, job_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                resume_text,
                ",".join(skills),
                experience,
                ",".join(qualifications),
                match_score,
                job_id
            )
        )
        conn.commit()
        logger.info(f"Stored candidate: {name}")
    except Exception as e:
        logger.error(f"Error storing candidate {name}: {e}")
    finally:
        conn.close()

def get_candidates_by_job_id(job_id):
    """
    Retrieve candidates by job ID.

    Args:
        job_id (str): Job identifier.

    Returns:
        list: List of candidate dictionaries.
    """
    try:
        conn = sqlite3.connect(Path(__file__).parent.parent / "candidates.db")
        c = conn.cursor()
        c.execute(
            "SELECT name, skills, experience, qualifications, match_score FROM candidates WHERE job_id = ?",
            (job_id,)
        )
        rows = c.fetchall()
        candidates = [
            {
                "name": row[0],
                "skills": row[1].split(",") if row[1] else [],
                "experience": row[2],
                "qualifications": row[3].split(",") if row[3] else [],
                "match_score": round(row[4] * 100, 2)
            }
            for row in rows
        ]
        logger.info(f"Retrieved {len(candidates)} candidates for job_id: {job_id}")
        return candidates
    except Exception as e:
        logger.error(f"Error retrieving candidates for job_id {job_id}: {e}")
        return []
    finally:
        conn.close()