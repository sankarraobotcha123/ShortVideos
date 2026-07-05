from app.db.session import db_session, init_db
from app.services.multilingual_planning_service import create_multilingual_plan, list_multilingual_plans, update_multilingual_plan


def test_multilingual_plan_crud(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "app.db"))
    # settings is already imported in app; patch direct path too
    from app.core.config import settings
    settings.database_path = tmp_path / "app.db"
    init_db()
    with db_session() as conn:
        plan = create_multilingual_plan(conn, {
            "source_language": "English",
            "target_language": "Telugu",
            "cultural_notes": "Use Telugu school-level words.",
            "glossary_terms": "chlorophyll = green pigment",
            "reviewer_name": "Reviewer",
        })
        assert plan["target_language"] == "Telugu"
        assert plan["readiness_score"] >= 80
        updated = update_multilingual_plan(conn, plan["id"], {**plan, "status": "ready_for_translation"})
        assert updated["status"] == "ready_for_translation"
        payload = list_multilingual_plans(conn)
        assert payload["summary"]["total"] == 1
