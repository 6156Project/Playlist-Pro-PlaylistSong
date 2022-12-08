from flask import Flask, Response, request
from datetime import datetime
import json
import rest_utils
from playlists_resource import PlaylistResource
from playlist_song_resource import PlaylistSongResource
from flask_cors import CORS

# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

CORS(app)


@app.get("/api/health")
def get_health():
    t = str(datetime.now())
    msg = {
        "name": "PlaylistSong Microservice",
        "health": "Good",
        "at time": t
    }

    # DFF TODO Explain status codes, content type, ... ...
    result = Response(json.dumps(msg), status=200, content_type="application/json")

    return result

@app.route("/api/playlists", methods=["OPTIONS"])
def getPlaylistOptions():

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps('Hello from Lambda!')
    }


@app.route("/api/playlists", methods=["GET"])
def getPlaylists():

    result = PlaylistResource.getPlaylists()

    if result:
        rsp = Response(json.dumps(result), status=200, content_type="application.json")
    else:
        rsp = Response("NOT FOUND", status=404, content_type="text/plain")

    return rsp


@app.route("/api/playlists", methods=["POST"])
def addPlaylist():
    request_inputs = rest_utils.RESTContext(request)

    data = request_inputs.data
    res = PlaylistResource.addPlaylist(data)

    rsp = Response("CREATED Playlist " + str(res), status=201, content_type="text/plain")

    return rsp

@app.route("/api/playlists/<playlistId>", methods=["GET"])
def getPlaylist(playlistId):
    res = PlaylistResource.getPlaylist(playlistId)

    rsp = Response(json.dumps(res), status=200, content_type="text/plain")

    return rsp

@app.route("/api/playlists/<id>", methods=["PUT"])
def updatePlaylist(id):
    request_inputs = rest_utils.RESTContext(request)

    res = PlaylistResource.updatePlaylist(id, new_values=request_inputs.data)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

    return rsp

@app.route("/api/playlists/<id>", methods=["DELETE"])
def deletePlaylist(id):
    request_inputs = rest_utils.RESTContext(request)

    res = PlaylistResource.deletePlaylist(id)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")

    return rsp

@app.route("/api/playlists/<playlistId>/song", methods=["POST"])
def addPlaylistSong(playlistId):
    request_inputs = rest_utils.RESTContext(request)

    data = request_inputs.data
    res = PlaylistSongResource.addPlaylistSong(data, playlistId)

    rsp = Response("CREATED PlaylistSong " + str(res), status=201, content_type="text/plain")

    return rsp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011)

