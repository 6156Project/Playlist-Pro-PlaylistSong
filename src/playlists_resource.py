import pymysql

import os


class PlaylistResource:

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
    def getPlaylists():

        sql = "SELECT * FROM PlaylistSong.Playlists"
        conn = PlaylistResource._get_connection()
        cur = conn.cursor()
        res = cur.execute(sql)
        result = cur.fetchall()

        return result


    @staticmethod
    def addPlaylist(new_resource):

        column_string = []
        i = 1
        for key, val in new_resource.items():
            if i < len(new_resource):
                column_string.append(key + ",")
                i += 1
            else:
                column_string.append(key)
        column_string = " ".join(column_string)

        value_string = []
        i = 1
        for key, val in new_resource.items():
            if i < len(new_resource):
                value_string.append(val)
                i += 1
            else:
                value_string.append(val)
        value_string = tuple(value_string)
        #value_string = " ".join(value_string)


        sql = "INSERT INTO PlaylistSong.Playlists " + " (" + column_string + ") VALUES %s;"
        conn = PlaylistResource._get_connection()
        cursor = conn.cursor()
        res = cursor.execute(sql, (value_string,))

        conn.commit()

        return new_resource["id"]

        pass

