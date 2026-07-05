from __future__ import annotations

import os
from pathlib import Path


def _load_dotenv(path: str = ".env") -> None:
    env_path = Path(path)
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


_load_dotenv()


def _bool_env(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).lower() in {"1", "true", "yes", "on"}


class Settings:
    """Small settings object to avoid extra dependencies in the MVP.

    The app runs without npm, Ollama, Transformers, or a TTS engine. Optional
    providers are enabled only when their environment variables and local tools
    are ready. Template/manual fallbacks keep the workflow moving.
    """

    app_name: str = os.getenv("APP_NAME", "Edu Content Platform MVP")
    database_path: Path = Path(os.getenv("DATABASE_PATH", "storage/app.db"))
    export_dir: Path = Path(os.getenv("EXPORT_DIR", "storage/exports"))
    audio_dir: Path = Path(os.getenv("AUDIO_DIR", "storage/audio"))
    video_draft_dir: Path = Path(os.getenv("VIDEO_DRAFT_DIR", "storage/video_drafts"))
    asset_library_dir: Path = Path(os.getenv("ASSET_LIBRARY_DIR", "storage/asset_library"))
    thumbnail_dir: Path = Path(os.getenv("THUMBNAIL_DIR", "storage/thumbnails"))
    source_safety_dir: Path = Path(os.getenv("SOURCE_SAFETY_DIR", "storage/source_safety"))
    trust_review_dir: Path = Path(os.getenv("TRUST_REVIEW_DIR", "storage/trust_reviews"))
    learning_output_dir: Path = Path(os.getenv("LEARNING_OUTPUT_DIR", "storage/learning_outputs"))
    handoff_dir: Path = Path(os.getenv("HANDOFF_DIR", "storage/handoffs"))

    # AI provider chain. The system tries each provider in order and falls back
    # safely to the built-in template provider.
    ai_provider_chain: list[str] = [
        item.strip().lower()
        for item in os.getenv("AI_PROVIDER_CHAIN", "ollama,transformers,template").split(",")
        if item.strip()
    ]

    use_ollama: bool = _bool_env("USE_OLLAMA", "false")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    ollama_timeout_seconds: int = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "30"))

    use_transformers: bool = _bool_env("USE_TRANSFORMERS", "false")
    transformers_model: str = os.getenv("TRANSFORMERS_MODEL", "distilgpt2")
    transformers_max_new_tokens: int = int(os.getenv("TRANSFORMERS_MAX_NEW_TOKENS", "220"))

    # TTS/audio provider chain. Windows SAPI is useful on Windows laptops without
    # Ollama. pyttsx3 is optional. manual_recording always works and creates a
    # recording guide when no speech engine is ready.
    tts_provider_chain: list[str] = [
        item.strip().lower()
        for item in os.getenv("TTS_PROVIDER_CHAIN", "windows_sapi,pyttsx3,manual_recording").split(",")
        if item.strip()
    ]
    use_windows_sapi: bool = _bool_env("USE_WINDOWS_SAPI_TTS", "true")
    use_pyttsx3: bool = _bool_env("USE_PYTTSX3_TTS", "false")
    tts_voice_id: str = os.getenv("TTS_VOICE_ID", "default")
    tts_rate: int = int(os.getenv("TTS_RATE", "165"))

    frontend_asset_version: str = os.getenv("FRONTEND_ASSET_VERSION", "28")

    # Authentication is a foundation layer for role-based review/publishing workflows.
    # Keep AUTH_REQUIRED=false during local MVP work if you do not want to block older routes yet.
    auth_required: bool = _bool_env("AUTH_REQUIRED", "false")
    auth_token_ttl_hours: int = int(os.getenv("AUTH_TOKEN_TTL_HOURS", "72"))
    auth_cookie_name: str = os.getenv("AUTH_COOKIE_NAME", "edu_content_session")
    auth_cookie_secure: bool = _bool_env("AUTH_COOKIE_SECURE", "false")
    auth_cookie_samesite: str = os.getenv("AUTH_COOKIE_SAMESITE", "lax").lower()
    auth_max_active_sessions_per_user: int = int(os.getenv("AUTH_MAX_ACTIVE_SESSIONS_PER_USER", "8"))
    default_admin_name: str = os.getenv("DEFAULT_ADMIN_NAME", "Local Admin")
    default_admin_email: str = os.getenv("DEFAULT_ADMIN_EMAIL", "admin@example.com")
    default_admin_password: str = os.getenv("DEFAULT_ADMIN_PASSWORD", "ChangeMe123!")

    cors_origins: list[str] = [
        item.strip()
        for item in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000",
        ).split(",")
        if item.strip()
    ]


settings = Settings()
