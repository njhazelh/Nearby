
from util.webshared import Message

def record_observation():
    # Needs user token
    # body: {"timestamp": "2016-04-24", "mac": "mac_value", "rssi": "rssi_value"}
    return Message("I'll remember that for the future.").json
