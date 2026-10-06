import pytest
from unittest.mock import MagicMock, patch

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def mock_connection():
    conn = MagicMock()
    cursor = MagicMock()
    conn.cursor.return_value = cursor
    return conn, cursor


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    data = response.get_json()

    assert data["status"] == "ok"


@patch("app.get_conn")
def test_get_notes(mock_get_conn, client):
    conn, cursor = mock_connection()

    cursor.fetchall.return_value = [
        (1, "Nota 1", "Contenido 1", "2026-01-01"),
        (2, "Nota 2", "Contenido 2", "2026-01-02"),
    ]

    mock_get_conn.return_value = conn

    response = client.get("/api/notes")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data) == 2
    assert data[0]["title"] == "Nota 1"
    assert data[1]["title"] == "Nota 2"


@patch("app.get_conn")
def test_create_note(mock_get_conn, client):
    conn, cursor = mock_connection()

    mock_get_conn.return_value = conn

    response = client.post(
        "/api/notes",
        json={
            "title": "Nueva nota",
            "content": "Contenido de prueba",
        },
    )

    assert response.status_code in (200, 201)

    cursor.execute.assert_called()


def test_create_note_sin_titulo(client):
    response = client.post(
        "/api/notes",
        json={
            "content": "Contenido sin título",
        },
    )

    assert response.status_code == 400


@patch("app.get_conn")
def test_delete_note(mock_get_conn, client):
    conn, cursor = mock_connection()

    mock_get_conn.return_value = conn

    response = client.delete("/api/notes/1")

    assert response.status_code in (200, 204)

    cursor.execute.assert_called()
