"""
The find dialog is translated from QFindDialogs.
https://github.com/Yet-Zio/QFindDialogs.git
Copyright (C) 2021 Yet-Zio

* Redistribution and use in source and binary forms,
* with or without modification, are permitted provided
* that the following conditions are met:
*
* 1. Redistributions of source code must retain the above copyright notice,
*    this list of conditions and the following disclaimer.
*
* 2. Redistributions in binary form must reproduce the above copyright notice,
*    this list of conditions and the following disclaimer in the documentation and/or other
*    materials provided with the distribution.
*
* 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or
*    promote products derived from this software without specific prior written permission.
*
* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
* AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
* OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
* COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
* CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
* LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
* WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
* OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

LibFind.py

"""

from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtGui import QTextCursor, QTextDocument
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QCheckBox, QGridLayout,
    QVBoxLayout, QWidget, QPushButton, QDialogButtonBox,
    QHBoxLayout, QPlainTextEdit
)


class FindDialog(QDialog):
    def __init__(self, search_editor: QPlainTextEdit, parent=None):
        super().__init__(parent)

        self.setWindowIcon(QtGui.QIcon("assets/icons/search.svg"))

        self.search_editor = search_editor
        self.last_match = False

        self.label = QLabel("Find &what: ")
        self.lineEdit = QLineEdit()
        self.label.setBuddy(self.lineEdit)

        self.caseCheckBox = QCheckBox("Match &case")
        self.caseCheckBox.setChecked(True)
        self.fromStartCheckBox = QCheckBox("Search from &start")
        self.fromStartCheckBox.setChecked(True)
        self.regexCheckBox = QCheckBox("Regex")
        self.regexCheckBox.setChecked(False)

        self.findButton = QPushButton("&Find")
        self.findButton.clicked.connect(self.find)
        self.findButton.setDefault(True)

        self.moreButton = QPushButton("&More")
        self.moreButton.setCheckable(True)
        self.moreButton.setAutoDefault(False)

        self.extension = QWidget()

        self.wholeWordsCheckBox = QCheckBox("&Whole words")
        self.backwardCheckBox = QCheckBox("Search &backward")
        self.searchSelectionCheckBox = QCheckBox("Search se&lection")

        self.buttonBox = QDialogButtonBox(Qt.Orientation.Vertical)
        self.buttonBox.addButton(self.findButton, QDialogButtonBox.ButtonRole.ActionRole)
        self.buttonBox.addButton(self.moreButton, QDialogButtonBox.ButtonRole.ActionRole)

        self.regexCheckBox.toggled.connect(self.regex_mode)
        self.moreButton.toggled.connect(self.extension.setVisible)

        extension_layout = QVBoxLayout()
        extension_layout.setContentsMargins(0, 0, 0, 0)
        extension_layout.addWidget(self.wholeWordsCheckBox)
        extension_layout.addWidget(self.backwardCheckBox)
        extension_layout.addWidget(self.searchSelectionCheckBox)
        self.extension.setLayout(extension_layout)

        top_left_layout = QHBoxLayout()
        top_left_layout.addWidget(self.label)
        top_left_layout.addWidget(self.lineEdit)

        left_layout = QVBoxLayout()
        left_layout.addLayout(top_left_layout)
        left_layout.addWidget(self.caseCheckBox)
        left_layout.addWidget(self.regexCheckBox)
        left_layout.addWidget(self.fromStartCheckBox)

        main_layout = QGridLayout()
        main_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetFixedSize)
        main_layout.addLayout(left_layout, 0, 0)
        main_layout.addWidget(self.buttonBox, 0, 1)
        main_layout.addWidget(self.extension, 1, 0, 1, 2)
        main_layout.setRowStretch(2, 1)

        self.setLayout(main_layout)

        self.setWindowTitle("Find")
        self.extension.hide()

    def find(self):
        query = self.lineEdit.text()
        re = QtCore.QRegularExpression()

        editor = self.search_editor

        if self.fromStartCheckBox.isChecked():
            cursor = editor.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.Start)
            editor.setTextCursor(cursor)
        self.fromStartCheckBox.setChecked(False)

        if self.regexCheckBox.isChecked():
            re.setPattern(query)
            if self.backwardCheckBox.isChecked():
                self.last_match = editor.find(re, QTextDocument.FindFlag.FindBackward)
            else:
                self.last_match = editor.find(re, QTextDocument.FindFlag(0))

        if self.searchSelectionCheckBox.isChecked():
            query = editor.textCursor().selectedText()
            editor.find(query)
        else:
            if self.backwardCheckBox.isChecked():
                flags = QTextDocument.FindFlag.FindBackward
                if self.wholeWordsCheckBox.isChecked() and self.caseCheckBox.isChecked():
                    flags |= QTextDocument.FindFlag.FindWholeWords | QTextDocument.FindFlag.FindCaseSensitively
                elif self.wholeWordsCheckBox.isChecked() and not self.caseCheckBox.isChecked():
                    flags |= QTextDocument.FindFlag.FindWholeWords
                elif not self.wholeWordsCheckBox.isChecked() and self.caseCheckBox.isChecked():
                    flags |= QTextDocument.FindFlag.FindCaseSensitively
            else:
                flags = QTextDocument.FindFlag(0)
                if self.wholeWordsCheckBox.isChecked() and self.caseCheckBox.isChecked():
                    flags |= QTextDocument.FindFlag.FindWholeWords | QTextDocument.FindFlag.FindCaseSensitively
                elif self.wholeWordsCheckBox.isChecked() and not self.caseCheckBox.isChecked():
                    flags |= QTextDocument.FindFlag.FindWholeWords
                elif not self.wholeWordsCheckBox.isChecked() and self.caseCheckBox.isChecked():
                    flags |= QTextDocument.FindFlag.FindCaseSensitively

            self.last_match = editor.find(query, flags)

    def regex_mode(self):
        self.caseCheckBox.setChecked(False)
        self.wholeWordsCheckBox.setChecked(False)

        self.caseCheckBox.setEnabled(False)
        self.wholeWordsCheckBox.setEnabled(False)

    def toggle_visibility(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    editor = QPlainTextEdit()
    editor.show()
    find = FindDialog(editor)
    find.show()
    app.exec()
