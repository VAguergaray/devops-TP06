import json
import os
import sys
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture
def client():
    # Mock de la conexion a Postgres: los tests no necesitan base de datos
    with patch('app.get_conn') as mock_conn:
        cur = MagicMock()
        conn = mock_conn.return_value
        conn.cursor.return_value = cur
        # por si el codigo usa "with conn.cursor() as cur:"
        conn.cursor.return_value.__enter__.return_value = cur
        cur.fetchall.return_value = [
            (1, "Nota test", "Contenido test", "2026-05-13 00:00:00")
        ]
        cur.fetchone.return_value = (1,)
        import app as flask_app
        flask_app.app.config['TESTING'] = True
        with flask_app.app.test_client() as c:
            yield c


def test_health(client):
    r = client.get('/health')
    assert r.status_code == 200
    assert 'status' in json.loads(r.data)


def test_get_notes(client):
    r = client.get('/api/notes')
    assert r.status_code == 200
    assert isinstance(json.loads(r.data), list)


def test_create_note(client):
    r = client.post(
        '/api/notes',
        data=json.dumps({'title': 'Test', 'content': 'Contenido'}),
        content_type='application/json',
    )
    assert r.status_code == 201


def test_create_note_sin_titulo(client):
    r = client.post(
        '/api/notes',
        data=json.dumps({'content': 'Sin titulo'}),
        content_type='application/json',
    )
    assert r.status_code in [400, 500]


def test_delete_note(client):
    r = client.delete('/api/notes/1')
    assert r.status_code in [200, 204]
