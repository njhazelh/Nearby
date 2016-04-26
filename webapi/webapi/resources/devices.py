from util.webshared import Message, JSONResponse, secure

class Devices(JSONResponse):
    def __init__(self, devices):
        self.devices = devices

    @property
    def json(self):
        return {
            "devices": [d.json for d in self.devices]
        }

class Device(JSONResponse):
    def __init__(self, device):
        self.device = device

    @property
    def json(self):
        return self.device


@secure()
def add_new_device():
    # Needs user token
    # Needs {'mac': 'mac_value'} in body
    # Store as [user_id, mac_value] in database
    # - DELETE FROM devices WHERE userid = token.userid
    # - INSERT INTO devices VALUE (token.userid, mac_value)
    return Message("Device associated with your account. Forgot the others").json

@secure()
def get_devices():
    # Needs user token
    # SELECT * FROM devices WHERE userid = token.userid
    return Devices([Device("ab:cd:ef:gh:ij:kl:mn:op")]).json
