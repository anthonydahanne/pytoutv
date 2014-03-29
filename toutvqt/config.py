from PyQt4.Qt import QDir
from PyQt4.Qt import QSettings
from PyQt4 import QtCore
from PyQt4 import Qt
import logging


class QTouTvConfig(Qt.QObject):
    _DEFAULT_DOWNLOAD_DIRECTORY = QDir.home().absoluteFilePath('TOU.TV Downloads')
    config_item_changed = QtCore.pyqtSignal(str, object)

    def __init__(self):
        super(QTouTvConfig, self).__init__()
        self._fill_defaults()
        self._config_dict = {}
        self.config_item_changed.connect(self.tmp)

    def _fill_defaults(self):
        """Fills defaults with sensible default values."""
        self.defaults = {}
        def_dl_dir = QTouTvConfig._DEFAULT_DOWNLOAD_DIRECTORY
        self.defaults['files/download_directory'] = def_dl_dir
        self.defaults['network/http_proxy'] = None

    def write_settings(self):
        settings = QSettings()
        settings.clear()

        for k in self._config_dict:
            if k in self.defaults:
                if self._config_dict[k] != self.defaults[k]:
                    settings.setValue(k, self._config_dict[k])
            else:
                msg = 'Config key {} not found in defaults'.format(k)
                logging.warning(msg)
                settings.setValue(k, self._config_dict[k])

    def read_settings(self):
        settings = QSettings()
        read_config = self.defaults.copy()
        keys = settings.allKeys()

        for k in keys:
            read_config[k] = settings.value(k)

        self.apply_config(read_config)

    def apply_config(self, new_config):
        for key in new_config:
            new_value = new_config[key]
            if key in self._config_dict:
                if new_value != self._config_dict[key]:
                    # Value changed
                    self.config_item_changed.emit(key, new_value)
            else:
                # New config key
                self.config_item_changed.emit(key, new_value)
            self._config_dict[key] = new_config[key]

        self.write_settings()

    def debug_print_config(self):
        print(self._config_dict)

    def tmp(self, k, v):
        print("%s changed to %s" % (k, v))
