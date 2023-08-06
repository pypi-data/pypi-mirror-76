""" Logging module for the Arduino Temperature
Sensors. The module manages a :class:`~Daemon.Daemon`
object over TCP communication.
"""

# Imports
from sys import argv
from configparser import Error as ConfigError
from argparse import ArgumentParser, Namespace

# Third party
from zc.lockfile import LockError
from lab_utils.socket_comm import Client
from lab_utils.custom_logging import configure_logging, getLogger

# Local packages
from arduino_temperature_sensors.Daemon import Daemon
from arduino_temperature_sensors.__project__ import (
    __documentation__ as docs_url,
    __module_name__ as module,
    __description__ as prog_desc,
)


def arduino_temperature_sensors():
    """The main routine. It parses the input argument and acts accordingly."""

    # The argument parser
    ap = ArgumentParser(
        prog=module,
        description=prog_desc,
        add_help=True,
        epilog='Check out the package documentation for more information:\n{}'.format(docs_url)
    )

    # Optional arguments
    ap.add_argument(
        '-l',
        '--logging-config-file',
        help='configuration file with the logging options',
        default=None,
        dest='logging_config_file',
        type=str,
    )
    ap.add_argument(
        '-s',
        '--server-config-file',
        help='configuration file with the Alarm Manager options',
        default=None,
        dest='server_config_file',
        type=str,
    )
    ap.add_argument(
        '-d',
        '--device-config-file',
        help='configuration file with the device options',
        default=None,
        dest='device_config_file',
        type=str,
    )
    ap.add_argument(
        '-db',
        '--database-config-file',
        help='configuration file with the Database options',
        default=None,
        dest='database_config_file',
        type=str,
    )
    ap.add_argument(
        '-a',
        '--address',
        help='host address',
        default=None,
        dest='host',
        type=str
    )
    ap.add_argument(
        '-p',
        '--port',
        help='host port',
        default=None,
        dest='port',
        type=int
    )

    # Mutually exclusive positional arguments
    pos_arg = ap.add_mutually_exclusive_group()
    pos_arg.add_argument(
        '--run',
        action='store_true',
        help='starts the Arduino Temperature Sensors daemon',
        default=False,
    )
    pos_arg.add_argument(
        '--control',
        type=str,
        help='send a [CONTROL] command to the running Arduino Temperature Sensors daemon',
        nargs='?',
    )

    # Auto-start option for supervisord
    ap.add_argument(
        '--autostart',
        action='store_true',
        help='start the daemon, connect to the device and start monitoring',
        default=False,
        dest='autostart',
    )

    # Parse the arguments
    args, extra = ap.parse_known_args(args=argv[1:])
    if extra is not None and args.control is not None:
        args.control += ' ' + ' '.join(extra)

    # Call appropriate function
    if args.run:
        run(args)
    else:
        send_message(args)


def send_message(args: Namespace):
    """ Sends a string message to a running Arduino
    Temperature Sensors :class:`Daemon` object over TCP."""

    try:
        # Start a client
        c = Client(
            config_file=args.server_config_file,
            host=args.host,
            port=args.port,
        )
        print('Opening connection to the Arduino Temperature Sensors server on {h}:{p}'.format(
            h=c.host,
            p=c.port
        ))

        # Send message and get reply
        print('Sending message: ', args.control)
        reply = c.send_message(args.control)
        print('Reply:\n', reply)

    except ConfigError:
        print('Did you provide a valid configuration file?')

    except OSError:
        print('Maybe the Arduino Temperature Sensors server is not running, or running elsewhere')

    except BaseException as e:
        # Undefined exception, full traceback to be printed
        print("{}: {}".format(type(e).__name__, e))

    else:
        exit(0)

    # Something went wrong...
    exit(1)


def run(args: Namespace):
    """ Launches an Arduino Temperature Sensors
    :class:`Daemon` object."""

    try:
        # Setup logging
        configure_logging(
            config_file=args.logging_config_file,
            logger_name='Arduino Temperature Sensors'
        )

        # Start the daemon
        getLogger().info('Starting the Arduino Temperature Sensors server...')
        the_daemon = Daemon(
            config_file=args.server_config_file,
            pid_file_name='/tmp/arduinoTemperatureSensors.pid',
            host=args.host,
            port=args.port,
            autostart=args.autostart,
            device_config_file=args.device_config_file,
            database_config_file=args.database_config_file,
        )

        the_daemon.start_daemon()
        getLogger().info('Arduino Temperature Sensors server stopped, bye!')

    except ConfigError as e:
        getLogger().error("{}: {}".format(type(e).__name__, e))
        getLogger().error('Did you provide a valid configuration file?')

    except OSError as e:
        getLogger().error("{}: {}".format(type(e).__name__, e))
        getLogger().error('Possible socket error, do you have permissions to the socket?')

    except LockError as e:
        getLogger().error("{}: {}".format(type(e).__name__, e))
        getLogger().error('Arduino Temperature Sensors daemon is probably running elsewhere.')

    except BaseException as e:
        # Undefined exception, full traceback to be printed
        getLogger().exception("{}: {}".format(type(e).__name__, e))

    else:
        exit(0)

    # Something went wrong...
    exit(1)
