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
from unittest import skip

from git import Repo

from testrunner.runners.nose_runner import NoseRunner


class NoseRunnerTest(unittest.TestCase):
    def setUp(self):
        self._tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self._tmp_dir)

    @skip(reason="Check why this is not working any more")
    def test_integration_zula(self):
        url = "https://github.com/efe/zula"
        Repo.clone_from(url, self._tmp_dir)
        runner = NoseRunner("zula", self._tmp_dir)
        out, err = runner.run()
        result = runner.get_run_result(out)
        self.assertGreater(result.statements, 0)
        self.assertGreaterEqual(result.missing, 0)
        self.assertGreater(result.coverage, 0)

    @skip(reason="Check why this is not working any more")
    def test_integration_ratelimitqueue(self):
        url = "https://github.com/JohnPaton/ratelimitqueue"
        Repo.clone_from(url, self._tmp_dir)
        runner = NoseRunner("ratelimitqueue", self._tmp_dir)
        out, err = runner.run()
        result = runner.get_run_result(out)
        self.assertGreater(result.statements, 0)
        self.assertGreaterEqual(result.missing, 0)
        self.assertGreater(result.coverage, 0)

    @skip(reason="Check why this is not working any more")
    def test_integration_extra_context_py(self):
        url = "https://github.com/WanzenBug/extra-context-py"
        Repo.clone_from(url, self._tmp_dir)
        runner = NoseRunner("extra-context-py", self._tmp_dir)
        out, err = runner.run()
        result = runner.get_run_result(out)
        self.assertGreater(result.statements, 0)
        self.assertGreater(result.missing, 0)
        self.assertGreater(result.coverage, 0)

    def test_no_match(self):
        runner = NoseRunner("test", "test")
        result = runner.get_run_result("test")
        self.assertEqual(-1, result.time)
        self.assertEqual(-1, result.coverage)

    def test_full_match_failed(self):
        runner = NoseRunner("test", "test")
        result = runner.get_run_result(
            "Ran 20 tests in 100.123s\nFAILED (DEPRECATED=3, errors=1, failures=2, SKIP=4, TODO=5)"
        )
        self.assertEqual(1, result.error)
        self.assertEqual(2, result.failed)
        self.assertEqual(4, result.skipped)
        self.assertEqual(5, result.passed)

    def test_full_match_ok(self):
        runner = NoseRunner("test", "test")
        result = runner.get_run_result(
            """Ran 20 tests in 100.123s
        OK (DEPRECATED=3, errors=1, failures=2, SKIP=4, TODO=5)"""
        )
        self.assertEqual(1, result.error)
        self.assertEqual(2, result.failed)
        self.assertEqual(4, result.skipped)

    def test_full_log(self):
        runner = NoseRunner("test", "test")
        log = """
        .......
Name               Stmts   Miss  Cover
--------------------------------------
blahblah.py            0      0   100%
spameggs.py           42      0   100%
--------------------------------------
TOTAL                 47      21   42%
----------------------------------------------------------------------
Ran 20 tests in 0.010s

FAILED (DEPRECATED=1, errors=2, failures=3, SKIP=4, TODO=5)
"""
        result = runner.get_run_result(log)
        self.assertEqual(5, result.passed)
        self.assertEqual(0.010, result.time)
        self.assertEqual(42, result.coverage)
        self.assertEqual(21, result.missing)
        self.assertEqual(47, result.statements)

    def test_information_missing_skip(self):
        runner = NoseRunner("test", "test")
        result = runner.get_run_result("Ran 10 tests in 42.424s\nOK (SKIP=1)")
        self.assertEqual(9, result.passed)
        self.assertEqual(1, result.skipped)

    def test_information_missing_error(self):
        runner = NoseRunner("test", "test")
        result = runner.get_run_result("Ran 10 tests in 42.424s\nFAILED (errors=1)")
        self.assertEqual(1, result.error)


if __name__ == "__main__":
    unittest.main()
