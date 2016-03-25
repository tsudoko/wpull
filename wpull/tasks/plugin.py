import asyncio
import gettext
import logging

from yapsy.PluginManager import PluginManager

from wpull.backport.logging import BraceMessage as __
from wpull.pipeline.pipeline import ItemTask
from wpull.tasks.app import AppSession

_logger = logging.getLogger(__name__)
_ = gettext.gettext


class PluginSetupTask(ItemTask[AppSession]):
    @asyncio.coroutine
    def process(self, session: AppSession):
        session.plugin_manager = PluginManager(plugin_info_ext='wpull-plugin')

        if session.args.plugin_script:
            session.plugin_manager.setPluginPlaces([session.args.plugin_script])

        session.plugin_manager.collectPlugins()

        for plugin_info in session.plugin_manager.getAllPlugins():
            _logger.info(__(
                _('Found plugin {name} from {filename}.'),
                filename=plugin_info.path,
                name=plugin_info.name
            ))

            plugin_info.plugin_object.app_session = session
            session.plugin_manager.activatePluginByName(plugin_info.name)
