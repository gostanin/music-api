
import json

import pytest

from unittest.mock import patch


@pytest.fixture
def dummy_request_body():
    return {
            'name': 'What is Love',
            'genre': 'Pop',
            'artist': 'Haddaway',
            'length': 215,
            'path': '/amazing/songs/haddaway',
            'ranking': 5}

@patch('music.controllers.songs.read_binary_stream')
@patch('music.controllers.songs.get_model_songs')
def test_get_song_206(get_model_songs, read_binary_stream, get_test_app):
    with get_test_app as app:
        song_binary = 'part of a song'
        path = '/path'
        read_binary_stream.return_value = song_binary
        get_model_songs().get_path.return_value = path

        request_body = {
            'id': '123456789012345678901234567890123456', 'from': 30, 'to': 55}
        res = app.get('/api/v1/songs', json=request_body)
        data = json.loads(res.data)
        assert res.status_code == 206
        assert data['song'] == song_binary

        read_binary_stream.assert_called_once_with(request_body['from'], request_body['to'], path)
        get_model_songs().get_path.assert_called_once_with(request_body['id'])


@pytest.mark.parametrize('request_body',
                         [
                             None,
                             {'id': '12345678901234567890123456789012345', 'from': 30, 'to': 55},
                             {'id': None, 'from': 30, 'to': 55},
                             {'id': '12345678901234567890123456789012345', 'from': 30, 'to': 20},
                             {'id': '123456789012345678901234567890123456', 'from': 30, 'to': ''},
                             {'id': '123456789012345678901234567890123456', 'from': 30},
                             {'id': '123456789012345678901234567890123456', 'from': '', 'to': 55}
                         ])
def test_get_song_400(get_test_app, request_body):
    with get_test_app as app:
        res = app.get('/api/v1/songs', json=request_body)
        data = json.loads(res.data)
        assert res.status_code == 400
        assert data['message']


@patch('music.controllers.songs.read_binary_stream')
@patch('music.controllers.songs.get_model_songs')
def test_get_song_read_binary_500(get_model_songs, read_binary_stream, get_test_app):
    with get_test_app as app:
        path = '/path'
        get_model_songs().get_path.return_value = path
        read_binary_stream.side_effect = Exception()

        request_body = {
            'id': '123456789012345678901234567890123456', 'from': 30, 'to': 55}
        res = app.get('/api/v1/songs', json=request_body)
        data = json.loads(res.data)
        assert res.status_code == 500
        assert data['message']

        read_binary_stream.assert_called_once_with(request_body['from'], request_body['to'], path)
        get_model_songs().get_path.assert_called_once_with(request_body['id'])


@patch('music.controllers.songs.uuid4')
@patch('music.controllers.songs.get_model_songs')
def test_create_song_204(get_model_songs, uuid4, get_test_app, dummy_request_body):
    with get_test_app as app:
        uuid = '123456'
        uuid4.return_value = uuid
        get_model_songs().create_song.return_value = 0

        res = app.post('/api/v1/songs', json=dummy_request_body)
        assert res.status_code == 204

        get_model_songs().create_song.assert_called_once_with(uuid,
                                                              dummy_request_body['name'],
                                                              dummy_request_body['genre'],
                                                              dummy_request_body['artist'],
                                                              dummy_request_body['length'],
                                                              dummy_request_body['path'],
                                                              dummy_request_body['ranking'],
                                                              )


@pytest.mark.parametrize('request_body',
                         [
                            None,
                            {
                                'name': 'What is Love', 
                                'genre': 'Pop', 
                                'artist': 'Haddaway',
                                'length': 215,
                                'path': '/amazing/songs/haddaway',
                                'ranking': -1
                            },
                            {
                                'name': 'What is Love', 
                                'genre': 'Pop', 
                                'artist': 'Haddaway',
                                'length': 215,
                                'path': '/amazing/songs/haddaway',
                                'ranking': 6
                            },
                            {
                                'genre': 'Pop', 
                                'artist': 'Haddaway',
                                'length': 215,
                                'path': '/amazing/songs/haddaway',
                                'ranking': 5
                            },
                            {
                                'name': 'What is Love', 
                                'artist': 'Haddaway',
                                'length': 215,
                                'path': '/amazing/songs/haddaway',
                                'ranking': 5
                            },
                            {
                                'name': 'What is Love', 
                                'genre': 'jazz', 
                                'artist': 'Haddaway',
                                'length': 215,
                                'path': '/amazing/songs/haddaway',
                                'ranking': 5
                            },
                            {
                                'name': 'What is Love', 
                                'genre': 'Pop', 
                                'length': 215,
                                'path': '/amazing/songs/haddaway',
                                'ranking': 5
                            },
                            {
                                'name': 'What is Love', 
                                'genre': 'Pop', 
                                'artist': 'Haddaway',
                                'path': '/amazing/songs/haddaway',
                                'ranking': 5
                            },
                            {
                                'name': 'What is Love', 
                                'genre': 'Pop', 
                                'artist': 'Haddaway',
                                'length': 215,
                                'ranking': 5
                            }
                         ])
def test_create_song_400(get_test_app, request_body):
    with get_test_app as app:
        res = app.post('/api/v1/songs', json=request_body)
        data = json.loads(res.data)
        assert res.status_code == 400
        assert data['message']


@patch('music.controllers.songs.get_model_songs')
def test_create_song_500(get_model_songs, get_test_app, dummy_request_body):
    with get_test_app as app:
        get_model_songs().create_song.side_effect = Exception()

        res = app.post('/api/v1/songs', json=dummy_request_body)
        data = json.loads(res.data)
        assert res.status_code == 500
        assert data['message']
