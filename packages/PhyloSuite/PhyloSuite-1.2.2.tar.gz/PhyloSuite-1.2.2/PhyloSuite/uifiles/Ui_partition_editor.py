# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\Work\python\bioinfo_excercise\PhyloSuite\codes\PhyloSuite\uifiles\partition_editor.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Partition_editor(object):
    def setupUi(self, Partition_editor):
        Partition_editor.setObjectName("Partition_editor")
        Partition_editor.resize(758, 525)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Partition_editor)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.splitter = QtWidgets.QSplitter(Partition_editor)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(18, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_codon = QtWidgets.QPushButton(self.layoutWidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/picture/resourses/converter.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_codon.setIcon(icon)
        self.pushButton_codon.setObjectName("pushButton_codon")
        self.horizontalLayout_4.addWidget(self.pushButton_codon)
        self.pushButton_nocodon = QtWidgets.QPushButton(self.layoutWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/picture/resourses/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_nocodon.setIcon(icon1)
        self.pushButton_nocodon.setObjectName("pushButton_nocodon")
        self.horizontalLayout_4.addWidget(self.pushButton_nocodon)
        self.horizontalLayout.addLayout(self.horizontalLayout_4)
        spacerItem1 = QtWidgets.QSpacerItem(18, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/picture/resourses/table_row_add_after.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setIcon(icon1)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableView_partition = QtWidgets.QTableView(self.layoutWidget)
        self.tableView_partition.setSortingEnabled(False)
        self.tableView_partition.setObjectName("tableView_partition")
        self.verticalLayout.addWidget(self.tableView_partition)
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.pushButton_recog = QtWidgets.QPushButton(self.layoutWidget1)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/picture/resourses/refresh-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_recog.setIcon(icon3)
        self.pushButton_recog.setObjectName("pushButton_recog")
        self.horizontalLayout_3.addWidget(self.pushButton_recog)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.textEdit = QtWidgets.QTextEdit(self.layoutWidget1)
        self.textEdit.setPlaceholderText("")
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_2.addWidget(self.textEdit)
        self.verticalLayout_3.addWidget(self.splitter)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.label_3 = QtWidgets.QLabel(Partition_editor)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        self.label_4 = ClickedLableGif(Partition_editor)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.retranslateUi(Partition_editor)
        QtCore.QMetaObject.connectSlotsByName(Partition_editor)

    def retranslateUi(self, Partition_editor):
        _translate = QtCore.QCoreApplication.translate
        Partition_editor.setWindowTitle(_translate("Partition_editor", "Partition editor"))
        self.label.setText(_translate("Partition_editor", "Specify the data blocks:"))
        self.pushButton_codon.setText(_translate("Partition_editor", "Codon Mode"))
        self.pushButton_nocodon.setText(_translate("Partition_editor", "Cancel Codon Mode"))
        self.pushButton_2.setText(_translate("Partition_editor", "Add Row"))
        self.pushButton.setText(_translate("Partition_editor", "Delete Row"))
        self.label_2.setText(_translate("Partition_editor", "Automatically recognize partition from text:"))
        self.pushButton_recog.setText(_translate("Partition_editor", "Recognize"))
        self.textEdit.setToolTip(_translate("Partition_editor", "For example:\n"
"atp6 = 1-693;\n"
"atp8 = 694-882;\n"
"cox1 = 883-2475;\n"
"cox2 = 2476-3225;\n"
"cox3 = 3226-4089;"))
        self.label_3.setText(_translate("Partition_editor", "Demo:"))
        self.label_4.setToolTip(_translate("Partition_editor", "Brief example"))

from src.CustomWidget import ClickedLableGif
from uifiles import myRes_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Partition_editor = QtWidgets.QDialog()
    ui = Ui_Partition_editor()
    ui.setupUi(Partition_editor)
    Partition_editor.show()
    sys.exit(app.exec_())

