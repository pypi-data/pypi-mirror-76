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

"""Global data singleton"""

# pylint: disable=W0702
# pylint: disable=W0703

import os
from os.path import sep, realpath, isdir, exists, isfile
from distutils.spawn import find_executable
from plugins.manager.pluginmanager import CDMPluginManager
from .project import CodimensionProject
from .briefmodinfocache import BriefModuleInfoCache
from .settings import SETTINGS_DIR


# This function needs to have a rope project built smart
def getSubdirs(path, baseNamesOnly=True, excludePythonModulesDirs=True):
    """Provides a list of sub directories for the given path"""
    subdirs = []
    try:
        path = realpath(path) + sep
        for item in os.listdir(path):
            candidate = path + item
            if isdir(candidate):
                if excludePythonModulesDirs:
                    modFile = candidate + sep + "__init__.py"
                    if exists(modFile):
                        continue
                if baseNamesOnly:
                    subdirs.append(item)
                else:
                    subdirs.append(candidate)
    except:
        pass
    return subdirs


class GlobalDataWrapper:

    """Global data singleton"""

    def __init__(self):
        self.application = None
        self.mainWindow = None
        self.skin = None
        self.screenWidth = 0
        self.screenHeight = 0
        self.version = "unknown"
        self.originalSysPath = None
        self.searchProviders = {}

        self.project = CodimensionProject()

        self.pluginManager = CDMPluginManager()

        self.briefModinfoCache = BriefModuleInfoCache()

        self.graphvizAvailable = self.__checkGraphviz()
        self.javaAvailable = self.__checkJava()
        self.hexdumpAvailable = self.__checkHexdump()

    def getProfileOutputPath(self, procuuid):
        """Provides the path to the profile output file"""
        if self.project.isLoaded():
            return self.project.userProjectDir + procuuid + '.profile.out'

        # No project loaded
        return SETTINGS_DIR + procuuid + '.profile.out'

    def getProjectImportDirs(self):
        """Provides a list of the project import dirs if so"""
        if not self.project.isLoaded():
            return []
        return self.project.getImportDirsAsAbsolutePaths()

    def isProjectScriptValid(self):
        """True if the project script valid"""
        scriptName = self.project.getProjectScript()
        if not scriptName:
            return False
        if not exists(scriptName):
            return False
        if not isfile(scriptName):
            return False

        from .fileutils import isPythonFile
        return isPythonFile(scriptName)

    def getFileLineDocstring(self, fName, line):
        """Provides a docstring if so for the given file and line"""
        from .fileutils import isPythonFile
        if not isPythonFile(fName):
            return ''

        infoCache = self.briefModinfoCache

        def checkFuncObject(obj, line):
            """Checks docstring for a function or a class"""
            if obj.line == line or obj.keywordLine == line:
                if obj.docstring is None:
                    return True, ''
                return True, obj.docstring.text
            for item in obj.classes + obj.functions:
                found, docstring = checkFuncObject(item, line)
                if found:
                    return True, docstring
            return False, ''

        try:
            info = infoCache.get(fName)
            for item in info.classes + info.functions:
                found, docstring = checkFuncObject(item, line)
                if found:
                    return docstring
        except:
            pass
        return ''

    def getModInfo(self, path):
        """Provides a module info for the given file"""
        from .fileutils import isPythonFile
        if not isPythonFile(path):
            raise Exception('Trying to parse non-python file: ' + path)
        return self.briefModinfoCache.get(path)

    def registerSearchProvider(self, cls):
        """Registers a search provider"""
        self.searchProviders[cls.getName()] = cls

    @staticmethod
    def __checkGraphviz():
        """Checks if graphviz is available"""
        return find_executable('dot') is not None

    @staticmethod
    def __checkJava():
        """Checks if java is available"""
        return find_executable('java') is not None

    @staticmethod
    def __checkHexdump():
        """Checks if hexdump is available"""
        return find_executable('hexdump') is not None


globalsSingleton = GlobalDataWrapper()


def GlobalData():
    """Global singleton access"""
    return globalsSingleton
