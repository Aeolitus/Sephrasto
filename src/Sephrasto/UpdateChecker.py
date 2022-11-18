import requests
from requests.exceptions import Timeout
import re
import Version
from PySide6 import QtWidgets, QtCore
import webbrowser
from EinstellungenWrapper import EinstellungenWrapper
from Wolke import Wolke

class UpdateChecker:

    _downloadLink = "https://dsaforum.de/app.php/dlext/?view=detail&df_id=213"

    @staticmethod
    def checkForUpdate():
        if Wolke.Settings["UpdateCheck_Disable"]:
            return

        try:
            response = requests.get(UpdateChecker._downloadLink, timeout = 1)
        except:
            return

        res = re.findall("Sephrasto_v(\S*).zip", response.text)
        if len(res) == 0:
            return

        version = [int(s) for s in res[0].split(".")]

        while len(version) < 3:
            version.append(0)

        if Version.isClientLower(version[0], version[1], version[2]):
            UpdateChecker.showUpdate(res[0])

    @staticmethod    
    def showUpdate(version):
        if Wolke.Settings["UpdateCheck_DisableFor"] == version:
            return

        messageBox = QtWidgets.QMessageBox()
        messageBox.setIcon(QtWidgets.QMessageBox.Information)
        messageBox.setWindowTitle("Neue Sephrasto-Version")
        messageBox.setText(f"Eine neue Version von Sephrasto ist verfügbar!\n\nInstallierte Version: {Version.toString()}\nNeue Version: {version}\n\nClicke auf Download, um zur Sephrasto-Seite auf dsaforum.de zu gelangen.")
        messageBox.addButton("Download", QtWidgets.QMessageBox.AcceptRole)
        messageBox.addButton("OK", QtWidgets.QMessageBox.AcceptRole)
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