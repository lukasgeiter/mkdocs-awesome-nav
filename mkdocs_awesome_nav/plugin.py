from mkdocs.config import Config, config_options
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin, event_priority
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation, get_navigation
from mkdocs.structure.pages import Page

from mkdocs_awesome_nav.log import log_warning
from mkdocs_awesome_nav.nav.context import MkdocsFilesContext
from mkdocs_awesome_nav.nav.directory import RootNavDirectory


class AwesomeNavConfig(Config):
    filename = config_options.Type(str, default=".nav.yml")


class AwesomeNavPlugin(BasePlugin[AwesomeNavConfig]):
    @event_priority(100)
    def on_nav(self, nav: Navigation, config: MkDocsConfig, files: Files) -> Navigation:
        if config.nav is not None:
            log_warning("'nav' config from mkdocs.yml is being replaced with one generated by awesome-nav")

        context = MkdocsFilesContext(files, self.config.filename)

        # clear pages created by mkdocs
        for file in files.documentation_pages():
            # check type for compatibility with material blog (preserve View objects)
            if type(file.page) is Page:
                file.page = None

        original_nav_config = config.nav
        config.nav = RootNavDirectory(context.root).resolve(context).to_mkdocs_config()
        nav = get_navigation(files, config)
        config.nav = original_nav_config

        return nav
