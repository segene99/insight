from fastapi.testclient import TestClient
from fastapi import APIRouter

router = APIRouter()

client = TestClient(router)

def test_get_text_from_image():
    response = client.get("/pic_to_text")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_transcribe():
    response = client.get("/transcribe")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_answer_from_gpt():
    response = client.get("/answer")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_text_to_speech():
    response = client.get("/text-to-speech")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
