# -*- coding: utf-8 -*-
#
# codimension - graphics python two-way code editor and analyzer
# Copyright (C) 2010-2016  Sergey Satskiy <sergey.satskiy@gmail.com>
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

"""Miscellaneuos utility functions"""

# pylint: disable=W0702
# pylint: disable=W0703

import os.path
import re
import getpass
import locale
import datetime
import logging
import traceback
import gc
from .globals import GlobalData
from .settings import SETTINGS_DIR
from .fileutils import getFileContent, isFileOpenable, isCreatable


# File name of the template for any new file.
# The file is searched nearby the project file.
templateFileName = 'template.py'

# File name with pylint settings
pylintFileName = 'pylintrc'


def splitThousands(value, sep="'"):
    """Provides thousands separated value"""
    if len(value) <= 3:
        return value
    return splitThousands(value[:-3], sep) + sep + value[-3:]


def getLocaleDate():
    """Provides locale formatted date"""
    now = datetime.datetime.now()
    try:
        date_format = locale.nl_langinfo(locale.D_FMT)
        return now.strftime(date_format)
    except:
        return now.strftime('%Y-%m-%d')


def getLocaleTime():
    """Provides locale formatted time"""
    now = datetime.datetime.now()
    try:
        time_format = locale.nl_langinfo(locale.T_FMT)
        return now.strftime(time_format)
    except:
        return now.strftime('%H:%M:%S')


def getLocaleDateTime():
    """Provides locale date time"""
    return getLocaleDate() + " " + getLocaleTime()


def getIDETemplateFile():
    """Provides the name of the IDE template file"""
    return SETTINGS_DIR + templateFileName


def getIDEPylintFile():
    """Provides the name of the IDE pylintrc file"""
    return SETTINGS_DIR + pylintFileName


def getProjectTemplateFile():
    """Provides the name of the project template file"""
    project = GlobalData().project
    if project.isLoaded():
        # Project is loaded - use from the project dir
        projectDir = os.path.dirname(project.fileName)
        if not projectDir.endswith(os.path.sep):
            projectDir += os.path.sep
        return projectDir + templateFileName
    return None


def getNewFileTemplate():
    """Searches for the template file and fills fields in it"""
    templateFile = getProjectTemplateFile()
    if templateFile is None:
        templateFile = getIDETemplateFile()
    elif not os.path.exists(templateFile):
        templateFile = getIDETemplateFile()

    if not os.path.exists(templateFile):
        return ""

    # read the file content: splitlines() eats the trailing \n
    content = getFileContent(templateFile)
    if content.endswith('\n') or content.endswith('\r\n'):
        content = content.splitlines() + ['']
    else:
        content = content.splitlines()

    # substitute the fields
    project = GlobalData().project
    projectLoaded = project.isLoaded()
    if projectLoaded:
        subs = [(re.compile(re.escape('$projectdate'), re.I),
                 project.props['creationdate']),
                (re.compile(re.escape('$author'), re.I),
                 project.props['author']),
                (re.compile(re.escape('$license'), re.I),
                 project.props['license']),
                (re.compile(re.escape('$copyright'), re.I),
                 project.props['copyright']),
                (re.compile(re.escape('$version'), re.I),
                 project.props['version']),
                (re.compile(re.escape('$email'), re.I),
                 project.props['email'])]
    else:
        subs = []

    # Common substitutions
    subs.append((re.compile(re.escape('$date'), re.I),
                 getLocaleDate()))
    subs.append((re.compile(re.escape('$time'), re.I),
                 getLocaleTime()))
    subs.append((re.compile(re.escape('$user'), re.I),
                 getpass.getuser()))

    if projectLoaded:
        # description could be multilined so it is a different story
        descriptionRegexp = re.compile(re.escape('$description'), re.I)
        description = project.props['description'].split('\n')

    result = []
    for line in content:
        for key, value in subs:
            line = re.sub(key, value, line)
        if projectLoaded:
            # description part if so
            match = re.search(descriptionRegexp, line)
            if match is not None:
                # description is in the line
                leadingPart = line[:match.start()]
                trailingPart = line[match.end():]
                for dline in description:
                    result.append(leadingPart + dline + trailingPart)
            else:
                result.append(line)
        else:
            result.append(line)

    return '\n'.join(result)


def getDefaultTemplate():
    """Provides a body (i.e. help) of the default template file"""
    return """#
# This template will be used when a new file is created.
#
# Codimension supports an IDE-wide template file and project-specific template
# files for each project. If a project is loaded then codimension checks the
# project-specific template file and IDE-wide one in this order. The first one
# found is used to create a new file. If no project is loaded then only the
# IDE-wide template file is checked.
# The IDE-wide template file is stored in the codimension settings directory
# while project-specific template files are stored in the top project
# directory. In both cases the template file is called 'template.py'.
#
# The following variables will be replaced with actual values if
# they are found in the template:
#
# $projectdate     Project creation date     (*)
# $author          Project author            (*)
# $license         Project license           (*)
# $copyright       Project copyright string  (*)
# $version         Project version           (*)
# $email           Project author e-mail     (*)
# $description     Project description       (*)
# $date            Current date
# $time            Current time
# $user            Current user name
#
# Note: variables marked with (*) are available only for the project-specific
#       templates. The values for the variables are taken from the project
#       properties dialogue.
#"""


def getDefaultProjectDoc(fName):
    """Provides a body (i.e. help) of the default project doc"""
    return """The project documentation is not found.

Codimension supports the markdown format for documentation purposes
and there are a few options to create and specify the project documentation
start point:

- create an .md file anywhere on the file system and specify the path to it in
  the project properties
- simply create the README.md in the project root directory (%s)

Please discard these instructions, provide the required content and save as
needed. If you do so, next time the project doc button is clicked, the project
doc markdown file will be displayed.
""".replace('%s', fName)


def getDefaultFileDoc(fName, anchor):
    """Provides a body (i.e. help) of the default auto doc"""
    return """Codimension supports markdown for the documentation purposes.

A doc link to this file has been inserted into your python file. When it
is clicked on the graphics pane this file will be displayed.

The source code doc link also has a generated anchor (${anchor}) so the
documentation can refer specifically to that doc link. To do so use the
following format:

```
[See in the source code](file:${fName}#${anchor})
```

When clicked, the source code file will be opened and scrolled to the doc link.

Please discard these instructions, provide the required content and save as
needed.
""".replace('${fName}', fName).replace('${anchor}', anchor)


# Dynamic mixin at runtime:
# http://stackoverflow.com/questions/8544983/
#        dynamically-mixin-a-base-class-to-an-instance-in-python
def extendInstance(obj, cls):
    """dynamic mixin support"""
    base_cls = obj.__class__
    base_cls_name = obj.__class__.__name__
    obj.__class__ = type(base_cls_name, (base_cls, cls), {})


ANCHOR_REGEXP = re.compile(r'\#[_a-zA-Z0-9]+$')

# Supported format:
# [file:]<absolute or relative path>[#anchor identifier]
def splitLinkPath(link):
    """Splits the link path into the path and the anchor"""
    if link.startswith('file:'):
        link = link[5:]
    link = os.path.normpath(link)

    anchor = None
    match = ANCHOR_REGEXP.search(link)
    if match is not None:
        anchorPart = match.group()
        anchor = anchorPart[1:]
        link = link[0:-1 * len(anchorPart)].strip()
    return link, anchor


def resolveFile(link, fromFile):
    """Tries to reslve file

    Returns: file name, list of tried paths
    """
    if os.path.isabs(link):
        if os.path.exists(link):
            return link, [link]
        return None, [link]

    tryPaths = []
    if fromFile:
        # Try relative to the 'fromFile' first
        dirName = os.path.dirname(fromFile)
        fName = os.path.normpath(dirName + os.path.sep + link)
        if os.path.exists(fName):
            return fName, [fName]
        tryPaths.append(fName)

    # Try relative to the project file second
    project = GlobalData().project
    if project.isLoaded():
        # Project is loaded - use from the project dir
        projectDir = os.path.dirname(project.fileName)
        fName = os.path.normpath(projectDir + os.path.sep + link)
        if fName not in tryPaths:
            if os.path.exists(fName):
                return fName, [fName]
            tryPaths.append(fName)

    return None, tryPaths


def checkExistingLinkTarget(fName):
    """Returns an error message or None if everything is fine"""
    if not os.path.isfile(fName):
        return ' '.join(("The resolved link path",
                         "'" + fName + "'",
                         "does not point to a file"))

    if not isFileOpenable(fName):
        return ' '.join(("The resolved link path",
                         "'" + fName + "'",
                         "does not point to a file which Codimension can open"))
    return None


# Used when the user clicks on a link
def resolveLinkPath(link, fromFile):
    """Resolves the link to the another file"""
    effectiveLink, anchor = splitLinkPath(link)
    fName, tryPaths = resolveFile(effectiveLink, fromFile)

    # fName is not None => file exists on FS
    if not fName:
        logging.error("The link '%s' does not point to an existing file. "
                      "Resolve tries: %s",effectiveLink, ', '.join(tryPaths))
        return None, None

    errMsg = checkExistingLinkTarget(fName)
    if errMsg:
        logging.error(errMsg)
        return None, None

    # All is good: it is a file, it is openable
    return fName, anchor


# Used in a dialog to suggest validity of the further operation
def preResolveLinkPath(link, fromFile, canBeCreated):
    """Tries to resolve the link and repors an error if any"""
    effectiveLink, anchor = splitLinkPath(link)
    fName, tryPaths = resolveFile(effectiveLink, fromFile)

    # Here: the file must not exist
    # If it exists then it should be a file and openable
    # If it does not then it should be creatable
    if fName:
        errMsg = checkExistingLinkTarget(fName)
        if errMsg:
            return None, None, errMsg
        return fName, anchor, None

    if not tryPaths:
        return None, None, \
               "The link '" + effectiveLink + \
               "' is invalid. Use an absolute path or save the file first."

    if canBeCreated:
        for path in tryPaths:
            canCreate, _ = isCreatable(path)
            if canCreate:
                # Can be created here
                return path, anchor, None

        return None, None, \
           "The link '" + effectiveLink + \
           "' points to non existing file which cannot be created due to " \
           "lack of permissions or invalid path. Tried paths: " + \
           ", ".join(tryPaths)

    return None, None, \
        "The link '" + effectiveLink + \
        "' does not point to an existing file"

def printStack(limit=100):
    """Prints the stack in the log window"""
    lines = []
    for line in traceback.format_stack():
        lines.append(line.strip())

    # The last item is this very one so strip it
    lines = lines[:-1]

    if len(lines) > limit:
        lines = lines[-limit:]
    print('\n'.join(lines))


def printReferences(obj):
    """Prints the object references"""
    if obj is None:
        print('No object to print references')
    else:
        refs = gc.get_referrers(obj)
        print('Object references (total ' + str(len(refs)) + '):')
        for item in refs:
            print('---')
            print(type(item))
            val = repr(item)
            if len(val) > 512:
                print('Truncated: ' + val[:512])
            else:
                print(val)

