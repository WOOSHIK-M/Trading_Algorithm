#!/usr/bin/env python3
#
#  MAKINAROCKS CONFIDENTIAL
#  ________________________
#
#  [2017] - [2020] MakinaRocks Co., Ltd.
#  All Rights Reserved.
#
#  NOTICE:  All information contained herein is, and remains
#  the property of MakinaRocks Co., Ltd. and its suppliers, if any.
#  The intellectual and technical concepts contained herein are
#  proprietary to MakinaRocks Co., Ltd. and its suppliers and may be
#  covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law. Dissemination
#  of this information or reproduction of this material is
#  strictly forbidden unless prior written permission is obtained
#  from MakinaRocks Co., Ltd.
import argparse
import re
import subprocess
from typing import Any, Optional, Set


# reference by https://github.com/pre-commit/pre-commit-hooks/blob/master/pre_commit_hooks/util.py
class CalledProcessError(RuntimeError):
    pass


def added_files() -> Set[str]:
    cmd = ("git", "diff", "--staged", "--name-only", "--diff-filter=A")
    return set(cmd_output(*cmd).splitlines())


def cmd_output(*cmd: str, retcode: Optional[int] = 0, **kwargs: Any) -> str:
    kwargs.setdefault("stdout", subprocess.PIPE)
    kwargs.setdefault("stderr", subprocess.PIPE)
    proc = subprocess.Popen(cmd, **kwargs)
    stdout, stderr = proc.communicate()
    stdout = stdout.decode()
    if retcode is not None and proc.returncode != retcode:
        raise CalledProcessError(cmd, retcode, proc.returncode, stdout, stderr)
    return stdout


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="license-checker")
    parser.add_argument("--license-file-path", type=str, default="./LICENSE")
    parsed = parser.parse_args()

    content = []
    pattern = ""
    with open(parsed.license_file_path, "r") as f:
        for line in f:
            pattern += r"^.*" + line.strip() + r".*$\n"

    filenames = added_files()
    for filename in filenames:
        if filename.endswith(".py") or filename.endswith(".ipynb"):
            with open(filename) as fp:
                content = fp.read()
                if not re.search(pattern, content, re.MULTILINE):
                    raise RuntimeError(
                        f'File "{filename}" does not contain correct license clauses!'
                    )
