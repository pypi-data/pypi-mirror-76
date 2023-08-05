# -*- coding: utf-8 -*-
"""
    saltfactories.plugins.logserver
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Salt Factories log server plugin
"""
import logging
import attr
from saltfactories.utils import ports
from saltfactories.utils.log_server import log_server_listener

@attr.s(kw_only=True, slots=True, frozen=True)
class LogServer:
    pluginmanager = attr.ib(repr=False)
    log_host = attr.ib(default="0.0.0.0")
    log_port = attr.ib(default=attr.Factory(ports.get_unused_localhost_port))
    log_level = attr.ib(init=False, repr=False)
    _log_server = attr.ib(init=False, repr=False)

    @log_level.default
    def _set_log_level(self):
        # If PyTest has no logging configured, default to ERROR level
        levels = [logging.ERROR]
        logging_plugin = self.pluginmanager.get_plugin("logging-plugin")
        try:
            level = logging_plugin.log_cli_handler.level
            if level is not None:
                levels.append(level)
        except AttributeError:
            # PyTest CLI logging not configured
            pass
        try:
            level = logging_plugin.log_file_level
            if level is not None:
                levels.append(level)
        except AttributeError:
            # PyTest Log File logging not configured
            pass

        level_str = logging.getLevelName(min(levels))
        return level_str

    @_log_server.default
    def _instantiate_log_server(self):
        return log_server_listener(self.log_host, self.log_port)

    def start(self):
        self._log_server.__enter__()

    def stop(self):
        self._log_server.__exit__()
