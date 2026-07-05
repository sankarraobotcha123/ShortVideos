import json

from app.core.config import settings
from app.services.learning_output_service import generate_learning_output


def test_generate_learning_output_contains_reusable_materials(tmp_path):
    settings.learning_output_dir = tmp_path / "learning_outputs"
    package = {
        "id": 1,
        "topic": "Why are leaves green?",
        "class_level": "Class 7",
        "subject": "Science",
        "hook": "Did you ever wonder why leaves are green?",
        "source_notes": "Leaves contain chlorophyll. Chlorophyll reflects green light.",
        "script_text": "Leaves look green because chlorophyll reflects green light. Think of it like a color mirror.",
        "title_options": json.dumps(["Why Leaves Are Green Explained"]),
        "quiz_question": "Quiz: Why do leaves look green?",
    }
    output = generate_learning_output(package)
    assert output["status"] == "generated"
    assert "Revision Notes" in output["revision_notes_markdown"]
    assert len(json.loads(output["flashcards_json"])) >= 3
    assert len(json.loads(output["quiz_json"])) == 5
    assert "Worksheet" in output["worksheet_markdown"]
