""" Driver for the Arduino Temperature Sensors. The device is
a...

The :class:`ArduinoBoard` main class manages the interface
to the device and provides connection and communication
methods through USB. The driver implements an auxiliary
:class:`Channel` class to hold information about the
available sensors. A custom exception :class:`StateError`
is used for internal error management.
"""

# Imports
from serial import (
    Serial,
    EIGHTBITS
)
from typing import List
import configparser

# Third party
from lab_utils.custom_logging import getLogger


class StateError(BaseException):
    """ Mock-up exception to deal with unexpected device status.
    It is used to signal for instance that the device should be
    connected but it is not at a certain execution point.
    """
    pass


class Channel:
    """ Simple container to hold channel information.
    """

    sensor_number: int = None    #: The channel ID number.
    logging: bool = False       #: Data from the sensor should be logged.
    label: str = ''             #: Label of the sensor, to be used when logging to a database.
    data: float = None          #: Latest temperature readout value.
    status: bool = False        #: Valid data

    def __init__(self, sensor_number: int = None, label: str = None):
        self.sensor_number = sensor_number
        self.label = label


class ArduinoBoard(object): # noqa (ignore CamelCase convention)
    """ Driver implementation for the ArduinoBoard.
    """

    # Attributes
    ETX = chr(3)    #: End text (Ctrl-c), chr(3), \\x03
    CR = chr(13)    #: Carriage return, chr(13), \\r
    LF = chr(10)    #: Line feed, chr(10), \\n
    ENQ = chr(5)    #: Enquiry, chr(5), \\x05
    ACK = chr(6)    #: Acknowledge, chr(6), \\x06
    NAK = chr(21)   #: Negative acknowledge, chr(21), \\x15

    # Serial port configuration
    serial: Serial = None                                   #: Serial port handler.
    baud_rate: int = 9600                                   #: Baud rate for serial communication.
    serial_port: str = '/dev/ArduinoTemperatureSensors'     #: Physical address of the device file.
    timeout: float = 1.0                                    #: Time-out for serial connection error.
    warmup_time: float = 0.0                                #: Waiting time before logging data to the database.

    # Device setup
    config_file: str = 'conf/arduinoTemperatureSensors.ini'     #: Device configuration file
    channel_info: List[Channel] = []                            #: Channel information, loaded from the config file.

    # Others
    connected: bool = False         #: Status flag.
    number_of_channels: int = 10    #: Maximum number of channels

    def __init__(self,
                 serial_port: str = None,
                 baud_rate: int = None,
                 connect: bool = False,
                 timeout: float = None,
                 config_file: str = None,
                 ):
        """ Initializes the :class:`ArduinoBoard` object. It calls
        the :meth:`config` method to set up the device if a
        :paramref:`~ArduinoBoard.__init__.config_file` is given. If
        the :paramref:`~ArduinoBoard.__init__.connect` flag is set
        to `True`, attempts the connection to the device.

        Parameters
        ----------
        serial_port : str, optional
            Physical address of the device file, default is 'None'

        timeout : float, optional
            Serial communication time out, default is 'None'

        baud_rate: int, optional
            Baud rate for serial communication, default is 'None'

        connect: bool, optional
            If set, attempt connection to the device, default is `False`

        config_file : str, optional
            Configuration file, default is 'None'.

        Raises
        ------
        :class:`configparser.Error`
           Configuration file error

        :class:`~serial.SerialException`
            The connection to the device has failed

        :class:`IOError`
            Communication error, probably message misspelt.

        :class:`StateError`
            Device was in the wrong state.
        """

        # Initialize variables
        self.connected = False
        for ch in range(self.number_of_channels):
            self.channel_info.append(Channel(sensor_number=ch+1))

        # Load config file, if given
        if config_file is not None:
            self.config(config_file)

        # Assign attributes, if given
        # They override they configuration file
        if baud_rate is not None:
            self.baud_rate = baud_rate
        if serial_port is not None:
            self.serial_port = serial_port
        if timeout is not None:
            self.timeout = timeout

        # Connect to the device
        if connect:
            self.connect()

    def config(self, new_config_file: str = None):
        """ Loads the Arduino Temperature Sensors configuration
        from a file. If :paramref:`~ArduinoBoard.config.new_config_file`
        is not given, the latest :attr:`config_file` is re-loaded;
        if it is given and the file is successfully parsed,
        :attr:`config_file` is updated to the new value.

        Parameters
        ----------
        new_config_file : str, optional
            New configuration file to be loaded.

        Raises
        ------
        :class:`configparser.Error`
           Configuration file error
        """

        # Update configuration file, if given
        if new_config_file is None:
            new_config_file = self.config_file

        # Initialize config parser and read file
        getLogger().info("Loading configuration file %s", new_config_file)
        config_parser = configparser.ConfigParser()
        config_parser.read(new_config_file)

        # Load serial port configuration
        self.serial_port = config_parser.get(section='Connection', option='device')
        self.baud_rate = config_parser.getint(section='Connection', option='baud_rate')
        self.timeout = config_parser.getfloat(section='Connection', option='timeout')
        self.warmup_time = config_parser.getfloat(section='Connection', option='warmup_time')

        # Load channel information
        for ch in range(self.number_of_channels):
            sec_name = 'Sensor_{}'.format(ch+1)
            log = False
            lab = None
            if config_parser.has_section(sec_name):
                log = config_parser.getboolean(sec_name, 'logging')
                lab = config_parser.get(sec_name, 'label')
                getLogger().debug('Found sensor %d: %s, %s', ch+1, str(log), lab)
            else:
                getLogger().debug('%s not found', sec_name)
            self.channel_info[ch].logging = log
            self.channel_info[ch].label = lab

        # If everything worked, update local config_file for future calls
        self.config_file = new_config_file

    def connect(self):
        """ Connects to the Arduino device.

        Raises
        ------
        :class:`~serial.SerialException`
            The connection to the device has failed.

        :class:`IOError`
            Communication error, probably message misspelt.

        :class:`StateError`
            Device was in the wrong state.
        """
        if self.connected:
            raise StateError('device was already ON')
        
        getLogger().info('Connecting to Arduino Temperature Sensors on port %s', self.serial_port)

        self.serial = Serial(
            port=self.serial_port,
            baudrate=self.baud_rate,
            bytesize=EIGHTBITS,
            timeout=self.timeout,
        )

        self.connected = True
        getLogger().info('Connection successful')

    def disconnect(self):
        """ Closes the connection to the Arduino Temperature Sensors.

        Raises
        ------
        :class:`serial.SerialException`
            The connection to the device has failed.

        :class:`IOError`
            Communication error, probably message misspelt.

        :class:`StateError`
            Device was in the wrong state.
        """
        # Check the device is connected
        if not self.connected:
            getLogger().warning('Device is not ON')
            raise StateError('Device is not ON')

        getLogger().info('Closing connection to Arduino Temperature Sensors on port %s', self.serial_port)
        self.connected = False
        self.serial.close()
        getLogger().info('Connection closed')

    def flush(self):
        """ Cleans the input buffer.

        Raises
        ------
        :class:`serial.SerialException`
            The connection to the device has failed.

        :class:`IOError`
            Communication error, probably message misspelt.

        :class:`StateError`
            Device was in the wrong state.
        """

        # Check the device is connected
        if not self.connected:
            getLogger().warning('Device is not ON')
            raise StateError('Device is not ON')

        getLogger().debug('Cleaning input buffer')
        self.serial.reset_input_buffer()

    def clear_data(self):
        """ Clears sensor data.

        Sets the :attr:`~.Channel.status` of every :class:`Channel`
        in :attr:`channel_info` to False.
        """
        getLogger().debug('Clearing sensor data')
        for ch in self.channel_info:
            ch.status = False

    def read_data(self):
        """ Reads data from the device buffer.

        Raises
        ------
        :class:`serial.SerialException`
            The connection to the device has failed.

        :class:`IOError`
            Communication error, probably message misspelt.

        :class:`StateError`
            Device was in the wrong state.
        """

        # Check the device is connected
        if not self.connected:
            getLogger().warning('Device is not ON')
            raise StateError('Device is not ON')

        # Read buffer
        getLogger().debug('Reading a line now')
        attempts = 0
        max_attempts = 10
        buffer = None
        while attempts < max_attempts:
            buffer = self.serial.readline().decode().rstrip(chr(10)).rstrip(chr(13))
            attempts += 1
            getLogger().debug('Attempt {}: {}'.format(attempts, buffer))

            # Check buffer length, sometimes empty lines are read
            if len(buffer) < 3:
                getLogger().debug('Empty line')
                continue

            # Check first and last characters
            if buffer[0] != '#' or buffer[-1] != '#':
                getLogger().warning('Readout data format error: {}'.format(buffer))
                continue

            # Data is valid, break loop
            break

        # Number of attempts
        if attempts == max_attempts:
            message = 'Could not read meaningful data from the device after {} attempts'.format(max_attempts)
            getLogger().warning(message)
            raise IOError(message)

        # Remove first and last characters
        buffer = buffer[1:-2]
        getLogger().debug('Buffer: {}'.format(buffer))

        # Split into list
        data = buffer.split(sep=';')
        getLogger().debug('Data: {}'.format(data))

        # Parse data
        for item in data:
            getLogger().debug('Item: {}'.format(item))
            channel, value = item.split(sep=' ')

            try:
                channel = int(channel)
                if channel-1 not in range(self.number_of_channels):
                    getLogger().warning('Unknown channel {}'.format(channel))
                self.channel_info[channel-1].data = float(value)
                self.channel_info[channel-1].status = True
            except ValueError as e:
                getLogger().error("{}: {}".format(type(e).__name__, e))

            getLogger().debug('Channel: {}      Value: {}'.format(channel, value))

        # Clean the buffer
        self.flush()
