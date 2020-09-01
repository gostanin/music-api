from uuid import uuid4

from flask import Blueprint, request, jsonify

from music.utils import read_binary_stream
from music.model.model_factory import get_model_songs

songs = Blueprint('songs', __name__)


# play a song
@songs.route('/', methods=['GET'], strict_slashes=False)
def get_song():
    data = request.get_json()

    if not data:
        return jsonify(message='Songs data is missing'), 400

    uuid = data.get('id')
    from_bytes = data.get('from')
    to_bytes = data.get('to')

    if not uuid:
        return jsonify(message='Songs body is missing [uuid]'), 400
    if not isinstance(uuid, str):
        return jsonify(message='Songs [id] must be type string'), 400
    if len(uuid) != 36:
        return jsonify(message='Songs [id] length must 36 characters'), 400

    if not from_bytes:
        return jsonify(message='Songs body is missing [from]'), 400
    if not isinstance(from_bytes, int):
        return jsonify(message='Songs [from] must be type integer'), 400
    if from_bytes < 0:
        return jsonify(message='Songs [from] length must positive integer'), 400

    if not to_bytes:
        return jsonify(message='Songs body is missing [to]'), 400
    if not isinstance(to_bytes, int):
        return jsonify(message='Songs [to] must be type integer'), 400
    if to_bytes < 0:
        return jsonify(message='Songs [to] length must positive integer'), 400

    if from_bytes > to_bytes:
        return jsonify(message='Songs [from] must be strictly less than [to] value'), 400

    res = None
    try:
        path = get_model_songs().get_path(uuid)
        res = read_binary_stream(from_bytes, to_bytes, path)
    except Exception:
        return jsonify(message='Unexpected error occured while retriving songs path'), 500

    return jsonify(song=res), 206


@songs.route('/', methods=['POST'], strict_slashes=False)
def create_song():
    data = request.get_json()

    if not data:
        return jsonify(message='Songs data is missing'), 400

    uuid = uuid4()
    name = data.get('name')
    genre = data.get('genre')
    artist = data.get('artist')
    length = data.get('length')
    song_path = data.get('path')
    ranking = data.get('ranking')

    if not name:
        return jsonify(message='Songs body is missing [name]'), 400
    if not isinstance(name, str):
        return jsonify(message='Songs [name] must be type string'), 400
    if len(name) > 255:
        return jsonify(message='Songs [name] length must be between [0-255]'), 400

    if not genre:
        return jsonify(message='Songs body is missing [genre]'), 400
    if not isinstance(genre, str):
        return jsonify(message='Songs [genre] must be type string'), 400
    if genre.lower() not in ['rock', 'pop', 'rap', 'r&b']:
        return jsonify(message='Songs [genre] must be ["Rock", "Pop", "Rap", "R&B"]'), 400

    if not artist:
        return jsonify(message='Songs body is missing [artist]'), 400
    if not isinstance(artist, str):
        return jsonify(message='Songs [artist] must be type string'), 400
    if len(artist) > 255:
        return jsonify(message='Songs [artist] length must be between [0-255]'), 400

    if not isinstance(length, int):
        return jsonify(message='Songs [length] must be type integer'), 400
    if length < 0:
        return jsonify(message='Songs [length] must be type positive number in seconds'), 400

    if not song_path:
        return jsonify(message='Songs body is missing [path]'), 400
    if not isinstance(song_path, str):
        return jsonify(message='Songs [path] must be type string'), 400
    if len(song_path) > 2056:
        return jsonify(message='Songs [path] length must be between [0-2056]'), 400

    if not isinstance(ranking, int):
        return jsonify(message='Songs [ranking] must be type integer'), 400
    if ranking < 0 or ranking > 5:
        return jsonify(message='Songs [ranking] must be type between [0-5]'), 400

    res = None
    try:
        res = get_model_songs().create_song(
            uuid, name, genre, artist, length, song_path, ranking)
    except Exception:
        return jsonify(message='Unexpected error occured while saving song'), 500

    if res == 1:
        return jsonify(message='Song cannot be created'), 400

    return '', 204


@songs.route('/', methods=['DELETE'], strict_slashes=False)
def delete_song():
    data = request.get_json()

    if not data:
        return jsonify(message='Songs data is missing'), 400

    uuid = data.get('id')

    if not isinstance(uuid, str):
        return jsonify(message='Songs [id] must be type string'), 400
    if len(uuid) != 36:
        return jsonify(message='Songs [id] length must 36 characters'), 400

    res = None
    try:
        res = get_model_songs().delete_song(uuid)
    except Exception:
        return jsonify(message='Unexpected error occured while saving song'), 500

    if res == 1:
        return jsonify(message='Song cannot be deleted. ID is not found'), 400

    return '', 204


@songs.route('/name', methods=['UPDATE'], strict_slashes=False)
def update_name():
    data = request.get_json()

    if not data:
        return jsonify(message='Songs data is missing'), 400

    uuid = data.get('id')
    name = data.get('name')

    if not name:
        return jsonify(message='Songs body is missing [name]'), 400
    if not isinstance(name, str):
        return jsonify(message='Songs [name] must be type string'), 400
    if len(name) > 255:
        return jsonify(message='Songs [name] length must be between [0-255]'), 400

    if not uuid:
        return jsonify(message='Songs body is missing [id]'), 400
    if not isinstance(uuid, str):
        return jsonify(message='Songs [id] must be type string'), 400
    if len(uuid) != 36:
        return jsonify(message='Songs [id] length must 36 characters'), 400

    res = None
    try:
        res = get_model_songs().update_name(uuid, name)
    except Exception:
        return jsonify(message='Unexpected error occured while updating song'), 500

    if res == 1:
        return jsonify(message='Song cannot be updated. ID is not found'), 400

    return '', 204


@songs.route('/genre', methods=['UPDATE'], strict_slashes=False)
def update_genre():
    data = request.get_json()

    if not data:
        return jsonify(message='Songs data is missing'), 400

    uuid = data.get('id')
    genre = data.get('genre')

    if not isinstance(genre, str):
        return jsonify(message='Songs [genre] must be type string'), 400
    if genre.lower() not in ['rock', 'pop', 'rap', 'r&b']:
        return jsonify(message='Songs [genre] must be ["Rock", "Pop", "Rap", "R&B"]'), 400

    if not uuid:
        return jsonify(message='Songs body is missing [id]'), 400
    if not isinstance(uuid, str):
        return jsonify(message='Songs [id] must be type string'), 400
    if len(uuid) != 36:
        return jsonify(message='Songs [id] length must 36 characters'), 400

    res = None
    try:
        res = get_model_songs().update_genre(uuid, genre)
    except Exception:
        return jsonify(message='Unexpected error occured while updating song'), 500

    if res == 1:
        return jsonify(message='Song cannot be updated. ID is not found'), 400

    return '', 204


@songs.route('/artist', methods=['UPDATE'], strict_slashes=False)
def update_artist():
    data = request.get_json()

    if not data:
        return jsonify(message='Songs data is missing'), 400

    uuid = data.get('id')
    artist = data.get('artist')

    if not isinstance(artist, str):
        return jsonify(message='Songs [artist] must be type string'), 400
    if len(artist) > 255:
        return jsonify(message='Songs [artist] length must be between [0-255]'), 400

    if not uuid:
        return jsonify(message='Songs body is missing [id]'), 400
    if not isinstance(uuid, str):
        return jsonify(message='Songs [id] must be type string'), 400
    if len(uuid) != 36:
        return jsonify(message='Songs [id] length must 36 characters'), 400

    res = None
    try:
        res = get_model_songs().update_artist(uuid, artist)
    except Exception:
        return jsonify(message='Unexpected error occured while updating song'), 500

    if res == 1:
        return jsonify(message='Song cannot be updated. ID is not found'), 400

    return '', 204


@songs.route('/length', methods=['UPDATE'], strict_slashes=False)
def update_length():
    data = request.get_json()

    if not data:
        return jsonify(message='Songs data is missing'), 400

    uuid = data.get('id')
    length = data.get('length')

    if not isinstance(length, int):
        return jsonify(message='Songs [length] must be type integer'), 400
    if length < 0:
        return jsonify(message='Songs [length] must be type positive number in seconds'), 400

    if not uuid:
        return jsonify(message='Songs body is missing [id]'), 400
    if not isinstance(uuid, str):
        return jsonify(message='Songs [id] must be type string'), 400
    if len(uuid) != 36:
        return jsonify(message='Songs [id] length must 36 characters'), 400

    res = None
    try:
        res = get_model_songs().update_length(uuid, length)
    except Exception:
        return jsonify(message='Unexpected error occured while updating song'), 500

    if res == 1:
        return jsonify(message='Song cannot be updated. ID is not found'), 400

    return '', 204


@songs.route('/path', methods=['UPDATE'], strict_slashes=False)
def update_song_path():
    data = request.get_json()

    if not data:
        return jsonify(message='Songs data is missing'), 400

    uuid = data.get('id')
    song_path = data.get('path')

    if not isinstance(song_path, str):
        return jsonify(message='Songs [path] must be type string'), 400
    if len(song_path) > 2056:
        return jsonify(message='Songs [path] length must be between [0-2056]'), 400

    if not uuid:
        return jsonify(message='Songs body is missing [id]'), 400
    if not isinstance(uuid, str):
        return jsonify(message='Songs [id] must be type string'), 400
    if len(uuid) != 36:
        return jsonify(message='Songs [id] length must 36 characters'), 400

    res = None
    try:
        res = get_model_songs().update_path(uuid, song_path)
    except Exception:
        return jsonify(message='Unexpected error occured while updating song'), 500

    if res == 1:
        return jsonify(message='Song cannot be updated. ID is not found'), 400

    return '', 204


@songs.route('/ranking', methods=['UPDATE'], strict_slashes=False)
def update_ranking():
    data = request.get_json()

    if not data:
        return jsonify(message='Songs data is missing'), 400

    uuid = data.get('id')
    ranking = data.get('ranking')

    if not isinstance(ranking, int):
        return jsonify(message='Songs [ranking] must be type integer'), 400
    if ranking < 0 or ranking > 5:
        return jsonify(message='Songs [ranking] must be type between [0-5]'), 400

    if not uuid:
        return jsonify(message='Songs body is missing [id]'), 400
    if not isinstance(uuid, str):
        return jsonify(message='Songs [id] must be type string'), 400
    if len(uuid) != 36:
        return jsonify(message='Songs [id] length must 36 characters'), 400

    res = None
    try:
        res = get_model_songs().update_ranking(uuid, ranking)
    except Exception:
        return jsonify(message='Unexpected error occured while updating song'), 500

    if res == 1:
        return jsonify(message='Song cannot be updated. ID is not found'), 400

    return '', 204
