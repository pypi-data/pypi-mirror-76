"""
Generic collector code to run config file
"""
from typing import Dict

from tabulate import tabulate

from jocasta.inputs.serial_connector import SerialSensor

from jocasta.connectors import file_system, influx

# io_adafruit, influx
from jocasta.command_line.setup import setup_config, convert_config_stanza
import click
import logging

from jocasta.validators import validate_temperature

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

logger = logging.getLogger(__name__)


@click.command()
@click.argument('port')
def main(port):
    sensor_reader = SerialSensor(port=port)

    reading = sensor_reader.read()
    logger.debug(f'Reading: {reading}')
    connectors = {}

    config = setup_config()
    for name, section in config.items():
        args = convert_config_stanza(section)
        if name == 'file_system':
            connectors['file_system'] = file_system.FileSystemConnector(**args)
        # elif name == 'adafruit':
        #     connectors['adafruit'] = io_adafruit.IOAdafruitConnector(**args)
        elif name == 'influxdb':
            connectors['influxdb'] = influx.InfluxDBConnector(**args)
    # elif name == 'file_system':
    #     connectors['file_system'] = file_system.FileSystemConnector(**args)
    # if name == 'DWEET_NAME':
    #     conn = dweet.DweetConnector(setting)
    # elif name == 'ADAFRUITIO_KEY':
    #     conn = io_adafruit.IOAdafruitConnector(setting)
    # elif name == 'FILE_SYSTEM_PATH':
    #     conn = file_system.FileSystemConnector(setting)
    # elif name == 'INFLUXDB':
    #     conn = influx.InfluxDBConnector(setting)

    if reading:
        display_table(reading)
        reading = validate_temperature(
            reading, convert_config_stanza(config['temperature_ranges'])
        )
        for name, connector in connectors.items():
            connector.send(data=reading)
    else:
        print('Unable to get reading.')


def display_table(reading: Dict):
    table_data = [
        [i.capitalize() for i in reading.keys()],
        [i for i in reading.values()],
    ]
    print(tabulate(table_data, tablefmt='fancy_grid'))


if __name__ == '__main__':
    logger.debug('Starting...')
    main()
