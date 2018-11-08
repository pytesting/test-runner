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
import subprocess
import tempfile
import virtualenv
from typing import Union, List, Tuple

from testrunner.utils.preconditions import Preconditions


class VirtualEnvironment(object):

    def __init__(self, env_name: str) -> None:
        Preconditions.check_argument(
            len(env_name) > 0,
            'Cannot create an virtual environment without a name!')
        self._env_name = env_name
        self._packages = []

        self._env_dir = tempfile.mkdtemp(suffix=env_name)
        virtualenv.create_environment(self._env_dir)

    def cleanup(self) -> None:
        shutil.rmtree(self._env_dir)

    def get_env_dir(self) -> Union[bytes, str, os.PathLike]:
        return self._env_dir

    def add_package_for_installation(self, package: str) -> None:
        self._packages.append(package)

    def add_packages_for_installation(self, packages: List[str]) -> None:
        self._packages.extend(packages)

    def run_commands(self, commands: List[str]) -> Tuple[str, str]:
        command_list = [
            'source {}'.format(os.path.join(self._env_dir, 'bin', 'activate')),
            'python -V']
        for package in self._packages:
            command_list.append('pip install {}'.format(package))
        command_list.extend(commands)
        cmd = ';'.join(command_list)
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        out, err = process.communicate()
        return out, err
