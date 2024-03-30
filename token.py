
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