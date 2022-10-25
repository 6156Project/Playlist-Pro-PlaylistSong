import pymysql
import os


class PlaylistResource:

    # def __int__(self):
    #     self.schema = os.environ.get("DBSCHEMA")
    #     self.table = "Playlist"

    # # @staticmethod
    # def _get_connection():

    #     usr = os.environ.get("DBUSER")
    #     pw = os.environ.get("DBPW")
    #     h = os.environ.get("DBHOST")
    #     port = os.environ.get("DBPORT")

    #     conn = pymysql.connect(
    #         user=usr,
    #         password=pw,
    #         host=h,
    #         port=port,
    #         cursorclass=pymysql.cursors.DictCursor,
    #         autocommit=True
    #     )
    #     return conn

    # # @staticmethod
    # def getPlaylists(self):

    #     sql = f"SELECT * FROM {self.schema}.Playlists"
    #     conn = PlaylistResource._get_connection()
    #     cur = conn.cursor()
    #     res = cur.execute(sql)
    #     result = cur.fetchall()

    #     return result

    def getPlaylist(id):
        sql = "select * FROM PlaylistSong.Playlists JOIN PlaylistSong.PlaylistSong ON PlaylistSong.Playlists.id = PlaylistSong.PlaylistSong.playlistId where PlaylistSong.Playlists.id=%s;"
        conn = PlaylistResource._get_connection()
        cursor = conn.cursor()
        res = cursor.execute(sql, (id))

        if res >= 1:
            result = cursor.fetchall()
        else:
            result = None

        return result

        pass


    # @staticmethod
    # def addPlaylist(new_resource):

    #     column_string = []
    #     i = 1
    #     for key, val in new_resource.items():
    #         if i < len(new_resource):
    #             column_string.append(key + ",")
    #             i += 1
    #         else:
    #             column_string.append(key)
    #     column_string = " ".join(column_string)

    #     value_string = []
    #     i = 1
    #     for key, val in new_resource.items():
    #         if i < len(new_resource):
    #             value_string.append(val)
    #             i += 1
    #         else:
    #             value_string.append(val)
    #     value_string = tuple(value_string)
    #     #value_string = " ".join(value_string)


    #     sql = "INSERT INTO PlaylistSong.Playlists " + " (" + column_string + ") VALUES %s;"
    #     conn = PlaylistResource._get_connection()
    #     cursor = conn.cursor()
    #     res = cursor.execute(sql, (value_string,))

    #     conn.commit()

    #     return new_resource["id"]

    #     pass

    @staticmethod
    def updatePlaylist(id, new_values):

        column_string = []
        i = 1
        for key, val in new_values.items():
            if i < len(new_values):
                column_string.append(key + "=" + '"' + str(val) + '"' + ",")
                i += 1
            else:
                column_string.append(key + "=" + '"' + str(val) + '"')
        column_string = " ".join(column_string)
        sql = "UPDATE PlaylistSong.Playlists" + " SET " + column_string + " where id=%s"
        conn = PlaylistResource._get_connection()
        cursor = conn.cursor()
        try:
            res = cursor.execute(sql, (id))
            conn.commit()
            return 1
        except:
            return 0
        pass

    @staticmethod
    def deletePlaylist(id):

        sql = "DELETE FROM PlaylistSong.Playlists WHERE id=%s"
        conn = PlaylistResource._get_connection()
        cursor = conn.cursor()

        try:
            res = cursor.execute(sql, (id))
            conn.commit()
            return 1
        except:
            return 0

        pass
