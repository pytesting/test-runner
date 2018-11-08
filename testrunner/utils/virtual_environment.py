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

import shutil
import tempfile
from typing import Union

from testrunner.utils.preconditions import Preconditions


class VirtualEnvironment(object):

    def __init__(self, env_name: str) -> None:
        Preconditions.check_argument(
            len(env_name) > 0,
            'Cannot create an virtual environment without a name!')
        self._env_name = env_name
        self._env_dir = tempfile.mkdtemp(suffix=env_name)
        self._old_cwd = os.getcwd()
        os.chdir(self._env_dir)

    def cleanup(self) -> None:
        os.chdir(self._old_cwd)
        shutil.rmtree(self._env_dir)

    def get_env_dir(self) -> Union[bytes, str, os.PathLike]:
        return self._env_dir
