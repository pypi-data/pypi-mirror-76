#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Artella About plugin implementation
"""

from __future__ import print_function, division, absolute_import

import logging

import artella
from artella import dcc
from artella.core import dcc as core_dcc
from artella.core import plugin, utils, qtutils

if qtutils.QT_AVAILABLE:
    from artella.externals.Qt import QtWidgets

logger = logging.getLogger('artella')


class AboutPlugin(plugin.ArtellaPlugin, object):

    ID = 'artella-plugins-about'
    INDEX = 101

    def __init__(self, config_dict=None, manager=None):
        super(AboutPlugin, self).__init__(config_dict=config_dict, manager=manager)

    def about(self):
        """
        Shows an about window that shows information about current installed Artella plugin
        """

        about_dialog = AboutDialog()
        about_dialog.exec_()


class AboutDialog(artella.Dialog, object):
    def __init__(self, parent=None, **kwargs):
        super(AboutDialog, self).__init__(parent, **kwargs)

        self.setWindowTitle('About Artella Plugin')

        self._fill_data()

    def get_main_layout(self):
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)

        return main_layout

    def setup_ui(self):
        super(AboutDialog, self).setup_ui()

        core_layout = QtWidgets.QHBoxLayout()
        core_layout.setContentsMargins(2, 2, 2, 2)
        core_layout.setSpacing(2)
        core_label = QtWidgets.QLabel('Artella Core version: ')
        self._artella_core_version_label = QtWidgets.QLabel()
        core_layout.addWidget(core_label)
        core_layout.addWidget(self._artella_core_version_label)
        core_layout.addStretch()

        dcc_layout = QtWidgets.QHBoxLayout()
        dcc_layout.setContentsMargins(2, 2, 2, 2)
        dcc_layout.setSpacing(2)
        self._artella_dcc_label = QtWidgets.QLabel()
        self._artella_dcc_version_label = QtWidgets.QLabel()
        dcc_layout.addWidget(self._artella_dcc_label)
        dcc_layout.addWidget(self._artella_dcc_version_label)
        dcc_layout.addStretch()

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setContentsMargins(2, 2, 2, 2)
        button_layout.setSpacing(2)
        self._show_plugins_btn = QtWidgets.QPushButton('Show Plugins')
        button_layout.addStretch()
        button_layout.addWidget(self._show_plugins_btn)
        button_layout.addStretch()

        self._plugins_tree = QtWidgets.QTreeWidget()
        self._plugins_tree.setHeaderLabels(['Name', 'Version', 'ID'])
        self._plugins_tree.setColumnCount(3)
        self._plugins_tree.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self._plugins_tree.setVisible(False)

        self.main_layout.addStretch()
        self.main_layout.addLayout(core_layout)
        self.main_layout.addLayout(dcc_layout)
        self.main_layout.addLayout(button_layout)
        self.main_layout.addStretch()
        self.main_layout.addLayout(button_layout)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self._plugins_tree)

        self._show_plugins_btn.clicked.connect(self._on_toggle_plugins_visibility)

    def _fill_data(self):
        added_packages = dict()

        # Retrieve Artella core version
        core_version = None
        core_version_path = 'artella.__version__'
        try:
            core_version_mod = utils.import_module(core_version_path)
            core_version = core_version_mod.get_version()
        except Exception as exc:
            logger.warning('Impossible to retrieve Artella Core version: {}'.format(exc))
        if core_version:
            self._artella_core_version_label.setText(core_version)
        else:
            self._artella_core_version_label.setText('Undefined')

        # Retrieve DCC plugin version
        dcc_name = dcc.name()
        self._artella_dcc_label.setText('Artella {} Version: '.format(dcc_name.title()))
        dcc_version = None
        dcc_module_name = core_dcc.CURRENT_DCC_MODULE
        if dcc_module_name:
            try:
                dcc_module_version = '{}.__version__'.format(dcc_module_name)
                dcc_version_mod = utils.import_module(dcc_module_version)
                dcc_version = dcc_version_mod.get_version()
            except Exception as exc:
                logger.warning('Impossible to retrieve DCC Artella plugin version: {}'.format(exc))
        if dcc_version:
            self._artella_dcc_version_label.setText(dcc_version)
        else:
            self._artella_dcc_version_label.setText('Undefined')

        # Retrieve Artella plugins versions
        plugins = artella.PluginsMgr().plugins
        for plugin_id, plugin_data in plugins.items():
            plugin_package = plugin_data.get('package', 'Not Defined')
            package_item = added_packages.get(plugin_package, None)
            if not package_item:
                package_item = QtWidgets.QTreeWidgetItem([plugin_package])
                self._plugins_tree.addTopLevelItem(package_item)
                added_packages[plugin_package] = package_item
            plugin_name = plugin_data['name']
            plugin_version = plugin_data.get('version', 'Undefined')
            plugin_item = QtWidgets.QTreeWidgetItem([plugin_name, plugin_version, plugin_id])
            package_item.addChild(plugin_item)

        self._plugins_tree.expandAll()
        self._plugins_tree.resizeColumnToContents(0)
        self._plugins_tree.resizeColumnToContents(1)
        self._plugins_tree.resizeColumnToContents(2)

    def _on_toggle_plugins_visibility(self):
        self._plugins_tree.setVisible(not self._plugins_tree.isVisible())
        self._show_plugins_btn.setText('Show Plugins' if not self._plugins_tree.isVisible() else 'Hide Plugins')
        self.resize(self.sizeHint())
