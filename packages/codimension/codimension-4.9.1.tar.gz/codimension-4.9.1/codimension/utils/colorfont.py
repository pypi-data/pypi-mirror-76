# -*- coding: utf-8 -*-
#
# codimension - graphics python two-way code editor and analyzer
# Copyright (C) 2016-2017  Sergey Satskiy <sergey.satskiy@gmail.com>
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

"""QT color and font general utils"""

from ui.qt import QColor, QFont, QFontComboBox
from .globals import GlobalData
from .settings import Settings


def checkColorRange(value):
    """Checks the color range"""
    if value < 0 or value > 255:
        raise Exception("Invalid color value")


def toHex(value):
    """Converts the value to a double digit hex string"""
    asStr = hex(value)[2:]
    if len(asStr) == 1:
        return '0' + asStr
    return asStr


def buildColor(color):
    """Six options are supported:

    #hhh                hexadecimal rgb
    #hhhh               hexadecimal rgba
    #hhhhhh             hexadecimal rrggbb
    #hhhhhhhh           hexadecimal rrggbbaa
    ddd,ddd,ddd         decimal rgb
    ddd,ddd,ddd,ddd     decimal rgba
    """
    if color.startswith('#'):
        def normalizeLength(spec):
            if len(spec) in [6, 8]:
                return spec
            normalized = ''
            for character in spec:
                normalized += 2 * character
            return normalized

        color = color[1:]
        length = len(color)
        if length not in [3, 4, 6, 8]:
            raise Exception("Invalid hexadecimal color format: #" + color)

        try:
            # The most common case
            normColor = normalizeLength(color)
            red = int(normColor[0:2], 16)
            checkColorRange(red)
            green = int(normColor[2:4], 16)
            checkColorRange(green)
            blue = int(normColor[4:6], 16)
            checkColorRange(blue)

            if length in [3, 6]:
                return QColor(red, green, blue)
            alpha = int(normColor[6:8], 16)
            checkColorRange(alpha)
            return QColor(red, green, blue, alpha)
        except:
            raise Exception("Invalid hexadecimal color format: #" + color)

    parts = color.split(',')
    length = len(parts)
    if length not in [3, 4]:
        raise Exception("Invalid decimal color format: " + color)

    try:
        red = int(parts[0].strip())
        checkColorRange(red)
        green = int(parts[1].strip())
        checkColorRange(green)
        blue = int(parts[2].strip())
        checkColorRange(blue)

        if length == 3:
            return QColor(red, green, blue)
        alpha = int(parts[3].strip())
        checkColorRange(alpha)
        return QColor(red, green, blue, alpha)
    except:
        raise Exception("Invalid decimal color format: " + color)


def cssLikeColor(color):
    """Converts to a css like string, possibly shortened"""
    asStr = color.name()
    alpha = color.alpha()
    if alpha != 255:
        asStr += toHex(alpha)

    # Shorten it if possible
    if len(asStr) == 7:
        # '#rgb'
        if asStr[1] == asStr[2] and asStr[3] == asStr[4] and \
           asStr[5] == asStr[6]:
            return '#' + asStr[1] + asStr[3] + asStr[5]
        return asStr

    # '#rgba'
    if asStr[1] == asStr[2] and asStr[3] == asStr[4] and \
       asStr[5] == asStr[6] and asStr[7] == asStr[8]:
        return '#' + asStr[1] + asStr[3] + asStr[5] + asStr[7]
    return asStr


def transparentColor(fgColor, bgColor, alpha):
    """Converts the color value considering the background and alpha"""
    if alpha == 255:
        return fgColor

    dAlpha = float(alpha)/255.0
    dFirst = float(fgColor) * dAlpha
    dSecond = float(bgColor) * (1.0 - dAlpha)
    return min(255, round(dFirst + dSecond))


def qtCssColor(color, bgColor=None):
    """Converts the given color to the QT compatible one (transparency is not supported"""
    alpha = color.alpha()
    if alpha == 255:
        return color.name()

    if bgColor is None:
        rTransp = transparentColor(color.red(), 255, alpha)
        gTransp = transparentColor(color.green(), 255, alpha)
        bTransp = transparentColor(color.blue(), 255, alpha)
    else:
        rTransp = transparentColor(color.red(), bgColor.red(), alpha)
        gTransp = transparentColor(color.green(), bgColor.green(), alpha)
        bTransp = transparentColor(color.blue(), bgColor.blue(), alpha)
    return ''.join(('#', toHex(rTransp), toHex(gTransp), toHex(bTransp)))


def colorAsString(color, hexadecimal=False):
    """Converts the given color to a string"""
    if hexadecimal:
        return '#' + ''.join([toHex(color.red()),
                              toHex(color.green()),
                              toHex(color.blue()),
                              toHex(color.alpha())])
    return ','.join([str(color.red()),
                     str(color.green()),
                     str(color.blue()),
                     str(color.alpha())])


def buildFont(fontAsStr):
    """Converts saved font into QFont object"""
    fontAsStr = fontAsStr.strip()
    font = QFont()
    font.fromString(fontAsStr)
    return font


def fontAsString(font):
    """Converts a font to a string"""
    return font.toString()


excludeFontList = ['webdings', 'cursor', 'mathematical', 'dingbats', 'hershey']


def isExcludeFont(family):
    """True if the font needs to be excluded"""
    lowerFamily = family.lower()
    for exclusion in excludeFontList:
        if exclusion in lowerFamily:
            return True
    return False


def getFontList(fontType):
    """Provides a list of certain type fonts"""
    result = []
    combo = QFontComboBox()
    combo.setFontFilters(fontType)
    for index in range(combo.count()):
        family = str(combo.itemText(index))
        if not isExcludeFont(family):
            result.append(family)
    return result


def getMonospaceFontList():
    """Provides a list of strings with the system installed monospace fonts"""
    return getFontList(QFontComboBox.MonospacedFonts)


def getScalableFontList():
    """Provides a list of scalable fonts"""
    return getFontList(QFontComboBox.ScalableFonts)


def getProportionalFontList():
    """Provides a list of proportional fonts"""
    return getFontList(QFontComboBox.ProportionalFonts)


def colorFontToJSON(pythonObj):
    """Custom serialization"""
    if isinstance(pythonObj, QColor):
        return colorAsString(pythonObj)
    if isinstance(pythonObj, QFont):
        return fontAsString(pythonObj)
    raise TypeError(repr(pythonObj) + ' is not JSON serializable')


def colorFontFromJSON(jsonObj):
    """Custom deserialization"""
    if '__class__' in jsonObj:
        if jsonObj['__class__'] == 'QColor':
            return buildColor(jsonObj['__value__'])
        if jsonObj['__class__'] == 'QFont':
            return buildFont(jsonObj['__value__'])
    return jsonObj


def getZoomedMonoFont():
    """Provides the current mono font respecting zoom"""
    font = QFont(GlobalData().skin['monoFont'])
    font.setPointSize(font.pointSize() + Settings()['zoom'])
    return font


def getZoomedCFMonoFont():
    """Provides the current mono font respecting zoom"""
    font = QFont(GlobalData().skin['cfMonoFont'])
    font.setPointSize(font.pointSize() + Settings()['flowZoom'])
    return font


def getZoomedCFBadgeFont():
    """Provides the current control flow badge font respecting zoom"""
    font = QFont(GlobalData().skin['badgeFont'])
    font.setPointSize(font.pointSize() + Settings()['flowZoom'])
    return font


def getZoomedMarginFont():
    """Provides the current margin font respecting zoom"""
    font = QFont(GlobalData().skin['lineNumFont'])
    font.setPointSize(font.pointSize() + Settings()['zoom'])
    return font


def setLineEditBackground(widget, color, bgColor=None):
    """Sets the widget background to the given color"""
    widget.setStyleSheet('QLineEdit {background-color: ' +
                         qtCssColor(color, bgColor) + '}')

