from resources.base_resource import BaseResource
import requests


class PlaylistSongsResource(BaseResource):

    def __init__(self, config):
        super().__init__(config)
        self.data_service = None
        self.columns = ['playlist_id', 'song_id']

    def get_full_collection_name(self):
        return self.config.collection_name

    def get_data_service(self):
        if self.data_service is None:
            self.data_service = self.config.data_service
        return self.data_service

    def get_resource_by_id(self, id):
        final_rsp = {'status': '', 'text':'', 'body':{}, 'links':[]}
        template = {'playlist_id': id}
        response = self.get_by_template(template=template)
        final_rsp['status'] = response['status']
        final_rsp['text'] = response['text']

        if final_rsp['status'] == 200:
            # get playlist info
            playlist_info_rsp = requests.get(
                f'{self.config.api_gateway}/api/playlists/{id}'
            )
            playlist_info_rsp = playlist_info_rsp.json()
            # get songs info
            songs_arr = []
            for s in response['body']:
                song_info_rsp = requests.get(
                    f'{self.config.api_gateway}/api/songs/{s["song_id"]}'
                )
                song_info_rsp = song_info_rsp.json()
                songs_arr.append(song_info_rsp['body'][0])



            final_rsp['body'] = {
                'playlist': {
                    'id': id,
                    'name': playlist_info_rsp['body'][0]['name']
                },
                'songs': songs_arr
                }
            
            final_rsp['links'] = [
                    {
                        "href": f"api/playlists/{id}/songs",
                        "rel": "self",
                        "type" : "PUT"
                    },{
                        "href": f"api/playlists/{id}/songs",
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
        response = {'status': '', 'text':'', 'body':{}, 'links':[]}
        if not resource_data:
            response['status'] = 400
            response['text'] = 'Empty data'
        elif not all(columns in resource_data for columns in self.columns):
            response['status'] = 400
            response['text'] = 'Missing data required'
        else:
            values = {
                'playlist_id': resource_data['playlist_id'],
                'song_id': resource_data['song_id']
            }
            rsp = super().create_resource(values)
            if rsp['status'] == 201:
                response['status'] = rsp['status']
                response['text'] = 'Resource created.' 
                response['body'] = {}
                response['links'] = [
                    {
                        "href": f"api/playlists/{values['playlist_id']}/songs",
                        "rel": "self",
                        "type" : "GET"
                    },{
                        "href": f"api/playlists/{values['playlist_id']}/songs",
                        "rel": "self",
                        "type" : "DELETE"
                    },{
                         "href": f"api/playlists/{id}",
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
        template = {'playlist_id': resource_data['playlist_id'], 'song_id': resource_data['song_id']}
        rsp = super().delete_resource(template)
        response['status'] = rsp['status']
        response['text'] = rsp['text']
        if rsp['status'] == 201:
            response['links'] = [
                {
                    "href": f"api/playlists/{resource_data['playlist_id']}/songs",
                    "rel": "self",
                    "type" : "GET"
                },{
                    "href": f"api/playlists/{resource_data['playlist_id']}/songs",
                    "rel": "self",
                    "type" : "POST"
                },{
                         "href": f"api/playlists/{id}",
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


