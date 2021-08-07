from PyQt5 import QtCore, QtWidgets, QtGui
from CharakterAssistent import ChoicePopup

class VariantPopupWrapper(object):
    def __init__(self, variantListCollection, windowTitle):
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
        self.setupMainForm(variantListCollection)
        self.formMain.show()

        self.formMain.setWindowModality(QtCore.Qt.ApplicationModal)
        self.formMain.show()
        self.ret = self.formMain.exec_()
        self.choices = []
        if self.ret == QtWidgets.QDialog.Accepted:
            for i in range(len(variantListCollection.choiceLists)):
                if self.buttons[i].isChecked():
                    self.choices.append(i)

    def setupMainForm(self, variantListCollection):
        self.buttons = []
        self.labels = []

        for variantList in variantListCollection.choiceLists:
            if variantListCollection.chooseOne:
                button = QtWidgets.QRadioButton(variantList.name)
                if variantList == variantListCollection.choiceLists[0]:
                    button.setChecked(True)
            else:
                button = QtWidgets.QCheckBox(variantList.name)

            self.buttons.append(button)
            self.ui.verticalLayout.addWidget(button)

            #labelText = ""
            #for choice in variantList.choices:
            #    choiceStr = choice.toString()
            #    if not choiceStr:
            #        continue
            #    labelText += choiceStr + ", "
            #labelText = labelText[:-2]
            #label = QtWidgets.QLabel(labelText)
            #self.labels.append(label)
            #self.ui.verticalLayout.addWidget(label)