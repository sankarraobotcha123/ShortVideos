from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from app.core.config import settings


SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS content_packages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    board_source TEXT NOT NULL,
    class_level TEXT NOT NULL,
    subject TEXT NOT NULL,
    topic TEXT NOT NULL,
    audience TEXT NOT NULL,
    language TEXT NOT NULL DEFAULT 'English',
    duration_seconds INTEGER NOT NULL DEFAULT 60,
    output_type TEXT NOT NULL DEFAULT 'Short',
    tone TEXT NOT NULL DEFAULT 'Curious',
    source_notes TEXT DEFAULT '',
    source_name TEXT DEFAULT '',
    source_license_type TEXT DEFAULT '',
    page_or_section_reference TEXT DEFAULT '',
    copied_text_used INTEGER NOT NULL DEFAULT 0,
    transformation_notes TEXT DEFAULT '',
    hook TEXT NOT NULL,
    script_text TEXT NOT NULL,
    storyboard_markdown TEXT NOT NULL,
    subtitle_srt TEXT NOT NULL,
    visual_prompts_markdown TEXT NOT NULL,
    title_options TEXT NOT NULL,
    description TEXT NOT NULL,
    hashtags TEXT NOT NULL,
    quiz_question TEXT NOT NULL,
    trust_score INTEGER NOT NULL,
    provider_used TEXT NOT NULL DEFAULT 'template',
    generation_mode TEXT NOT NULL DEFAULT 'deterministic_template',
    provider_chain TEXT NOT NULL DEFAULT 'template',
    provider_notes TEXT DEFAULT '',
    provider_attempts TEXT DEFAULT '[]',
    review_status TEXT NOT NULL DEFAULT 'draft',
    reviewer_notes TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS manual_analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id INTEGER NOT NULL,
    platform TEXT NOT NULL DEFAULT 'YouTube Shorts',
    entry_date TEXT NOT NULL DEFAULT CURRENT_DATE,
    views INTEGER NOT NULL DEFAULT 0,
    likes INTEGER NOT NULL DEFAULT 0,
    comments INTEGER NOT NULL DEFAULT 0,
    shares INTEGER NOT NULL DEFAULT 0,
    avg_view_duration_seconds REAL DEFAULT 0,
    retention_pct REAL DEFAULT 0,
    ctr_pct REAL DEFAULT 0,
    notes TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE CASCADE
);
"""


def ensure_storage() -> None:
    settings.database_path.parent.mkdir(parents=True, exist_ok=True)
    settings.export_dir.mkdir(parents=True, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    ensure_storage()
    conn = sqlite3.connect(settings.database_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def db_session() -> Iterator[sqlite3.Connection]:
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    ensure_storage()
    with db_session() as conn:
        conn.executescript(SCHEMA_SQL)
        _apply_lightweight_migrations(conn)


def _apply_lightweight_migrations(conn: sqlite3.Connection) -> None:
    """Add missing columns for users who already created an MVP database."""
    columns = {row[1] for row in conn.execute("PRAGMA table_info(content_packages)").fetchall()}
    additions = {
        "provider_used": "ALTER TABLE content_packages ADD COLUMN provider_used TEXT NOT NULL DEFAULT 'template'",
        "generation_mode": "ALTER TABLE content_packages ADD COLUMN generation_mode TEXT NOT NULL DEFAULT 'deterministic_template'",
        "provider_chain": "ALTER TABLE content_packages ADD COLUMN provider_chain TEXT NOT NULL DEFAULT 'template'",
        "provider_notes": "ALTER TABLE content_packages ADD COLUMN provider_notes TEXT DEFAULT ''",
        "provider_attempts": "ALTER TABLE content_packages ADD COLUMN provider_attempts TEXT DEFAULT '[]'",
    }
    for column, sql in additions.items():
        if column not in columns:
            conn.execute(sql)
