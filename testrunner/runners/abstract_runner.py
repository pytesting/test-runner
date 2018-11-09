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
from abc import ABCMeta, abstractmethod
from typing import Union, List

from testrunner.utils.preconditions import Preconditions


class AbstractRunner(metaclass=ABCMeta):

    def __init__(self,
                 project_name: str,
                 path: Union[bytes, str, os.PathLike]) -> \
            None:
        Preconditions.check_argument(
            len(project_name) > 0, 'Project name must not be empty!')
        Preconditions.check_argument(
            len(path) > 0, 'Path must not be empty!')
        self._project_name = project_name
        self._path = path

    @abstractmethod
    def run(self):
        pass

    def _extract_necessary_packages(self) -> List[str]:
        packages = []

        requirements_file = os.path.join(self._path, 'requirements.txt')
        packages.extend(self._extract_packages(requirements_file))

        requirements_file = os.path.join(self._path, 'dev-requirements.txt')
        packages.extend(self._extract_packages(requirements_file))

        return packages

    @staticmethod
    def _extract_packages(requirements_file):
        packages = []
        if os.path.exists(requirements_file) \
                and os.path.isfile(requirements_file):
            with open(requirements_file) as f:
                for line in f.readlines():
                    packages.append(line)
        return packages
