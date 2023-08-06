# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\Work\python\bioinfo_excercise\PhyloSuite\PhyloSuite\PhyloSuite\uifiles\tRNA_reANNT.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_tRNA_ANNT(object):
    def setupUi(self, tRNA_ANNT):
        tRNA_ANNT.setObjectName("tRNA_ANNT")
        tRNA_ANNT.resize(615, 587)
        tRNA_ANNT.setFocusPolicy(QtCore.Qt.NoFocus)
        self.gridLayout_3 = QtWidgets.QGridLayout(tRNA_ANNT)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox = QtWidgets.QGroupBox(tRNA_ANNT)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setOpenExternalLinks(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(self.groupBox)
        self.textBrowser.setUndoRedoEnabled(True)
        self.textBrowser.setReadOnly(True)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 1, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/picture/resourses/Save-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(tRNA_ANNT)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.textBrowser_2 = QtWidgets.QTextBrowser(self.groupBox_2)
        self.textBrowser_2.setUndoRedoEnabled(True)
        self.textBrowser_2.setReadOnly(False)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.gridLayout_2.addWidget(self.textBrowser_2, 1, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_2)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/picture/resourses/if_start_60207.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 2, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_2, 1, 0, 1, 1)

        self.retranslateUi(tRNA_ANNT)
        QtCore.QMetaObject.connectSlotsByName(tRNA_ANNT)

    def retranslateUi(self, tRNA_ANNT):
        _translate = QtCore.QCoreApplication.translate
        tRNA_ANNT.setWindowTitle(_translate("tRNA_ANNT", "Predict tRNA"))
        self.groupBox.setTitle(_translate("tRNA_ANNT", "Step 1"))
        self.label.setText(_translate("tRNA_ANNT", "<html><head/><body><p>Import the unrecognized tRNAs (listed below) into <a href=\"http://130.235.46.10/ARWEN/\"><span style=\" text-decoration: underline; color:#0000ff;\">ARWEN</span></a></p></body></html>"))
        self.pushButton.setText(_translate("tRNA_ANNT", "Save to file"))
        self.groupBox_2.setTitle(_translate("tRNA_ANNT", "Step 2"))
        self.label_2.setText(_translate("tRNA_ANNT", "<html><head/><body><p>Paste the ARWEN results here and click <span style=\" font-weight:600; color:#ff0000;\">start</span></p></body></html>"))
        self.pushButton_2.setText(_translate("tRNA_ANNT", "Start"))

from uifiles import myRes_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    tRNA_ANNT = QtWidgets.QDialog()
    ui = Ui_tRNA_ANNT()
    ui.setupUi(tRNA_ANNT)
    tRNA_ANNT.show()
    sys.exit(app.exec_())

