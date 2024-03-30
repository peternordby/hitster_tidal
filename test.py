
import json
from datetime import datetime

import tidalapi


# Just a couple helper functions...
def datetime_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError('Type not serializable')

def json_stringify(obj, fullfile):
    """
        @param obj: The object to stringify.
        @param fullfile: The full path to the file to write the JSON to.

        This function takes in an object and returns a JSON string representation of it.
    """
    # Write the dictionary to a JSON file
    with open(fullfile, 'w') as f:
        json.dump(obj, f, default=datetime_serializer)

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

# Get your first session manually like this
session = tidalapi.Session()
session.login_oauth_simple()

# Save your token to a json file
token = {
    'token_type': session.token_type,
    'access_token': session.access_token,
    'refresh_token': session.refresh_token,
    'expiry_time': session.expiry_time
}
json_stringify(token, 'token.json')

# Loading your token from json file
mytoken = json_parse('token.json')

# Init a session with your token
session = tidalapi.Session()
session.load_oauth_session(mytoken['token_type'], mytoken['access_token'], mytoken['refresh_token'], mytoken['expiry_time'])