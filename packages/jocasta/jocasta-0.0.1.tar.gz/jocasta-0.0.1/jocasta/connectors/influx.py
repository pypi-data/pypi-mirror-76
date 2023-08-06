from influxdb import InfluxDBClient
import json
from datetime import datetime
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger(__name__)


class InfluxDBConnector(object):
    def __init__(self, database, password, username, host=None, port=None):

        self.database = database

        if not host:
            self.host = 'localhost'

        if not port:
            self.port = 8086

        self.influx_client = InfluxDBClient(
            self.host, self.port, username, password, self.database
        )

    def send(self, data):

        if not data:
            f = open('/tmp/zeep_latest_reading.json', 'r')
            data = f.read()
            data = json.loads(data)
            f.close()

        json_payload = []
        time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        try:
            for name, value in data.iteritems():
                payload = {
                    'measurement': name,
                    'tags': {'host': 'jarvis', 'location': 'office'},
                    'time': time,
                    'fields': {'value': value},
                }
                json_payload.append(payload)
            self.influx_client.write_points(json_payload)
        except Exception as exception:
            logger.error(f'Failed to write to Influx. Error {exception.message}')
