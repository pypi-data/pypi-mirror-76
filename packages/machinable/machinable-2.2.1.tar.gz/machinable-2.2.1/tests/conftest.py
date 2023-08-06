import os
import shutil

import pytest

import machinable as ml


class Helpers:
    @staticmethod
    def tmp_directory(append=""):
        path = os.path.join("./_test_data/", append)
        shutil.rmtree(path, ignore_errors=True)
        os.makedirs(path)
        return path


@pytest.fixture
def helpers():
    return Helpers


def pytest_sessionstart(session):
    if "DISABLE_STORAGE_GENERATION" in os.environ:
        return

    # setup storage test data
    path = Helpers.tmp_directory("storage")

    ml.execute(
        ml.Experiment().components(("nodes.observations", {"id": 1})).repeat(3),
        path,
        project="./test_project",
    )
    ml.execute(
        ml.Experiment()
        .components(("nodes.observations", {"id": 2}), "thechildren")
        .repeat(2),
        path,
        project="./test_project",
    )

    ml.execute(
        ml.Experiment()
        .components(("nodes.observations", {"id": 3, "test": True}))
        .repeat(4),
        path,
        seed="tttttt",
        project="./test_project",
    )

    ml.execute(
        ml.Experiment()
        .components(("nodes.observations", {"id": 4}))
        .directory("subdirectory"),
        path,
        seed="TTTTTT",
        project="./test_project",
    )

    ml.execute(
        ml.Experiment().components(("nodes.observations", {"id": 4, "corrupt": True})),
        path,
        seed="corupt",
        project="./test_project",
    )

    # corrupt some data
    shutil.rmtree(os.path.join(path, "corupt"), ignore_errors=True)
