import re
import Version
from PySide6 import QtWidgets, QtCore, QtWebEngineCore
from EinstellungenWrapper import EinstellungenWrapper
from Wolke import Wolke
import webbrowser

class UpdateChecker:

    _apiLink = "https://api.github.com/repos/Aeolitus/Sephrasto/releases/latest"
    _downloadLink = "https://github.com/Aeolitus/Sephrasto/releases/latest"
    _page = None

    @staticmethod
    def checkForUpdate():
        if Wolke.Settings["UpdateCheck_Disable"] or UpdateChecker._page is not None:
            return

        UpdateChecker._page = QtWebEngineCore.QWebEnginePage()

        def onTextDownloaded(text):
            UpdateChecker._page = None
            res = re.findall("Sephrasto_(\S*).zip", text)
            if len(res) == 0:
                return
            version = Version.disectVersionString(res[0])
            if not version:
                return
            if Version.isClientLower(version):
                UpdateChecker.showUpdate(res[0])

        def loadFinished(ok):
            if ok:
                UpdateChecker._page.toPlainText(onTextDownloaded)
            else:
                UpdateChecker._page = None

        UpdateChecker._page.loadFinished.connect(loadFinished)
        UpdateChecker._page.load(QtCore.QUrl(UpdateChecker._apiLink))

    @staticmethod    
    def showUpdate(version):
        if Wolke.Settings["UpdateCheck_DisableFor"] == version:
            return

        messageBox = QtWidgets.QMessageBox()
        messageBox.setIcon(QtWidgets.QMessageBox.Information)
        messageBox.setWindowTitle("Neue Sephrasto-Version")
        messageBox.setText(f"Eine neue Version von Sephrasto ist verfügbar! Clicke auf Download, um zur Sephrasto-Seite auf github.com zu gelangen.\n\nInstallierte Version: {Version.toString()}\nNeue Version: {version}")
        messageBox.addButton("Download", QtWidgets.QMessageBox.AcceptRole)
        messageBox.addButton("Später", QtWidgets.QMessageBox.AcceptRole)
        messageBox.setEscapeButton(QtWidgets.QMessageBox.Close)  

        check = QtWidgets.QCheckBox("Information für dieses Update nicht mehr anzeigen.")
        check.setCheckState(QtCore.Qt.Unchecked)
        messageBox.setCheckBox(check)

        result = messageBox.exec()

        if result == 0:
            webbrowser.open(UpdateChecker._downloadLink)

        if check.isChecked():
            Wolke.Settings["UpdateCheck_DisableFor"] = version
            EinstellungenWrapper.save()