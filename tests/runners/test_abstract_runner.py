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
import unittest
from unittest.mock import patch

from testrunner.runners.abstract_runner import AbstractRunner
from testrunner.utils.preconditions import IllegalArgumentException


class AbstractRunnerTest(unittest.TestCase):

    def test_cannot_instantiate(self):
        """Showing we normally cannot instantiate an abstract class"""
        with self.assertRaises(TypeError):
            AbstractRunner('foo', 'bar')

    @patch.multiple(AbstractRunner,
                    __abstractmethods__=set())
    def test_empty_project_name(self):
        with self.assertRaises(IllegalArgumentException) as context:
            AbstractRunner('', 'bar')
        self.assertTrue(
            isinstance(context.exception, IllegalArgumentException))
        self.assertTrue(
            'Project name must not be empty!' in str(context.exception))

    @patch.multiple(AbstractRunner,
                    __abstractmethods__=set())
    def test_empty_path(self):
        with self.assertRaises(IllegalArgumentException) as context:
            AbstractRunner('foo', '')
        self.assertTrue(
            isinstance(context.exception, IllegalArgumentException))
        self.assertTrue(
            'Path must not be empty!' in str(context.exception))


if __name__ == '__main__':
    unittest.main()
