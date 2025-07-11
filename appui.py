# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'radio.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QGraphicsView, QLCDNumber,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSlider, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.ApplicationModal)
        Dialog.resize(1032, 730)
        self.freq_reduce = QPushButton(Dialog)
        self.freq_reduce.setObjectName(u"freq_reduce")
        self.freq_reduce.setGeometry(QRect(670, 310, 141, 24))
        self.freq_increase = QPushButton(Dialog)
        self.freq_increase.setObjectName(u"freq_increase")
        self.freq_increase.setGeometry(QRect(830, 310, 141, 24))
        self.inputfreq = QLineEdit(Dialog)
        self.inputfreq.setObjectName(u"inputfreq")
        self.inputfreq.setGeometry(QRect(670, 350, 301, 41))
        self.freq_display = QLCDNumber(Dialog)
        self.freq_display.setObjectName(u"freq_display")
        self.freq_display.setGeometry(QRect(640, 160, 291, 111))
        font = QFont()
        font.setPointSize(6)
        self.freq_display.setFont(font)
        self.AM = QPushButton(Dialog)
        self.AM.setObjectName(u"AM")
        self.AM.setGeometry(QRect(670, 400, 71, 24))
        self.FM = QPushButton(Dialog)
        self.FM.setObjectName(u"FM")
        self.FM.setGeometry(QRect(740, 400, 71, 24))
        self.LSB = QPushButton(Dialog)
        self.LSB.setObjectName(u"LSB")
        self.LSB.setGeometry(QRect(890, 400, 80, 24))
        self.USB = QPushButton(Dialog)
        self.USB.setObjectName(u"USB")
        self.USB.setGeometry(QRect(810, 400, 80, 24))
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(140, -50, 771, 191))
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(700, 110, 251, 31))
        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(280, 600, 521, 51))
        self.label_6 = QLabel(Dialog)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(940, 170, 61, 61))
        self.label_7 = QLabel(Dialog)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(720, 461, 221, 20))
        self.volumebar = QSlider(Dialog)
        self.volumebar.setObjectName(u"volumebar")
        self.volumebar.setGeometry(QRect(719, 490, 221, 41))
        self.volumebar.setOrientation(Qt.Horizontal)
        self.decodemode = QLabel(Dialog)
        self.decodemode.setObjectName(u"decodemode")
        self.decodemode.setGeometry(QRect(940, 230, 58, 31))
        self.spectrumplot = QGraphicsView(Dialog)
        self.spectrumplot.setObjectName(u"spectrumplot")
        self.spectrumplot.setGeometry(QRect(140, 140, 411, 291))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.freq_reduce.setText(QCoreApplication.translate("Dialog", u"Freq-", None))
        self.freq_increase.setText(QCoreApplication.translate("Dialog", u"Freq+", None))
        self.inputfreq.setText(QCoreApplication.translate("Dialog", u"Input Frequency", None))
#if QT_CONFIG(tooltip)
        self.freq_display.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"right\"><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.AM.setText(QCoreApplication.translate("Dialog", u"AM", None))
        self.FM.setText(QCoreApplication.translate("Dialog", u"FM", None))
        self.LSB.setText(QCoreApplication.translate("Dialog", u"LSB", None))
        self.USB.setText(QCoreApplication.translate("Dialog", u"USB", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:72pt; font-weight:600;\">Doomsday Radio</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Frequency</span></p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">Patrolling the mojave almost makes you wish for a nuclear winter</span></p></body></html>", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600;\">KHz</span></p></body></html>", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">Volume</span></p></body></html>", None))
        self.decodemode.setText("")
    # retranslateUi

