from PyQt6 import QtWidgets, QtCore, QtGui
from text_ui import Ui_MainWindow

import pathlib


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.bold = False
        self.curve = False
        self.underline = False

        self.path = pathlib.Path.cwd()

        self.untitled = "Untitled.txt"
        self.name = ""

        self.change_untitled()
        self.name = self.untitled

        self.change_untitled()

        self.setWindowTitle(self.name)

        self.ui.left_pushButton.clicked.connect(
            lambda: self.ui.textEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        )
        self.ui.right_pushButton.clicked.connect(
            lambda: self.ui.textEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        )
        self.ui.center_pushButton.clicked.connect(
            lambda: self.ui.textEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        )
        self.ui.justify_pushButton.clicked.connect(
            lambda: self.ui.textEdit.setAlignment(QtCore.Qt.AlignmentFlag.AlignJustify)
        )

        self.ui.bold_pushButton.setCheckable(True)
        self.ui.curve_pushButton.setCheckable(True)
        self.ui.ess_pushButton.setCheckable(True)

        self.ui.bold_pushButton.toggled.connect(lambda x: self.ui.textEdit.setFontWeight(QtGui.QFont.Weight.Bold if x
                                                                                         else QtGui.QFont.Weight.Normal))
        self.ui.curve_pushButton.toggled.connect(self.ui.textEdit.setFontItalic)
        self.ui.ess_pushButton.toggled.connect(self.ui.textEdit.setFontUnderline)

        self.ui.font.currentFontChanged.connect(self.ui.textEdit.setCurrentFont)
        self.ui.comboBox.currentIndexChanged.connect(lambda x: self.ui.textEdit.setFontPointSize(int(x)))

        self.ui.actionNew.triggered.connect(self.new_file)
        self.ui.actionOpen.triggered.connect(self.open_file)
        self.ui.actionSave.triggered.connect(self.save_file)
        self.ui.actionSave_as.triggered.connect(self.save_file_as)

    def change_untitled(self):
        i = 0
        while True:
            file_name = "Untitled"
            if i:
                file_name += f" ({i})"
            else:
                i += 1
            i += 1
            file_name += ".txt"
            if not (pathlib.Path(str(self.path / file_name)).exists()):
                self.untitled = file_name
                break

    def Message(self):
        message = QtWidgets.QMessageBox.question(
            self,
            "Choose message",
            f"Do you want save changes in file {self.name}?",
            (
                QtWidgets.QMessageBox.StandardButton.Yes
                | QtWidgets.QMessageBox.StandardButton.No
                | QtWidgets.QMessageBox.StandardButton.Cancel
            ),
            QtWidgets.QMessageBox.StandardButton.Cancel,
        )
        return message

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if (self.path / self.name ).exists() is not True and self.ui.textEdit.toPlainText() == "":
            a0.accept()
            return

        if (self.path / self.name).exists() is not True or open(self.path / self.name).read() != self.ui.textEdit.toPlainText():
            message = self.Message()

            if message == QtWidgets.QMessageBox.StandardButton.Yes:
                self.save_file((self.path / self.name).exists())
                a0.accept()
            elif message == QtWidgets.QMessageBox.StandardButton.No:
                a0.accept()
            else:
                a0.ignore()
        else:
            a0.accept()

    def save_file_as(self):
        file_filter = (
            "Text file (*.txt);; Word file (*.doc, *.docx);; Html file (*.html)"
        )
        self.change_untitled()
        response = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            directory=str(self.path / self.untitled),
            caption="Save file",
            filter=file_filter,
            initialFilter="Text file (*.txt)",
        )
        if response[0]:
            path = pathlib.Path(response[0])
            self.path = path.parent
            self.name = path.name
            self.setWindowTitle(self.name)

            if "Untitled" in str(self.name):
                self.change_untitled()
                
            self.save_file(True)

    def save_file(self, flag=False):
        if flag or (self.path / self.name).exists():
            text = self.ui.textEdit.toPlainText()
            f = open(str(self.path / self.name), 'w')
            f.write(text)
            f.close()
        else:
            self.save_file_as()

    def new_file(self):
        if ( self.path / self.name ).exists() is False and self.ui.textEdit.toPlainText() == "":
            return

        if (self.path / self.name).exists() is False or open(self.path / self.name).read() != self.ui.textEdit.toPlainText():
            message = self.Message()
            if message == QtWidgets.QMessageBox.StandardButton.Yes:
                if (self.path / self.name).exists():
                    self.save_file()
                    self.change_untitled()
                    self.name = self.untitled
                    self.setWindowTitle(self.name)
                else:
                    self.save_file_as()
                    self.name = self.untitled
                    self.setWindowTitle(self.name)
                self.ui.textEdit.clear()
            elif message == QtWidgets.QMessageBox.StandardButton.No:
                self.ui.textEdit.clear()
                self.name = self.untitled
                self.setWindowTitle(self.name)

    def open_file(self):
        file_filter = (
            "Text file (*.txt);; Word file (*.doc, *.docx);; Html file (*.html)"
        )

        response = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            directory=str(self.path),
            caption="Select file",
            filter=file_filter,
            initialFilter="Text file (*.txt)",
        )

        if response[0]:
            path = pathlib.Path(response[0])
            self.path = path.parent
            self.name = path.name
            text = open(self.path / self.name).read()
            self.ui.textEdit.setPlainText(text)

            self.setWindowTitle(self.name)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication([])
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec())
