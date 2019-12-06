"""
Test runner is a library for running unit tests on Python code.

It offers the opinion to automatically detect the correct run settings for
the tests and gives information about the test results and coverage information.

Test-Runner is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Test-Runner is distributed in the hope that it will be useful
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with Test-Runner.  If not, see <https://www.gnu.org/licenses/>.
"""
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
        result = runner.get_run_result(out)
        self.assertGreater(result.statements, 0)
        self.assertGreaterEqual(result.missing, 0)
        self.assertGreater(result.coverage, 0)

    @unittest.skip("Skip test until runner is implemented")
    def test_integration_ratelimitqueue(self):
        url = "https://github.com/JohnPaton/ratelimitqueue"
        Repo.clone_from(url, self._tmp_dir)
        runner = ToxRunner("ratelimitqueue", self._tmp_dir)
        out, err = runner.run()
        result = runner.get_run_result(out)
        self.assertGreater(result.statements, 0)
        self.assertGreaterEqual(result.missing, 0)
        self.assertGreater(result.coverage, 0)


if __name__ == "__main__":
    unittest.main()
