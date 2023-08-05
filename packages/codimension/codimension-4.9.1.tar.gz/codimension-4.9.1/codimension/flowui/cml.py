# -*- coding: utf-8 -*-
#
# codimension - graphics python two-way code editor and analyzer
# Copyright (C) 2015-2017  Sergey Satskiy <sergey.satskiy@gmail.com>
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

"""CML utilities"""

from sys import maxsize
from cdmcfparser import (IF_FRAGMENT, FOR_FRAGMENT, WHILE_FRAGMENT,
                         TRY_FRAGMENT, CONTROL_FLOW_FRAGMENT, CLASS_FRAGMENT,
                         FUNCTION_FRAGMENT, CML_COMMENT_FRAGMENT)
from utils.colorfont import buildColor, cssLikeColor


def escapeCMLTextValue(src):
    """Escapes the string before inserting it to the code (CML value)"""
    dst = ''
    for char in src:
        if char == '\n':
            dst += '\\n'
        elif char in ('"', '\\'):
            dst += '\\' + char
        else:
            dst += char
    return dst


def unescapeCMLTextValue(src):
    """Removes escaping from the value received from the code"""
    dst = ''
    lastIndex = len(src) - 1
    index = 0
    while index <= lastIndex:
        if src[index] == '\\' and index < lastIndex:
            if src[index + 1] == '\\':
                dst += '\\'
                index += 1
            elif src[index + 1] == 'n':
                dst += '\n'
                index += 1
            elif src[index + 1] == '"':
                dst += '"'
                index += 1
            else:
                dst += '\\'     # forgiving the other escape characters
        else:
            dst += src[index]
        index += 1
    return dst


def appendTextItem(name, value):
    """Provides a line to append"""
    if value:
        if ' ' in value or '"' in value:
            return ' ' + name + '="' + escapeCMLTextValue(value) + '"'
        return ' ' + name + '=' + escapeCMLTextValue(value)
    return ''


class CMLColorBase:

    """Covers the common colors for CML comments"""

    def __init__(self):
        self.bgColor = None         # background color
        self.fgColor = None         # foreground color
        self.border = None          # border color

    def populateColors(self):
        """Populate colors"""
        if "bg" in self.ref.properties:
            self.bgColor = buildColor(self.ref.properties["bg"])
        if "fg" in self.ref.properties:
            self.fgColor = buildColor(self.ref.properties["fg"])
        if "border" in self.ref.properties:
            self.border = buildColor(self.ref.properties["border"])

    @staticmethod
    def generateColors(background, foreground, border):
        """Generates the colors part"""
        parts = []
        if background is not None:
            parts.append('bg=' + cssLikeColor(background))
        if foreground is not None:
            parts.append('fg=' + cssLikeColor(foreground))
        if border is not None:
            parts.append('border=' + cssLikeColor(border))
        return ' '.join(parts)



class CMLCommentBase:

    """Base class for all the CML comments"""

    def __init__(self, ref=None):
        self.ref = ref
        self.kind = CML_COMMENT_FRAGMENT

    def validateRecordType(self, code):
        """Validates the record type"""
        if self.ref.recordType != code:
            raise Exception("Invalid CML comment type. "
                            "Expected: '" + code + "'. Received: '" +
                            self.ref.recordType + "'.")

    def __isSideComment(self, editor):
        """True if it is a side comment"""
        # The only first part needs to be checked
        firstPart = self.ref.parts[0]
        # Editor has 0-based lines
        leftStripped = editor.lines[firstPart.beginLine - 1].lstrip()
        return not leftStripped.startswith(firstPart.getContent())

    def removeFromText(self, editor):
        """Removes the comment from the code"""
        # Note: it is supposed that the 'with editor:' is done outside.
        #       This is because the required changes could be done for more
        #       than one place.
        if editor is None:
            return

        isSideComment = self.__isSideComment(editor)

        oldLine, oldPos = editor.cursorPosition
        line = self.ref.endLine
        while line >= self.ref.beginLine:
            if isSideComment:
                raise Exception("Side CML comments removal "
                                "has not been implemented yet")
            else:
                # Editor has 0-based lines
                del editor.lines[line - 1]
                if oldLine >= line - 1:
                    oldLine -= 1
            line -= 1

        editor.cursorPosition = oldLine, oldPos

    def getLineRange(self):
        """Provides the line range"""
        # The CML comments may appear in a suite and range may be asked from
        # them to decide if the grouping is available
        return [self.ref.parts[0].beginLine,
                self.ref.parts[-1].endLine]

    def getAbsPosRange(self):
        """Provides the absolute position range"""
        return [self.ref.parts[0].begin, self.ref.parts[-1].end]

    @property
    def beginPos(self):
        return self.ref.parts[0].beginPos


class CMLsw(CMLCommentBase):

    """Covers the 'if' statement CML SW (switch branches) comments"""

    CODE = "sw"

    def __init__(self, ref):
        CMLCommentBase.__init__(self, ref)
        self.validate()

    def validate(self):
        """Validates the CML comment"""
        self.validateRecordType(CMLsw.CODE)
        CMLVersion.validate(self.ref)

    @staticmethod
    def description():
        """Provides the CML comment description"""
        return "The '" + CMLsw.CODE + \
               "' comment is used for 'if' and 'elif' statements " \
               "to switch default branch location i.e. to have " \
               "the 'No' branch at the right.\n" \
               "Supported properties: none\n\n" \
               "Example:\n" \
               "# cml 1 " + CMLsw.CODE

    @staticmethod
    def generate(pos=1):
        """Generates a complete line to be inserted"""
        return " " * (pos - 1) + "# cml 1 sw"


class CMLcc(CMLCommentBase, CMLColorBase):

    """Covers 'Custom Colors' spec for most of the items"""

    CODE = "cc"

    def __init__(self, ref):
        CMLCommentBase.__init__(self, ref)
        CMLColorBase.__init__(self)
        self.validate()

    def validate(self):
        """Validates the CML comment"""
        self.validateRecordType(CMLcc.CODE)
        CMLVersion.validate(self.ref)

        self.populateColors()
        if self.bgColor is None and \
                self.fgColor is None and self.border is None:
            raise Exception("The '" + CMLcc.CODE + "' CML comment does not "
                            "supply neither background nor foreground color "
                            "nor border color")

    @staticmethod
    def description():
        """Provides the CML comment description"""
        return "The '" + CMLcc.CODE + \
               "' comment is used for custom colors of most of " \
               "the graphics items.\n" \
               "Supported properties:\n" \
               "- color properties as described in the common section\n\n" \
               "Example:\n" \
               "# cml 1 " + CMLcc.CODE + \
               " bg=#f6f4e4 fg=#000 border=#fff"

    @staticmethod
    def generate(background, foreground, border, pos=1):
        """Generates a complete line to be inserted"""
        return  ' ' * (pos - 1) + '# cml 1 cc ' + \
                CMLColorBase.generateColors(background, foreground, border)


class CMLdoc(CMLCommentBase, CMLColorBase):

    """Covers the 'documentation link' comment"""

    CODE = "doc"

    def __init__(self, ref):
        CMLCommentBase.__init__(self, ref)
        CMLColorBase.__init__(self)
        self.link = None    # file path, abs or relative
        self.anchor = None  # id of this comment to let a link from the doc
        self.title = None   # text to display
        self.validate()

    def validate(self):
        """Validates the CMD doc comment"""
        self.validateRecordType(CMLdoc.CODE)
        CMLVersion.validate(self.ref)

        self.populateColors()

        self.link = self.ref.properties.get('link', None)
        self.anchor = self.ref.properties.get('anchor', None)
        self.title = self.ref.properties.get('title', '')

        if self.link is None and self.anchor is None:
            raise Exception("The '" + CMLdoc.CODE +
                            "' CML comment supplies neither "
                            "a link nor an anchor")
        if self.anchor:
            if ' ' in self.anchor or '\t' in self.anchor:
                raise Exception("The '" + CMLdoc.CODE +
                                "' CML comment anchor attribute "
                                "must contain neither spaces nor tabs")

    @staticmethod
    def description():
        """Provides the CML comment description"""
        return "The '" + CMLdoc.CODE + \
            "' comment is used to provide a link to a documentation.\n" \
            "Supported properties:\n" \
            "- 'link': link to the appropriate documentation\n" \
            "- 'anchor': this ID could be used to provide a link to this comment\n" \
            "- 'title': what to display on graphics\n" \
            "- color properties as described in the common section\n\n" \
            "Example:\n" \
            "# cml 1 " + CMLdoc.CODE + " link=file:doc/mydoc.md title=\"See more\""

    @staticmethod
    def generate(link, anchor, title, background, foreground, border, pos=1):
        """Generates a complete line to be inserted"""
        res = ' ' * (pos - 1) + '# cml 1 ' + CMLdoc.CODE + \
              appendTextItem('link', link) + \
              appendTextItem('anchor', anchor) + \
              appendTextItem('title', title)
        colorPart = CMLColorBase.generateColors(background, foreground, border)
        if colorPart:
            return res + ' ' + colorPart
        return res

    def getTitle(self):
        """Provides unescaped text"""
        return unescapeCMLTextValue(self.title)

    def updateCustomColors(self, editor, bgcolor, fgcolor, bordercolor):
        """Updates the custom colors"""
        firstCommentLine = self.ref.parts[0].beginLine
        pos = self.ref.parts[0].beginPos
        newCommentLine = CMLdoc.generate(self.link, self.anchor, self.title,
                                         bgcolor, fgcolor, bordercolor, pos)
        self.removeFromText(editor)
        editor.insertLines(newCommentLine, firstCommentLine)

    def removeCustomColors(self, editor):
        """Removes the custom colors"""
        self.updateCustomColors(editor, None, None, None)



class CMLrt(CMLCommentBase):

    """Covers 'Replace text' comment"""

    CODE = "rt"

    def __init__(self, ref):
        CMLCommentBase.__init__(self, ref)
        self.text = None
        self.validate()

    def validate(self):
        """Validates the CML rt comment"""
        self.validateRecordType(CMLrt.CODE)
        CMLVersion.validate(self.ref)

        self.text = self.ref.properties.get("text", None)

        if self.text is None:
            raise Exception("The '" + CMLrt.CODE +
                            "' CML comment does not supply text")

    @staticmethod
    def description():
        """Provides the CML comment description"""
        return "The '" + CMLrt.CODE + \
               "' comment is used for replacing the text of most of " \
               "the graphics items.\n" \
               "Supported properties:\n" \
               "- 'text': text to be shown instead of the real code\n\n" \
               "Example:\n" \
               "# cml 1 " + CMLrt.CODE + " text=\"Reset the dictionary\""

    @staticmethod
    def generate(txt, pos=1):
        """Generates a complete line to be inserted"""
        return " " * (pos - 1) + "# cml 1 " + CMLrt.CODE + \
               appendTextItem('text', txt)

    def getText(self):
        """Provides unescaped text"""
        if self.text is None:
            return None
        return unescapeCMLTextValue(self.text)


class CMLgb(CMLCommentBase, CMLColorBase):

    """Covers the 'group begin' comment"""

    CODE = 'gb'

    def __init__(self, ref):
        CMLCommentBase.__init__(self, ref)
        CMLColorBase.__init__(self)
        self.id = None
        self.title = None
        self.validate()

    def validate(self):
        """Validates the CML gb comment"""
        self.validateRecordType(CMLgb.CODE)
        CMLVersion.validate(self.ref)

        self.populateColors()

        self.title = self.ref.properties.get('title', None)
        if 'id' in self.ref.properties:
            self.id = self.ref.properties['id'].strip()

        if not self.id:
            raise Exception("The '" + CMLgb.CODE +
                            "' CML comment does not supply id")

    @staticmethod
    def description():
        """Provides the CML comment description"""
        return "The '" + CMLgb.CODE + \
               "' is used to indicate the beginning of the visual group. It " \
               "needs a counterpart " + CMLge.CODE + " CML comment which " \
               "indicates the end of the visual group.\n" \
               "Supported properties:\n" \
               "- 'title': title to be shown when the group is collapsed\n" \
               "- 'id': unique identifier of the visual group\n" \
               "- color properties as described in the common section\n\n" \
               "Example:\n" \
               "# cml 1 " + CMLgb.CODE + " id=\"1234-5678-444444\" " \
               "title=\"MD5 calculation\""

    @staticmethod
    def generate(groupid, title, background, foreground, border, pos=1):
        """Generates a complete line to be inserted"""
        res = ' ' * (pos - 1) + '# cml 1 ' + CMLgb.CODE + \
              appendTextItem('id', groupid) + \
              appendTextItem('title', title)
        colorPart = CMLColorBase.generateColors(background, foreground, border)
        if colorPart:
            return res + ' ' + colorPart
        return res

    def getTitle(self):
        """Provides unescaped title"""
        if self.title is None:
            return None
        return unescapeCMLTextValue(self.title)

    def updateTitle(self, editor, newTitle):
        """Updates the group title in the editor"""
        if newTitle == self.title:
            return

        firstCommentLine = self.ref.parts[0].beginLine
        lastCommentLine = self.ref.parts[-1].endLine
        if self.title is None:
            # Need to add the title= attribute to the last comment line
            lastLine = editor.lines[lastCommentLine - 1]
            newLastLine = lastLine.rstrip() + ' title="' + \
                escapeCMLTextValue(newTitle) + '"'
            editor.lines[lastCommentLine - 1] = newLastLine
            return

        # The title was there, so re-generate the comment line, remove the old
        # one and insert a new one
        pos = self.ref.parts[0].beginPos
        newCommentLine = CMLgb.generate(self.id, newTitle, self.bgColor,
                                        self.fgColor, self.border, pos)
        self.removeFromText(editor)
        editor.insertLines(newCommentLine, firstCommentLine)

    def updateCustomColors(self, editor, bgcolor, fgcolor, bordercolor):
        """Updates the custom colors"""
        firstCommentLine = self.ref.parts[0].beginLine
        pos = self.ref.parts[0].beginPos
        newCommentLine = CMLgb.generate(self.id, self.title, bgcolor,
                                        fgcolor, bordercolor, pos)
        self.removeFromText(editor)
        editor.insertLines(newCommentLine, firstCommentLine)

    def removeCustomColors(self, editor):
        """Removes the custom colors"""
        self.updateCustomColors(editor, None, None, None)



class CMLge(CMLCommentBase):

    """Covers the 'group end' comment"""

    CODE = 'ge'

    def __init__(self, ref):
        CMLCommentBase.__init__(self, ref)
        self.id = None
        self.validate()

    def validate(self):
        """Validates the CML ge comment"""
        self.validateRecordType(CMLge.CODE)
        CMLVersion.validate(self.ref)

        if 'id' in self.ref.properties:
            self.id = self.ref.properties['id'].strip()

        if not self.id:
            raise Exception("The '" + CMLge.CODE +
                            "' CML comment does not supply id")

    @staticmethod
    def description():
        """Provides the CML comment description"""
        return "The '" + CMLge.CODE + \
               "' is used to indicate the end of the visual group. It " \
               "needs a counterpart " + CMLgb.CODE + " CML comment which " \
               "indicates the beginning of the visual group.\n" \
               "Supported properties:\n" \
               "- 'id': unique identifier of the visual group\n\n" \
               "Example:\n" \
               "# cml 1 " + CMLge.CODE + " id=\"1234-5678-444444\""

    @staticmethod
    def generate(groupid, pos=1):
        """Generates a complete line to be inserted"""
        res = ' ' * (pos - 1) + '# cml 1 ' + CMLge.CODE
        if ' ' in groupid:
            res += ' id="' + groupid + '"'
        else:
            res += ' id=' + groupid
        return res



class CMLVersion:

    """Describes the current CML version"""

    VERSION = 1     # Current CML version
    COMMENT_TYPES = {CMLsw.CODE: CMLsw,
                     CMLcc.CODE: CMLcc,
                     CMLrt.CODE: CMLrt,
                     CMLgb.CODE: CMLgb,
                     CMLge.CODE: CMLge,
                     CMLdoc.CODE: CMLdoc}

    def __init__(self):
        pass

    @staticmethod
    def validate(cmlComment):
        """Valides the vestion"""
        if cmlComment.version > CMLVersion.VERSION:
            raise Exception("The CML comment version " +
                            str(cmlComment.version) +
                            " is not supported. Max supported version is " +
                            str(CMLVersion.VERSION))

    @staticmethod
    def find(cmlComments, cmlType):
        """Finds the CML comment"""
        for comment in cmlComments:
            if hasattr(comment, "CODE"):
                if comment.CODE == cmlType.CODE:
                    return comment
        return None

    @staticmethod
    def getType(cmlComment):
        """Provides the CML comment type"""
        try:
            return CMLVersion.COMMENT_TYPES[cmlComment.recordType]
        except KeyError:
            return None

    @staticmethod
    def validateCMLComments(item, validGroups, allGroupId,
                            pickLeadingComments=True):
        """Validates recursively all the CML items in the control flow.

        Replaces the recognized CML comments from the module with their higher
        level counterparts.
        Returns back a list of warnings. Also populates a list of valid groups.
        """
        scopeGroupStack = []    # [(id, lineBegin, lineEnd), ...]

        warnings = []
        if pickLeadingComments:
            # This is a special case for CML comments for the module.
            # They need to be considered as belonging to the module suite.
            if hasattr(item, "leadingCMLComments"):
                warnings += CMLVersion.validateCMLList(
                    item.leadingCMLComments, True, scopeGroupStack,
                    validGroups, allGroupId)

        # Some items are containers
        if item.kind == IF_FRAGMENT:
            for index, part in enumerate(item.parts):
                if index == 0:
                    # The very first part
                    warnings += CMLVersion.validateCMLList(
                        part.leadingCMLComments, True, scopeGroupStack,
                        validGroups, allGroupId)
                else:
                    warnings += CMLVersion.validateCMLList(
                        part.leadingCMLComments, False, None, None, None,
                        'elif or else parts')
                warnings += CMLVersion.validateCMLComments(
                    part, validGroups, allGroupId, False)
        elif item.kind in [FOR_FRAGMENT, WHILE_FRAGMENT]:
            if item.elsePart:
                warnings += CMLVersion.validateCMLList(
                    item.elsePart.leadingCMLComments, False, None, None, None,
                    'loop else parts')
                warnings += CMLVersion.validateCMLComments(
                    item.elsePart, validGroups, allGroupId, False)
        elif item.kind == TRY_FRAGMENT:
            if item.elsePart:
                warnings += CMLVersion.validateCMLList(
                    item.elsePart.leadingCMLComments, False,
                    None, None, None, 'try else parts')
                warnings += CMLVersion.validateCMLComments(
                    item.elsePart, validGroups, allGroupId, False)
            if item.finallyPart:
                warnings += CMLVersion.validateCMLList(
                    item.finallyPart.leadingCMLComments, False,
                    None, None, None, 'try finally parts')
                warnings += CMLVersion.validateCMLComments(
                    item.finallyPart, validGroups, allGroupId, False)
            for part in item.exceptParts:
                warnings += CMLVersion.validateCMLList(
                    part.leadingCMLComments, False,
                    None, None, None, 'try except parts')
                warnings += CMLVersion.validateCMLComments(
                    part, validGroups, allGroupId, False)
        elif item.kind in [CONTROL_FLOW_FRAGMENT,
                           CLASS_FRAGMENT, FUNCTION_FRAGMENT]:
            if item.docstring:
                warnings += CMLVersion.validateCMLList(
                    item.docstring.leadingCMLComments, False,
                    None, None, None, 'docstrings')
                warnings += CMLVersion.validateCMLList(
                    item.docstring.sideCMLComments, False,
                    None, None, None, 'docstrings')

            if item.kind in [CLASS_FRAGMENT, FUNCTION_FRAGMENT]:
                if item.decorators:
                    for index, decorator in enumerate(item.decorators):
                        if index == 0:
                            warnings += CMLVersion.validateCMLList(
                                decorator.leadingCMLComments, True,
                                scopeGroupStack, validGroups, allGroupId)
                        else:
                            warnings += CMLVersion.validateCMLList(
                                decorator.leadingCMLComments, False,
                                None, None, None, ' not first decorators')
                        warnings += CMLVersion.validateCMLList(
                            decorator.sideCMLComments, False,
                            None, None, None, 'decorators')

        if hasattr(item, "sideCMLComments"):
            warnings += CMLVersion.validateCMLList(
                item.sideCMLComments, False, None, None, None, 'side comments')

        if hasattr(item, "suite"):
            for index, nestedItem in enumerate(item.suite):
                if nestedItem.kind == CML_COMMENT_FRAGMENT:
                    # independent CML comment
                    warn, replace = CMLVersion.validateCMLComment(nestedItem)
                    if replace is not None:
                        item.suite[index] = replace
                        if replace.CODE in [CMLgb.CODE, CMLge.CODE]:
                            CMLVersion.handleScopeGroup(replace,
                                                        scopeGroupStack,
                                                        warnings,
                                                        validGroups,
                                                        allGroupId)
                    if warn is not None:
                        warnings.append(warn)
                    continue

                if nestedItem.kind in [CLASS_FRAGMENT, FUNCTION_FRAGMENT]:
                    if nestedItem.decorators:
                        warnings += CMLVersion.validateCMLList(
                            nestedItem.decorators[0].leadingCMLComments, True,
                            scopeGroupStack, validGroups, allGroupId)
                    else:
                        warnings += CMLVersion.validateCMLList(
                            nestedItem.leadingCMLComments, True,
                            scopeGroupStack, validGroups, allGroupId)
                elif hasattr(nestedItem, "leadingCMLComments"):
                    warnings += CMLVersion.validateCMLList(
                        nestedItem.leadingCMLComments, True, scopeGroupStack,
                        validGroups, allGroupId)
                if nestedItem.kind == IF_FRAGMENT:
                    warnings += CMLVersion.validateCMLList(
                        nestedItem.parts[0].leadingCMLComments, True,
                        scopeGroupStack, validGroups, allGroupId)

                warnings += CMLVersion.validateCMLComments(nestedItem,
                                                           validGroups,
                                                           allGroupId, False)

        for group in scopeGroupStack:
            warnings.append((group[1], -1, 'CML ' + CMLgb.CODE + ' comment '
                             'does not have a matching CML ' + CMLge.CODE +
                             ' comment'))

        return warnings

    @staticmethod
    def handleScopeGroup(cmlComment, groupStack, warnings,
                         validGroups, allGroupId):
        """Processes the cml grouping comments"""
        line = cmlComment.ref.parts[0].beginLine
        if cmlComment.CODE == CMLgb.CODE:
            groupStack.append((cmlComment.id, line))
            if cmlComment.id:
                allGroupId.add(cmlComment.id)
            return
        if cmlComment.CODE == CMLge.CODE:
            if not groupStack:
                warnings.append((line, -1,
                                 'CML ' + CMLge.CODE + ' comment '
                                 'without CML ' + CMLgb.CODE + ' comment'))
                return
            if groupStack[-1][0] != cmlComment.id:
                warnings.append((line, -1,
                                 'CML ' + CMLge.CODE + ' comment id does not '
                                 'match the previous CML ' + CMLgb.CODE +
                                 ' comment id at line ' +
                                 str(groupStack[-1][1])))
                return
            validGroups.append((cmlComment.id, groupStack[-1][1], line))
            groupStack.pop()

    @staticmethod
    def validateCMLList(comments, pickGroups, groupStack,
                        validGroups, allGroupId, itemName=None):
        """Validates the CML comments in the provided list (internal use)"""
        warnings = []
        if comments:
            for index, item in enumerate(comments):
                if isinstance(item, CMLCommentBase):
                    continue

                warn, replace = CMLVersion.validateCMLComment(item)
                if replace is not None:
                    comments[index] = replace
                    if replace.CODE in [CMLgb.CODE, CMLge.CODE]:
                        if pickGroups:
                            CMLVersion.handleScopeGroup(replace,
                                                        groupStack,
                                                        warnings,
                                                        validGroups,
                                                        allGroupId)
                        else:
                            line = replace.ref.parts[0].beginLine
                            pos = replace.ref.parts[0].beginPos
                            warn = (line, pos, 'Groups are not allowed for ' +
                                    itemName)
                if warn is not None:
                    warnings.append(warn)
        return warnings

    @staticmethod
    def validateCMLComment(cmlComment):
        """Validates a CML comment (internal use)"""
        warning = None
        highLevel = None
        cmlType = CMLVersion.getType(cmlComment)
        if cmlType:
            try:
                highLevel = cmlType(cmlComment)
            except Exception as exc:
                line = cmlComment.parts[0].beginLine
                pos = cmlComment.parts[0].beginPos
                warning = (line, pos, "Invalid CML comment: " + str(exc))
        else:
            line = cmlComment.parts[0].beginLine
            pos = cmlComment.parts[0].beginPos
            warning = (line, pos,
                       "CML comment type '" + cmlComment.recordType +
                       "' is not supported")
        return warning, highLevel

    @staticmethod
    def getFirstLine(comments):
        """Provides the first line of the comment"""
        # The list may contain raw comments and high level comments
        line = maxsize
        if comments:
            if hasattr(comments[0], "ref"):
                # High level CML comment
                return comments[0].ref.parts[0].beginLine
            # Raw CML comment
            if comments[0].parts:
                return comments[0].parts[0].beginLine
        return line

    @staticmethod
    def description():
        """Provides the common parameters for various CML comments"""
        return "Color properties supported by the '" + CMLcc.CODE + \
               "' and the '" + CMLgb.CODE + "' comments:\n" \
               "- 'bg': background color for the item\n" \
               "- 'fg': foreground color for the item\n" \
               "- 'border': border color for the item\n" \
               "Color spec formats:\n" \
               "- '#hhh': hexadecimal RGB\n" \
               "- '#hhhh': hexadecimal RGBA\n" \
               "- '#hhhhhh': hexadecimal RRGGBB\n" \
               "- '#hhhhhhhh': hexadecimal RRGGBBAA\n" \
               "- 'ddd,ddd,ddd': decimal RGB\n" \
               "- 'ddd,ddd,ddd,ddd': decimal RGBA"
