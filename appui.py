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
from PySide6.QtWidgets import (QApplication, QDialog, QLCDNumber, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSlider,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.ApplicationModal)
        Dialog.resize(1032, 730)
        self.freq_reduce = QPushButton(Dialog)
        self.freq_reduce.setObjectName(u"freq_reduce")
        self.freq_reduce.setGeometry(QRect(550, 340, 141, 24))
        self.freq_increase = QPushButton(Dialog)
        self.freq_increase.setObjectName(u"freq_increase")
        self.freq_increase.setGeometry(QRect(710, 340, 141, 24))
        self.inputfreq = QLineEdit(Dialog)
        self.inputfreq.setObjectName(u"inputfreq")
        self.inputfreq.setGeometry(QRect(550, 380, 301, 41))
        self.freq_display = QLCDNumber(Dialog)
        self.freq_display.setObjectName(u"freq_display")
        self.freq_display.setGeometry(QRect(550, 190, 291, 111))
        font = QFont()
        font.setPointSize(6)
        self.freq_display.setFont(font)
        self.AM = QPushButton(Dialog)
        self.AM.setObjectName(u"AM")
        self.AM.setGeometry(QRect(550, 430, 71, 24))
        self.FM = QPushButton(Dialog)
        self.FM.setObjectName(u"FM")
        self.FM.setGeometry(QRect(780, 430, 71, 24))
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(140, -50, 771, 191))
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(570, 140, 251, 31))
        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(280, 600, 521, 51))
        self.label_6 = QLabel(Dialog)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(850, 200, 61, 61))
        self.label_7 = QLabel(Dialog)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(600, 491, 221, 20))
        self.volumebar = QSlider(Dialog)
        self.volumebar.setObjectName(u"volumebar")
        self.volumebar.setGeometry(QRect(599, 520, 221, 41))
        self.volumebar.setOrientation(Qt.Horizontal)
        self.decodemode = QLabel(Dialog)
        self.decodemode.setObjectName(u"decodemode")
        self.decodemode.setGeometry(QRect(850, 260, 58, 31))
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(170, 190, 58, 16))
        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(170, 260, 58, 16))
        self.ip = QLineEdit(Dialog)
        self.ip.setObjectName(u"ip")
        self.ip.setGeometry(QRect(170, 210, 231, 41))
        self.port = QLineEdit(Dialog)
        self.port.setObjectName(u"port")
        self.port.setGeometry(QRect(170, 280, 231, 41))

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
        self.label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:72pt; font-weight:600;\">Doomsday Radio</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">Frequency</span></p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">Patrolling the mojave almost makes you wish for a nuclear winter</span></p></body></html>", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600;\">KHz</span></p></body></html>", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">Volume</span></p></body></html>", None))
        self.decodemode.setText("")
        self.label_3.setText(QCoreApplication.translate("Dialog", u"IP", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Port", None))
        self.ip.setText(QCoreApplication.translate("Dialog", u"IP", None))
        self.port.setText(QCoreApplication.translate("Dialog", u"1234", None))
    # retranslateUi

