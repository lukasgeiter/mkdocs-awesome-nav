from __future__ import annotations

from functools import cached_property
from pathlib import PurePosixPath
from typing import Annotated, Literal, Optional

import yaml
from mkdocs.structure.files import File
from pydantic import BaseModel, Field, RootModel

from mkdocs_awesome_nav.nav.context import Directory, MkdocsFilesContext, Page
from mkdocs_awesome_nav.nav.link import NavLink
from mkdocs_awesome_nav.nav.page import NavPage
from mkdocs_awesome_nav.nav.section import NavSection
from mkdocs_awesome_nav.utils import create_absolute_pattern

NonEmptyString = Annotated[str, Field(min_length=1)]

inherit_token = "$inherit"


class NavConfig:
    def __init__(
        self,
        model: ConfigModel,
        *,
        directory_path: PurePosixPath,
        config_path: Optional[PurePosixPath] = None,
        parent: Optional[NavConfig] = None,
    ):
        self._model = model
        self._directory_path = directory_path
        self.config_path = config_path
        self._parent = parent

    @cached_property
    def nav(self) -> list[NavConfigItem]:
        nav = self._model.nav.copy()
        if self.append_unmatched:
            nav.append(NavConfigItemPatternOptions(glob="*", ignore_no_matches=True))
        return nav

    @cached_property
    def title(self) -> Optional[str]:
        return self._model.title

    @cached_property
    def hide(self) -> bool:
        return self._model.hide

    @cached_property
    def preserve_directory_names(self) -> bool:
        return (
            self._model.preserve_directory_names
            if self._model.preserve_directory_names is not None
            else self._parent.preserve_directory_names
            if self._parent is not None
            else False
        )

    @cached_property
    def flatten_single_child_sections(self) -> bool:
        return (
            self._model.flatten_single_child_sections
            if self._model.flatten_single_child_sections is not None
            else self._parent.flatten_single_child_sections
            if self._parent is not None
            else False
        )

    @cached_property
    def use_index_title(self) -> bool:
        return (
            self._model.use_index_title
            if self._model.use_index_title is not None
            else self._parent.use_index_title
            if self._parent is not None
            else False
        )

    @cached_property
    def sort(self) -> SortConfig:
        by = self._model.sort.by
        direction = self._model.sort.direction
        type = self._model.sort.type
        sections = self._model.sort.sections
        ignore_case = self._model.sort.ignore_case

        if self._parent:
            by = by or self._parent.sort.by
            direction = direction or self._parent.sort.direction
            type = type or self._parent.sort.type
            sections = sections or self._parent.sort.sections
            ignore_case = ignore_case or self._parent.sort.ignore_case

        return SortConfig(
            by=by or "path",
            direction=direction or "asc",
            type=type or "natural",
            sections=sections or "last",
            ignore_case=ignore_case or False,
        )

    @cached_property
    def ignore(self) -> list[str]:
        patterns = list()
        for pattern in self._model.ignore.patterns:
            if pattern == inherit_token:
                if self._parent is not None:
                    patterns.extend(self._parent.ignore)
            else:
                base_path = self._directory_path
                if pattern.startswith("/"):
                    pattern = pattern.removeprefix("/")
                else:
                    base_path /= "**"

                patterns.append(create_absolute_pattern(base_path, pattern))

        return patterns

    @cached_property
    def append_unmatched(self) -> bool:
        return (
            self._model.append_unmatched
            if self._model.append_unmatched is not None
            else self._parent.append_unmatched
            if self._parent is not None
            else False
        )

    @staticmethod
    def from_file(file: File, parent: Optional[NavConfig] = None) -> NavConfig:
        path = PurePosixPath(file.src_uri)
        return NavConfig(
            ConfigModel.from_yaml(file.content_string),
            directory_path=path.parent,
            parent=parent,
            config_path=path,
        )


class SortConfig(BaseModel):
    by: Optional[Literal["path", "filename", "title"]] = None
    direction: Optional[Literal["asc", "desc"]] = None
    type: Optional[Literal["natural", "alphabetical"]] = None
    sections: Optional[Literal["first", "last", "mixed"]] = None
    ignore_case: Optional[bool] = None


class IgnoreConfig(RootModel):
    root: Optional[NonEmptyString | list[NonEmptyString]] = None

    @property
    def patterns(self) -> list[str]:
        if self.root is None:
            return [inherit_token]
        if isinstance(self.root, list):
            return self.root
        return [self.root]


class NavConfigItemStr(RootModel):
    root: NonEmptyString

    def parse(self, *, path: PurePosixPath, config: NavConfig, context: MkdocsFilesContext):
        from mkdocs_awesome_nav.nav.directory import NavDirectory
        from mkdocs_awesome_nav.nav.pattern import NavPattern

        file_object = context.get_by_path(path / self.root)

        if isinstance(file_object, Page):
            return NavPage(file_object)
        elif isinstance(file_object, Directory):
            return NavDirectory(file_object, parent_config=config)
        else:
            return NavPattern(self.root, path=path, config=config)


class NavConfigItemDict(RootModel):
    root: Annotated[dict[NonEmptyString, NonEmptyString | list[NavConfigItem]], Field(min_length=1, max_length=1)]

    def parse(self, *, path: PurePosixPath, context: MkdocsFilesContext, config: NavConfig):
        from mkdocs_awesome_nav.nav.directory import NavDirectory

        (key, value) = list(self.root.items())[0]
        if isinstance(value, str):
            file_object = context.get_by_path(path / value)
            if isinstance(file_object, Page):
                return NavPage(file_object, title=key)
            elif isinstance(file_object, Directory):
                return NavDirectory(file_object, parent_config=config, title=key)
            else:
                return NavLink(value, title=key)
        elif isinstance(value, list):
            children = [item.parse(path=path, config=config, context=context) for item in value]
            return NavSection(children, path=path, title=key)


class NavConfigItemPatternOptions(BaseModel):
    glob: NonEmptyString
    flatten_single_child_sections: Optional[bool] = None
    preserve_directory_names: Optional[bool] = None
    sort: SortConfig = SortConfig()
    ignore: IgnoreConfig = IgnoreConfig()
    append_unmatched: Optional[bool] = None
    ignore_no_matches: bool = False

    def parse(self, *, path: PurePosixPath, context: MkdocsFilesContext, config: NavConfig):
        from mkdocs_awesome_nav.nav.pattern import NavPattern

        local_config = NavConfig(
            ConfigModel(
                sort=self.sort,
                flatten_single_child_sections=self.flatten_single_child_sections,
                preserve_directory_names=self.preserve_directory_names,
                ignore=self.ignore,
                append_unmatched=self.append_unmatched,
            ),
            directory_path=path,
            config_path=config.config_path,
            parent=config,
        )

        return NavPattern(self.glob, path=path, config=local_config, ignore_no_matches=self.ignore_no_matches)


NavConfigItem = NavConfigItemStr | NavConfigItemDict | NavConfigItemPatternOptions


class ConfigModel(BaseModel):
    title: Optional[NonEmptyString] = None
    hide: bool = False
    flatten_single_child_sections: Optional[bool] = None
    preserve_directory_names: Optional[bool] = None
    use_index_title: Optional[bool] = None
    sort: SortConfig = SortConfig()
    ignore: IgnoreConfig = IgnoreConfig()
    nav: list[NavConfigItem] = [
        NavConfigItemPatternOptions(glob="@(index.md|README.md)", ignore_no_matches=True),
        NavConfigItemPatternOptions(glob="*", ignore_no_matches=True),
    ]
    append_unmatched: Optional[bool] = None

    @staticmethod
    def from_yaml(contents: str) -> ConfigModel:
        data = yaml.safe_load(contents) or {}
        return ConfigModel(**data)
