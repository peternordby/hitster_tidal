import json
from datetime import datetime

import lxml.html
import requests
import tidalapi
from flask import Flask, make_response, request

app = Flask(__name__)

def json_parse(fullfile):
    """
        @param fullfile: The full path to the file to read the JSON from.
    """
    # Read the JSON file into a dictionary
    with open(fullfile, 'r') as f:
        loaded_dict = json.load(f)

    # Parse datetime strings back to datetime objects
    for key, value in loaded_dict.items():
        if isinstance(value, str):
            try:
                loaded_dict[key] = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')  # ISO format
            except ValueError:
                # if conversion fails, retain the original string
                pass
    return loaded_dict

@app.route('/', methods=['GET', 'OPTIONS'])
def convert():
    link = request.args.get('link')

    if request.method == 'OPTIONS':
        response = make_response("Success", 200)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add('Access-Control-Allow-Methods', '*')
        return response

    # get response from link
    response = requests.get(link)

    # parse response
    tree = lxml.html.fromstring(response.text)

    # get title of page
    title = tree.xpath('//title/text()')[0]
    
    # get artist and song name
    song, artist = title.split(' - song and lyrics by ')
    artist = artist.split(' |')[0]

    print(song)
    print(artist)

    # search for song on tidal
    
    # Loading your token from json file
    mytoken = json_parse('token.json')

    # Init a session with your token
    session = tidalapi.Session()
    session.load_oauth_session(mytoken['token_type'], mytoken['access_token'], mytoken['refresh_token'], mytoken['expiry_time'])

    if mytoken['expiry_time'] < datetime.now():
        response = make_response("Token expired", 401)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add('Access-Control-Allow-Methods', '*')
        return response
    
    # search for song
    tracks = session.search(query=f'{song} {artist}', limit=1, models=[tidalapi.Track])
    track = tracks['top_hit']

    response = make_response(track.get_url(), 200)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    return response