from util.webshared import Message, Error, JSONResponse, secure
from bottle import request, response
from util.validation import validate_mac
from data.db_models import Device

from sqlalchemy.orm.exc import NoResultFound


class DevicesJSON(JSONResponse):
    """
    Object to generate JSON for multiple devices
    """

    def __init__(self, devices):
        """
        A list of JSON devices
        """
        self.devices = devices

    def from_db(db_devices):
        """
        Convert a database device to a JSON device

        :param db_devices: A list of database devices
        :returns: A DevicesJSON of JSON devices
        """
        return DevicesJSON([DeviceJSON.from_db(d) for d in db_devices])


class DeviceJSON(JSONResponse):
    """
    An object to generate JSON for a single device
    """
    def __init__(self, mac):
        """
        :param mac: The MAC address of the device
        """
        self.mac = mac

    def from_db(db_device):
        """
        Convert a database device to a JSON device
        :param db_device: The database device to convert
        :returns: The device info in a JSON object
        """
        return DeviceJSON(db_device.mac)


@secure()
def add_new_device(db):
    """
    A resource to change/add a device to a user. Currently, each user may only
    have one device.  Adding a new device when one already exists will overwrite
    the old device.

    JSON body must contain:
     {
        "mac": <string>, // MAC Address eg. "ab:cd:ef:12:34:56:78:90"
     }

    :param db: The database session
    :returns: Error JSON on fail or device JSON on success.
    """
    # Get User info from request environment
    user = request.environ.get('user_info')
    if user is None:
        raise RuntimeError("add_new_device should always have user_info")

    # Access and validate the JSON body
    try:
        data = request.json
        if data is None:
            raise ValueError

        if 'mac' not in data or not validate_mac(data['mac']):
            raise ValueError

        mac_address = data['mac']
    except ValueError:
        response.status = 400
        return Error("Missing JSON with valid mac").json

    try:
        # Try to update the MAC of the device already associated with the user
        device = db.query(Device).filter(Device.user_id == user.id).one()
        if mac_address != device.mac:
            count = db.query(Device).filter(Device.mac == mac_address).count()
            if count != 0:
                # MAC already exists
                response.status = 400
                return Error(
                    "Device with MAC '%s' already exists" % mac_address).json
        device.mac = mac_address
    except NoResultFound:
        # Fall back to creating a new device
        count = db.query(Device).filter(Device.mac == mac_address).count()
        if count != 0:
            # MAC already exists
            response.status = 400
            return Error(
                "Device with MAC '%s' already exists" % mac_address).json
        device = Device(user_id=user.id, mac=mac_address)
        db.add(device)
    db.commit()
    return DeviceJSON.from_db(device).json


@secure()
def get_devices(db):
    """
    A resource for getting a list of devices associated with a user (max 1).

    :param db: The database session
    :returns: JSON containing info related to devices associated to current user
    """
    user = request.environ.get('user_info')
    if user is None:
        raise RuntimeError("get_devices should always have user_info")
    devices = db.query(Device).filter(Device.user_id == user.id).all()
    return DevicesJSON.from_db(devices).json
