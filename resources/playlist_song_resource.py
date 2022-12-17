from resources.base_resource import BaseResource
import requests


class PlaylistSongsResource(BaseResource):

    def __init__(self, config):
        super().__init__(config)
        self.data_service = None

    def get_full_collection_name(self):
        return self.config.collection_name

    def get_data_service(self):
        if self.data_service is None:
            self.data_service = self.config.data_service
        return self.data_service

    def get_resource_by_id(self, id, req_inputs):
        final_rsp = {'status': '', 'text':'', 'body':{}, 'links':[]}
        template = {'playlist_id': id}
        response = self.get_by_template(template=template, limit=req_inputs.limit, offset=req_inputs.offset)
        final_rsp['status'] = response['status']
        final_rsp['text'] = response['text']


        if final_rsp['status'] == 200:
            # get playlist info
            playlist_info_rsp = requests.get(
                f'{self.config.api_gateway}/api/playlists/{id}'
            )
            playlist_info_rsp = playlist_info_rsp.json()

            final_rsp['body'] = {
                    'playlist': {
                        'id': id,
                        'name': playlist_info_rsp['body'][0]['name']
                    },
                    'songs': []
                }

            # get songs info
            songs_arr = []
            for s in response['body']:
                song_info_rsp = requests.get(
                    f'{self.config.api_gateway}/api/songs/{s["song_id"]}'
                )
                song_info_rsp = song_info_rsp.json()
                songs_arr.append(song_info_rsp['body'][0])
            
            final_rsp['body']['songs'] = songs_arr
            final_rsp['links'] = [
                    {
                        "href": f"api/playlistsongs/{id}",
                        "rel": "self",
                        "type" : "PUT"
                    },{
                        "href": f"api/playlistsongs/{id}",
                        "rel": "self",
                        "type" : "DELETE"
                    },{
                         "href": f"api/playlists/{id}",
                        "rel": "playlists",
                        "type" : "GET"
                    }
                ]

        return final_rsp

    def get_by_template(self,
                        relative_path=None,
                        path_parameters=None,
                        template=None,
                        field_list=None,
                        limit=None,
                        offset=None,
                        order_by=None):
        response = {'status': '', 'text':'', 'body':{}, 'links':[]}
        rsp = super().get_by_template(relative_path, path_parameters, template, field_list,
                                         limit, offset, order_by)
        if rsp:
            response['status'] = 200
            response['text'] = 'OK'
            response['body'] = rsp
        else:
            response['status'] = 404
            response['text'] = 'Resource not found.'
        return response

    def create_resource(self, resource_data):
        data_columns = [
            'playlist_id', 
            'song_id',
            'song_name',
            'artist_id',
            'artist_name',
            'album_id',
            'album_name']
        response = {'status': '', 'text':'', 'body':{}, 'links':[]}
        # check data integrity
        if not resource_data:
            response['status'] = 400
            response['text'] = 'Empty data'
        elif not all(columns in resource_data for columns in data_columns):
            response['status'] = 400
            response['text'] = 'Missing data required'
        else:
            # filter body to required fields
            values = {
                'playlist_id': resource_data['playlist_id'],
                'song_id': resource_data['song_id'],
                'song_name': resource_data['song_name'],
                'artist_id': resource_data['artist_id'],
                'artist_name': resource_data['artist_name'],
                'album_id': resource_data['album_id'],
                'album_name': resource_data['album_name']
            }
            # check if playlist exists
            playlist_rsp = requests.get(
                f'{self.config.api_gateway}/api/playlists/{values["playlist_id"]}'
            )
            playlist_rsp = playlist_rsp.json()
            if playlist_rsp['status'] != 200:
                return {
                    'status': 404,
                    'text': 'Playlist not found.'
                }

            # check if songs exist
            song_rsp = requests.get(
                f'{self.config.api_gateway}/api/songs/{values["song_id"]}'
            )
            song_rsp = song_rsp.json()
            # if song not found, post
            if song_rsp['status'] == 404:
                song_post_rsp = requests.post(
                    f'{self.config.api_gateway}/api/songs',
                    json=values
            )
            
            rsp = super().create_resource({
                    'playlist_id': values['playlist_id'],
                    'song_id': values['song_id']
                }
            )
            if rsp['status'] == 201:
                response['status'] = rsp['status']
                response['text'] = 'Resource created.' 
                response['body'] = {}
                response['links'] = [
                    {
                        "href": f"api/playlistsongs/{values['playlist_id']}",
                        "rel": "self",
                        "type" : "GET"
                    },{
                        "href": f"api/playlistsongs/{values['playlist_id']}",
                        "rel": "self",
                        "type" : "DELETE"
                    },{
                         "href": f"api/playlists/{values['playlist_id']}",
                        "rel": "playlists",
                        "type" : "GET"
                    }
                    ]
            else:
                response['status'] = rsp['status']
                response['text'] = rsp['text']
        return response

    def delete_resource(self, resource_data):
        response = {'status': '', 'text':'', 'body':{}, 'links':[]}
        data_columns = [
            'playlist_id', 
            'song_id'
            ]
        # check data integrity
        if not resource_data:
            response['status'] = 400
            response['text'] = 'Empty data'
        elif not all(columns in resource_data for columns in data_columns):
            response['status'] = 400
            response['text'] = 'Missing data required'
        template = {'playlist_id': resource_data['playlist_id'], 'song_id': resource_data['song_id']}
        rsp = super().delete_resource(template)
        response['status'] = rsp['status']
        response['text'] = rsp['text']
        if rsp['status'] == 201:
            response['links'] = [
                {
                    "href": f"api/playlistsongs/{resource_data['playlist_id']}",
                    "rel": "self",
                    "type" : "GET"
                },{
                    "href": f"api/playlistsongs/{resource_data['playlist_id']}",
                    "rel": "self",
                    "type" : "POST"
                },{
                   "href": f"api/playlists/{resource_data['playlist_id']}",
                    "rel": "playlists",
                    "type" : "GET"
                    }
                ]
        return response

    def update_resource(self, resource_data):
        pass
        
    def loadPlaylistsByUser():
        # TODO @ZACH
        pass


