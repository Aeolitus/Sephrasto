from CharakterAssistent import Choice, ChoicePopup
from PyQt5 import QtCore, QtGui, QtWidgets


class ChoicePopupWrapper(object):
    def __init__(self, choiceList, windowTitle):
        super().__init__()
        self.formMain = QtWidgets.QDialog()
        self.formMain.setWindowFlags(
            QtCore.Qt.Window
            | QtCore.Qt.CustomizeWindowHint
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowCloseButtonHint
        )
        self.ui = ChoicePopup.Ui_formMain()
        self.ui.setupUi(self.formMain)
        self.formMain.setWindowTitle(
            self.formMain.windowTitle() + " (" + windowTitle + ")"
        )
        self.setupMainForm(choiceList)
        self.formMain.show()

        self.formMain.setWindowModality(QtCore.Qt.ApplicationModal)
        self.formMain.show()
        self.ret = self.formMain.exec_()
        self.choice = None
        if self.ret == QtWidgets.QDialog.Accepted:
            for i in range(len(choiceList.choices)):
                if self.buttons[i].isChecked():
                    self.choice = choiceList.choices[i]
                    return

    def setupMainForm(self, choiceList):
        self.buttons = []

        for choice in choiceList.choices:
            choiceStr = choice.toString()
            if not choiceStr:
                continue

            button = QtWidgets.QRadioButton(choiceStr)
            if len(self.buttons) == 0:
                button.setChecked(True)
            self.buttons.append(button)
            self.ui.verticalLayout.addWidget(button)
