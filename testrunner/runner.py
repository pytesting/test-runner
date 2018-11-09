# -*- coding: utf-8 -*-

# This file is part of test-runner.
#
# test-runner is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# test-runner is distributed in the hope that it will be useful
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with test-runner.  If not, see <https://www.gnu.org/licenses/>.
import os

from enum import Enum, auto
from typing import Union, Tuple

from testrunner.runners.abstract_runner import AbstractRunner
from testrunner.runners.pytest_runner import PyTestRunner
from testrunner.runners.setup_py_runner import SetupPyRunner
from testrunner.utils.preconditions import IllegalStateException


class RunnerType(Enum):
    """Various types of known runners"""

    AUTO_DETECT = auto()
    """Use the auto-detection for the correct runner.
    ATTENTION: This is not yet implemented!"""

    PYTEST = auto()
    """Use the PyTest runner."""

    SETUP_PY = auto()
    """Use setup.py test as runner."""

    _UNKNOWN = auto()


class Runner(object):
    """
    The runner
    """

    def __init__(
        self,
        project_name: str,
        repo_path: Union[bytes, str, os.PathLike],
        runner: RunnerType = RunnerType.AUTO_DETECT,
    ) -> None:
        """
        Creates a new runner for tests.

        :param project_name: The name of the project
        :param repo_path: Path to the project's source code
        :param runner: The RunnerType that should be used
        """
        self._project_name = project_name
        self._repo_path = repo_path
        if runner != RunnerType.AUTO_DETECT:
            self._runner_type = runner
        else:
            self._runner_type = self._detect_runner_type()
        self._runner = self._instantiate_runner()

    def _detect_runner_type(self) -> RunnerType:
        return RunnerType._UNKNOWN

    def _instantiate_runner(self) -> AbstractRunner:
        if self._runner_type == RunnerType.PYTEST:
            runner = PyTestRunner(self._project_name, self._repo_path)
        elif self._runner_type == RunnerType.SETUP_PY:
            runner = SetupPyRunner(self._project_name, self._repo_path)
        else:
            raise IllegalStateException("Could not find a matching runner!")
        return runner

    def run(self) -> Tuple[str, str]:
        """
        Run the test runner for the project

        :return: A tuple (stdout, stderr) with the outputs of the run process
        """
        return self._runner.run()