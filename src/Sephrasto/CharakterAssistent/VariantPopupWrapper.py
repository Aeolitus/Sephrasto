from PySide6 import QtCore, QtWidgets, QtGui
from UI import ChoicePopup
from Wolke import Wolke

class VariantPopupWrapper(object):
    def __init__(self, variantListCollection, windowTitle, currentEP):
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

        self.form.setWindowModality(QtCore.Qt.ApplicationModal)
        self.form.show()

        self.ret = self.form.exec()
        self.choices = []
        if self.ret == QtWidgets.QDialog.Accepted:
            for i in range(len(variantListCollection.choiceLists)):
                if self.buttons[i].isChecked():
                    self.choices.append(i)