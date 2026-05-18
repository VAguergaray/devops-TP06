import os
import sys
import json

import pytest

from unittest.mock import patch, MagicMock


sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture
def client():

    with patch('app.get_conn') as mock_conn:

        mock_cursor = MagicMock()

        mock_conn.return_value.cursor.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [
            (1, "Nota test", "Contenido test", "2026-05-13")
        ]

        mock_cursor.fetchone.return_value = (1,)

        import app as flask_app

        flask_app.app.config['TESTING'] = True

        with flask_app.app.test_client() as client:
            yield client


def test_health(client):

    with patch('app.get_conn') as mock_conn:

        mock_conn.return_value

        response = client.get('/health')

        assert response.status_code == 200


def test_get_notes(client):

    response = client.get('/api/notes')

    assert response.status_code == 200

    data = json.loads(response.data)

    assert isinstance(data, list)


def test_create_note(client):

    response = client.post(
        '/api/notes',
        data=json.dumps({
            'title': 'Test',
            'content': 'Contenido'
        }),
        content_type='application/json'
    )

    assert response.status_code == 201


def test_delete_note(client):

    response = client.delete('/api/notes/1')

    assert response.status_code == 200
