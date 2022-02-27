from PyQt5 import QtCore, QtWidgets, QtGui
from UI import ChoicePopup
from Wolke import Wolke

class VariantPopupWrapper(object):
    def __init__(self, variantListCollection, windowTitle, currentEP):
        super().__init__()
        self.formMain = QtWidgets.QDialog()
        self.formMain.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint)
        self.ui = ChoicePopup.Ui_formMain()
        self.ui.setupUi(self.formMain)
        self.formMain.setWindowTitle(self.formMain.windowTitle() + " (" + windowTitle + ")")

        self.buttons = []
        self.labels = []
        self.ui.labelEP.setText(str(currentEP))
        for variantList in variantListCollection.choiceLists:
            if variantListCollection.chooseOne:
                button = QtWidgets.QRadioButton(variantList.toString())
                if variantList == variantListCollection.choiceLists[0]:
                    button.setChecked(True)
            else:
                button = QtWidgets.QCheckBox(variantList.toString())

            self.buttons.append(button)
            self.ui.verticalLayout.addWidget(button)

            desc = variantList.getDescription()
            if desc:
                label = QtWidgets.QLabel(desc)
                self.labels.append(label)
                self.ui.verticalLayout.addWidget(label)

        self.formMain.setWindowModality(QtCore.Qt.ApplicationModal)
        self.formMain.show()

        self.ret = self.formMain.exec_()
        self.choices = []
        if self.ret == QtWidgets.QDialog.Accepted:
            for i in range(len(variantListCollection.choiceLists)):
                if self.buttons[i].isChecked():
                    self.choices.append(i)