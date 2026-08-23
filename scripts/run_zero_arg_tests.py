#!/usr/bin/env python3
"""Dependency-independent runner for this repository's fixture-free tests.

The suite intentionally contains unittest.TestCase methods and pytest-compatible module
functions with no fixtures.  This runner executes both forms and fails closed if a future
module-level test introduces parameters, preventing a silent skip when pytest is absent.
CI still installs and may run pytest independently.
"""
from __future__ import annotations

import argparse
import inspect
import runpy
import sys
import traceback
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def test_files(search_root: Path) -> list[Path]:
    if search_root.is_file():
        return [search_root]
    return sorted(search_root.rglob("test_*.py"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default="tests")
    args = parser.parse_args()
    search_root = (ROOT / args.path).resolve()
    try:
        search_root.relative_to(ROOT)
    except ValueError:
        print("test path must remain inside the repository")
        return 2
    files = test_files(search_root)
    if not files:
        print(f"no tests found under {search_root.relative_to(ROOT)}")
        return 2

    failures: list[str] = []
    executed = 0
    for index, path in enumerate(files):
        module_name = f"_ixsf_test_{index}"
        namespace = runpy.run_path(str(path), run_name=module_name)

        suite = unittest.TestSuite()
        for value in namespace.values():
            if (
                inspect.isclass(value)
                and issubclass(value, unittest.TestCase)
                and value is not unittest.TestCase
                and value.__module__ == module_name
            ):
                suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(value))
        result = unittest.TestResult()
        suite.run(result)
        executed += result.testsRun
        for case, detail in result.failures + result.errors:
            failures.append(f"{path.relative_to(ROOT)}::{case}\n{detail}")

        for name, value in sorted(namespace.items()):
            if not (
                name.startswith("test_")
                and inspect.isfunction(value)
                and value.__module__ == module_name
            ):
                continue
            parameters = inspect.signature(value).parameters
            if parameters:
                failures.append(
                    f"{path.relative_to(ROOT)}::{name} uses unsupported fixture/parameters: "
                    + ", ".join(parameters)
                )
                continue
            executed += 1
            try:
                value()
            except Exception:  # noqa: BLE001
                failures.append(
                    f"{path.relative_to(ROOT)}::{name}\n{traceback.format_exc()}"
                )

    if failures:
        print(f"SELF-CONTAINED TEST SUITE: {executed - len(failures)} passed, {len(failures)} failed")
        for failure in failures:
            print(failure)
        return 1
    print(f"SELF-CONTAINED TEST SUITE: {executed} passed, 0 failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
