

def add_new_device():
    # Needs user token
    # Needs {'mac': 'mac_value'} in body
    # Store as [user_id, mac_value] in database
    # - DELETE FROM devices WHERE userid = token.userid
    # - INSERT INTO devices VALUE (token.userid, mac_value)
    return "Device associated with your account. Forgot the others"

def get_devices():
    # Needs user token
    # SELECT * FROM devices WHERE userid = token.userid
    return []
