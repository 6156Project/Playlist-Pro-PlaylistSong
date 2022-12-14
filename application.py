from flask import Flask, Response, request
from datetime import datetime
import json
import rest_utils
from service_factory import ServiceFactory
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv

# load environment variables fron .env
load_dotenv()

# Create the Flask application object.
application = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

CORS(application)

service_factory = ServiceFactory()


@application.route("/api/playlistsongs/health", methods=["GET"])
def get_health():
    msg = {
        "name": "PlaylistSong Microservice",
        "health": "Good",
        "at time": str(datetime.now())
    }
    rsp = Response(json.dumps(msg), status=200, content_type="application/json")
    return rsp

# get all playlists filtered by user
@application.route("/api/playlistsongs", methods=["GET", "OPTIONS"])
@cross_origin()
def loadPlaylistsByUser():
    request_inputs = rest_utils.RESTContext(request)
    svc = service_factory.get("playlistsongs", None)

    if request_inputs.method == "GET":
        res = svc.loadPlaylistsByUser()
        rsp = Response(json.dumps(res), status=res['status'], content_type="application/json")
    elif request_inputs.method == "OPTIONS":
        rsp = Response("Options", status=200, content_type="application/json")
    else:
        rsp = Response("NOT IMPLEMENTED", status=501, content_type="text/plain")

    return rsp

# add songs to playlists
@application.route("/api/playlistsongs/<id>", methods=["GET", "POST", "DELETE", "OPTIONS"])
@cross_origin()
def addPlaylistSong(id):
    request_inputs = rest_utils.RESTContext(request, id)
    svc = service_factory.get("playlistsongs", None)

    if request_inputs.method == "GET":
        res = svc.get_resource_by_id(id, request_inputs)
        rsp = Response(json.dumps(res), status=res['status'], content_type="application/json")
    elif request_inputs.method == "POST":
        request_inputs.data['playlist_id'] = id
        res = svc.create_resource(resource_data=request_inputs.data)
        rsp = Response(json.dumps(res), status=res['status'], content_type="application/json")
    elif request_inputs.method == "DELETE":
        request_inputs.data['playlist_id'] = id
        res = svc.delete_resource(resource_data=request_inputs.data)
        rsp = Response(json.dumps(res), status=res['status'], content_type="application/json")
    elif request_inputs.method == "OPTIONS":
        rsp = Response("Options", status=200, content_type="application/json")
    else:
        rsp = Response("NOT IMPLEMENTED", status=501, content_type="text/plain")

    return rsp


if __name__ == "__main__":
    application.run(port=5011)

