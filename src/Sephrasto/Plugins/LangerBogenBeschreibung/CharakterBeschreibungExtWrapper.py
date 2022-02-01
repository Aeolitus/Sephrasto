from PyQt5 import QtWidgets, QtCore, QtGui
from LangerBogenBeschreibung import CharakterBeschreibungExt
import lxml.etree as etree
from Wolke import Wolke
import logging
from PyQt5.QtGui import QPixmap
import base64
import pdf
import tempfile
import os
from shutil import which
import platform

class CharakterBeschreibungExtWrapper(QtCore.QObject):
    modified = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.form = QtWidgets.QWidget()
        self.ui = CharakterBeschreibungExt.Ui_formBeschreibung()
        self.ui.setupUi(self.form)

        self.ui.chkKultur.stateChanged.connect(lambda state: self.ui.leKultur.setEnabled(self.ui.chkKultur.isChecked()))

        self.ui.leProfession.textChanged.connect(self.valueChanged)
        self.ui.leGeschlecht.textChanged.connect(self.valueChanged)
        self.ui.leGeburtsdatum.textChanged.connect(self.valueChanged)
        self.ui.leGroesse.textChanged.connect(self.valueChanged)
        self.ui.leGewicht.textChanged.connect(self.valueChanged)
        self.ui.leHaarfarbe.textChanged.connect(self.valueChanged)
        self.ui.leAugenfarbe.textChanged.connect(self.valueChanged)
        self.ui.leTitel.textChanged.connect(self.valueChanged)

        self.ui.leAussehen1.textChanged.connect(self.valueChanged)
        self.ui.leAussehen2.textChanged.connect(self.valueChanged)
        self.ui.leAussehen3.textChanged.connect(self.valueChanged)
        self.ui.leAussehen4.textChanged.connect(self.valueChanged)
        self.ui.leAussehen5.textChanged.connect(self.valueChanged)
        self.ui.leAussehen6.textChanged.connect(self.valueChanged)

        self.ui.leHintergrund0.textChanged.connect(self.valueChanged)
        self.ui.leHintergrund1.textChanged.connect(self.valueChanged)
        self.ui.leHintergrund2.textChanged.connect(self.valueChanged)
        self.ui.leHintergrund3.textChanged.connect(self.valueChanged)
        self.ui.leHintergrund4.textChanged.connect(self.valueChanged)
        self.ui.leHintergrund5.textChanged.connect(self.valueChanged)
        self.ui.leHintergrund6.textChanged.connect(self.valueChanged)
        self.ui.leHintergrund7.textChanged.connect(self.valueChanged)
        self.ui.leHintergrund8.textChanged.connect(self.valueChanged)

        self.characterImage = None
        self.labelImageText = self.ui.labelImage.text()
        self.ui.buttonLoadImage.clicked.connect(self.buttonLoadImageClicked)
        self.ui.buttonDeleteImage.clicked.connect(self.buttonDeleteImageClicked)

    def setImage(self, pixmap):
        self.ui.labelImage.setPixmap(pixmap.scaled(self.ui.labelImage.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

    def buttonLoadImageClicked(self):
        spath, _ = QtWidgets.QFileDialog.getOpenFileName(None,"Bild laden...", "", "Bild Dateien (*.png *.jpg *.bmp)")
        if spath == "":
            return
        
        self.characterImage = QPixmap(spath).scaled(QtCore.QSize(260, 340), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.setImage(self.characterImage)

    def buttonDeleteImageClicked(self):
        self.characterImage = None
        self.ui.labelImage.setPixmap(QPixmap())
        self.ui.labelImage.setText(self.labelImageText)

    def valueChanged(self):
        self.modified.emit()

    def pdfExportHook(self, fields):
        if self.ui.chkKultur.isChecked():
            fields['Kultur'] = self.ui.leKultur.text()

        fields['Profession'] = self.ui.leProfession.text()
        fields['Geschlecht'] = self.ui.leGeschlecht.text()
        fields['Geburtsdatum'] = self.ui.leGeburtsdatum.text()
        fields['Groesse'] = self.ui.leGroesse.text()
        fields['Gewicht'] = self.ui.leGewicht.text()
        fields['Haarfarbe'] = self.ui.leHaarfarbe.text()
        fields['Augenfarbe'] = self.ui.leAugenfarbe.text()
        fields['Titel'] = self.ui.leTitel.text()

        fields['Aussehen1'] = self.ui.leAussehen1.text()
        fields['Aussehen2'] = self.ui.leAussehen2.text()
        fields['Aussehen3'] = self.ui.leAussehen3.text()
        fields['Aussehen4'] = self.ui.leAussehen4.text()
        fields['Aussehen5'] = self.ui.leAussehen5.text()
        fields['Aussehen6'] = self.ui.leAussehen6.text()
        
        fields['Hintergrund0'] = self.ui.leHintergrund0.text()
        fields['Hintergrund1'] = self.ui.leHintergrund1.text()
        fields['Hintergrund2'] = self.ui.leHintergrund2.text()
        fields['Hintergrund3'] = self.ui.leHintergrund3.text()
        fields['Hintergrund4'] = self.ui.leHintergrund4.text()
        fields['Hintergrund5'] = self.ui.leHintergrund5.text()
        fields['Hintergrund6'] = self.ui.leHintergrund6.text()
        fields['Hintergrund7'] = self.ui.leHintergrund7.text()
        fields['Hintergrund8'] = self.ui.leHintergrund8.text()
        return fields

    def pdfConcatHook(self, pages):
        if not self.ui.labelImage.pixmap():
            return pages

        if platform.system() != 'Windows' and which("convert") is None:
            messagebox = QtWidgets.QMessageBox()
            messagebox.setWindowTitle("Kann Charakterbild nicht einfügen")
            messagebox.setText("Das Einfügen des Charakterbilds benötigt das Programm 'convert' im Systempfad. Installationsdetails gibt es unter https://imagemagick.org.")
            messagebox.setIcon(QtWidgets.QMessageBox.Warning)
            messagebox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            messagebox.exec_()
            return pages

        # The approach is to convert the image to pdf and stamp it over the char sheet with pdftk

        handle, image_file = tempfile.mkstemp()
        os.close(handle)
        self.ui.labelImage.pixmap().save(image_file, "JPG")

        handle, image_pdf = tempfile.mkstemp()
        os.close(handle)
        image_pdf += ".pdf"

        handle, page1_pdf = tempfile.mkstemp()
        os.close(handle)

        handle, page1stamped_pdf = tempfile.mkstemp()
        os.close(handle)

        handle, pageRest_pdf = tempfile.mkstemp()
        os.close(handle)

        # pdftk stamps over every single page. We only want to stamp the first, so we need to split the char sheet first
        pdf.check_output_silent(['pdftk', pages[0], "cat", "1", "output", page1_pdf])
        pdf.check_output_silent(['pdftk', pages[0], "cat", "2-end", "output", pageRest_pdf])

        # Setting page size to a2 so stamping has to reduce size - this way we can use a higher image resolution.
        # The numbers after the page size are offsets from bottom and right to fit the image in the right spot
        # Density (dpi) has to be fixed, otherwise page offsets break
        # gravity + extent adds letterboxes to the image if needed, this keeps the image centered and allows to use fixed page offsets
        convertPath = "convert"
        if platform.system() == 'Windows':
            convertPath = "Bin\\ImageMagick\\convert"

        pdf.check_output_silent(convertPath + " \"" + image_file + "\" -resize 260x340 -gravity Center -extent 260x340 -density 96 -page a2+115.55+89.55 \"" + image_pdf + "\"")
        pdf.check_output_silent(['pdftk', page1_pdf, 'stamp', image_pdf, 'output', page1stamped_pdf, 'need_appearances'])

        os.remove(pages[0])
        os.remove(image_file)
        os.remove(image_pdf)
        os.remove(page1_pdf)

        pages[0] = page1stamped_pdf
        pages.insert(1, pageRest_pdf)
        return pages

    def charakterXmlSchreibenHook(self, root):
        sub =  etree.SubElement(root,'AllgemeineInfosExt')

        if self.ui.chkKultur.isChecked():
            etree.SubElement(sub,'kultur').text = self.ui.leKultur.text()

        etree.SubElement(sub,'profession').text = self.ui.leProfession.text()
        etree.SubElement(sub,'geschlecht').text = self.ui.leGeschlecht.text()
        etree.SubElement(sub,'geburtsdatum').text = self.ui.leGeburtsdatum.text()
        etree.SubElement(sub,'groesse').text = self.ui.leGroesse.text()
        etree.SubElement(sub,'gewicht').text = self.ui.leGewicht.text()
        etree.SubElement(sub,'haarfarbe').text = self.ui.leHaarfarbe.text()
        etree.SubElement(sub,'augenfarbe').text = self.ui.leAugenfarbe.text()
        etree.SubElement(sub,'titel').text = self.ui.leTitel.text()

        etree.SubElement(sub,'aussehen1').text = self.ui.leAussehen1.text()
        etree.SubElement(sub,'aussehen2').text = self.ui.leAussehen2.text()
        etree.SubElement(sub,'aussehen3').text = self.ui.leAussehen3.text()
        etree.SubElement(sub,'aussehen4').text = self.ui.leAussehen4.text()
        etree.SubElement(sub,'aussehen5').text = self.ui.leAussehen5.text()
        etree.SubElement(sub,'aussehen6').text = self.ui.leAussehen6.text()
        
        etree.SubElement(sub,'hintergrund0').text = self.ui.leHintergrund0.text()
        etree.SubElement(sub,'hintergrund1').text = self.ui.leHintergrund1.text()
        etree.SubElement(sub,'hintergrund2').text = self.ui.leHintergrund2.text()
        etree.SubElement(sub,'hintergrund3').text = self.ui.leHintergrund3.text()
        etree.SubElement(sub,'hintergrund4').text = self.ui.leHintergrund4.text()
        etree.SubElement(sub,'hintergrund5').text = self.ui.leHintergrund5.text()
        etree.SubElement(sub,'hintergrund6').text = self.ui.leHintergrund6.text()
        etree.SubElement(sub,'hintergrund7').text = self.ui.leHintergrund7.text()
        etree.SubElement(sub,'hintergrund8').text = self.ui.leHintergrund8.text()

        if self.ui.labelImage.pixmap():
            buffer = QtCore.QBuffer()
            buffer.open(QtCore.QIODevice.WriteOnly);
            self.characterImage.save(buffer, "JPG")
            etree.SubElement(sub,'bild').text = base64.b64encode(buffer.data())

        return root

    def charakterXmlLadenHook(self, root):
        alg = root.find('AllgemeineInfosExt')
        if alg is None:
            return root
        
        if alg.find('kultur') is not None:
            self.ui.chkKultur.setChecked(True)
            self.ui.leKultur.setText(alg.find('kultur').text or '')

        self.ui.leProfession.setText(alg.find('profession').text or '')
        self.ui.leGeschlecht.setText(alg.find('geschlecht').text or '')
        self.ui.leGeburtsdatum.setText(alg.find('geburtsdatum').text or '')
        self.ui.leGroesse.setText(alg.find('groesse').text or '')
        self.ui.leGewicht.setText(alg.find('gewicht').text or '')
        self.ui.leHaarfarbe.setText(alg.find('haarfarbe').text or '')
        self.ui.leAugenfarbe.setText(alg.find('augenfarbe').text or '')
        self.ui.leTitel.setText(alg.find('titel').text or '')

        self.ui.leAussehen1.setText(alg.find('aussehen1').text or '')
        self.ui.leAussehen2.setText(alg.find('aussehen2').text or '')
        self.ui.leAussehen3.setText(alg.find('aussehen3').text or '')
        self.ui.leAussehen4.setText(alg.find('aussehen4').text or '')
        self.ui.leAussehen5.setText(alg.find('aussehen5').text or '')
        self.ui.leAussehen6.setText(alg.find('aussehen6').text or '')

        self.ui.leHintergrund0.setText(alg.find('hintergrund0').text or '')
        self.ui.leHintergrund1.setText(alg.find('hintergrund1').text or '')
        self.ui.leHintergrund2.setText(alg.find('hintergrund2').text or '')
        self.ui.leHintergrund3.setText(alg.find('hintergrund3').text or '')
        self.ui.leHintergrund4.setText(alg.find('hintergrund4').text or '')
        self.ui.leHintergrund5.setText(alg.find('hintergrund5').text or '')
        self.ui.leHintergrund6.setText(alg.find('hintergrund6').text or '')
        self.ui.leHintergrund7.setText(alg.find('hintergrund7').text or '')
        self.ui.leHintergrund8.setText(alg.find('hintergrund8').text or '')

        if alg.find('bild') is not None:
            self.characterImage = QtGui.QPixmap()
            byteArray = bytes(alg.find('bild').text, 'utf-8')
            self.characterImage.loadFromData(base64.b64decode(byteArray))
            self.setImage(self.characterImage)

        return root

    def cbextUpdateHandler(self, name, value):
        if name == 'kultur':
            self.ui.chkKultur.setChecked(True)
            self.ui.leKultur.setText(value)
        elif name == 'profession':
            self.ui.leProfession.setText(value)
        elif name == 'geschlecht':
            self.ui.leGeschlecht.setText(value)
        elif name == 'geburtsdatum':
            self.ui.leGeburtsdatum.setText(value)
        elif name == 'groesse':
            self.ui.leGroesse.setText(value)
        elif name == 'gewicht':
            self.ui.leGewicht.setText(value)
        elif name == 'haarfarbe':
            self.ui.leHaarfarbe.setText(value)
        elif name == 'augenfarbe':
            self.ui.leAugenfarbe.setText(value)
        elif name == 'titel':
            self.ui.leTitel.setText(value)
        elif name == 'aussehen1':
            self.ui.leAussehen1.setText(value)
        elif name == 'aussehen2':
            self.ui.leAussehen2.setText(value)
        elif name == 'aussehen3':
            self.ui.leAussehen3.setText(value)
        elif name == 'aussehen4':
            self.ui.leAussehen4.setText(value)
        elif name == 'aussehen5':
            self.ui.leAussehen5.setText(value)
        elif name == 'aussehen6':
            self.ui.leAussehen6.setText(value)
        elif name == 'hintergrund0':
            self.ui.leHintergrund0.setText(value)
        elif name == 'hintergrund1':
            self.ui.leHintergrund1.setText(value)
        elif name == 'hintergrund2':
            self.ui.leHintergrund2.setText(value)
        elif name == 'hintergrund3':
            self.ui.leHintergrund3.setText(value)
        elif name == 'hintergrund4':
            self.ui.leHintergrund4.setText(value)
        elif name == 'hintergrund5':
            self.ui.leHintergrund5.setText(value)
        elif name == 'hintergrund6':
            self.ui.leHintergrund6.setText(value)
        elif name == 'hintergrund7':
            self.ui.leHintergrund7.setText(value)
        elif name == 'hintergrund8':
            self.ui.leHintergrund8.setText(value)
        else:
            logging.warn("CharakterBeschreibungExt: Unbekannter Parametername " + name)
            
    def cbextGetHook(self, name):
        if name == 'kultur':
            return self.ui.leKultur.text()
        elif name == 'profession':
            return self.ui.leProfession.text()
        elif name == 'geschlecht':
            return self.ui.leGeschlecht.text()
        elif name == 'geburtsdatum':
            return self.ui.leGeburtsdatum.text()
        elif name == 'groesse':
            return self.ui.leGroesse.text()
        elif name == 'gewicht':
            return self.ui.leGewicht.text()
        elif name == 'haarfarbe':
            return self.ui.leHaarfarbe.text()
        elif name == 'augenfarbe':
            return self.ui.leAugenfarbe.text()
        elif name == 'titel':
            return self.ui.leTitel.text()
        elif name == 'aussehen1':
            return self.ui.leAussehen1.text()
        elif name == 'aussehen2':
            return self.ui.leAussehen2.text()
        elif name == 'aussehen3':
            return self.ui.leAussehen3.text()
        elif name == 'aussehen4':
            return self.ui.leAussehen4.text()
        elif name == 'aussehen5':
            return self.ui.leAussehen5.text()
        elif name == 'aussehen6':
            return self.ui.leAussehen6.text()
        elif name == 'hintergrund0':
            return self.ui.leHintergrund0.text()
        elif name == 'hintergrund1':
            return self.ui.leHintergrund1.text()
        elif name == 'hintergrund2':
            return self.ui.leHintergrund2.text()
        elif name == 'hintergrund3':
            return self.ui.leHintergrund3.text()
        elif name == 'hintergrund4':
            return self.ui.leHintergrund4.text()
        elif name == 'hintergrund5':
            return self.ui.leHintergrund5.text()
        elif name == 'hintergrund6':
            return self.ui.leHintergrund6.text()
        elif name == 'hintergrund7':
            return self.ui.leHintergrund7.text()
        elif name == 'hintergrund8':
            return self.ui.leHintergrund8.text()
        else:
            logging.warn("CharakterBeschreibungExt: Unbekannter Parametername " + name)

    def addWidgetHandler(self, widget, row, column):
        if widget is None:
            widgetItem = self.ui.gridLayout_2.itemAtPosition(row, column)
            if widgetItem and widgetItem.widget():
                widgetItem.widget().hide()
        else:
            self.ui.gridLayout_2.addWidget(widget, row, column)
                   