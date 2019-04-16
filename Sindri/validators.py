from PySide2.QtGui import QDoubleValidator, QIntValidator, QRegExpValidator
from PySide2.QtCore import QRegExp


def getDoubleValidator():
    dblValidator = QDoubleValidator()
    return dblValidator


def getDoubleValidatorRegex(parent):
    regex = QRegExp("[-+]?\d*(\.[0-9]*)?([eE][-+]?[0-9]+)?")
    doublevalidator = QRegExpValidator(regex, parent)
    return doublevalidator


def getPositiveIntValidator():
    intval = QIntValidator()
    intval.setBottom(0)
    return intval
