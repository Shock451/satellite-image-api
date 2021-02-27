import io
import requests
from urllib import parse
import json

# flask
from flask import Flask, send_file, request  # redirect, Response

app = Flask(__name__)

API_KEY = "4_MY_EYES_ONLY"
map_types = ["satellite", "roadmap", "terrain", "hybrid"]


def get_satellite_image(url, lat, lng, key, zoom=15, map_type=0, size="600x300"):
    link = url + "center={},{}&zoom={}&size={}&maptype={}&key={}".format(
        lat, lng, zoom, size, map_types[map_type], key)
    r = requests.get(link)

    return r.content


@app.route('/satellite-image')
def imgsat():

    url = "https://maps.googleapis.com/maps/api/staticmap?"

    latitudes = request.args.get('lat').split(",")

    lat = sum([float(latitude) for latitude in latitudes])/len(latitudes)

    longitudes = request.args.get('lng').split(",")

    lng = sum([float(longitude) for longitude in longitudes])/len(longitudes)

    visible_string = "&visible="
    path_string = "&path=color:0x00000000|weight:5|fillcolor:0xFFFF0033|"
    params = ""

    for i in range(len(latitudes)):
        params = params + "{},{}".format(latitudes[i], longitudes[i]) + ("|" if i is not len(latitudes) - 1 else "")

    url = url + visible_string + params + path_string + params

    zoom = request.args.get('zoom', default=15, type=int)

    map_type = request.args.get('type', default=0, type=int)

    data = get_satellite_image(url, lat, lng, API_KEY, zoom, map_type)

    return send_file(io.BytesIO(data), mimetype='image/png')
