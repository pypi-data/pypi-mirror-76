# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parsec/core/gui/forms/menu_widget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MenuWidget(object):
    def setupUi(self, MenuWidget):
        MenuWidget.setObjectName("MenuWidget")
        MenuWidget.resize(260, 689)
        MenuWidget.setMinimumSize(QtCore.QSize(260, 0))
        MenuWidget.setMaximumSize(QtCore.QSize(260, 16777215))
        MenuWidget.setStyleSheet("QWidget#widget_menu {\n"
"    background-color: #222222;\n"
"}\n"
"\n"
"#button_devices, #button_files, #button_users, #button_logout {\n"
"    color: #999999;\n"
"    background-color: #222222;\n"
"    text-align: left;\n"
"    padding-left: 10px;\n"
"    font-size: 16px;\n"
"}\n"
"\n"
"#button_devices:checked, #button_files:checked, #button_users:checked {\n"
"    background-color: #333333;\n"
"    border: 0;\n"
"    color: #FFFFFF;\n"
"}\n"
"\n"
"#button_devices:hover, #button_files:hover, #button_users:hover, #button_logout:hover {\n"
"    color: #EEEEEE;\n"
"}\n"
"\n"
"QWidget#widget_misc {\n"
"    background-color: #333333;\n"
"}\n"
"\n"
"#label_connection_state, #label_device, #label_organization, #label_username {\n"
"    color: #FFFFFF;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(MenuWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_menu = QtWidgets.QWidget(MenuWidget)
        self.widget_menu.setMinimumSize(QtCore.QSize(200, 0))
        self.widget_menu.setObjectName("widget_menu")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.widget_menu)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget_3 = QtWidgets.QWidget(self.widget_menu)
        self.widget_3.setMinimumSize(QtCore.QSize(0, 60))
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setContentsMargins(20, 20, 10, 40)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.widget_3)
        self.label.setMinimumSize(QtCore.QSize(210, 32))
        self.label.setMaximumSize(QtCore.QSize(210, 32))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/logos/images/logos/parsec.png"))
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.verticalLayout_3.addWidget(self.widget_3)
        self.button_files = MenuButton(self.widget_menu)
        self.button_files.setEnabled(True)
        self.button_files.setMinimumSize(QtCore.QSize(0, 64))
        self.button_files.setMaximumSize(QtCore.QSize(16777215, 64))
        self.button_files.setBaseSize(QtCore.QSize(64, 0))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.button_files.setFont(font)
        self.button_files.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/images/material/folder_open.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_files.setIcon(icon)
        self.button_files.setIconSize(QtCore.QSize(32, 32))
        self.button_files.setCheckable(True)
        self.button_files.setFlat(True)
        self.button_files.setProperty("checked_color", QtGui.QColor(27, 141, 215))
        self.button_files.setProperty("unchecked_color", QtGui.QColor(153, 153, 153))
        self.button_files.setObjectName("button_files")
        self.verticalLayout_3.addWidget(self.button_files)
        self.button_users = MenuButton(self.widget_menu)
        self.button_users.setEnabled(True)
        self.button_users.setMinimumSize(QtCore.QSize(0, 64))
        self.button_users.setMaximumSize(QtCore.QSize(16777215, 64))
        self.button_users.setBaseSize(QtCore.QSize(0, 64))
        self.button_users.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/images/material/supervisor_account.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_users.setIcon(icon1)
        self.button_users.setIconSize(QtCore.QSize(32, 32))
        self.button_users.setCheckable(True)
        self.button_users.setFlat(True)
        self.button_users.setProperty("checked_color", QtGui.QColor(27, 141, 215))
        self.button_users.setProperty("unchecked_color", QtGui.QColor(153, 153, 153))
        self.button_users.setObjectName("button_users")
        self.verticalLayout_3.addWidget(self.button_users)
        self.button_devices = MenuButton(self.widget_menu)
        self.button_devices.setEnabled(True)
        self.button_devices.setMinimumSize(QtCore.QSize(0, 64))
        self.button_devices.setMaximumSize(QtCore.QSize(16777215, 64))
        self.button_devices.setBaseSize(QtCore.QSize(0, 64))
        self.button_devices.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/images/material/devices.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_devices.setIcon(icon2)
        self.button_devices.setIconSize(QtCore.QSize(32, 32))
        self.button_devices.setCheckable(True)
        self.button_devices.setChecked(False)
        self.button_devices.setFlat(True)
        self.button_devices.setProperty("checked_color", QtGui.QColor(27, 141, 215))
        self.button_devices.setProperty("unchecked_color", QtGui.QColor(153, 153, 153))
        self.button_devices.setObjectName("button_devices")
        self.verticalLayout_3.addWidget(self.button_devices)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.button_logout = Button(self.widget_menu)
        self.button_logout.setEnabled(True)
        self.button_logout.setMinimumSize(QtCore.QSize(0, 64))
        self.button_logout.setMaximumSize(QtCore.QSize(16777215, 64))
        self.button_logout.setBaseSize(QtCore.QSize(0, 64))
        self.button_logout.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/images/material/exit_to_app.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_logout.setIcon(icon3)
        self.button_logout.setIconSize(QtCore.QSize(24, 24))
        self.button_logout.setCheckable(False)
        self.button_logout.setFlat(True)
        self.button_logout.setProperty("color", QtGui.QColor(153, 153, 153))
        self.button_logout.setObjectName("button_logout")
        self.verticalLayout_3.addWidget(self.button_logout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_3.addItem(spacerItem1)
        self.widget_misc = QtWidgets.QWidget(self.widget_menu)
        self.widget_misc.setObjectName("widget_misc")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_misc)
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_connection = QtWidgets.QWidget(self.widget_misc)
        self.widget_connection.setObjectName("widget_connection")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_connection)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(10)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.icon_connection = IconLabel(self.widget_connection)
        self.icon_connection.setMinimumSize(QtCore.QSize(32, 32))
        self.icon_connection.setMaximumSize(QtCore.QSize(32, 32))
        self.icon_connection.setText("")
        self.icon_connection.setPixmap(QtGui.QPixmap(":/icons/images/material/cloud_off.svg"))
        self.icon_connection.setScaledContents(True)
        self.icon_connection.setProperty("color", QtGui.QColor(27, 141, 215))
        self.icon_connection.setObjectName("icon_connection")
        self.horizontalLayout_6.addWidget(self.icon_connection)
        self.label_connection_state = QtWidgets.QLabel(self.widget_connection)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_connection_state.setFont(font)
        self.label_connection_state.setText("")
        self.label_connection_state.setObjectName("label_connection_state")
        self.horizontalLayout_6.addWidget(self.label_connection_state)
        self.verticalLayout_2.addWidget(self.widget_connection)
        self.widget_info = QtWidgets.QWidget(self.widget_misc)
        self.widget_info.setMinimumSize(QtCore.QSize(0, 88))
        self.widget_info.setMaximumSize(QtCore.QSize(16777215, 88))
        self.widget_info.setObjectName("widget_info")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.widget_info)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(10)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.icon_user = IconLabel(self.widget_info)
        self.icon_user.setMinimumSize(QtCore.QSize(32, 32))
        self.icon_user.setMaximumSize(QtCore.QSize(32, 32))
        self.icon_user.setText("")
        self.icon_user.setPixmap(QtGui.QPixmap(":/icons/images/material/person.svg"))
        self.icon_user.setScaledContents(True)
        self.icon_user.setAlignment(QtCore.Qt.AlignCenter)
        self.icon_user.setProperty("color", QtGui.QColor(27, 141, 215))
        self.icon_user.setObjectName("icon_user")
        self.horizontalLayout_9.addWidget(self.icon_user)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_organization = QtWidgets.QLabel(self.widget_info)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_organization.setFont(font)
        self.label_organization.setText("")
        self.label_organization.setObjectName("label_organization")
        self.verticalLayout_7.addWidget(self.label_organization)
        self.label_username = QtWidgets.QLabel(self.widget_info)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_username.setFont(font)
        self.label_username.setText("")
        self.label_username.setObjectName("label_username")
        self.verticalLayout_7.addWidget(self.label_username)
        self.label_device = QtWidgets.QLabel(self.widget_info)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_device.setFont(font)
        self.label_device.setText("")
        self.label_device.setObjectName("label_device")
        self.verticalLayout_7.addWidget(self.label_device)
        self.horizontalLayout_9.addLayout(self.verticalLayout_7)
        self.verticalLayout_2.addWidget(self.widget_info)
        self.verticalLayout_3.addWidget(self.widget_misc)
        self.verticalLayout_8.addLayout(self.verticalLayout_3)
        self.verticalLayout.addWidget(self.widget_menu)

        self.retranslateUi(MenuWidget)
        QtCore.QMetaObject.connectSlotsByName(MenuWidget)

    def retranslateUi(self, MenuWidget):
        _translate = QtCore.QCoreApplication.translate
        MenuWidget.setWindowTitle(_translate("MenuWidget", "Form"))
        self.button_files.setText(_translate("MenuWidget", "ACTION_MENU_DOCUMENTS"))
        self.button_users.setText(_translate("MenuWidget", "ACTION_MENU_USERS"))
        self.button_devices.setText(_translate("MenuWidget", "ACTION_MENU_DEVICES"))
        self.button_logout.setText(_translate("MenuWidget", "ACTION_LOG_OUT"))
from parsec.core.gui.custom_widgets import Button, IconLabel, MenuButton
from parsec.core.gui import resources_rc
