from bottle import request, response
from util.webshared import Message, Error, secure
from data.db_models import Observation, Device
from util.validation import validate_mac, validate_timestamp

from sqlalchemy.orm.exc import NoResultFound

@secure()
def record_observation(db):
    user = request.environ.get('user_info')
    if user is None:
        raise RuntimeError("record_observation should always have user_info")

    data = request.json
    if data is None:
        response.status = 400
        return Error("Missing JSON body").json

    if 'timestamp' not in data or not validate_timestamp(data['timestamp']):
        response.status = 400
        return Error("Missing or invalid 'timestamp'").json
    if 'mac' not in data or not validate_mac(data['mac']):
        response.status = 400
        return Error("Missing or invalid 'mac'").json

    timestamp = data.get('timestamp')
    mac = data.get('mac')

    try:
        device = db.query(Device).filter(Device.mac == mac).one()
    except NoResultFound:
        return Message("MAC not recognized").json

    observation = Observation(
        timestamp=timestamp, device_id=device.id, user_id=user.id)
    db.add(observation)
    db.commit()

    return Message("MAC recognized").json
