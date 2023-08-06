import copy
import io
import json
import os
import sys

import pendulum

from ..utils.dicts import serialize, update_dict
from ..utils.formatting import exception_to_str
from .log import Log
from .record import Record

try:
    import cPickle as pickle
except ImportError:
    import pickle


class OutputRedirection:
    def __init__(self, stream_type, mode, file_open, file_name=None):
        if stream_type not in ["stdout", "stderr"]:
            raise ValueError(f"Invalid stream type: {stream_type}")

        self._file_stream = None
        self.stream_type = stream_type
        self.mode = mode
        self.file_open = file_open
        self.file_name = file_name or stream_type + ".log"
        self.sys_stream = getattr(sys, stream_type)

        # capture output from other consumers of the underlying file descriptor
        if self.mode != "DISCARD":
            try:
                output_file_descriptor = os.dup(self.sys_stream.fileno())
                os.dup2(self.file_stream.fileno(), output_file_descriptor)
            except (AttributeError, IOError, io.UnsupportedOperation):
                pass

    @property
    def file_stream(self):
        if self._file_stream is None:
            self._file_stream = self.file_open(self.file_name, "a", buffering=1)

        return self._file_stream

    @property
    def streams(self):
        if self.mode == "DISCARD":
            return []

        if self.mode == "FILE_ONLY":
            return [self.file_stream]

        return [self.file_stream, self.sys_stream]

    def write(self, message):
        for i, stream in enumerate(self.streams):
            try:
                stream.write(message)
            except (IOError, AttributeError):
                if i == 0:
                    # close corrupt file stream
                    self.close_file_stream()

    def close_file_stream(self):
        try:
            self._file_stream.exit_on_completion()
        except (IOError, AttributeError):
            pass
        finally:
            self._file_stream = None

    # forward attributes to standard sys stream

    def __getattr__(self, item):
        return getattr(self.sys_stream, item)

    @classmethod
    def apply(cls, mode, file_open, file_name=None):
        if mode not in ["DISABLED", "FILE_ONLY", "SYS_AND_FILE", "DISCARD"]:
            raise ValueError(f"Invalid output redirection mode: {mode}")

        if mode == "DISABLED":
            return

        sys.stdout.flush()
        sys.stderr.flush()
        sys.stdout = cls("stdout", mode, file_open, file_name)
        sys.stderr = cls("stderr", mode, file_open, file_name)

    @classmethod
    def revert(cls):
        if isinstance(sys.stdout, cls):
            sys.stdout.close_file_stream()
            sys.stdout = sys.stdout.sys_stream
        if isinstance(sys.stderr, cls):
            sys.stderr.close_file_stream()
            sys.stderr = sys.stderr.sys_stream


class Store:
    """Store interface

    ::: tip
    Becomes available as ``self.store``
    :::

    # Arguments
    config: dict, configuration options
    heartbeat: Integer, seconds between two heartbeat events
    """

    def __init__(self, config=None, component=None):
        self._component = component

        # todo: refactor to use Storage abstraction

        if isinstance(config, dict):
            config = copy.deepcopy(config)

        if isinstance(config, str):
            config = {"url": config}

        # default settings
        self.config = update_dict(
            {
                "url": "mem://",
                "log": {},
                "records": {},
                "directory": "",
                "experiment": "",
                "output_redirection": "SYS_AND_FILE",  # DISABLED, FILE_ONLY, SYS_AND_FILE, DISCARD
            },
            config,
            copy=True,
        )
        self.statistics = {}

        if "://" not in self.config["url"]:
            self.config["url"] = "osfs://" + self.config["url"]

        # todo: migrate to FileSystem abstraction
        from fs import open_fs

        self.filesystem = open_fs(self.config["url"], create=True)
        self.filesystem.makedirs(
            self.get_path(), recreate=self.config.get("allow_overwrites", False)
        )

        self._record_writers = {}
        self._log = None
        self._store = {}

        # status
        self._status = dict()
        self._status["started_at"] = str(pendulum.now())
        self._status["finished_at"] = False
        self.refresh_status(log_errors=True)

        if not self.config["url"].startswith("mem://"):
            OutputRedirection.apply(
                self.config["output_redirection"], self.get_stream, "output.log"
            )

    def destroy(self):
        """Destroys the store instance"""
        # write finished status (not triggered in the case of an unhandled exception)
        self._status["finished_at"] = str(pendulum.now())
        self.refresh_status(log_errors=True)

        OutputRedirection.revert()

    def directory(self, append=""):
        """Returns the write directory"""
        return os.path.join(self.config["url"], self.get_path(append))

    def local_directory(self, append=""):
        """Returns the local filesystem path, or False if non-local

        # Returns
        Local filesystem path, or False if non-local
        """
        if not self.config["url"].startswith("osfs://"):
            return False

        return os.path.join(
            self.config["url"].split("osfs://")[-1], self.get_path(append)
        )

    def refresh_status(self, log_errors=False):
        """Updates the status.json file with a heartbeat at the current time
        """
        if not self.config.get("component", None):
            return False

        try:
            self._status["heartbeat_at"] = str(pendulum.now())
            self.write("status.json", self._status, overwrite=True, _meta=True)
        except (IOError, Exception) as ex:
            if log_errors:
                self.log.error(
                    f"Could not write status information. {exception_to_str(ex)}"
                )

            return ex

        return True

    def get_record_writer(self, scope):
        """Creates or returns an instance of a record writer

        # Arguments
        scope: Name of the record writer

        # Returns
        machinable.store.record.Record
        """
        if scope not in self._record_writers:
            self._record_writers[scope] = Record(
                store=self, config=self.config["records"], scope=scope
            )

        return self._record_writers[scope]

    @property
    def stored(self):
        return self._store

    @property
    def record_writers(self):
        return self._record_writers

    @property
    def record(self):
        """Record interface

        # Returns
        machinable.store.record.Record
        """
        return self.get_record_writer("default")

    @property
    def log(self):
        """Log interface

        # Returns
        machinable.store.log.Log
        """
        if self._log is None:
            self._log = Log(observer=self, config=self.config["log"])

        return self._log

    def has_records(self, scope="default"):
        """Determines whether record writer exists

        # Arguments
        scope: String, name of the record writer. Defaults to 'default'

        # Returns
        True if records have been written
        """
        return scope in self._record_writers

    def has_logs(self):
        """Determines whether log writer exists

        # Returns
        True if log writer exists
        """
        return self._log is not None

    def write(self, name, data, overwrite=False, _meta=False):
        """Stores a data object

        # Arguments
        name: String, name identifier.
            You can provide an extension to instruct machinable to write the data in its own file and not as part
            of a dictionary with other stored values.
            Supported formats are .json (JSON), .npy (numpy), .p (pickle), .txt (txt)
        data: The data object
        overwrite: Boolean, if True existing values will be overwritten
        """
        mode = "w" if overwrite else "a"
        path = os.path.dirname(name)
        name = os.path.basename(name)
        _, ext = os.path.splitext(name)

        if not _meta:
            path = "store/" + path
            self.filesystem.makedir(self.get_path(path), recreate=True)
        filepath = os.path.join(path, name)

        # todo: check overwrite for files

        if ext == "":
            # automatic handling
            if name in self._store and not overwrite:
                raise ValueError(
                    f"'{name}' already exist. "
                    f"Use overwrite=True if you intent to overwrite existing data"
                )
            self._store[name] = data
            with self.get_stream("store.json", "w") as f:
                f.write(json.dumps(self._store, ensure_ascii=False, default=serialize))
        elif ext == ".json":
            # json
            with self.get_stream(filepath, mode) as f:
                f.write(json.dumps(data, ensure_ascii=False, default=serialize))
        elif ext == ".npy":
            import numpy as np

            if "b" not in mode:
                mode += "b"
            # numpy
            with self.get_stream(filepath, mode) as f:
                np.save(f, data)

        elif ext == ".p":
            if "b" not in mode:
                mode += "b"
            with self.get_stream(filepath, mode) as f:
                pickle.dump(data, f)

        elif ext == ".txt":
            with self.get_stream(filepath, mode) as f:
                f.write(data)
        else:
            raise ValueError(
                f"Invalid format: '{ext}'. "
                f"Supported formats are .json (JSON), .npy (numpy), .p (pickle), .txt (txt)"
            )

        if self._component is not None:
            self._component.events.trigger(
                "store.on_change", "store.save", {"name": name, "data": data}
            )

    def get_stream(self, path, mode="r", *args, **kwargs):
        """Returns a file stream on the store write

        # Arguments
        path: Relative file path
        mode: Python file mode
        *args, **kwargs: Optional arguments passed into stream open()
        """
        return self.filesystem.open(self.get_path(path), mode, *args, **kwargs)

    def get_path(self, append="", create=False):
        """Returns the write path

        # Arguments
        append: String, optional postfix that is appended to the path
        create: Boolean, if True path is being created if not existing
        """
        path = os.path.join(
            self.config["directory"],
            self.config["experiment"],
            self.config.get("component", ""),
            append,
        )

        if create:
            self.filesystem.makedirs(path, recreate=True)

        return path

    def get_url(self, append=""):
        return os.path.join(self.config["url"], self.get_path(append, create=False))
