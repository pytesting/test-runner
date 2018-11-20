# -*- coding: utf-8 -*-
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
