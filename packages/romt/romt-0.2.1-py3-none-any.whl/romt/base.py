#!/usr/bin/env python3
# coding=utf-8

import argparse
from pathlib import Path
from typing import List, Optional

from romt import error
import romt.download


def verify_commands(commands: List[str], valid_commands: List[str]) -> None:
    for command in commands:
        if command not in valid_commands:
            raise error.UsageError("invalid COMMAND {}".format(repr(command)))


def add_downloader_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--assume-ok",
        action="store_true",
        default=False,
        help="assume already-downloaded files are OK (skip hash check)",
    )


class BaseMain:
    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args
        self._downloader = None  # type: Optional[romt.download.Downloader]

    @property
    def downloader(self) -> romt.download.Downloader:
        if self._downloader is None:
            self._downloader = romt.download.Downloader()
        return self._downloader

    def get_archive_path(self) -> Path:
        if not self.args.archive:
            raise error.UsageError("missing archive name")
        return Path(self.args.archive)
