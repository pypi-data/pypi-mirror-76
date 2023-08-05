# -*- coding: utf-8 -*-
#
# codimension - graphics python two-way code editor and analyzer
# Copyright (C) 2010-2017  Sergey Satskiy <sergey.satskiy@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""Codimension main window status bar"""

import os.path
from utils.pixmapcache import getIcon
from plugins.vcssupport.intervaldlg import VCSUpdateIntervalConfigDialog
from .qt import Qt, QPalette, QColor, QMenu, QDialog, QApplication
from .labels import (StatusBarPixmapLabel, StatusBarPathLabel,
                     StatusBarFramedLabel)


class MainWindowStatusBarMixin:

    """Main window status bar mixin"""

    def __init__(self):

        self.__statusBar = None
        self.sbLanguage = None
        self.sbFile = None
        self.sbEol = None
        self.sbPos = None
        self.sbLine = None
        self.sbWritable = None
        self.sbEncoding = None
        self.sbPyflakes = None
        self.sbCC = None
        self.sbVCSStatus = None
        self.sbDebugState = None
        self.__createStatusBar()

    def __createStatusBar(self):
        """Creates status bar"""
        self.__statusBar = self.statusBar()
        self.__statusBar.setSizeGripEnabled(True)

        self.sbVCSStatus = StatusBarPixmapLabel('ignore', self.__statusBar)
        self.__statusBar.addPermanentWidget(self.sbVCSStatus)
        self.sbVCSStatus.setVisible(False)
        self.sbVCSStatus.setContextMenuPolicy(Qt.CustomContextMenu)
        self.sbVCSStatus.customContextMenuRequested.connect(
            self._showVCSLabelContextMenu)

        self.sbDebugState = StatusBarFramedLabel(
            text='Debugger: unknown', callback=None, parent=self.__statusBar)
        dbgPalette = self.sbDebugState.palette()
        dbgPalette.setColor(QPalette.Background, QColor(255, 255, 127))
        self.sbDebugState.setPalette(dbgPalette)
        self.__statusBar.addPermanentWidget(self.sbDebugState)
        self.sbDebugState.setVisible(False)

        self.sbLanguage = StatusBarFramedLabel(parent=self.__statusBar)
        self.__statusBar.addPermanentWidget(self.sbLanguage)

        self.sbEncoding = StatusBarFramedLabel(parent=self.__statusBar)
        self.__statusBar.addPermanentWidget(self.sbEncoding)

        self.sbEol = StatusBarFramedLabel(parent=self.__statusBar)
        self.__statusBar.addPermanentWidget(self.sbEol)

        self.sbWritable = StatusBarFramedLabel(parent=self.__statusBar)
        self.__statusBar.addPermanentWidget(self.sbWritable)

        self.sbPyflakes = StatusBarPixmapLabel('signal', self.__statusBar)
        self.__statusBar.addPermanentWidget(self.sbPyflakes)

        self.sbCC = StatusBarPixmapLabel('signal', self.__statusBar)
        self.__statusBar.addPermanentWidget(self.sbCC)

        self.sbFile = StatusBarPathLabel(
            callback=self._onPathLabelDoubleClick,
            parent=self.__statusBar)
        self.sbFile.setMaximumWidth(512)
        self.sbFile.setMinimumWidth(128)
        self.__statusBar.addPermanentWidget(self.sbFile, True)
        self.sbFile.setContextMenuPolicy(Qt.CustomContextMenu)
        self.sbFile.customContextMenuRequested.connect(
            self._showPathLabelContextMenu)

        self.sbLine = StatusBarFramedLabel(callback=self.copyLine,
                                           parent=self.__statusBar)
        self.sbLine.setMinimumWidth(72)
        self.sbLine.setAlignment(Qt.AlignCenter)
        self.__statusBar.addPermanentWidget(self.sbLine)

        self.sbPos = StatusBarFramedLabel(callback=self.copyPos,
                                          parent=self.__statusBar)
        self.sbPos.setMinimumWidth(72)
        self.sbPos.setAlignment(Qt.AlignCenter)
        self.__statusBar.addPermanentWidget(self.sbPos)

    def copyLine(self):
        """Copies the line number to the buffer"""
        self.__copyLinePos(self.sbLine)

    def copyPos(self):
        """Copies the pos number to the buffer"""
        self.__copyLinePos(self.sbPos)

    @staticmethod
    def __copyLinePos(label):
        """Copies the line/pos label content to the buffer"""
        txt = label.text().strip().lower()
        if not txt.endswith('n/a'):
            txt = txt[txt.find(':') + 1:].strip()
            QApplication.clipboard().setText(txt)

    def showStatusBarMessage(self, msg, timeout=10000):
        """Shows a temporary status bar message, default 10sec"""
        self.__statusBar.showMessage(msg, timeout)

    def clearStatusBarMessage(self):
        """Clears the status bar message in the given slot"""
        self.__statusBar.clearMessage()

    def getCurrentStatusBarMessage(self):
        """Provides the current status bar message"""
        return self.__statusBar.currentMessage()

    def _showVCSLabelContextMenu(self, pos):
        """Triggered when a context menu is requested for a VCS label"""
        contextMenu = QMenu(self)
        contextMenu.addAction(getIcon("vcsintervalmenu.png"),
                              "Configure monitor interval",
                              self.__onVCSMonitorInterval)
        contextMenu.popup(self.sbVCSStatus.mapToGlobal(pos))

    def __onVCSMonitorInterval(self):
        """Runs the VCS monitor interval setting dialog"""
        dlg = VCSUpdateIntervalConfigDialog(
            self.settings['vcsstatusupdateinterval'], self)
        if dlg.exec_() == QDialog.Accepted:
            self.settings['vcsstatusupdateinterval'] = dlg.interval

    def _showPathLabelContextMenu(self, pos):
        """Triggered when a context menu is requested for the path label"""
        contextMenu = QMenu(self)
        contextMenu.addAction(getIcon('copymenu.png'),
                              'Copy full path to clipboard (double click)',
                              self._onPathLabelDoubleClick)
        contextMenu.addSeparator()
        contextMenu.addAction(getIcon(''), 'Copy directory path to clipboard',
                              self._onCopyDirToClipboard)
        contextMenu.addAction(getIcon(''), 'Copy file name to clipboard',
                              self._onCopyFileNameToClipboard)
        contextMenu.popup(self.sbFile.mapToGlobal(pos))

    def _onPathLabelDoubleClick(self):
        """Double click on the status bar path label"""
        txt = self.__getPathLabelFilePath()
        if txt.lower() not in ['', 'n/a']:
            QApplication.clipboard().setText(txt)

    def _onCopyDirToClipboard(self):
        """Copies the dir path of the current file into the clipboard"""
        txt = self.__getPathLabelFilePath()
        if txt.lower() not in ['', 'n/a']:
            try:
                QApplication.clipboard().setText(os.path.dirname(txt) +
                                                 os.path.sep)
            except:
                pass

    def _onCopyFileNameToClipboard(self):
        """Copies the file name of the current file into the clipboard"""
        txt = self.__getPathLabelFilePath()
        if txt.lower() not in ['', 'n/a']:
            try:
                QApplication.clipboard().setText(os.path.basename(txt))
            except:
                pass

    def __getPathLabelFilePath(self):
        """Provides undecorated path label content"""
        txt = str(self.sbFile.getPath())
        if txt.startswith('File: '):
            txt = txt.replace('File: ', '')
        return txt
