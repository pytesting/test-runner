# -*- coding: utf-8 -*-
import os
import re
from typing import Union, Optional, Tuple, Dict, Any

from pytesting_utils import virtualenv

from testrunner.runners.abstract_runner import AbstractRunner


class PyTestRunner(AbstractRunner):
    def __init__(
        self, project_name: str, path: Union[bytes, str, os.PathLike]
    ) -> None:
        super().__init__(project_name, path)

    def run(self) -> Optional[Tuple[str, str]]:
        # TODO make sure nothing goes wrong here

        with virtualenv(self._project_name) as env:
            old_dir = os.getcwd()
            os.chdir(self._path)

            if "-" in self._project_name and os.path.exists(
                os.path.join(os.getcwd(), self._project_name.replace("-", ""))
            ):
                project_name = self._project_name.replace("-", "")
            elif "_" in self._project_name and os.path.exists(
                os.path.join(os.getcwd(), self._project_name.replace("_", ""))
            ):
                project_name = self._project_name.replace("_", "")
            elif "-" in self._project_name and os.path.exists(
                os.path.join(os.getcwd(), self._project_name.replace("-", "_"))
            ):
                project_name = self._project_name.replace("-", "_")
            elif os.path.exists(os.path.join(os.getcwd(), self._project_name)):
                project_name = self._project_name
            else:
                directories = [
                    o
                    for o in os.listdir(os.getcwd())
                    if os.path.isdir(os.path.join(os.getcwd(), o))
                ]
                if len(directories) > 2:
                    project_name = self._project_name
                else:
                    project_name = "."
                for d in directories:
                    if self._project_name in d:
                        project_name = d
                        break

            packages = self._extract_necessary_packages()
            env.add_packages_for_installation(packages)
            env.add_package_for_installation("pytest")
            env.add_package_for_installation("pytest-cov")
            out, err = env.run_commands(
                [
                    "pytest --cov={} --cov-report=term-missing".format(
                        project_name
                    )
                ]
            )
            os.chdir(old_dir)
            return out, err

    def get_total_result(self, log: str) -> Optional[Tuple[int, int, str]]:
        matches = re.search(
            r"TOTAL\s+"
            r"([0-9]+)\s+"
            r"([0-9]+)\s+"
            r"(([0-9]+)\s+([0-9]+)\s+)?"
            r"([0-9]+%)",
            log,
        )
        if matches:
            statements = int(matches.group(1)) if matches.group(1) else 0
            missing = int(matches.group(2)) if matches.group(2) else 0
            coverage = matches.group(6) if matches.group(6) else "0.0%"
            return statements, missing, coverage
        else:
            matches = re.search(
                r".py\s+"
                r"([0-9]+)\s+"
                r"([0-9]+)\s+"
                r"(([0-9]+)\s+([0-9]+)\s+)?"
                r"([0-9]+%)",
                log,
            )
            if matches:
                statements = int(matches.group(1)) if matches.group(1) else 0
                missing = int(matches.group(2)) if matches.group(2) else 0
                coverage = matches.group(6) if matches.group(6) else "0.0%"
                return statements, missing, coverage
        return None

    def get_summary_result(self, log: str) -> Optional[Dict[str, Any]]:
        matches = re.search(
            r"[=]+ (([0-9]+) failed, )?"
            r"([0-9]+) passed"
            r"(, ([0-9]+) skipped)?"
            r"(, ([0-9]+) warnings)?"
            r"(, ([0-9]+) error)?"
            r" in ([0-9.]+) seconds",
            log,
        )
        if matches:
            return {
                "failed": int(matches.group(2)) if matches.group(2) else 0,
                "passed": int(matches.group(3)) if matches.group(3) else 0,
                "skipped": int(matches.group(5)) if matches.group(5) else 0,
                "warnings": int(matches.group(7)) if matches.group(7) else 0,
                "error": int(matches.group(9)) if matches.group(9) else 0,
                "time": float(matches.group(10)) if matches.group(10) else 0.0,
            }
        return None
