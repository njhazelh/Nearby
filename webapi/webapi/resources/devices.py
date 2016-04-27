from util.webshared import Message, Error, JSONResponse, secure
from bottle import request, response
from util.validation import validate_mac
from data.db_models import Device

from sqlalchemy.orm.exc import NoResultFound


class Devices(JSONResponse):

    def __init__(self, devices):
        self.devices = devices

    @property
    def json(self):
        return {
            "devices": [d.json for d in self.devices]
        }


class DeviceJSON(JSONResponse):

    def __init__(self, mac):
        self.mac = mac


@secure()
def add_new_device(db):
    user = request.environ.get('user_info')
    if user is None:
        raise RuntimeError("add_new_device should always have user_info")

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
        device = db.query(Device).filter(Device.user_id == user.id).one()
        if mac_address != device.mac:
            count = db.query(Device).filter(Device.mac == mac_address).count()
            if count != 0:
                response.status = 400
                return Error("Device with MAC '%s' already exists" % mac_address).json
        device.mac = mac_address
    except NoResultFound:
        count = db.query(Device).filter(Device.mac == mac_address).count()
        if count != 0:
            response.status = 400
            return Error("Device with MAC '%s' already exists" % mac_address).json
        device = Device(user_id=user.id, mac=mac_address)
        db.add(device)
    db.commit()
    return DeviceJSON(device.mac).json


@secure()
def get_devices(db):
    user = request.environ.get('user_info')
    if user is None:
        raise RuntimeError("get_devices should always have user_info")
    devices = db.query(Device).filter(Device.user_id == user.id).all()
    devices = [DeviceJSON(d.mac) for d in devices]
    return Devices(devices).json
