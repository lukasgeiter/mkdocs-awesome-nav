from typing import Optional, Type

from mkdocs.utils import dirname_to_title
from pydantic import ValidationError
from yaml import YAMLError

from mkdocs_awesome_nav import log
from mkdocs_awesome_nav.log import format_log_message
from mkdocs_awesome_nav.nav.config import ConfigModel, NavConfig
from mkdocs_awesome_nav.nav.context import Directory, MkdocsFilesContext
from mkdocs_awesome_nav.nav.link import NavLink
from mkdocs_awesome_nav.nav.page import NavPage
from mkdocs_awesome_nav.nav.section import NavSection, RootSection


class NavDirectory:
    def __init__(self, directory: Directory, *, parent_config: Optional[NavConfig] = None, title: Optional[str] = None):
        self._directory = directory
        self.path = directory.path
        self.config = self._load_config(parent_config)
        self._title = title or self.config.title or self._generate_title()

    def resolve(self, context: MkdocsFilesContext) -> NavSection | NavPage | list[NavSection | NavPage]:
        context.visit(self._directory)
        section = self._create_section(context)
        return self._flatten_section(section)

    def _load_config(self, parent_config: Optional[NavConfig]):
        config_file = self._directory.config_file
        if config_file is not None:
            try:
                return NavConfig.from_file(config_file, parent=parent_config)
            except YAMLError as e:
                log.write(
                    "error",
                    format_log_message("Parsing error", config_file.src_uri) + "\n" + str(e),
                )
            except ValidationError as e:
                lines = str(e).splitlines()
                lines[0] = format_log_message("Validation error", config_file.src_uri)
                log.write("error", "\n".join(lines))

        return NavConfig(ConfigModel(), directory_path=self.path, parent=parent_config)

    def _generate_title(self) -> str:
        if self.config.preserve_directory_names:
            return self.path.name

        return dirname_to_title(self.path.name)

    def _flatten_section(self, section: NavSection) -> NavSection | NavPage | list[NavSection | NavPage]:
        if len(section.children) == 0:
            return []

        if self.config.flatten_single_child_sections and len(section.children) == 1:
            child = section.children[0]
            if isinstance(child, NavPage) or isinstance(child, NavSection):
                return child

        return section

    def _create_section(self, context: MkdocsFilesContext, *, section_type: Type[NavSection] = NavSection):
        from mkdocs_awesome_nav.nav.resolve import resolve_in_priority_order

        parsed_children = [item.parse(path=self.path, config=self.config, context=context) for item in self.config.nav]

        resolved_children: list[NavPage | NavSection | NavLink] = resolve_in_priority_order(parsed_children, context)

        return section_type(resolved_children, path=self.path, title=self._title)


class RootNavDirectory(NavDirectory):
    def __init__(self, directory: Directory):
        super().__init__(directory, title="root")

        if self.config.title is not None:
            log.write(
                log.levels.root_title or "warning",
                "'title' option has no effect at the top level",
                self.config.config_path,
            )
        if self.config.hide:
            log.write(
                log.levels.root_hide or "warning",
                "'hide' option has no effect at the top level",
                self.config.config_path,
            )

    def resolve(self, context: MkdocsFilesContext) -> NavSection:
        return super()._create_section(context, section_type=RootSection)
