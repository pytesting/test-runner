# -*- coding: utf-8 -*-
import os
import re
from typing import Union, Optional, Tuple

from pytesting_utils import virtualenv

from testrunner.runners.abstract_runner import AbstractRunner, RunResult


class ToxRunner(AbstractRunner):  # pragma: no cover
    def __init__(
        self, project_name: str, path: Union[bytes, str, os.PathLike]
    ) -> None:
        super().__init__(project_name, path)

    def run(self) -> Optional[Tuple[str, str]]:

        with virtualenv(self._project_name) as env:
            old_dir = os.getcwd()
            os.chdir(self._path)

            packages = self._extract_necessary_packages()
            env.add_packages_for_installation(packages)
            env.add_package_for_installation("tox")
            out, err = env.run_commands(
                [
                    "tox"
                ]
            )
            os.chdir(old_dir)
            return out, err

    def get_run_result(self, log: str) -> RunResult:
        statements = -1
        missing = -1
        coverage = -1.0
        failed = -1
        passed = -1
        skipped = -1
        warnings = -1
        error = -1
        time = -1.0

        matches = re.search(
            r"([0-9]+) passed in ([0-9.]+) seconds",
            log
        )

        if matches:
            passed = int(matches.group(1)) if matches.group(1) else 0
            time = float(matches.group(2)) if matches.group(2) else 0.0

        result = RunResult(
            statements=statements,
            missing=missing,
            coverage=coverage,
            failed=failed,
            passed=passed,
            skipped=skipped,
            warnings=warnings,
            error=error,
            time=time,
        )
        return result
