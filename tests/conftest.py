import logging
import os
from pathlib import Path

import pytest
import yaml
from _pytest.logging import LogCaptureFixture
from mkdocs.commands.build import build
from mkdocs.config import load_config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin, event_priority
from mkdocs.structure import StructureItem
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Link, Navigation, Section
from mkdocs.structure.pages import Page


class MkdocsFixture:
    def __init__(self):
        self.files(
            """
            docs/
            mkdocs.yml
            | site_name: Test
            | plugins:
            |   - awesome-nav
            """
        )

    def files(self, template: str, base_path: Path = Path(".")):
        lines = template.splitlines()

        def _process_lines(path: Path, parent_indentation: int):
            while lines:
                line = lines.pop(0).rstrip()
                line_contents = line.lstrip()
                indentation = len(line) - len(line_contents)
                if not line_contents:
                    continue
                if indentation <= parent_indentation:
                    lines.insert(0, line)
                    return
                if line_contents.endswith("/"):
                    directory = path / line_contents
                    directory.mkdir(parents=True, exist_ok=True)
                    _process_lines(directory, indentation)
                else:
                    contents = ""
                    while lines and lines[0].strip().startswith("|"):
                        contents += f"{lines.pop(0).strip()[2:]}\n"

                    file = path / line_contents
                    file.write_text(contents)

        _process_lines(base_path, 0)

    def docs(self, template: str):
        self.files(template, Path("docs"))

    def build(self, **kwargs):
        config = load_config(**kwargs)
        nav_assertion = NavAssertionPlugin()
        config.plugins["nav-assertion"] = nav_assertion
        build(config)
        return nav_assertion


class NavAssertionPlugin(BasePlugin):
    def __init__(self) -> None:
        super().__init__()
        self.navs: list[Navigation] = []

    @event_priority(-100)
    def on_nav(self, nav: Navigation, config: MkDocsConfig, files: Files):
        self.navs.append(nav)

    def assert_nav(self, *expected: str):
        assert [self._to_plain(nav.items) for nav in self.navs] == [yaml.safe_load(expected) for expected in expected]

    def assert_nav_empty(self):
        self.assert_nav("[]")

    def _to_plain(self, items: list[StructureItem]):
        return [self._to_plain_item(item) for item in items]

    def _to_plain_item(self, item: StructureItem):
        if isinstance(item, Page):
            return {item.title: item.file.src_uri}
        if isinstance(item, Link):
            return {item.title: item.url}
        if isinstance(item, Section):
            return {item.title: self._to_plain(item.children)}


@pytest.fixture
def mkdocs(tmp_path):
    saved_path = os.getcwd()
    os.chdir(tmp_path)
    yield MkdocsFixture()
    os.chdir(saved_path)


class LogsFixture:
    def __init__(self, caplog: LogCaptureFixture):
        self._caplog = caplog

    @property
    def all(self):
        return [(r.levelno, r.getMessage()) for r in self._caplog.records]

    @property
    def from_plugin(self):
        return [(r.levelno, r.getMessage()) for r in self._caplog.records if r.name == "mkdocs.plugins.awesome-nav"]

    @staticmethod
    def info(message: str):
        return logging.INFO, message

    @staticmethod
    def warning(message: str):
        return logging.WARNING, message

    @staticmethod
    def error(message: str):
        return logging.ERROR, message


@pytest.fixture
def logs(caplog):
    caplog.set_level(logging.INFO)
    return LogsFixture(caplog)
