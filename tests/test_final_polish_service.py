from app.services.final_polish_service import build_final_polish_report


def test_final_polish_report_contains_manual_qa_and_commit_message():
    report = build_final_polish_report()
    assert report["summary"]["commit_message"] == "Add final project audit and test stability tools"
    assert report["commit_message"] == "Add final project audit and test stability tools"
    assert any(item["key"] == "cross_origin_auth_cookies" for item in report["completed_items"])
    assert any(group["area"] == "Login and protected downloads" for group in report["manual_qa_steps"])
    assert "Final MVP Bug-fix and UI Polish Report" in report["report_markdown"]
