# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DatenbankMain.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets, QtGui
import Fertigkeiten
import Datenbank
import DatenbankEditFertigkeit
import DatenbankEditTalent
import DatenbankEditVorteil
import DatenbankSelectType

class Ui_Form(object):
    def __init__(self):
        self.datenbank = Datenbank.Datenbank()
        
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(543, 452)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 521, 431))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.showTalente = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.showTalente.setChecked(True)
        self.showTalente.setObjectName("showTalente")
        self.showTalente.stateChanged.connect(self.updateGUI)
        self.verticalLayout.addWidget(self.showTalente)
        self.showVorteile = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.showVorteile.setChecked(True)
        self.showVorteile.setTristate(False)
        self.showVorteile.setObjectName("showVorteile")
        self.showVorteile.stateChanged.connect(self.updateGUI)
        self.verticalLayout.addWidget(self.showVorteile)
        self.showFertigkeiten = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.showFertigkeiten.setChecked(True)
        self.showFertigkeiten.setObjectName("showFertigkeiten")
        self.showFertigkeiten.stateChanged.connect(self.updateGUI)
        self.verticalLayout.addWidget(self.showFertigkeiten)
        self.showUebernatuerlicheFertigkeiten = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.showUebernatuerlicheFertigkeiten.setChecked(True)
        self.showUebernatuerlicheFertigkeiten.setObjectName("showUebernatuerlicheFertigkeiten")
        self.showUebernatuerlicheFertigkeiten.stateChanged.connect(self.updateGUI)
        self.verticalLayout.addWidget(self.showUebernatuerlicheFertigkeiten)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.loadDatenbank)
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.saveDatenbank)
        
        self.verticalLayout.addWidget(self.pushButton)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.listDatenbank = QtWidgets.QListView(self.horizontalLayoutWidget)
        self.listDatenbank.setObjectName("listDatenbank")
        
        self.model = QtGui.QStandardItemModel(self.listDatenbank)
        self.listDatenbank.setModel(self.model)
        self.listDatenbank.doubleClicked.connect(self.listItemEvent)
        
        self.verticalLayout_2.addWidget(self.listDatenbank)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.buttonHinzufuegen = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.buttonHinzufuegen.setObjectName("buttonHinzufuegen")
        self.horizontalLayout.addWidget(self.buttonHinzufuegen)
        self.buttonEditieren = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.buttonEditieren.setObjectName("buttonEditieren")
        self.buttonEditieren.clicked.connect(self.editSelected)
        
        self.horizontalLayout.addWidget(self.buttonEditieren)
        self.buttonLoeschen = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.buttonLoeschen.setObjectName("buttonLoeschen")
        self.buttonLoeschen.clicked.connect(self.deleteSelected)
        
        self.horizontalLayout.addWidget(self.buttonLoeschen)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.showTalente, self.showVorteile)
        Form.setTabOrder(self.showVorteile, self.showFertigkeiten)
        Form.setTabOrder(self.showFertigkeiten, self.showUebernatuerlicheFertigkeiten)
        Form.setTabOrder(self.showUebernatuerlicheFertigkeiten, self.buttonHinzufuegen)
        Form.setTabOrder(self.buttonHinzufuegen, self.buttonEditieren)
        Form.setTabOrder(self.buttonEditieren, self.buttonLoeschen)
        Form.setTabOrder(self.buttonLoeschen, self.pushButton_2)
        Form.setTabOrder(self.pushButton_2, self.pushButton)
        
        self.buttonHinzufuegen.clicked.connect(self.hinzufuegen)
        self.updateGUI()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Datenbank-Editor"))
        self.showTalente.setText(_translate("Form", "Talente"))
        self.showVorteile.setText(_translate("Form", "Vorteile"))
        self.showFertigkeiten.setText(_translate("Form", "Profane Fertigkeiten"))
        self.showUebernatuerlicheFertigkeiten.setText(_translate("Form", "Übernatürliche Fertigkeiten"))
        self.pushButton_2.setText(_translate("Form", "Andere Regelbasis laden"))
        self.pushButton.setText(_translate("Form", "Regelbasis speichern"))
        self.buttonHinzufuegen.setText(_translate("Form", "Hinzufügen"))
        self.buttonEditieren.setText(_translate("Form", "Editieren"))
        self.buttonLoeschen.setText(_translate("Form", "Löschen"))
        
    def updateGUI(self):
        self.model.clear()
        if self.showTalente.isChecked():
            for itm in self.datenbank.talente:
                item = QtGui.QStandardItem(itm + " : Talent")
                item.setEditable(False)
                self.model.appendRow(item)
        if self.showVorteile.isChecked():
            for itm in self.datenbank.vorteile:
                item = QtGui.QStandardItem(itm + " : Vorteil")
                item.setEditable(False)
                self.model.appendRow(item) 
        if self.showFertigkeiten.isChecked():
            for itm in self.datenbank.fertigkeiten:
                item = QtGui.QStandardItem(itm + " : Fertigkeit")
                item.setEditable(False)
                self.model.appendRow(item) 
        if self.showUebernatuerlicheFertigkeiten.isChecked():
            for itm in self.datenbank.übernatürlicheFertigkeiten:
                item = QtGui.QStandardItem(itm + " : Übernatürliche Fertigkeit")
                item.setEditable(False)
                self.model.appendRow(item) 
        self.listDatenbank.setModel(self.model)
               
    @QtCore.pyqtSlot("QModelIndex")   
    def listItemEvent(self, item):
        tmp = self.model.itemData(item)[0].split(" : ")
        if tmp[1] == "Talent":
            nameSt = self.datenbank.talente[tmp[0]].name
            tal = self.editTalent(self.datenbank.talente[tmp[0]])
            if tal is not None:
                self.datenbank.talente.pop(nameSt,None)
                self.datenbank.talente.update({tal.name: tal})
                self.updateGUI()
        elif tmp[1] == "Vorteil":
            nameSt = self.datenbank.vorteile[tmp[0]].name
            vor = self.editVorteil(self.datenbank.vorteile[tmp[0]])
            if vor is not None:
                self.datenbank.vorteile.pop(nameSt,None)
                self.datenbank.vorteile.update({vor.name: vor})
                self.updateGUI()
        elif tmp[1] == "Fertigkeit":
            nameSt = self.datenbank.fertigkeiten[tmp[0]].name
            fer = self.editFertigkeit(self.datenbank.fertigkeiten[tmp[0]])
            if fer is not None:
                self.datenbank.fertigkeiten.pop(nameSt,None)
                self.datenbank.fertigkeiten.update({fer.name: fer})
                self.updateGUI()
        elif tmp[1] == "Übernatürliche Fertigkeit":
            nameSt = self.datenbank.übernatürlicheFertigkeiten[tmp[0]].name
            fer = self.editUebernatuerlich(self.datenbank.übernatürlicheFertigkeiten[tmp[0]])
            if fer is not None:
                self.datenbank.übernatürlicheFertigkeiten.pop(nameSt,None)
                self.datenbank.übernatürlicheFertigkeiten.update({fer.name: fer})
                self.updateGUI()
    
    def hinzufuegen(self):
        '''
        Lässt den Nutzer einen neuen Eintrag in die Datenbank einfügen.
        Öffnet zunächst den DatenbankSelectType-Dialog, welcher den 
        Nutzer fragt, was für ein Eintrag angelegt werden soll. 
        Akzeptiert der Nutzer, wird seiner Auswahl nach ein Dialog zum
        Erstellen des Eintrages geöffnet.
        '''
        Dialog = QtWidgets.QDialog()
        ui = DatenbankSelectType.Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.show()
        ret = Dialog.exec_()
        if ret == QtWidgets.QDialog.Accepted:
            entryType = ui.returnEntryType()
            if entryType is "Talent":
                self.addTalent()
            elif entryType is "Vorteil":
                self.addVorteil()
            elif entryType is "Fertigkeit":
                self.addFertigkeit()
            else:
                self.addUebernatuerlich()
        
    def addTalent(self):
        tal = Fertigkeiten.Talent()
        ret = self.editTalent(tal)
        if ret is not None:
            self.datenbank.talente.update({ret.name: ret})
            self.updateGUI();
    def addVorteil(self):
        vor = Fertigkeiten.Vorteil()
        ret = self.editVorteil(vor)
        if ret is not None:
            self.datenbank.vorteile.update({ret.name: ret})
            self.updateGUI();
    def addFertigkeit(self):
        fer = Fertigkeiten.Fertigkeit()
        ret = self.editFertigkeit(fer)
        if ret is not None:
            self.datenbank.fertigkeiten.update({ret.name: ret})
            self.updateGUI();
    def addUebernatuerlich(self):
        fer = Fertigkeiten.Fertigkeit()
        ret = self.editUebernatuerlich(fer)
        if ret is not None:
            self.datenbank.übernatürlicheFertigkeiten.update({ret.name: ret})
            self.updateGUI();
            
    def editTalent(self,talent):
        talentDialog = QtWidgets.QDialog()
        ui = DatenbankEditTalent.Ui_talentDialog()
        ui.setupUi(talentDialog)
        ui.nameEdit.setText(talent.name)
        if talent.verbilligt:
            ui.buttonVerbilligt.setChecked(True)
        elif talent.kosten is not 0:
            ui.buttonVerbilligt.setChecked(True)
            ui.comboKosten.setCurrentText(str(talent.kosten) + " EP")
        else:
            ui.buttonRegulaer.setChecked(True)
        ui.fertigkeitenEdit.setText(repr(talent.fertigkeiten))
        ui.voraussetzungenEdit.setText(repr(talent.voraussetzungen))
        ui.textEdit.setPlainText(talent.text)
        talentDialog.show()
        ret = talentDialog.exec_()
        if ret == QtWidgets.QDialog.Accepted:
            talent = ui.createTalent()
            return talent
        else:
            return None
        
    def editVorteil(self,vorteil):
        vorteilDialog = QtWidgets.QDialog()
        ui = DatenbankEditVorteil.Ui_vorteilDialog()
        ui.setupUi(vorteilDialog)
        ui.nameEdit.setText(vorteil.name)
        ui.kostenEdit.setValue(vorteil.kosten)
        ui.comboNachkauf.setCurrentText(vorteil.nachkauf)
        ui.voraussetzungenEdit.setText(repr(vorteil.voraussetzungen))
        ui.textEdit.setPlainText(vorteil.text)
        vorteilDialog.show()
        ret = vorteilDialog.exec_()
        if ret == QtWidgets.QDialog.Accepted:
            vorteil = ui.createVorteil()
            return vorteil
        else:
            return None
        
    def editFertigkeit(self,fertigkeit):
        fertDialog = QtWidgets.QDialog()
        ui = DatenbankEditFertigkeit.Ui_fertigkeitDialog()
        ui.setupUi(fertDialog)
        ui.nameEdit.setText(fertigkeit.name)
        ui.steigerungsfaktorEdit.setValue(fertigkeit.steigerungsfaktor)
        ui.comboAttribut1.setCurrentText(fertigkeit.attribute[0])
        ui.comboAttribut2.setCurrentText(fertigkeit.attribute[1])
        ui.comboAttribut3.setCurrentText(fertigkeit.attribute[2])
        ui.voraussetzungenEdit.setText(" - ")
        if fertigkeit.kampffertigkeit is 1:
            ui.checkKampffertigkeit.setChecked();
        ui.radioProfan.setChecked(True)
        ui.radioUebernatuerlich.setCheckable(False)
        ui.voraussetzungenEdit.setReadOnly(True)
        ui.textEdit.setPlainText(fertigkeit.text)
        
        fertDialog.show()
        ret = fertDialog.exec_()
        if ret == QtWidgets.QDialog.Accepted:
            fert = ui.createFertigkeit()
            return fert
        else:
            return None
        
    def editUebernatuerlich(self,fertigkeit):
        fertDialog = QtWidgets.QDialog()
        ui = DatenbankEditFertigkeit.Ui_fertigkeitDialog()
        ui.setupUi(fertDialog)
        ui.nameEdit.setText(fertigkeit.name)
        ui.steigerungsfaktorEdit.setValue(fertigkeit.steigerungsfaktor)
        ui.comboAttribut1.setCurrentText(fertigkeit.attribute[0])
        ui.comboAttribut2.setCurrentText(fertigkeit.attribute[1])
        ui.comboAttribut3.setCurrentText(fertigkeit.attribute[2])
        ui.voraussetzungenEdit.setText(repr(fertigkeit.voraussetzungen))
        ui.checkKampffertigkeit.setCheckable(False)
        ui.radioProfan.setCheckable(False)
        ui.radioUebernatuerlich.setChecked(True)
        ui.voraussetzungenEdit.setReadOnly(False)
        ui.textEdit.setPlainText(fertigkeit.text)
        
        fertDialog.show()
        ret = fertDialog.exec_()
        if ret == QtWidgets.QDialog.Accepted:
            fert = ui.createFertigkeit()
            return fert
        else:
            return None
        
    def editSelected(self):
        for itm in self.listDatenbank.selectedIndexes():
            tmp = self.model.itemData(itm)[0].split(" : ")
            if tmp[1] == "Talent":
                tal = self.datenbank.talente[tmp[0]]
                if tal is not None:
                    ret = self.editTalent(tal)
                    if ret is not None:
                        self.datenbank.talente.pop(tmp[0],None)
                        self.datenbank.talente.update({ret.name: ret})
                        self.updateGUI();
            elif tmp[1] == "Vorteil":
                tal = self.datenbank.vorteile[tmp[0]]
                if tal is not None:
                    ret = self.editVorteil(tal)
                    if ret is not None:
                        self.datenbank.vorteile.pop(tmp[0],None)
                        self.datenbank.vorteile.update({ret.name: ret})
                        self.updateGUI();
            elif tmp[1] == "Fertigkeit":
                tal = self.datenbank.fertigkeiten[tmp[0]]
                if tal is not None:
                    ret = self.editFertigkeit(tal)
                    if ret is not None:
                        self.datenbank.fertigkeiten.pop(tmp[0],None)
                        self.datenbank.fertigkeiten.update({ret.name: ret})
                        self.updateGUI();
            elif tmp[1] == "Übernatürliche Fertigkeit":
                tal = self.datenbank.übernatürlicheFertigkeiten[tmp[0]]
                if tal is not None:
                    ret = self.editUebernatuerlich(tal)
                    if ret is not None:
                        self.datenbank.übernatürlicheFertigkeiten.pop(tmp[0],None)
                        self.datenbank.übernatürlicheFertigkeiten.update({ret.name: ret})
                        self.updateGUI();
                                
    def deleteSelected(self):
        for itm in self.listDatenbank.selectedIndexes():
            tmp = self.model.itemData(itm)[0].split(" : ")
            if tmp[1] == "Talent":
                self.datenbank.talente.pop(tmp[0],None)
                self.updateGUI();
            elif tmp[1] == "Vorteil":
                self.datenbank.vorteile.pop(tmp[0],None)
                self.updateGUI();
            elif tmp[1] == "Fertigkeit":
                self.datenbank.fertigkeiten.pop(tmp[0],None)
                self.updateGUI();
            elif tmp[1] == "Übernatürliche Fertigkeit":
                self.datenbank.übernatürlicheFertigkeiten.pop(tmp[0],None)
                self.updateGUI();
                              
    def saveDatenbank(self):
        spath, _ = QtWidgets.QFileDialog.getSaveFileName(None,"Datenbank speichern...","","XML-Datei (*.xml)")
        if ".xml" not in spath:
            spath = spath + ".xml"
        self.datenbank.datei = spath
        self.datenbank.xmlSchreiben()
        
    
    def loadDatenbank(self):
        spath, _ = QtWidgets.QFileDialog.getOpenFileName(None,"Datenbank laden...","","XML-Datei (*.xml)")
        self.datenbank.datei = spath
        self.datenbank.xmlLaden()
        self.updateGUI()

if __name__ == "__main__":
    import sys
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    #sys.exit(app.exec_())
    app.exec_()

