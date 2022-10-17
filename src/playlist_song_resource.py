import pymysql

import os


class PlaylistSongResource:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():

        usr = os.environ.get("DBUSER")
        pw = os.environ.get("DBPW")
        h = os.environ.get("DBHOST")

        conn = pymysql.connect(
            user=usr,
            password=pw,
            host=h,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def addPlaylistSong(new_resource, playlistId):

        column_string = []
        column_string.append("playlistId,")
        i = 1
        for key, val in new_resource.items():
            if i < len(new_resource):
                column_string.append(key + ",")
                i += 1
            else:
                column_string.append(key)
        column_string = " ".join(column_string)

        value_string = []
        value_string.append(playlistId)
        i = 1
        for key, val in new_resource.items():
            if i < len(new_resource):
                value_string.append(val)
                i += 1
            else:
                value_string.append(val)
        value_string = tuple(value_string)
        #value_string = " ".join(value_string)


        sql = "INSERT INTO PlaylistSong.PlaylistSong " + " (" + column_string + ") VALUES %s;"
        conn = PlaylistSongResource._get_connection()
        cursor = conn.cursor()
        res = cursor.execute(sql, (value_string,))

        conn.commit()

        return new_resource["songId"]

        pass

