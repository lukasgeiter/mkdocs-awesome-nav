from collections.abc import Callable
from pathlib import PurePosixPath
from typing import Any, cast

from mkdocs.utils.meta import get_data
from natsort import natsort_keygen, ns
from wcmatch import glob

from mkdocs_awesome_nav import log
from mkdocs_awesome_nav.nav.config import NavConfig
from mkdocs_awesome_nav.nav.context import Directory, MkdocsFilesContext, Page
from mkdocs_awesome_nav.nav.directory import NavDirectory
from mkdocs_awesome_nav.nav.page import NavPage
from mkdocs_awesome_nav.nav.section import NavSection
from mkdocs_awesome_nav.utils import create_absolute_pattern


class NavPattern:
    def __init__(self, pattern: str, *, path: PurePosixPath, config: NavConfig, ignore_no_matches: bool = False):
        self.pattern = pattern
        self.path = path
        self.config = config
        self._ignore_no_matches = ignore_no_matches

    def resolve(self, context: MkdocsFilesContext) -> list[NavPage | NavSection]:
        from mkdocs_awesome_nav.nav.resolve import resolve_in_priority_order

        matches = self._find_matches(context)

        if len(matches) == 0 and not self._ignore_no_matches:
            log.write(
                log.levels.no_matches or "warning",
                f"The nav item '{self.pattern}' doesn't match any files or directories",
                self.config.config_path,
            )

        items: list[NavPage | NavSection] = resolve_in_priority_order(matches, context)

        self._sort_items(items)

        return items

    def _find_matches(self, context: MkdocsFilesContext):
        absolut_pattern = create_absolute_pattern(self.path, self.pattern)
        matches: list[NavPage | NavDirectory] = []

        for file_object in context.unvisited:
            path = file_object.path.as_posix()
            if isinstance(file_object, Directory):
                path += "/"

            if glob.globmatch(
                path,
                absolut_pattern,
                flags=glob.GLOBSTAR | glob.EXTGLOB,
                exclude=self.config.ignore,
            ):
                if isinstance(file_object, Page):
                    matches.append(NavPage(file_object))
                elif isinstance(file_object, Directory):
                    directory_item = NavDirectory(file_object, parent_config=self.config)
                    if not directory_item.config.hide:
                        matches.append(directory_item)

        return matches

    def _sort_items(self, items: list[NavPage | NavSection]) -> None:
        key = self._sort_key_by_path
        if self.config.sort.by == "filename":
            key = self._sort_key_by_filename
        if self.config.sort.by == "title":
            key = self._sort_key_by_title

        if self.config.sort.type == "natural":
            natsort_flags = ns.GROUPLETTERS | ns.INT
            if self.config.sort.by != "title":
                natsort_flags |= ns.PATH
            if self.config.sort.ignore_case:
                natsort_flags |= ns.IGNORECASE
            key = cast(Any, natsort_keygen(key=key, alg=natsort_flags))
        elif self.config.sort.ignore_case:
            key = self._casefold_sort_key(key)

        items.sort(key=key, reverse=self.config.sort.direction == "desc")

        if self.config.sort.sections != "mixed":

            def _sort_key_type(item: NavPage | NavSection):
                if isinstance(item, NavSection):
                    return 2
                return 1

            items.sort(
                key=_sort_key_type,
                reverse=self.config.sort.sections == "first",
            )

    @staticmethod
    def _sort_key_by_path(item: NavPage | NavSection):
        return NavPattern._get_item_path(item).as_posix()

    @staticmethod
    def _sort_key_by_filename(item: NavPage | NavSection):
        path = NavPattern._get_item_path(item)
        return path.name, path.as_posix()

    @staticmethod
    def _sort_key_by_title(item: NavPage | NavSection):
        path = NavPattern._get_item_path(item)
        if isinstance(item, NavSection):
            return item.title, path.name, path.as_posix()

        markdown, metadata = get_data(item.page.file.content_string)
        return metadata.get("title") or item.page.path.name, path.name, path.as_posix()

    @staticmethod
    def _get_item_path(item: NavPage | NavSection):
        if isinstance(item, NavSection):
            return item.path
        return item.page.path

    @staticmethod
    def _casefold_sort_key(key: Callable[[NavPage | NavSection], tuple[str, str] | str]):
        def _casefolded_key(item: NavPage | NavSection):
            value = key(item)
            if isinstance(value, str):
                return value.casefold()
            return tuple([item.casefold() for item in value])

        return _casefolded_key
