# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\Work\python\bioinfo_excercise\PhyloSuite\codes\PhyloSuite\uifiles\extract_setting.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ExtractSettings(object):
    def setupUi(self, ExtractSettings):
        ExtractSettings.setObjectName("ExtractSettings")
        ExtractSettings.resize(725, 682)
        self.gridLayout = QtWidgets.QGridLayout(ExtractSettings)
        self.gridLayout.setContentsMargins(3, 3, 3, 3)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget_container = QtWidgets.QWidget(ExtractSettings)
        self.widget_container.setObjectName("widget_container")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_container)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.widget_container)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(36, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.checkBox_2 = QtWidgets.QCheckBox(self.widget_container)
        self.checkBox_2.setMinimumSize(QtCore.QSize(50, 0))
        self.checkBox_2.setObjectName("checkBox_2")
        self.horizontalLayout_2.addWidget(self.checkBox_2)
        spacerItem1 = QtWidgets.QSpacerItem(37, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.toolButton = QtWidgets.QToolButton(self.widget_container)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/picture/resourses/add-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton.setIcon(icon)
        self.toolButton.setAutoRaise(True)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout_2.addWidget(self.toolButton)
        self.verticalLayout_3.addWidget(self.widget_container)
        self.listWidget = AdvanceQlistwidget(ExtractSettings)
        self.listWidget.setStyleSheet("QToolTip {\n"
"    color: black; \n"
"    background-color: #FFFFFF;\n"
"    border: 1px solid white;\n"
"    min-height: 20px;\n"
"}")
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_3.addWidget(self.listWidget)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_container3 = QtWidgets.QWidget(ExtractSettings)
        self.widget_container3.setObjectName("widget_container3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_container3)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.widget_container3)
        self.label_2.setStatusTip("")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.checkBox = QtWidgets.QCheckBox(self.widget_container3)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout.addWidget(self.checkBox)
        self.toolButton_6 = QtWidgets.QToolButton(self.widget_container3)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/picture/resourses/import.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_6.setIcon(icon1)
        self.toolButton_6.setAutoRaise(True)
        self.toolButton_6.setObjectName("toolButton_6")
        self.horizontalLayout.addWidget(self.toolButton_6)
        self.toolButton_5 = QtWidgets.QToolButton(self.widget_container3)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/picture/resourses/up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_5.setIcon(icon2)
        self.toolButton_5.setAutoRaise(True)
        self.toolButton_5.setObjectName("toolButton_5")
        self.horizontalLayout.addWidget(self.toolButton_5)
        self.toolButton_3 = QtWidgets.QToolButton(self.widget_container3)
        self.toolButton_3.setIcon(icon)
        self.toolButton_3.setAutoRaise(True)
        self.toolButton_3.setObjectName("toolButton_3")
        self.horizontalLayout.addWidget(self.toolButton_3)
        self.toolButton_4 = QtWidgets.QToolButton(self.widget_container3)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/picture/resourses/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_4.setIcon(icon3)
        self.toolButton_4.setAutoRaise(True)
        self.toolButton_4.setObjectName("toolButton_4")
        self.horizontalLayout.addWidget(self.toolButton_4)
        self.verticalLayout.addWidget(self.widget_container3)
        self.tableView = QtWidgets.QTableView(ExtractSettings)
        self.tableView.setAcceptDrops(True)
        self.tableView.setStyleSheet("QToolTip {\n"
"    color: black; \n"
"    background-color: #FFFFFF;\n"
"    border: 1px solid white;\n"
"    min-height: 20px;\n"
"}")
        self.tableView.setTabKeyNavigation(True)
        self.tableView.setDragEnabled(True)
        self.tableView.setDragDropOverwriteMode(False)
        self.tableView.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.tableView.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.setObjectName("tableView")
        self.verticalLayout.addWidget(self.tableView)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 2, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_container2 = QtWidgets.QWidget(ExtractSettings)
        self.widget_container2.setObjectName("widget_container2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_container2)
        self.horizontalLayout_3.setContentsMargins(3, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.widget_container2)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        spacerItem3 = QtWidgets.QSpacerItem(58, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.toolButton_2 = QtWidgets.QToolButton(self.widget_container2)
        self.toolButton_2.setIcon(icon)
        self.toolButton_2.setAutoRaise(True)
        self.toolButton_2.setObjectName("toolButton_2")
        self.horizontalLayout_3.addWidget(self.toolButton_2)
        self.verticalLayout_2.addWidget(self.widget_container2)
        self.listWidget_2 = AdvanceQlistwidget(ExtractSettings)
        self.listWidget_2.setStyleSheet("QToolTip {\n"
"    color: black; \n"
"    background-color: #FFFFFF;\n"
"    border: 1px solid white;\n"
"    min-height: 20px;\n"
"}")
        self.listWidget_2.setProperty("showDropIndicator", True)
        self.listWidget_2.setDragEnabled(True)
        self.listWidget_2.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.listWidget_2.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.listWidget_2.setObjectName("listWidget_2")
        self.verticalLayout_2.addWidget(self.listWidget_2)
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.checkBox_3 = QtWidgets.QCheckBox(ExtractSettings)
        self.checkBox_3.setChecked(True)
        self.checkBox_3.setObjectName("checkBox_3")
        self.horizontalLayout_5.addWidget(self.checkBox_3)
        self.spinBox = QtWidgets.QSpinBox(ExtractSettings)
        self.spinBox.setMaximum(999999999)
        self.spinBox.setSingleStep(10)
        self.spinBox.setProperty("value", 1)
        self.spinBox.setDisplayIntegerBase(10)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout_5.addWidget(self.spinBox)
        self.checkBox_4 = QtWidgets.QCheckBox(ExtractSettings)
        self.checkBox_4.setChecked(True)
        self.checkBox_4.setObjectName("checkBox_4")
        self.horizontalLayout_5.addWidget(self.checkBox_4)
        self.spinBox_2 = QtWidgets.QSpinBox(ExtractSettings)
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setMaximum(999999999)
        self.spinBox_2.setSingleStep(10)
        self.spinBox_2.setProperty("value", 1)
        self.spinBox_2.setDisplayIntegerBase(10)
        self.spinBox_2.setObjectName("spinBox_2")
        self.horizontalLayout_5.addWidget(self.spinBox_2)
        self.gridLayout.addLayout(self.horizontalLayout_5, 2, 0, 1, 2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_14 = QtWidgets.QPushButton(ExtractSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_14.sizePolicy().hasHeightForWidth())
        self.pushButton_14.setSizePolicy(sizePolicy)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/picture/resourses/version-control-icon_88399.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_14.setIcon(icon4)
        self.pushButton_14.setObjectName("pushButton_14")
        self.horizontalLayout_4.addWidget(self.pushButton_14)
        self.pushButton_13 = QtWidgets.QPushButton(ExtractSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_13.sizePolicy().hasHeightForWidth())
        self.pushButton_13.setSizePolicy(sizePolicy)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/picture/resourses/refresh-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_13.setIcon(icon5)
        self.pushButton_13.setObjectName("pushButton_13")
        self.horizontalLayout_4.addWidget(self.pushButton_13)
        self.label_6 = ClickedLableGif(ExtractSettings)
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.gridLayout.addLayout(self.horizontalLayout_4, 3, 0, 1, 2)

        self.retranslateUi(ExtractSettings)
        self.checkBox_2.toggled['bool'].connect(self.listWidget.setDisabled)
        self.checkBox_2.toggled['bool'].connect(self.toolButton.setDisabled)
        self.checkBox_3.toggled['bool'].connect(self.spinBox.setEnabled)
        self.checkBox_4.toggled['bool'].connect(self.spinBox_2.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(ExtractSettings)

    def retranslateUi(self, ExtractSettings):
        _translate = QtCore.QCoreApplication.translate
        ExtractSettings.setWindowTitle(_translate("ExtractSettings", "GenBank File Extract Settings"))
        self.label.setText(_translate("ExtractSettings", "Features to be extracted:"))
        self.checkBox_2.setToolTip(_translate("ExtractSettings", "Extract all features"))
        self.checkBox_2.setText(_translate("ExtractSettings", "All"))
        self.toolButton.setToolTip(_translate("ExtractSettings", "Add"))
        self.toolButton.setText(_translate("ExtractSettings", "..."))
        self.listWidget.setToolTip(_translate("ExtractSettings", "<html>\n"
"<head>\n"
"<meta http-equiv=content-type content=text/html;charset=ISO-8859-1>\n"
"</head>\n"
"<body>\n"
"<div>\n"
"<font face=\"Courier New\">\n"
"<span style=\'font-weight:600; color:purple;\'>For Example:</span><br>\n"
"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style=\'font-weight:600; color:#ff0000;\'>CDS</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2058..3272<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/gene=\"nad4\"<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/codon_start=1<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/transl_table=9<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/product=\"NADH&nbsp;dehydrogenase&nbsp;subunit&nbsp;4\"<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/protein_id=\"YP_009442302.1\"<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style=\'font-weight:600; color:#ff0000;\'>tRNA</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3274..3336<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/product=\"Q\"<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style=\'font-weight:600; color:#ff0000;\'>rRNA</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;8524..9472<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/product=\"rrnL\"<br>\n"
"</font>\n"
"</div>\n"
"</body>\n"
"</html>"))
        self.label_2.setToolTip(_translate("ExtractSettings", "Values corresponding to specific qualifiers"))
        self.label_2.setText(_translate("ExtractSettings", "Names unification:"))
        self.checkBox.setText(_translate("ExtractSettings", "Only extract these genes"))
        self.toolButton_6.setToolTip(_translate("ExtractSettings", "Import Table (.csv)"))
        self.toolButton_6.setText(_translate("ExtractSettings", "..."))
        self.toolButton_5.setToolTip(_translate("ExtractSettings", "Export Table"))
        self.toolButton_5.setText(_translate("ExtractSettings", "..."))
        self.toolButton_3.setToolTip(_translate("ExtractSettings", "Add"))
        self.toolButton_3.setText(_translate("ExtractSettings", "..."))
        self.toolButton_4.setToolTip(_translate("ExtractSettings", "Delete"))
        self.toolButton_4.setText(_translate("ExtractSettings", "..."))
        self.tableView.setToolTip(_translate("ExtractSettings", "<html>\n"
"<head>\n"
"<meta http-equiv=content-type content=text/html;charset=ISO-8859-1>\n"
"</head>\n"
"<body>\n"
"<div>\n"
"<font face=\"Courier New\">\n"
"<span style=\'font-weight:600; color:purple;\'>For Example:</span><br>\n"
"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;CDS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2058..3272\n"
"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/gene=\"<span style=\'font-weight:600; color:#ff0000;\'>nad4</span>\"\n"
"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/codon_start=1\n"
"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/transl_table=9\n"
"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/product=\"<span style=\'font-weight:600; color:#ff0000;\'>NADH&nbsp;dehydrogenase&nbsp;subunit&nbsp;4</span>\"\n"
"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/protein_id=\"YP_009442302.1\"\n"
"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;tRNA&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3274..3336\n"
"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/product=\"<span style=\'font-weight:600; color:#ff0000;\'>Q</span>\"\n"
"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;rRNA&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;8524..9472\n"
"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/product=\"<span style=\'font-weight:600; color:#ff0000;\'>rrnL</span>\"\n"
"</font>\n"
"</div>\n"
"</body>\n"
"</html>"))
        self.label_3.setText(_translate("ExtractSettings", "Qualifiers to be recognized:"))
        self.toolButton_2.setToolTip(_translate("ExtractSettings", "Add"))
        self.toolButton_2.setText(_translate("ExtractSettings", "..."))
        self.listWidget_2.setToolTip(_translate("ExtractSettings", "<html>\n"
"<head>\n"
"<meta http-equiv=content-type content=text/html;charset=ISO-8859-1>\n"
"</head>\n"
"<body>\n"
"<div>\n"
"<font face=\"Courier New\">\n"
"<span style=\'font-weight:600; color:purple;\'>For Example:</span><br>\n"
"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;CDS&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2058..3272\n"
"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/<span style=\'font-weight:600; color:#ff0000;\'>gene</span>=\"nad4\"\n"
"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/codon_start=1\n"
"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/transl_table=9\n"
"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/<span style=\'font-weight:600; color:#ff0000;\'>product</span>=\"NADH&nbsp;dehydrogenase&nbsp;subunit&nbsp;4\"\n"
"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/protein_id=\"YP_009442302.1\"\n"
"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;tRNA&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3274..3336\n"
"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/<span style=\'font-weight:600; color:#ff0000;\'>product</span>=\"Q\"\n"
"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;rRNA&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;8524..9472\n"
"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/<span style=\'font-weight:600; color:#ff0000;\'>product</span>=\"rrnL\"\n"
"</font>\n"
"</div>\n"
"</body>\n"
"</html>"))
        self.checkBox_3.setText(_translate("ExtractSettings", "Extract intergenic regions (> ? bp):"))
        self.checkBox_4.setText(_translate("ExtractSettings", "Extract overlapping regions (> ? bp):"))
        self.pushButton_14.setText(_translate("ExtractSettings", "Version"))
        self.pushButton_13.setText(_translate("ExtractSettings", "import/export settings"))
        self.label_6.setToolTip(_translate("ExtractSettings", "Brief example"))

from src.CustomWidget import AdvanceQlistwidget, ClickedLableGif
from uifiles import myRes_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ExtractSettings = QtWidgets.QDialog()
    ui = Ui_ExtractSettings()
    ui.setupUi(ExtractSettings)
    ExtractSettings.show()
    sys.exit(app.exec_())

