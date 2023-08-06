import os

import pendulum

from ..config.mapping import config_map
from .collections import ComponentStorageCollection
from .component import ComponentStorage
from .models.filesystem import StorageFileSystemModel


class ExperimentStorage:
    def __init__(self, url: str):
        self._model = StorageFileSystemModel.create(url)
        if self._model.component_id is not None:
            raise ValueError(
                "URL is a component URL. Use ComponentStorage interface instead."
            )
        self._components = {}

    @property
    def id(self):
        """6-digit experiment ID, e.g. F4K3r6"""
        return self._model.experiment_id

    @property
    def url(self):
        """Returns the file system URL"""
        return self._model.url

    @property
    def seed(self):
        """Returns the global random seed used in the experiment"""
        return self._model.file("execution.json")["seed"]

    @property
    def timestamp(self):
        """Returns the timestamp of the experiment"""
        return self._model.file("execution.json")["timestamp"]

    @property
    def code_backup(self):
        """True if code backup is available"""
        return self._model.file("code.json")["code_backup"]

    @property
    def code_version(self):
        """Returns information about the source code version as a dictionary

        ```
        project:
          path: VCS url
          commit: Commit hash or None
          is_dirty: Whether everything has been commited to VCS
        vendor: Dict of vendor project information with the same structure as above
        ```
        """
        return config_map(self._model.file("code.json")["code_version"])

    @property
    def started_at(self):
        """Start of execution
        """
        return pendulum.parse(self._model.file("execution.json")["started_at"])

    @property
    def host(self):
        """Returns information on the experiment host"""
        return config_map(self._model.file("host.json"))

    @property
    def output(self):
        """Returns the captured output"""
        return self._model.file("output.log")

    @property
    def schedule(self):
        """Returns the experiment schedule"""
        return self._model.file("schedule.json")

    @property
    def components(self):
        """List of components
        """
        if len(self._components) == 0:
            self._components = {
                component: ComponentStorage(
                    os.path.join(self.url, component), experiment=self
                )
                for component in self._model.file("execution.json")["components"]
            }

        return ComponentStorageCollection(list(self._components.values()))

    def __len__(self):
        """Returns the number of components in this experiment"""
        return len(self._model.file("execution.json")["components"])

    def __iter__(self):
        yield from self.components

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Storage: Experiment <{self.id}>"
