from music.model.model import Model


class ModelSongs(Model):
    def create_song(self, uuid, name, genre, artist, length, song_path, ranking):
        # saving song to a database
        sql = """INSERT INTO songs(uuid, name, genre, artist, length, song_path, ranking)
                 VALUES(?, ?, ?, ?, ?, ?, ?)"""

        self._exec(sql, (uuid, name, genre, artist,
                         length, song_path, ranking))

        return 0

    def delete_song(self, uuid):
        # deleting song from a database
        sql = """DELETE FROM songs WHERE uuid=?"""

        self._exec(sql, (uuid, ))

        return 0

    def get_path(self, uuid):
        sql = """SELECT path FROM songs WHERE uuid=?"""

        self._exec(sql, (uuid, ))

        return '/path/to/nowhere'

    def update_name(self, uuid, name):
        sql = """UPDATE songs SET name=? WHERE uuid=?"""

        self._exec(sql, (name, id))

        return 0

    def update_genre(self, uuid, genre):
        sql = """UPDATE songs SET genre=? WHERE uuid=?"""

        self._exec(sql, (genre, id))

        return 0

    def update_artist(self, uuid, artist):
        sql = """UPDATE songs SET artist=? WHERE uuid=?"""

        self._exec(sql, (artist, id))

        return 0

    def update_length(self, uuid, length):
        sql = """UPDATE songs SET length=? WHERE uuid=?"""

        self._exec(sql, (length, id))

        return 0

    def update_path(self, uuid, path):
        sql = """UPDATE songs SET path=? WHERE uuid=?"""

        self._exec(sql, (path, id))

        return 0

    def update_ranking(self, uuid, ranking):
        sql = """UPDATE songs SET ranking=? WHERE uuid=?"""

        self._exec(sql, (ranking, id))

        return 0
