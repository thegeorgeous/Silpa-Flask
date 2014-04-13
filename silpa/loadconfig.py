__all__ = ['IncompleteConfigError', 'config']

import ConfigParser
import os

class IncompleteConfigError(Exception):
    def __init__(self, section, option):
        self.section = section
        self.option = option

    def __str__(self):
        if self.option is not None:
            return ">> Missing option {option} in section {section}" + \
                "of config file".format(option=self.option,
                                        section=self.section)
        else:
            return ">> Missiong section {section} in config file".format(
                section=self.section)


class _Config(ConfigParser.ConfigParser):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(_Config, cls).__new__(cls, *args, **kwargs)
            return cls._instance

    def __init__(self, location="silpa.conf"):
        ConfigParser.ConfigParser.__init__(self)
        self.read(location)
        self.verify

    def verify(self):
        self._verify_item("main", "site")
        self._verify_item("main", "baseurl")
        self._verify_item("logging", "log_level")
        self._verify_item("logging", "log_folder")
        self._verify_item("logging", "log_name")

        if not self.has_section("modules"):
            raise IncompleteConfigError("modules", None)

        if not self.has_section("modules_display"):
            raise IncompleteConfigError("modules_display")

    def _verify_item(self, section, option):
        if not self.has_option(section, option):
            raise IncompleteConfigError(section, option)

config = _Config(os.path.join(os.path.dirname(__file__), "silpa.conf"))