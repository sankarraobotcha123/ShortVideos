from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from app.core.config import settings


SCHEMA_SQL = """
PRAGMA foreign_keys = ON;


CREATE TABLE IF NOT EXISTS user_accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'content_admin',
    active INTEGER NOT NULL DEFAULT 1,
    last_login_at TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS auth_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    token TEXT NOT NULL UNIQUE,
    expires_at TEXT NOT NULL,
    revoked_at TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES user_accounts(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS content_batches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    niche TEXT NOT NULL DEFAULT '',
    target_audience TEXT NOT NULL DEFAULT '',
    start_date TEXT DEFAULT '',
    end_date TEXT DEFAULT '',
    planned_count INTEGER NOT NULL DEFAULT 20,
    status TEXT NOT NULL DEFAULT 'planning',
    notes TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS content_packages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id INTEGER,
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
    generation_duration_ms INTEGER NOT NULL DEFAULT 0,
    prompt_template_id INTEGER,
    prompt_template_name TEXT DEFAULT '',
    prompt_template_style TEXT DEFAULT '',
    prompt_template_snapshot TEXT DEFAULT '',
    review_status TEXT NOT NULL DEFAULT 'draft',
    reviewer_notes TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(batch_id) REFERENCES content_batches(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS publishing_calendar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id INTEGER NOT NULL UNIQUE,
    planned_publish_date TEXT NOT NULL,
    actual_publish_date TEXT DEFAULT '',
    platform TEXT NOT NULL DEFAULT 'YouTube Shorts',
    status TEXT NOT NULL DEFAULT 'planned',
    playlist_name TEXT DEFAULT '',
    notes TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS calendar_bulk_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id INTEGER,
    start_date TEXT NOT NULL,
    limit_count INTEGER NOT NULL DEFAULT 20,
    videos_per_day INTEGER NOT NULL DEFAULT 1,
    days_between INTEGER NOT NULL DEFAULT 0,
    platform TEXT NOT NULL DEFAULT 'YouTube Shorts',
    playlist_name TEXT DEFAULT '',
    status TEXT NOT NULL DEFAULT 'planned',
    order_by TEXT NOT NULL DEFAULT 'created_at',
    created_by TEXT DEFAULT '',
    scheduled_count INTEGER NOT NULL DEFAULT 0,
    skipped_count INTEGER NOT NULL DEFAULT 0,
    run_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(batch_id) REFERENCES content_batches(id) ON DELETE SET NULL
);


CREATE TABLE IF NOT EXISTS audio_assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id INTEGER NOT NULL,
    provider_used TEXT NOT NULL DEFAULT 'manual_recording',
    status TEXT NOT NULL DEFAULT 'manual_required',
    file_path TEXT NOT NULL,
    file_name TEXT NOT NULL,
    mime_type TEXT NOT NULL DEFAULT 'text/plain',
    voice_id TEXT DEFAULT '',
    duration_seconds REAL DEFAULT 0,
    script_snapshot TEXT NOT NULL,
    provider_notes TEXT DEFAULT '',
    provider_attempts TEXT DEFAULT '[]',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS assembly_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id INTEGER NOT NULL,
    plan_markdown TEXT NOT NULL,
    plan_json TEXT NOT NULL,
    scene_count INTEGER NOT NULL DEFAULT 0,
    estimated_duration_seconds INTEGER NOT NULL DEFAULT 60,
    assembly_mode TEXT NOT NULL DEFAULT 'capcut_manual_plan',
    provider_notes TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS video_drafts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'generated',
    file_path TEXT NOT NULL,
    file_name TEXT NOT NULL,
    mime_type TEXT NOT NULL DEFAULT 'video/mp4',
    draft_mode TEXT NOT NULL DEFAULT 'scene_card_silent_mp4',
    duration_seconds INTEGER NOT NULL DEFAULT 60,
    scene_count INTEGER NOT NULL DEFAULT 0,
    has_audio INTEGER NOT NULL DEFAULT 0,
    provider_notes TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS visual_assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    tags TEXT NOT NULL DEFAULT '',
    description TEXT DEFAULT '',
    file_path TEXT NOT NULL,
    file_name TEXT NOT NULL,
    mime_type TEXT NOT NULL DEFAULT 'application/octet-stream',
    source_type TEXT NOT NULL DEFAULT 'self_created',
    license_type TEXT DEFAULT '',
    notes TEXT DEFAULT '',
    reuse_count INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS thumbnail_guides (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'generated',
    file_path TEXT NOT NULL,
    file_name TEXT NOT NULL,
    mime_type TEXT NOT NULL DEFAULT 'text/markdown',
    thumbnail_mode TEXT NOT NULL DEFAULT 'manual_canva_capcut_guide',
    text_ideas TEXT NOT NULL DEFAULT '[]',
    layout_guide TEXT NOT NULL DEFAULT '',
    canva_prompt TEXT NOT NULL DEFAULT '',
    provider_notes TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS source_safety_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'needs_human_review',
    risk_level TEXT NOT NULL DEFAULT 'medium',
    similarity_score REAL NOT NULL DEFAULT 0,
    sequence_similarity REAL NOT NULL DEFAULT 0,
    keyword_overlap REAL NOT NULL DEFAULT 0,
    approval_required INTEGER NOT NULL DEFAULT 1,
    copied_text_used INTEGER NOT NULL DEFAULT 0,
    checklist_json TEXT NOT NULL DEFAULT '[]',
    recommendation TEXT NOT NULL DEFAULT '',
    review_markdown TEXT NOT NULL DEFAULT '',
    file_path TEXT NOT NULL,
    file_name TEXT NOT NULL,
    mime_type TEXT NOT NULL DEFAULT 'text/markdown',
    reviewer_decision TEXT NOT NULL DEFAULT 'pending',
    reviewer_notes TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS teacher_trust_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'generated',
    factual_accuracy_score INTEGER NOT NULL DEFAULT 80,
    age_appropriateness_score INTEGER NOT NULL DEFAULT 80,
    simplicity_score INTEGER NOT NULL DEFAULT 80,
    visual_clarity_score INTEGER NOT NULL DEFAULT 80,
    engagement_score INTEGER NOT NULL DEFAULT 80,
    source_safety_score INTEGER NOT NULL DEFAULT 80,
    reviewer_confidence_score INTEGER NOT NULL DEFAULT 80,
    overall_trust_score INTEGER NOT NULL DEFAULT 80,
    approval_required INTEGER NOT NULL DEFAULT 1,
    checklist_json TEXT NOT NULL DEFAULT '[]',
    recommendation TEXT NOT NULL DEFAULT '',
    reviewer_decision TEXT NOT NULL DEFAULT 'pending',
    reviewer_notes TEXT DEFAULT '',
    file_path TEXT NOT NULL,
    file_name TEXT NOT NULL,
    mime_type TEXT NOT NULL DEFAULT 'text/markdown',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS learning_outputs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'generated',
    output_mode TEXT NOT NULL DEFAULT 'notes_quiz_flashcards_worksheet',
    revision_notes_markdown TEXT NOT NULL DEFAULT '',
    flashcards_json TEXT NOT NULL DEFAULT '[]',
    quiz_json TEXT NOT NULL DEFAULT '[]',
    worksheet_markdown TEXT NOT NULL DEFAULT '',
    file_path TEXT NOT NULL,
    file_name TEXT NOT NULL,
    mime_type TEXT NOT NULL DEFAULT 'text/markdown',
    provider_notes TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS prompt_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    task_type TEXT NOT NULL DEFAULT 'script',
    style_key TEXT NOT NULL DEFAULT '',
    template_text TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1,
    notes TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_provider_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id INTEGER,
    provider TEXT NOT NULL DEFAULT 'template',
    available INTEGER NOT NULL DEFAULT 0,
    success INTEGER NOT NULL DEFAULT 0,
    message TEXT DEFAULT '',
    duration_ms INTEGER NOT NULL DEFAULT 0,
    attempt_order INTEGER NOT NULL DEFAULT 1,
    generation_mode TEXT NOT NULL DEFAULT 'deterministic_template',
    provider_chain TEXT NOT NULL DEFAULT 'template',
    total_generation_duration_ms INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS publishing_approvals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'blocked',
    gate_status TEXT NOT NULL DEFAULT 'blocked',
    required_failures_count INTEGER NOT NULL DEFAULT 0,
    optional_warnings_count INTEGER NOT NULL DEFAULT 0,
    checklist_json TEXT NOT NULL DEFAULT '[]',
    recommendation TEXT NOT NULL DEFAULT '',
    report_markdown TEXT NOT NULL DEFAULT '',
    reviewer_decision TEXT NOT NULL DEFAULT 'pending',
    reviewer_name TEXT DEFAULT '',
    reviewer_notes TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS content_production_cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id INTEGER NOT NULL UNIQUE,
    stage TEXT NOT NULL DEFAULT 'script_review',
    priority TEXT NOT NULL DEFAULT 'normal',
    owner TEXT DEFAULT '',
    due_date TEXT DEFAULT '',
    notes TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE CASCADE
);



CREATE TABLE IF NOT EXISTS content_ideas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    subject TEXT NOT NULL DEFAULT 'Science',
    class_level TEXT NOT NULL DEFAULT 'Class 7',
    target_audience TEXT NOT NULL DEFAULT 'School students',
    language TEXT NOT NULL DEFAULT 'English',
    idea_type TEXT NOT NULL DEFAULT 'curiosity',
    hook_angle TEXT DEFAULT '',
    source_hint TEXT DEFAULT '',
    batch_id INTEGER,
    status TEXT NOT NULL DEFAULT 'backlog',
    notes TEXT DEFAULT '',
    curiosity_score INTEGER NOT NULL DEFAULT 7,
    evergreen_score INTEGER NOT NULL DEFAULT 7,
    visual_potential_score INTEGER NOT NULL DEFAULT 7,
    student_value_score INTEGER NOT NULL DEFAULT 7,
    production_effort_score INTEGER NOT NULL DEFAULT 4,
    monetization_potential_score INTEGER NOT NULL DEFAULT 5,
    total_score REAL NOT NULL DEFAULT 70,
    priority TEXT NOT NULL DEFAULT 'medium',
    recommendation TEXT DEFAULT '',
    score_breakdown_json TEXT NOT NULL DEFAULT '{}',
    converted_package_id INTEGER,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(batch_id) REFERENCES content_batches(id) ON DELETE SET NULL,
    FOREIGN KEY(converted_package_id) REFERENCES content_packages(id) ON DELETE SET NULL
);



CREATE TABLE IF NOT EXISTS content_series (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    niche TEXT NOT NULL DEFAULT 'Class 6-8 Science curiosity Shorts',
    target_audience TEXT NOT NULL DEFAULT 'School students and curious learners',
    subject TEXT NOT NULL DEFAULT 'Science',
    class_level TEXT NOT NULL DEFAULT 'Class 7',
    language TEXT NOT NULL DEFAULT 'English',
    series_goal TEXT DEFAULT '',
    status TEXT NOT NULL DEFAULT 'planning',
    planned_count INTEGER NOT NULL DEFAULT 10,
    episode_style TEXT DEFAULT '',
    cta_strategy TEXT DEFAULT '',
    notes TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS content_series_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    series_id INTEGER NOT NULL,
    idea_id INTEGER,
    package_id INTEGER,
    order_index INTEGER NOT NULL DEFAULT 1,
    episode_title TEXT NOT NULL DEFAULT '',
    hook_angle TEXT DEFAULT '',
    target_status TEXT NOT NULL DEFAULT 'planned',
    notes TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(series_id) REFERENCES content_series(id) ON DELETE CASCADE,
    FOREIGN KEY(idea_id) REFERENCES content_ideas(id) ON DELETE SET NULL,
    FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS batch_handoff_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id INTEGER,
    handoff_name TEXT NOT NULL DEFAULT 'Production Handoff',
    ready_only INTEGER NOT NULL DEFAULT 1,
    package_count INTEGER NOT NULL DEFAULT 0,
    skipped_count INTEGER NOT NULL DEFAULT 0,
    file_path TEXT NOT NULL DEFAULT '',
    file_name TEXT NOT NULL DEFAULT '',
    manifest_json TEXT NOT NULL DEFAULT '{}',
    created_by TEXT DEFAULT '',
    notes TEXT DEFAULT '',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(batch_id) REFERENCES content_batches(id) ON DELETE SET NULL
);


CREATE TABLE IF NOT EXISTS multilingual_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_id INTEGER,
    source_language TEXT NOT NULL DEFAULT 'English',
    target_language TEXT NOT NULL DEFAULT 'Hindi',
    status TEXT NOT NULL DEFAULT 'planning',
    priority TEXT NOT NULL DEFAULT 'medium',
    translation_goal TEXT DEFAULT '',
    cultural_notes TEXT DEFAULT '',
    glossary_terms TEXT DEFAULT '',
    voice_strategy TEXT NOT NULL DEFAULT 'manual_voice',
    subtitle_strategy TEXT NOT NULL DEFAULT 'manual_review',
    reviewer_name TEXT DEFAULT '',
    notes TEXT DEFAULT '',
    needs_human_translation_review INTEGER NOT NULL DEFAULT 1,
    readiness_score INTEGER NOT NULL DEFAULT 0,
    recommendation TEXT DEFAULT '',
    checklist_json TEXT NOT NULL DEFAULT '[]',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE SET NULL
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
    settings.audio_dir.mkdir(parents=True, exist_ok=True)
    settings.video_draft_dir.mkdir(parents=True, exist_ok=True)
    settings.asset_library_dir.mkdir(parents=True, exist_ok=True)
    settings.thumbnail_dir.mkdir(parents=True, exist_ok=True)
    settings.source_safety_dir.mkdir(parents=True, exist_ok=True)
    settings.trust_review_dir.mkdir(parents=True, exist_ok=True)
    settings.learning_output_dir.mkdir(parents=True, exist_ok=True)
    settings.handoff_dir.mkdir(parents=True, exist_ok=True)
    settings.youtube_oauth_dir.mkdir(parents=True, exist_ok=True)


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


def _add_column_if_missing(conn: sqlite3.Connection, table: str, column: str, alter_sql: str) -> None:
    columns = {row[1] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}
    if column not in columns:
        conn.execute(alter_sql)


def _apply_lightweight_migrations(conn: sqlite3.Connection) -> None:
    """Add missing tables/columns for users who already created an MVP database."""

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS user_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'content_admin',
            active INTEGER NOT NULL DEFAULT 1,
            last_login_at TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS auth_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT NOT NULL UNIQUE,
            expires_at TEXT NOT NULL,
            revoked_at TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES user_accounts(id) ON DELETE CASCADE
        )
        """
    )
    from app.services.auth_service import bootstrap_default_admin
    bootstrap_default_admin(conn)

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS content_batches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            niche TEXT NOT NULL DEFAULT '',
            target_audience TEXT NOT NULL DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            planned_count INTEGER NOT NULL DEFAULT 20,
            status TEXT NOT NULL DEFAULT 'planning',
            notes TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS publishing_calendar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            package_id INTEGER NOT NULL UNIQUE,
            planned_publish_date TEXT NOT NULL,
            actual_publish_date TEXT DEFAULT '',
            platform TEXT NOT NULL DEFAULT 'YouTube Shorts',
            status TEXT NOT NULL DEFAULT 'planned',
            playlist_name TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE CASCADE
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS calendar_bulk_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_id INTEGER,
            start_date TEXT NOT NULL,
            limit_count INTEGER NOT NULL DEFAULT 20,
            videos_per_day INTEGER NOT NULL DEFAULT 1,
            days_between INTEGER NOT NULL DEFAULT 0,
            platform TEXT NOT NULL DEFAULT 'YouTube Shorts',
            playlist_name TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'planned',
            order_by TEXT NOT NULL DEFAULT 'created_at',
            created_by TEXT DEFAULT '',
            scheduled_count INTEGER NOT NULL DEFAULT 0,
            skipped_count INTEGER NOT NULL DEFAULT 0,
            run_json TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(batch_id) REFERENCES content_batches(id) ON DELETE SET NULL
        )
        """
    )


    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS audio_assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            package_id INTEGER NOT NULL,
            provider_used TEXT NOT NULL DEFAULT 'manual_recording',
            status TEXT NOT NULL DEFAULT 'manual_required',
            file_path TEXT NOT NULL,
            file_name TEXT NOT NULL,
            mime_type TEXT NOT NULL DEFAULT 'text/plain',
            voice_id TEXT DEFAULT '',
            duration_seconds REAL DEFAULT 0,
            script_snapshot TEXT NOT NULL,
            provider_notes TEXT DEFAULT '',
            provider_attempts TEXT DEFAULT '[]',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE CASCADE
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS assembly_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            package_id INTEGER NOT NULL,
            plan_markdown TEXT NOT NULL,
            plan_json TEXT NOT NULL,
            scene_count INTEGER NOT NULL DEFAULT 0,
            estimated_duration_seconds INTEGER NOT NULL DEFAULT 60,
            assembly_mode TEXT NOT NULL DEFAULT 'capcut_manual_plan',
            provider_notes TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE CASCADE
        )
        """
    )



    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS video_drafts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            package_id INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'generated',
            file_path TEXT NOT NULL,
            file_name TEXT NOT NULL,
            mime_type TEXT NOT NULL DEFAULT 'video/mp4',
            draft_mode TEXT NOT NULL DEFAULT 'scene_card_silent_mp4',
            duration_seconds INTEGER NOT NULL DEFAULT 60,
            scene_count INTEGER NOT NULL DEFAULT 0,
            has_audio INTEGER NOT NULL DEFAULT 0,
            provider_notes TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE CASCADE
        )
        """
    )


    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS visual_assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            tags TEXT NOT NULL DEFAULT '',
            description TEXT DEFAULT '',
            file_path TEXT NOT NULL,
            file_name TEXT NOT NULL,
            mime_type TEXT NOT NULL DEFAULT 'application/octet-stream',
            source_type TEXT NOT NULL DEFAULT 'self_created',
            license_type TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            reuse_count INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS thumbnail_guides (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            package_id INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'generated',
            file_path TEXT NOT NULL,
            file_name TEXT NOT NULL,
            mime_type TEXT NOT NULL DEFAULT 'text/markdown',
            thumbnail_mode TEXT NOT NULL DEFAULT 'manual_canva_capcut_guide',
            text_ideas TEXT NOT NULL DEFAULT '[]',
            layout_guide TEXT NOT NULL DEFAULT '',
            canva_prompt TEXT NOT NULL DEFAULT '',
            provider_notes TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE CASCADE
        )
        """
    )


    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS source_safety_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            package_id INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'needs_human_review',
            risk_level TEXT NOT NULL DEFAULT 'medium',
            similarity_score REAL NOT NULL DEFAULT 0,
            sequence_similarity REAL NOT NULL DEFAULT 0,
            keyword_overlap REAL NOT NULL DEFAULT 0,
            approval_required INTEGER NOT NULL DEFAULT 1,
            copied_text_used INTEGER NOT NULL DEFAULT 0,
            checklist_json TEXT NOT NULL DEFAULT '[]',
            recommendation TEXT NOT NULL DEFAULT '',
            review_markdown TEXT NOT NULL DEFAULT '',
            file_path TEXT NOT NULL,
            file_name TEXT NOT NULL,
            mime_type TEXT NOT NULL DEFAULT 'text/markdown',
            reviewer_decision TEXT NOT NULL DEFAULT 'pending',
            reviewer_notes TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE CASCADE
        )
        """
    )



    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS teacher_trust_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            package_id INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'generated',
            factual_accuracy_score INTEGER NOT NULL DEFAULT 80,
            age_appropriateness_score INTEGER NOT NULL DEFAULT 80,
            simplicity_score INTEGER NOT NULL DEFAULT 80,
            visual_clarity_score INTEGER NOT NULL DEFAULT 80,
            engagement_score INTEGER NOT NULL DEFAULT 80,
            source_safety_score INTEGER NOT NULL DEFAULT 80,
            reviewer_confidence_score INTEGER NOT NULL DEFAULT 80,
            overall_trust_score INTEGER NOT NULL DEFAULT 80,
            approval_required INTEGER NOT NULL DEFAULT 1,
            checklist_json TEXT NOT NULL DEFAULT '[]',
            recommendation TEXT NOT NULL DEFAULT '',
            reviewer_decision TEXT NOT NULL DEFAULT 'pending',
            reviewer_notes TEXT DEFAULT '',
            file_path TEXT NOT NULL,
            file_name TEXT NOT NULL,
            mime_type TEXT NOT NULL DEFAULT 'text/markdown',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE CASCADE
        )
        """
    )


    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS learning_outputs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            package_id INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'generated',
            output_mode TEXT NOT NULL DEFAULT 'notes_quiz_flashcards_worksheet',
            revision_notes_markdown TEXT NOT NULL DEFAULT '',
            flashcards_json TEXT NOT NULL DEFAULT '[]',
            quiz_json TEXT NOT NULL DEFAULT '[]',
            worksheet_markdown TEXT NOT NULL DEFAULT '',
            file_path TEXT NOT NULL,
            file_name TEXT NOT NULL,
            mime_type TEXT NOT NULL DEFAULT 'text/markdown',
            provider_notes TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE CASCADE
        )
        """
    )



    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS ai_provider_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            package_id INTEGER,
            provider TEXT NOT NULL DEFAULT 'template',
            available INTEGER NOT NULL DEFAULT 0,
            success INTEGER NOT NULL DEFAULT 0,
            message TEXT DEFAULT '',
            duration_ms INTEGER NOT NULL DEFAULT 0,
            attempt_order INTEGER NOT NULL DEFAULT 1,
            generation_mode TEXT NOT NULL DEFAULT 'deterministic_template',
            provider_chain TEXT NOT NULL DEFAULT 'template',
            total_generation_duration_ms INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE CASCADE
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS publishing_approvals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            package_id INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'blocked',
            gate_status TEXT NOT NULL DEFAULT 'blocked',
            required_failures_count INTEGER NOT NULL DEFAULT 0,
            optional_warnings_count INTEGER NOT NULL DEFAULT 0,
            checklist_json TEXT NOT NULL DEFAULT '[]',
            recommendation TEXT NOT NULL DEFAULT '',
            report_markdown TEXT NOT NULL DEFAULT '',
            reviewer_decision TEXT NOT NULL DEFAULT 'pending',
            reviewer_name TEXT DEFAULT '',
            reviewer_notes TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE CASCADE
        )
        """
    )


    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS content_production_cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            package_id INTEGER NOT NULL UNIQUE,
            stage TEXT NOT NULL DEFAULT 'script_review',
            priority TEXT NOT NULL DEFAULT 'normal',
            owner TEXT DEFAULT '',
            due_date TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE CASCADE
        )
        """
    )





    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS batch_handoff_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_id INTEGER,
            handoff_name TEXT NOT NULL DEFAULT 'Production Handoff',
            ready_only INTEGER NOT NULL DEFAULT 1,
            package_count INTEGER NOT NULL DEFAULT 0,
            skipped_count INTEGER NOT NULL DEFAULT 0,
            file_path TEXT NOT NULL DEFAULT '',
            file_name TEXT NOT NULL DEFAULT '',
            manifest_json TEXT NOT NULL DEFAULT '{}',
            created_by TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(batch_id) REFERENCES content_batches(id) ON DELETE SET NULL
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS content_ideas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject TEXT NOT NULL DEFAULT 'Science',
            class_level TEXT NOT NULL DEFAULT 'Class 7',
            target_audience TEXT NOT NULL DEFAULT 'School students',
            language TEXT NOT NULL DEFAULT 'English',
            idea_type TEXT NOT NULL DEFAULT 'curiosity',
            hook_angle TEXT DEFAULT '',
            source_hint TEXT DEFAULT '',
            batch_id INTEGER,
            status TEXT NOT NULL DEFAULT 'backlog',
            notes TEXT DEFAULT '',
            curiosity_score INTEGER NOT NULL DEFAULT 7,
            evergreen_score INTEGER NOT NULL DEFAULT 7,
            visual_potential_score INTEGER NOT NULL DEFAULT 7,
            student_value_score INTEGER NOT NULL DEFAULT 7,
            production_effort_score INTEGER NOT NULL DEFAULT 4,
            monetization_potential_score INTEGER NOT NULL DEFAULT 5,
            total_score REAL NOT NULL DEFAULT 70,
            priority TEXT NOT NULL DEFAULT 'medium',
            recommendation TEXT DEFAULT '',
            score_breakdown_json TEXT NOT NULL DEFAULT '{}',
            converted_package_id INTEGER,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(batch_id) REFERENCES content_batches(id) ON DELETE SET NULL,
            FOREIGN KEY(converted_package_id) REFERENCES content_packages(id) ON DELETE SET NULL
        )
        """
    )



    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS content_series (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            niche TEXT NOT NULL DEFAULT 'Class 6-8 Science curiosity Shorts',
            target_audience TEXT NOT NULL DEFAULT 'School students and curious learners',
            subject TEXT NOT NULL DEFAULT 'Science',
            class_level TEXT NOT NULL DEFAULT 'Class 7',
            language TEXT NOT NULL DEFAULT 'English',
            series_goal TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'planning',
            planned_count INTEGER NOT NULL DEFAULT 10,
            episode_style TEXT DEFAULT '',
            cta_strategy TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS content_series_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            series_id INTEGER NOT NULL,
            idea_id INTEGER,
            package_id INTEGER,
            order_index INTEGER NOT NULL DEFAULT 1,
            episode_title TEXT NOT NULL DEFAULT '',
            hook_angle TEXT DEFAULT '',
            target_status TEXT NOT NULL DEFAULT 'planned',
            notes TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(series_id) REFERENCES content_series(id) ON DELETE CASCADE,
            FOREIGN KEY(idea_id) REFERENCES content_ideas(id) ON DELETE SET NULL,
            FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE SET NULL
        )
        """
    )



    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS multilingual_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            package_id INTEGER,
            source_language TEXT NOT NULL DEFAULT 'English',
            target_language TEXT NOT NULL DEFAULT 'Hindi',
            status TEXT NOT NULL DEFAULT 'planning',
            priority TEXT NOT NULL DEFAULT 'medium',
            translation_goal TEXT DEFAULT '',
            cultural_notes TEXT DEFAULT '',
            glossary_terms TEXT DEFAULT '',
            voice_strategy TEXT NOT NULL DEFAULT 'manual_voice',
            subtitle_strategy TEXT NOT NULL DEFAULT 'manual_review',
            reviewer_name TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            needs_human_translation_review INTEGER NOT NULL DEFAULT 1,
            readiness_score INTEGER NOT NULL DEFAULT 0,
            recommendation TEXT DEFAULT '',
            checklist_json TEXT NOT NULL DEFAULT '[]',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(package_id) REFERENCES content_packages(id) ON DELETE SET NULL
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS prompt_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            task_type TEXT NOT NULL DEFAULT 'script',
            style_key TEXT NOT NULL DEFAULT '',
            template_text TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 1,
            notes TEXT DEFAULT '',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    from app.services.prompt_template_service import seed_default_prompt_templates
    seed_default_prompt_templates(conn)

    additions = {
        "batch_id": "ALTER TABLE content_packages ADD COLUMN batch_id INTEGER REFERENCES content_batches(id) ON DELETE SET NULL",
        "provider_used": "ALTER TABLE content_packages ADD COLUMN provider_used TEXT NOT NULL DEFAULT 'template'",
        "generation_mode": "ALTER TABLE content_packages ADD COLUMN generation_mode TEXT NOT NULL DEFAULT 'deterministic_template'",
        "provider_chain": "ALTER TABLE content_packages ADD COLUMN provider_chain TEXT NOT NULL DEFAULT 'template'",
        "provider_notes": "ALTER TABLE content_packages ADD COLUMN provider_notes TEXT DEFAULT ''",
        "provider_attempts": "ALTER TABLE content_packages ADD COLUMN provider_attempts TEXT DEFAULT '[]'",
        "generation_duration_ms": "ALTER TABLE content_packages ADD COLUMN generation_duration_ms INTEGER NOT NULL DEFAULT 0",
        "prompt_template_id": "ALTER TABLE content_packages ADD COLUMN prompt_template_id INTEGER",
        "prompt_template_name": "ALTER TABLE content_packages ADD COLUMN prompt_template_name TEXT DEFAULT ''",
        "prompt_template_style": "ALTER TABLE content_packages ADD COLUMN prompt_template_style TEXT DEFAULT ''",
        "prompt_template_snapshot": "ALTER TABLE content_packages ADD COLUMN prompt_template_snapshot TEXT DEFAULT ''",
    }
    for column, sql in additions.items():
        _add_column_if_missing(conn, "content_packages", column, sql)

