from PyQt5 import QtCore, QtWidgets, QtGui
from UI import ChoicePopup
from CharakterAssistent import Choice
from Wolke import Wolke

class ChoicePopupWrapper(object):
    def __init__(self, choiceList, windowTitle, currentEP):
        super().__init__()
        self.form = QtWidgets.QDialog()
        self.form.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint)
        self.ui = ChoicePopup.Ui_formMain()
        self.ui.setupUi(self.form)

        self.form.setWindowTitle(self.form.windowTitle() + " (" + windowTitle + ")")
        self.buttons = []
        self.ui.labelEP.setText(str(currentEP))
        for choice in choiceList.choices:
            choiceStr = choice.toString()
            if not choiceStr:
                continue

            button = QtWidgets.QRadioButton(choiceStr)
            if len(self.buttons) == 0:
                button.setChecked(True)
            self.buttons.append(button)
            self.ui.verticalLayout.addWidget(button)

        self.form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.form.show()

        self.ret = self.form.exec_()
        self.choice = None
        if self.ret == QtWidgets.QDialog.Accepted:
            for i in range(len(choiceList.choices)):
                if self.buttons[i].isChecked():
                    self.choice = choiceList.choices[i]
                    return