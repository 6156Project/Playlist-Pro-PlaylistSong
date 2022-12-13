import os
from resources.rds_data_service import RDSDataService
from resources.playlist_song_resource import PlaylistSongsResource

# DATABASE CONFIGS
class RDSDataServiceConfig:
    def __init__(self, db_user, db_pw, db_host, db_port):
        self.db_user = db_user
        self.db_pw = db_pw
        self.db_host = db_host
        self.db_port = db_port


# RESOURCES CONFIGS
class PlaylistSongsResourceConfig:
    def __init__(self, 
            data_service, 
            collection_name, 
            api_gateway,
            songs_table,
            access_table,
            playlist_table):
        self.data_service = data_service
        self.collection_name = collection_name
        self.api_gateway = api_gateway
        self.songs_table = songs_table
        self.access_table = access_table
        self.playlist_table = playlist_table



class ServiceFactory:
    def __init__(self):
        self.rds_svc_config = RDSDataServiceConfig(
            os.environ.get("RDS_USERNAME"),
            os.environ.get("RDS_PASSWORD"),
            os.environ.get("RDS_HOSTNAME"),
            os.environ.get("RDS_PORT")
        )
        self.rds_service = RDSDataService(self.rds_svc_config)
        # connect playlist songs resource to mongo
        self.playlistsongs_service_config = PlaylistSongsResourceConfig(
            self.rds_service,
            os.environ.get("RDS_TABLE_PLAYLISTSONGS"),
            os.environ.get("API_GATEWAY"),
            os.environ.get("RDS_TABLE_SONGS"),
            os.environ.get("RDS_TABLE_PLAYLISTACCESS"),
            os.environ.get("RDS_TABLE_PLAYLISTS"))
        self.playlistsongs_resource = PlaylistSongsResource(self.playlistsongs_service_config)

    def get(self, resource_name, default):
        if resource_name == "playlistsongs":
            result = self.playlistsongs_resource
        else:
            result = default
        return result
