#!/usr/bin/env python3
# coding=utf-8

import argparse
from pathlib import Path
import re
import shutil
from typing import (
    List,
    Set,
    Tuple,
)

from romt import base
from romt import common
from romt import dist
from romt import error
from romt import integrity
from romt import signature
from romt.manifest import Manifest, Package

description = """\
Mirror and manage toolchain artifacts.
"""

epilog = """\

SPEC is one of:
  <channel>
  <channel>-YYYY-MM-DD
  <channel>-latest
  <channel>-*
  *-YYYY-MM-DD
  *-latest
  *-*
  YYYY-MM-DD
  latest
  *
Where:
- <channel> is one of: nightly, beta, stable, X.Y.Z
- Single ``*`` represents date, not channel; equivalent to ``*-*``.
- Multiple SPEC options may be given.
- Each SPEC option will be split at commas and whitespace.

TARGET is standard 3- or 4-tuple; common examples:
- x86_64-unknown-linux-gnu (alias ``linux``)
- x86_64-pc-windows-msvc (alias ``windows``)
- x86_64-apple-darwin (alias ``darwin``)

COMMAND values:
  Typical:
    download        download artifacts matching SPEC and TARGET to DEST
    pack            pack DEST artifacts matching SPEC and TARGET into ARCHIVE
    unpack          unpack ARCHIVE into DEST, setting SPEC and TARGET
  Less common:
    fetch-manifest  download manifest matching SPEC and TARGET to DEST
    verify          verify DEST artifacts matching SPEC and TARGET
    list            print DEST artifacts and targets matching SPEC
    all-targets     print all known targets mentioned in SPEC
    fixup           publish manifest variants for SPEC, updating undated

When multiple COMMANDs are given, they share all option values.

For complete details, try ``romt --readme`` to view README.rst.
"""


def parse_spec(spec: str) -> Tuple[str, str]:
    """parse spec into (date, channel).

    Forms with channel:
      <channel>
      <channel>-YYYY-MM-DD
      <channel>-latest
      <channel>-*
      *-YYYY-MM-DD
      *-latest
      *-*
    Forms with only date:
      YYYY-MM-DD
      latest
      *

    Where:
    - <channel> is one of: nightly, beta, stable, X.Y.Z
    - Single ``*`` represents date, not channel; equivalent to ``*-*``.

    """

    # Single "*" is treated as wildcard for date, not channel.
    if spec == "*":
        return "*", "*"

    channel_rex = r"""
        (?P<channel>
            nightly | beta | stable | \* | (?: \d+\.\d+\.\d+ )
        )
        """

    date_rex = r"""
        (?P<date>
            \d\d\d\d-\d\d-\d\d | latest | \*
        )
        """

    m = re.match(
        r"{} (?: - {})? $".format(channel_rex, date_rex), spec, re.VERBOSE
    )
    if m:
        channel = m.group("channel")
        date = m.group("date") or ""
        return date, channel

    m = re.match(r"{} $".format(date_rex), spec, re.VERBOSE)
    if m:
        date = m.group("date")
        return date, "*"

    raise error.UsageError("invalid SPEC {}".format(repr(spec)))


def channel_rel_path(date: str, channel: str) -> str:
    channel_name = "channel-rust-{}.toml".format(channel)
    if date:
        rel_path = "{}/{}".format(date, channel_name)
    else:
        rel_path = "{}".format(channel_name)
    return rel_path


def add_arguments(parser: argparse.ArgumentParser) -> None:
    base.add_downloader_arguments(parser)

    parser.add_argument(
        "-s",
        "--select",
        action="append",
        dest="specs",
        metavar="SPEC",
        default=[],
        help="""one or more SPEC values for toolchain selection""",
    )

    parser.add_argument(
        "-t",
        "--target",
        action="append",
        dest="targets",
        default=[],
        help="""target to download (default varies by COMMAND)""",
    )

    parser.add_argument(
        "--dest",
        action="store",
        default="dist",
        help="""local download directory (default: %(default)s)""",
    )

    parser.add_argument(
        "--url",
        action="store",
        default="https://static.rust-lang.org/dist",
        help="""base URL of dist (default: %(default)s)""",
    )

    parser.add_argument(
        "--archive",
        action="store",
        metavar="ARCHIVE",
        default="toolchain.tar.gz",
        help="use archive ARCHIVE for pack/unpack (default: %(default)s)",
    )

    parser.add_argument(
        "--warn-signature",
        action="store_true",
        default=False,
        help="warn (instead of fail) on signature verification failure",
    )

    parser.add_argument(
        "--no-signature",
        action="store_true",
        default=False,
        help="disable all uses of signature files (*.asc); mainly for testing",
    )

    parser.add_argument(
        "commands",
        nargs="*",
        metavar="COMMAND",
        help="""commands to execute in the order given""",
    )


class Main(dist.DistMain):
    def __init__(self, args: argparse.Namespace) -> None:
        super().__init__(args)
        self.downloader.set_warn_signature(args.warn_signature)
        self._with_sig = not args.no_signature

    def manifest_url_path(self, date: str, channel: str) -> Tuple[str, Path]:
        rel_path = channel_rel_path(date, channel)
        manifest_url = self.url_from_rel_path(rel_path)
        manifest_path = self.dest_path_from_rel_path(rel_path)
        return manifest_url, manifest_path

    def manifest_path(self, date: str, channel: str) -> Path:
        _, man_path = self.manifest_url_path(date, channel)
        return man_path

    def get_manifest(
        self, date: str, channel: str, *, download: bool
    ) -> Manifest:
        man_url, man_path = self.manifest_url_path(date, channel)
        if download:
            if date:
                # Dated manifests may always be cached.
                cached = True
            else:
                # Undated manifests should always be re-downloaded.  They
                # might be newer than what's on disk (either because of the
                # passage of time or because a fixup operation might overwrite
                # the undated manifest with old information before a download).
                cached = False
            self.downloader.download_verify(
                man_url, man_path, cached=cached, with_sig=self._with_sig
            )
        else:
            self.downloader.verify(man_path, with_sig=self._with_sig)
        return Manifest.from_toml_path(man_path)

    def select_manifest(
        self, spec: str, *, download: bool, canonical: bool = False
    ) -> Manifest:
        date, channel = parse_spec(spec)
        manifest = self.get_manifest(date, channel, download=download)
        if canonical and (
            manifest.date != date or manifest.channel != channel
        ):
            manifest = self.get_manifest(
                manifest.date, manifest.channel, download=download
            )
        return manifest

    def channels_in_dest_date(self, date: str) -> List[str]:
        date_path = self.dest_path / date
        prefix = "channel-rust-"
        suffix = ".toml"
        channels = [
            p.name[len(prefix) : -len(suffix)]
            for p in date_path.glob(prefix + "*" + suffix)
        ]
        return channels

    def adjust_download_specs(self, specs: List[str]) -> List[str]:
        # For downloads, require explicit date and channel.
        for spec in specs:
            date, channel = parse_spec(spec)
            if "*" in (date, channel) or date == "latest":
                raise error.UsageError("invalid wild SPEC: {}".format(spec))
        return dist.require_specs(specs)

    def expand_wild_spec(self, spec: str) -> List[str]:
        specs = []  # type: List[str]
        date, channel = parse_spec(spec)
        if "*" in (date, channel) or date == "latest":
            if channel == "*":
                channel_patterns = set("nightly beta stable".split())
            else:
                channel_patterns = set([channel])
            if date in ("*", "latest"):
                dates = common.reversed_date_dir_names(self.dest_path)
            else:
                dates = [date]
            for d in dates:
                channels = channel_patterns.intersection(
                    self.channels_in_dest_date(d)
                )
                specs.extend(
                    "{}-{}".format(channel, d) for channel in channels
                )
                if date == "latest" and specs:
                    break
        else:
            specs.append(spec)

        if not specs:
            raise error.UsageError(
                "no matches for wild SPEC {}".format(repr(spec))
            )

        return specs

    def adjust_wild_specs(self, specs: List[str]) -> List[str]:
        # For non-downloads, handle wild specs.
        adjusted_specs = []
        for spec in specs:
            adjusted_specs.extend(self.expand_wild_spec(spec))
        return dist.require_specs(adjusted_specs)

    def downloaded_packages(self, manifest: Manifest) -> List[Package]:
        packages = []
        for package_info in manifest.gen_available_packages():
            dest_path = self.dest_path_from_rel_path(package_info.rel_path)
            if dest_path.is_file():
                packages.append(package_info)
        return packages

    def downloaded_targets(self, manifest: Manifest) -> List[str]:
        targets = set(p.target for p in self.downloaded_packages(manifest))
        targets.discard("*")
        return sorted(targets)

    def adjust_targets(
        self, manifest: Manifest, base_targets: List[str]
    ) -> List[str]:
        possible_targets = set(p.target for p in manifest.gen_packages())
        targets = set()
        for target in base_targets:
            if target == "all":
                targets.update(possible_targets)
            elif target == "*":
                targets.update(self.downloaded_targets(manifest))
            elif target not in possible_targets:
                raise error.UsageError(
                    "target {} not found in manifest".format(repr(target))
                )
            else:
                targets.add(target)
        return sorted(targets)

    def cmd_fetch_manifest(self) -> None:
        for spec in self.adjust_download_specs(self.specs):
            common.iprint("Fetch manifest: {}".format(spec))
            manifest = self.select_manifest(spec, download=True)
            common.iprint("  ident: {}".format(manifest.ident))

    def _download_verify(
        self, download: bool, specs: List[str], base_targets: List[str]
    ) -> None:
        for spec in specs:
            common.iprint(
                "{}: {}".format("Download" if download else "Verify", spec)
            )
            manifest = self.select_manifest(
                spec, download=download, canonical=True
            )
            common.iprint("  ident: {}".format(manifest.ident))

            targets = self.adjust_targets(manifest, base_targets)
            packages = list(manifest.gen_available_packages(targets=targets))
            common.iprint(
                "  packages: {}, targets: {}".format(
                    len(packages), len(targets)
                )
            )
            for t in targets:
                common.vvprint("  target: {}".format(t))

            for package in packages:
                rel_path = package.rel_path
                dest_path = self.dest_path_from_rel_path(rel_path)
                dest_url = self.url_from_rel_path(rel_path)
                if download:
                    self.downloader.download_verify(
                        dest_url,
                        dest_path,
                        assume_ok=self.args.assume_ok,
                        with_sig=self._with_sig,
                    )
                else:
                    self.downloader.verify(dest_path, with_sig=self._with_sig)

    def cmd_download(self) -> None:
        specs = self.adjust_download_specs(self.specs)
        base_targets = dist.require_targets(self.targets)
        self._download_verify(
            download=True, specs=specs, base_targets=base_targets
        )

    def cmd_verify(self) -> None:
        specs = self.adjust_wild_specs(self.specs)
        base_targets = dist.require_targets(self.targets, default="*")
        self._download_verify(
            download=False, specs=specs, base_targets=base_targets
        )

    def cmd_list(self) -> None:
        max_verbosity = common.get_max_verbosity()
        show_details = max_verbosity >= common.VERBOSITY_INFO
        for spec in self.adjust_wild_specs(self.specs):
            common.vprint("List: {}".format(spec))
            manifest = self.select_manifest(spec, download=False)
            if show_details:
                available_packages = manifest.available_packages()
                available_targets = manifest.available_targets()
                packages = self.downloaded_packages(manifest)
                targets = self.downloaded_targets(manifest)

                target_out = "targets[{}/{}]".format(
                    len(targets), len(available_targets),
                )
                package_out = "packages[{}/{}]".format(
                    len(packages), len(available_packages),
                )
                # Example output:
                #   stable-2020-01-30(1.41.0)    \
                #     targets[84/84], packages[272/326]
                common.iprint(
                    "{:28} {:16} {:18}".format(
                        manifest.ident, target_out, package_out
                    )
                )
                for target in targets:
                    common.iprint("  {}".format(target))
            else:
                common.eprint(manifest.ident)

    def cmd_all_targets(self) -> None:
        for spec in self.adjust_wild_specs(self.specs):
            common.iprint("All targets: {}".format(spec))
            manifest = self.select_manifest(spec, download=False)
            common.iprint("  ident: {}".format(manifest.ident))
            for target in manifest.all_targets():
                common.eprint(target)

    def cmd_pack(self) -> None:
        base_targets = dist.require_targets(self.targets, default="*")
        archive_path = self.get_archive_path()
        common.iprint("Packing archive: {}".format(archive_path))
        with common.tar_context(archive_path, "w") as tar_f:

            def pack_path(rel_path: str) -> None:
                dest_path = self.dest_path_from_rel_path(rel_path)
                packed_name = "dist/" + rel_path
                common.vprint("[pack] {}".format(rel_path))
                try:
                    tar_f.add(str(dest_path), packed_name)
                except FileNotFoundError:
                    raise error.MissingFileError(str(dest_path))

            def pack_rel_path(rel_path: str) -> None:
                pack_path(rel_path)
                pack_path(integrity.append_hash_suffix(rel_path))
                if self._with_sig:
                    pack_path(signature.append_sig_suffix(rel_path))

            for spec in self.adjust_wild_specs(self.specs):
                common.iprint("Pack: {}".format(spec))
                manifest = self.select_manifest(
                    spec, download=False, canonical=True
                )
                common.iprint("  ident: {}".format(manifest.ident))

                targets = self.adjust_targets(manifest, base_targets)
                packages = list(
                    manifest.gen_available_packages(targets=targets)
                )
                common.iprint(
                    "  packages: {}, targets: {}".format(
                        len(packages), len(targets)
                    )
                )
                for t in targets:
                    common.vvprint("  target: {}".format(t))

                # Pack channel file.
                pack_rel_path(
                    channel_rel_path(manifest.date, manifest.channel)
                )

                # Pack up package file parts.
                for package in packages:
                    pack_rel_path(package.rel_path)

    def _detect_specs(self, rel_paths: Set[str]) -> List[str]:
        specs = []
        for rel_path in rel_paths:
            m = re.match(
                r"""
                (?P<date>\d\d\d\d-\d\d-\d\d)
                /channel-rust-
                (?P<channel>nightly|stable|beta)
                \.toml$
                """,
                rel_path,
                re.VERBOSE,
            )
            if m:
                date = m.group("date")
                channel = m.group("channel")
                specs.append("{}-{}".format(channel, date))
        return specs

    def _detect_targets(
        self, specs: List[str], rel_paths: Set[str]
    ) -> List[str]:
        targets = set()
        for spec in specs:
            manifest = self.select_manifest(spec, download=False)
            for package in manifest.gen_available_packages():
                if package.target != "*" and package.rel_path in rel_paths:
                    targets.add(package.target)
        return sorted(targets)

    def cmd_unpack(self) -> None:
        archive_path = self.get_archive_path()
        common.iprint("Unpacking archive: {}".format(archive_path))
        dist_prefix = "dist/"
        extracted = set()
        with common.tar_context(archive_path, "r") as tar_f:
            for tar_info in tar_f:
                if tar_info.isdir():
                    continue
                if not tar_info.name.startswith(dist_prefix):
                    raise error.UnexpectedArchiveMemberError(tar_info.name)

                rel_path = tar_info.name[len(dist_prefix) :]
                dest_path = self.dest_path_from_rel_path(rel_path)
                tar_info.name = str(dest_path)
                common.vprint("[unpack] {}".format(rel_path))
                tar_f.extract(tar_info)
                extracted.add(rel_path)

        specs = self._detect_specs(extracted)
        targets = self._detect_targets(specs, extracted)

        common.iprint("Unpacked specs: {}".format(len(specs)))
        for spec in specs:
            common.iprint("  {}".format(spec))

        common.iprint("Unpacked targets: {}".format(len(targets)))
        for target in targets:
            common.iprint("  {}".format(target))

        self.specs = specs
        self.targets = targets

    def _write_manifest(
        self, manifest: Manifest, date: str, channel: str
    ) -> None:
        src_path = self.manifest_path(manifest.date, manifest.channel)
        dst_path = self.manifest_path(date, channel)
        common.iprint("[publish] {}".format(dst_path))
        shutil.copyfile(src_path, dst_path)
        src_hash_path = integrity.path_append_hash_suffix(src_path)
        dst_hash_path = integrity.path_append_hash_suffix(dst_path)
        shutil.copyfile(src_hash_path, dst_hash_path)
        src_sig_path = signature.path_append_sig_suffix(src_path)
        dst_sig_path = signature.path_append_sig_suffix(dst_path)
        shutil.copyfile(src_sig_path, dst_sig_path)

    def _write_manifest_variations(self, manifest: Manifest) -> None:
        date = manifest.date
        channel = manifest.channel

        # Write top-level manifest, unless a newer one already exists, e.g.:
        #   dist/channel-rust-nightly.toml
        top_path = self.manifest_path("", channel)
        if top_path.is_file():
            top_man = self.get_manifest("", channel, download=False)
            write_top = manifest.date >= top_man.date
        else:
            write_top = True
        if write_top:
            self._write_manifest(manifest, "", channel)

        if channel == "stable":
            # Write version-numbered manifests, e.g.:
            #   dist/yyyy-mm-dd/channel-rust-x.y.z.toml
            #   dist/channel-rust-x.y.z.toml
            self._write_manifest(manifest, date, manifest.version)
            self._write_manifest(manifest, "", manifest.version)

    def cmd_fixup(self) -> None:
        for spec in self.adjust_wild_specs(self.specs):
            common.iprint("Fixup: {}".format(spec))
            manifest = self.select_manifest(
                spec, download=False, canonical=True
            )
            common.vprint("  ident: {}".format(manifest.ident))
            self._write_manifest_variations(manifest)

    def run(self) -> None:
        valid_commands = [
            "fetch-manifest",
            "download",
            "verify",
            "list",
            "all-targets",
            "pack",
            "unpack",
            "fixup",
        ]
        commands = self.args.commands
        if commands:
            base.verify_commands(commands, valid_commands)
        else:
            common.iprint("nothing to do; try a COMMAND")
            return

        for cmd in commands:
            if cmd == "fetch-manifest":
                self.cmd_fetch_manifest()

            elif cmd == "download":
                self.cmd_download()
                self.cmd_fixup()

            elif cmd == "verify":
                self.cmd_verify()

            elif cmd == "list":
                self.cmd_list()

            elif cmd == "all-targets":
                self.cmd_all_targets()

            elif cmd == "pack":
                self.cmd_pack()

            elif cmd == "unpack":
                self.cmd_unpack()
                self.cmd_verify()
                self.cmd_fixup()

            elif cmd == "fixup":
                self.cmd_fixup()
