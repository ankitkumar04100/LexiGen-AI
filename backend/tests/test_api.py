# backend/tests/test_api.py
import os
import tempfile
import pytest
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    client = flask_app.test_client()
    yield client

def test_index(client):
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"LexiGen AI Backend Running" in rv.data

def test_upload_and_summary(client, tmp_path):
    # create a temp txt file
    p = tmp_path / "sample.txt"
    p.write_text("This is a sample legal text. Clause one. Clause two.")
    with open(p, "rb") as fh:
        data = {"file": (fh, "sample.txt")}
        rv = client.post("/api/v1/upload", data=data, content_type='multipart/form-data')
        assert rv.status_code == 200
        j = rv.get_json()
        doc_id = j.get("doc_id")
        assert doc_id is not None

        # get summary
        rv2 = client.get(f"/api/v1/summary/{doc_id}")
        assert rv2.status_code == 200
        j2 = rv2.get_json()
        assert "Summary" in j2.get("summary")
