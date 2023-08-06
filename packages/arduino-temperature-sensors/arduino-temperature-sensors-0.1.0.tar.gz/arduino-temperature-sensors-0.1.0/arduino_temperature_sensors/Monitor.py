""" Background monitoring thread based on the :obj:`threading`
library. A :obj:`Monitor` object starts a background
:class:`thread<threading.Thread>` which reads out the Arduino
:attr:`~Monitor.device` every second. The data can then be
printed to the terminal and/or saved to a PostgreSQL database
using the :obj:`lab_utils.database` library. The monitoring
thread is intended to be self-sustainable and will try to deal
with unexpected errors (usually issues with communication to
the device), recover, log them and keep running.
"""

# Imports
from datetime import datetime
from time import sleep
from threading import Thread, Event
from typing import List

# Third party
from lab_utils.database import Database, DataType, Constraint
from lab_utils.custom_logging import getLogger
from serial.serialutil import SerialException

# Local
from .ArduinoBoard import ArduinoBoard, StateError


class Monitor(Thread):
    """ Manages a background
    :class:`thread<threading.Thread>`
    which logs data from the TPG-256A
    :attr:`~Monitor.device`."""

    # Thread objects
    device: ArduinoBoard = None     #: :class:`Arduino device<.ArduinoBoard>` handler.
    db: Database = None             #: :class:`Database<lab_utils.database.Database>` object.

    # Thread flags
    run_flag: Event = None          #: :class:`Flag<threading.Event>` to signal the thread to stop.
    database_flag: Event = False    #: Database usage :class:`flag<threading.Event>`.
    terminal_flag: Event = False    #: Terminal output :class:`flag<threading.Event>`.

    # Monitor Variables
    table_name: str = 'epic_temperature'    #: Name of the PostgreSQL table where data will be saved.
    column_list: List[str] = None           #: :class:`~typing.List` of data labels to save.

    def __init__(self,
                 device: ArduinoBoard,
                 name: str = 'Monitor Thread',
                 database_flag: bool = False,
                 database_config_file: str = None,
                 terminal_flag: bool = False,
                 table_name: str = 'epic_temperature'):
        """ Initializes the :class:`Monitor` object. The
        constructor checks that the given :paramref:`device`
        is initialized. If :paramref:`database_flag` is set
        to `True`, the :meth:`prepare_database` method is
        called, which initializes the :attr:`database<db>`
        object and sets up the connection. A table named
        :paramref:`table_name` is created, as well as the
        necessary :attr:`columns<column_list>` to store the
        temperature data.

        Finally, the method :meth:`run` starts and detaches
        a background thread which will run indefinitely,
        reading the Arduino :attr:`device`. The data is
        saved to the :attr:`database` if :paramref:`database_flag`
        is set to `True`, and it is printed to the terminal if
        :paramref:`terminal_flag` is set to `True`.

        Parameters
        ----------
        device: :class:`.ArduinoBoard`
            Device handle, must be already initialized and connected.

        name: str, optional
            Thread name for logging purposes, default is 'Monitor Thread'

        database_flag: bool, optional
            Save data to a PostgreSQL database, default is 'False'

        terminal_flag: bool, optional
            Print data to the logging terminal sink with 'info'
            level, default is 'False'

        table_name: str, optional
            Name of the PostgreSQL table where the data is saved, default is 'epic_temperature'.


        Raises
        ------
        :class:`StateError`
            The supplied :attr:`device` was not properly initialized.

        :class:`configparser.Error`
            Database configuration file error.

        :class:`psycopg2.DatabaseError`
            Database error (connection, access...)
        """

        # Assign arguments
        self.table_name = table_name

        # Check device is ON and ready
        self.device = device
        if not device.connected:
            raise StateError('Device not connected')

        # Call the parent class initializer
        super().__init__(name=name)

        # Initialize flags
        self.run_flag = Event()
        self.database_flag = Event()
        self.terminal_flag = Event()

        # Set flags
        self.run_flag.set()
        if database_flag:
            getLogger().info('Database option active')
            self.database_flag.set()
        if terminal_flag:
            getLogger().info('Terminal option active')
            self.terminal_flag.set()

        # Initialize database
        if database_flag:
            self.prepare_database(database_config_file)

        # Run
        self.start()

    def prepare_database(self,
                         database_config_file: str = None,
                         ):
        """ Ensures the :attr:`database<db>` is ready to accept
        data from the Arduino :attr:`device`. Initializes
        the :attr:`database<db>` object and sets up the
        connection. If the table :attr:`table_name` does not
        exist, it is created, as well as the necessary
        :attr:`columns<column_list>` to store the temperature
        data. The labels of the columns are retrieved from
        device's :attr:`~.ArduinoBoard.channel_info`.

        Parameters
        ----------
        database_config_file: str, optional
            The configuration file of the database

        Raises
        ------
        :class:`configparser.Error`
            Error reading configuration file.

        :class:`psycopg2.Error`
            Base exception for all kinds of database errors.

        """

        getLogger().info('Setting up database')
        self.db = Database(config_file=database_config_file)
        self.db.connect(print_version=True)

        # Check table exists, create otherwise
        if not self.db.check_table(self.table_name):
            self.db.create_timescale_db(self.table_name)
            if not self.db.check_table(self.table_name):
                raise RuntimeError('could not create TimescaleDB object \'%s\'', self.table_name)
        getLogger().debug('Table \'%s\' ready', self.table_name)

        # Create column list
        self.column_list = []
        for ch in self.device.channel_info:
            if ch.logging:
                self.column_list.append(ch.label)

        # Check columns exist, create otherwise
        getLogger().debug('Creating columns: %s', '; '.join(self.column_list))

        for label in self.column_list:
            # Raises an error if the column could not be created
            self.db.new_column(
                table_name=self.table_name,
                column_name=label,
                data_type=DataType.float,
                constraints=None,
            )
            getLogger().debug('Column \'%s\' ready', label)

        # Recreate aggregate view
        self.db.create_aggregate_view(table_name=self.table_name)

    def stop(self) -> bool:
        """ Clears the :attr:`run_flag` to signal the
        background thread to stop. The thread status is
        then checked every 0.1 second (up to 5 seconds).
        Returns `True` if the thread stopped, `False`
        otherwise.

        Returns
        -------
        bool:
            `True` if the thread is not running within
            5 seconds, `False` otherwise.
        """

        getLogger().info('Sending stop signal to the logging thread')
        self.run_flag.clear()

        # Check thread status every 0.1 seconds, for 5 seconds
        for _ in range(50):
            if not self.is_alive():
                getLogger().info('Monitor thread successfully stopped')
                return True
            sleep(0.1)

        # Thread should have stopped by now, something went wrong
        getLogger().error('Monitor thread did not finish within a reasonable time')
        return False

    def run(self) -> None:
        """ Monitoring method start upon object creation.
        The Arduino :attr:`device` is read every second
        in an endless loop. The temperature data may be saved
        to a PostgreSQL :attr:`database<db>` and/or printed
        to the terminal, if the respective :attr:`terminal_flag`
        and :attr:`database_flag` flags were set.

        In case of unexpected error (which happens often with
        the RS-232 communication protocol), the method will
        try to recover, log any information and continue operations.

        To stop logging and break the loop, the :meth:`stop`
        method should be used to set the :attr:`run_flag` flag.
        """

        # Let the server reply to the client to produce a cleaner log
        sleep(0.1)
        getLogger().info('Starting monitor')

        # Wait until the next turn of the second
        seconds = datetime.now().second
        while datetime.now().second == seconds:
            sleep(0.001)
        seconds = datetime.now().second
        start_time = seconds

        # Flush data
        self.device.flush()

        # Endless loop, use the stop() method to break it
        while self.run_flag.is_set():
            try:
                # Read temperature data from the device
                self.device.read_data()

                # Save to database after warm-up time
                if start_time - seconds >= self.device.warmup_time:
                    self.save_to_database()

                # Print to terminal and/or file
                self.print_string()

                # Clear data
                self.device.clear_data()

            except (SerialException, StateError, IOError) as e:
                getLogger().error("{}: {}".format(type(e).__name__, e))
                for i in range(5):
                    sleep(2)
                    getLogger().error('Attempting to reset the device (%d out of 5)', i)
                    try:
                        if self.device.connected:
                            self.device.disconnect()
                        self.device.connect()
                    except (SerialException, StateError, IOError) as e:
                        getLogger().error("{}: {}".format(type(e).__name__, e))
                    else:
                        # Leave the reconnection "for" loop and return to the main "while" loop
                        break
                # The reconnection attempts have failed, terminate the thread and notify the alarm manager
                getLogger().error('Terminating Arduino Temperature Sensors Monitor!')
                raise SystemExit(
                    'Could not re-establish connection to the device after 5 attempts, terminating thread now...'
                )

            # Wait until the next turn of the second
            while datetime.now().second == seconds:
                sleep(0.001)
            seconds = datetime.now().second

        # We reach here when 'run_flag' has been cleared by the stop() method
        getLogger().info('Stop signal! Quitting logging thread')

    def print_string(self):
        """ Prints the retrieved data to the terminal. The log
        level will be `INFO` if :attr:`terminal_flag` is set,
        and `DEBUG` otherwise."""

        # Build message string
        msg = ''
        for ch in self.device.channel_info:
            if ch.logging:
                if not ch.status:
                    msg += '{:20}'.format('{:7}: Invalid'.format(ch.label))
                else:
                    msg += '{:20}'.format('{:7}: {}'.format(ch.label, ch.data))

        # Print to terminal
        if self.terminal_flag.is_set():
            getLogger().info(msg)
        else:
            getLogger().debug(msg)

    def save_to_database(self):
        """ Saves the latest temperature data to the
        PostgreSQL :attr:`database<db>`. If
        :attr:`database_flag` is not set, the
        method does nothing.

        Raises
        ------
        :class:`psycopg2.Error`
            Base exception for all kinds of database errors.
        """

        if not self.database_flag.is_set():
            return

        if self.db is None:
            raise StateError('database not initialized')

        data = []
        for ch in self.device.channel_info:
            if ch.logging:
                if ch.status:
                    data.append(ch.data)
                else:
                    data.append('NaN')

        self.db.new_entry(
            table_name=self.table_name,
            columns=self.column_list,
            data=data,
            check_columns=False,
        )
