import pytest
from fastapi.testclient import TestClient

from app.api.main import create_app
from app.config import Settings

PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 20


@pytest.fixture()
def client(tmp_path):
    s = Settings()
    s.database_url = f"sqlite:///{tmp_path}/t.db"
    s.upload_dir = str(tmp_path / "up")
    s.ocr_engine = "mock"  # mock trả "x = 4"
    return TestClient(create_app(s))


def auth(client, name="alice"):
    client.post("/auth/register", json={"username": name, "password": "secret123"})
    t = client.post("/auth/login", json={"username": name, "password": "secret123"}).json()["access_token"]
    return {"Authorization": f"Bearer {t}"}


def test_protected_requires_token(client):
    assert client.get("/submissions").status_code == 401
    assert client.post("/assignments", json={}).status_code == 401
    assert client.get("/assignments").status_code == 200  # công khai


def test_full_flow(client):
    h = auth(client)
    a = client.post("/assignments", headers=h, json={"title": "t", "question": "2x+4=12",
                                                     "correct_answer": "4"}).json()
    r = client.post("/submissions", headers=h, data={"assignment_id": a["id"]},
                    files={"file": ("a.png", PNG, "image/png")})
    assert r.status_code == 201 and r.json()["is_correct"] is True and r.json()["score"] == 10
    sid = r.json()["id"]
    assert client.get(f"/submissions/{sid}", headers=h).status_code == 200
    assert client.delete(f"/submissions/{sid}", headers=h).status_code == 204
    assert client.get(f"/submissions/{sid}", headers=h).status_code == 404


def test_wrong_answer_and_equivalence(client):
    h = auth(client)
    a = client.post("/assignments", headers=h, json={"title": "t", "question": "q",
                                                     "correct_answer": "5"}).json()
    r = client.post("/submissions", headers=h, data={"assignment_id": a["id"]},
                    files={"file": ("a.png", PNG, "image/png")}).json()
    assert r["is_correct"] is False
    from app.infrastructure.sympy_grader import SympyAnswerGrader
    g = SympyAnswerGrader()
    assert g.grade("2x+4", "2(x+2)").is_correct
    assert g.grade("1/2", "0.5").is_correct
    assert g.grade("\\frac{1}{2}", "x = 0.5").is_correct
    assert not g.grade("3", "4").is_correct


def test_cannot_read_others_and_bad_file(client):
    h1, h2 = auth(client, "alice"), auth(client, "bob")
    a = client.post("/assignments", headers=h1, json={"title": "t", "question": "q",
                                                      "correct_answer": "4"}).json()
    sid = client.post("/submissions", headers=h1, data={"assignment_id": a["id"]},
                      files={"file": ("a.png", PNG, "image/png")}).json()["id"]
    assert client.get(f"/submissions/{sid}", headers=h2).status_code == 403
    bad = client.post("/submissions", headers=h1, data={"assignment_id": a["id"]},
                      files={"file": ("a.txt", b"hi", "text/plain")})
    assert bad.status_code == 422


def test_login_wrong_password(client):
    auth(client)
    assert client.post("/auth/login", json={"username": "alice", "password": "wrongpass"}).status_code == 401
