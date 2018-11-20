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
import shutil
import tempfile
import unittest
from git import Repo

from testrunner.runners.tox_runner import ToxRunner


class ToxRunnerTest(unittest.TestCase):
    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    @unittest.skip("Skip test until runner is implemented")
    def test_integration_zula(self):
        url = "https://github.com/efe/zula"
        Repo.clone_from(url, self._tmp_dir)
        runner = ToxRunner("zula", self._tmp_dir)
        out, err = runner.run()
        statements, missing, coverage = runner.get_total_result(out)
        self.assertGreater(statements, 0)
        self.assertGreaterEqual(missing, 0)
        self.assertGreater(int(coverage[:-1]), 0)

    @unittest.skip("Skip test until runner is implemented")
    def test_integration_ratelimitqueue(self):
        url = "https://github.com/JohnPaton/ratelimitqueue"
        Repo.clone_from(url, self._tmp_dir)
        runner = ToxRunner("ratelimitqueue", self._tmp_dir)
        out, err = runner.run()
        statements, missing, coverage = runner.get_total_result(out)
        self.assertGreater(statements, 0)
        self.assertGreaterEqual(missing, 0)
        self.assertGreater(int(coverage[:-1]), 0)


if __name__ == "__main__":
    unittest.main()
