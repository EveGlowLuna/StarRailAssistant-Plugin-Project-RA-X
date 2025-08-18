# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGroupBox, QHBoxLayout, QLabel, QMainWindow,
    QMenuBar, QPushButton, QScrollArea, QSizePolicy,
    QSpinBox, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(819, 519)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, -190, 787, 636))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.languagesettings = QGroupBox(self.scrollAreaWidgetContents)
        self.languagesettings.setObjectName(u"languagesettings")
        self.languagesettings.setMinimumSize(QSize(0, 200))
        self.languagesettings.setMaximumSize(QSize(16777215, 200))
        self.verticalLayout_3 = QVBoxLayout(self.languagesettings)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame_2 = QFrame(self.languagesettings)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_lang_warning = QLabel(self.frame_2)
        self.label_lang_warning.setObjectName(u"label_lang_warning")

        self.horizontalLayout_3.addWidget(self.label_lang_warning)


        self.verticalLayout_3.addWidget(self.frame_2)

        self.frame_3 = QFrame(self.languagesettings)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_language = QLabel(self.frame_3)
        self.label_language.setObjectName(u"label_language")

        self.horizontalLayout_4.addWidget(self.label_language)

        self.comboBox = QComboBox(self.frame_3)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(0, 30))
        self.comboBox.setInsertPolicy(QComboBox.InsertPolicy.InsertAtCurrent)

        self.horizontalLayout_4.addWidget(self.comboBox)


        self.verticalLayout_3.addWidget(self.frame_3)


        self.verticalLayout.addWidget(self.languagesettings)

        self.logviewsettings = QGroupBox(self.scrollAreaWidgetContents)
        self.logviewsettings.setObjectName(u"logviewsettings")
        self.logviewsettings.setMinimumSize(QSize(0, 100))
        self.logviewsettings.setMaximumSize(QSize(16777215, 100))
        self.verticalLayout_2 = QVBoxLayout(self.logviewsettings)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame = QFrame(self.logviewsettings)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.checkbox_display = QCheckBox(self.frame)
        self.checkbox_display.setObjectName(u"checkbox_display")

        self.horizontalLayout.addWidget(self.checkbox_display)


        self.verticalLayout_2.addWidget(self.frame)


        self.verticalLayout.addWidget(self.logviewsettings)

        self.task_flag_settings = QGroupBox(self.scrollAreaWidgetContents)
        self.task_flag_settings.setObjectName(u"task_flag_settings")
        self.task_flag_settings.setMinimumSize(QSize(0, 200))
        self.verticalLayout_5 = QVBoxLayout(self.task_flag_settings)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.frame_6 = QFrame(self.task_flag_settings)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_checktask_warning = QLabel(self.frame_6)
        self.label_checktask_warning.setObjectName(u"label_checktask_warning")

        self.horizontalLayout_7.addWidget(self.label_checktask_warning)


        self.verticalLayout_5.addWidget(self.frame_6)

        self.frame_8 = QFrame(self.task_flag_settings)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label = QLabel(self.frame_8)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.horizontalLayout_9.addWidget(self.label)

        self.spinBox = QSpinBox(self.frame_8)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimum(60)
        self.spinBox.setMaximum(1440)

        self.horizontalLayout_9.addWidget(self.spinBox)

        self.label_2 = QLabel(self.frame_8)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)

        self.horizontalLayout_9.addWidget(self.label_2)

        self.btn_enable_taskflag = QPushButton(self.frame_8)
        self.btn_enable_taskflag.setObjectName(u"btn_enable_taskflag")
        self.btn_enable_taskflag.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_9.addWidget(self.btn_enable_taskflag)


        self.verticalLayout_5.addWidget(self.frame_8)


        self.verticalLayout.addWidget(self.task_flag_settings)

        self.processprotect_settings = QGroupBox(self.scrollAreaWidgetContents)
        self.processprotect_settings.setObjectName(u"processprotect_settings")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.processprotect_settings.sizePolicy().hasHeightForWidth())
        self.processprotect_settings.setSizePolicy(sizePolicy1)
        self.processprotect_settings.setMinimumSize(QSize(0, 100))
        self.processprotect_settings.setMaximumSize(QSize(16777215, 200))
        self.verticalLayout_4 = QVBoxLayout(self.processprotect_settings)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.frame_4 = QFrame(self.processprotect_settings)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_processprotect_warning = QLabel(self.frame_4)
        self.label_processprotect_warning.setObjectName(u"label_processprotect_warning")

        self.horizontalLayout_5.addWidget(self.label_processprotect_warning)

        self.button_enable_processprotect = QPushButton(self.frame_4)
        self.button_enable_processprotect.setObjectName(u"button_enable_processprotect")
        self.button_enable_processprotect.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_5.addWidget(self.button_enable_processprotect)


        self.verticalLayout_4.addWidget(self.frame_4)


        self.verticalLayout.addWidget(self.processprotect_settings)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_2.addWidget(self.scrollArea)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 819, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.comboBox.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Projected RAX", None))
        self.languagesettings.setTitle(QCoreApplication.translate("MainWindow", u"[Under construction] \u8bed\u8a00/Language", None))
        self.label_lang_warning.setText(QCoreApplication.translate("MainWindow", u"\u8b66\u544a\uff1a\u66f4\u6539\u8bed\u8a00\u540e\uff0c\u4ec5\u66f4\u6539SRA\u754c\u9762\u663e\u793a\u8bed\u8a00\uff0c\u5e76\u4e0d\u80fd\u66f4\u6539\u65e5\u5fd7\u8bed\u8a00\u4ee5\u53ca\u5c4f\u5e55\u68c0\u6d4b\u65f6\u7684\u56fe\u50cf\u8bed\u8a00\u3002\n"
"\u5982\u9700\u672c\u5730\u5316\u652f\u6301\uff0c\u8bf7\u63d0\u4f9b\u6709\u5173\u8bed\u8a00\u7684\u526f\u672c\u540d\u79f0\uff08\u4e2d\u5916\u5bf9\u7167\u4ee5\u4fbf\u6838\u5bf9\uff09\n"
"\u8be5\u529f\u80fd\u6b63\u5728\u5b9e\u73b0\u4e2d\u3002", None))
        self.label_language.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u8bed\u8a00", None))
        self.logviewsettings.setTitle(QCoreApplication.translate("MainWindow", u"\u900f\u660e\u65e5\u5fd7", None))
        self.checkbox_display.setText(QCoreApplication.translate("MainWindow", u"\u542f\u7528\u5728\u5c4f\u5e55\u4e2d\u663e\u793a\u65e5\u5fd7", None))
        self.task_flag_settings.setTitle(QCoreApplication.translate("MainWindow", u"\u68c0\u67e5\u6bcf\u65e5\u6267\u884c", None))
        self.label_checktask_warning.setText(QCoreApplication.translate("MainWindow", u"\u5728\u6bcf\u5929\u6267\u884c\u8fc7\u4efb\u52a1\u540e\u9694\u4e00\u6bb5\u65f6\u95f4\u68c0\u6d4b\u4e00\u6b21\uff0c\u5982\u679c\u4e0a\u4e00\u6b21\u4efb\u52a1\u5931\u8d25\uff08\u6ca1\u6709\u5b8c\u6210\u63d0\u793a\uff09\u5219\u91cd\u65b0\u6267\u884c\u4efb\u52a1\u3002\n"
"\u76ee\u524d\u7b56\u7565\uff1a\u68c0\u6d4b\"\u4efb\u52a1\u5168\u90e8\u5b8c\u6210\"\u662f\u5426\u51fa\u73b0\n"
"\u8be5\u529f\u80fd\u9700\u8981\u6bcf\u6b21\u542f\u52a8 SRA \u540e\u624b\u52a8\u542f\u7528\uff08\u8fdb\u7a0b\u4fdd\u62a4\u9664\u5916\uff09", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"When every ...", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Minutes", None))
        self.btn_enable_taskflag.setText(QCoreApplication.translate("MainWindow", u"\u542f\u7528\u6bcf\u65e5\u6267\u884c", None))
        self.processprotect_settings.setTitle(QCoreApplication.translate("MainWindow", u"\u8fdb\u7a0b\u4fdd\u62a4", None))
        self.label_processprotect_warning.setText(QCoreApplication.translate("MainWindow", u"\u76ee\u524d\u7b56\u7565\uff1a\u901a\u8fc7\u5916\u90e8\u5e94\u7528\u5bf9SRA\u8fdb\u7a0b\u8fdb\u884c\u68c0\u6d4b\uff0c\u5d29\u6e83\u540e\u81ea\u52a8\u91cd\u542f\u3002", None))
        self.button_enable_processprotect.setText(QCoreApplication.translate("MainWindow", u"\u542f\u7528\u8fdb\u7a0b\u4fdd\u62a4", None))
    # retranslateUi

