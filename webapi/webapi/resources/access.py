from bottle import request, response
import json

def login():
    try:
        try:
            login_info = request.json
        except RuntimeError as e:
            # log the error once I set up logging
            raise ValueError

        if login_info is None:
            raise ValueError

        # validate data
    except ValueError:
        print("ValueError")
        response.status = 400
        return

    # check if username and password match

    # if match generate new session and return JWT

    return json.dumps(login_info)

def logout():
    return "You are now logged out!"
