# -*- coding: utf-8 -*-
"""
This file contains code from the fdfgen repository (https://github.com/ccnmtl/fdfgen),
which is a port of the PHP forge_fdf library by Sid Steward (http://www.pdfhacks.com/forge_fdf/)
Anders Pearson <anders@columbia.edu> at Columbia Center For New Media Teaching
and Learning <http://ccnmtl.columbia.edu/>
"""

import codecs
import sys
import shutil
import platform
from os import remove
import os
import tempfile
from re import match
from tempfile import NamedTemporaryFile
import subprocess
import logging
from PySide6 import QtCore, QtWebEngineCore, QtWidgets
from contextlib import contextmanager
import base64

@contextmanager
def waitForSignal(signal):
    loop = QtCore.QEventLoop()
    signal.connect(loop.quit)
    try:
        yield
    finally:
        loop.exec()

def check_output_silent(call):
    try:
        if platform.system() == 'Windows':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            return subprocess.check_output(call, startupinfo=startupinfo, stderr=subprocess.STDOUT)
        else:
            return subprocess.check_output(call, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        processError = error.output.decode('utf-8')
        if "Failed to open" in processError:
            processError = "Vermutlich hat ein anderes Programm ein Überschreiben der Datei verhindert. Bitte schließe alle Programme, in denen die Datei geöffnet ist."
        raise Exception(processError)

def write_pdf(source, fields, out_file = None, flatten=False):
    '''
    Take a source file path, list or dictionary of fdf fields, and
    output path, and create a filled-out pdf.
    '''
    fdf = forge_fdf(fdf_data_strings=fields)
    with NamedTemporaryFile(delete=False) as file:
        file.write(fdf)

    if not out_file:
        handle, out_file = tempfile.mkstemp()
        os.close(handle)

    call = ['pdftk', source, 'fill_form', file.name, 'output', out_file]
    if flatten:
        call.append('flatten')
    else:
        call.append('need_appearances')
    
    check_output_silent(call)
    remove(file.name)
    return out_file

def smart_encode_str(s):
    """Create a UTF-16 encoded PDF string literal for `s`."""
    if isinstance(s, str):
        utf16 = s.encode('utf_16_be')
    else: #ints and floats
        utf16 = str(s).encode('utf_16_be')
    safe = utf16.replace(b'\x00)', b'\x00\\)').replace(b'\x00(', b'\x00\\(')
    return b''.join((codecs.BOM_UTF16_BE, safe))


def handle_hidden(key, fields_hidden):
    if key in fields_hidden:
        return b"/SetF 2"
    else:
        return b"/ClrF 2"


def handle_readonly(key, fields_readonly):
    if key in fields_readonly:
        return b"/SetFf 1"
    else:
        return b"/ClrFf 1"


class FDFIdentifier(object):
    """A PDF value, such as /Yes or /Off that should be passed through with the / and without parenthesis (which would indicate it was a value, not an identifier)
    This allows for different checkbox checked/unchecked names per checkbox!
    """
    def __init__(self, value):
        if value.startswith('/'):
            value = value[1:]

        if isinstance(value, bytes):
            value = value.decode('utf-8')

        value = u'/%s' % value
        value = value.encode('utf-8')

        self._value = value

    @property
    def value(self):
        return self._value
        

def handle_data_strings(fdf_data_strings, fields_hidden, fields_readonly,
                        checkbox_checked_name):
    if isinstance(fdf_data_strings, dict):
        fdf_data_strings = fdf_data_strings.items()

    for (key, value) in fdf_data_strings:
        if value is True:
            value = FDFIdentifier(checkbox_checked_name).value
        elif value is False:
            value = FDFIdentifier('Off').value
        elif isinstance(value, FDFIdentifier):
            value = value.value
        else:
            value = b''.join([b'(', smart_encode_str(value), b')'])

        yield b''.join([
            b'<<',
            b'/T(',
            smart_encode_str(key),
            b')',
            b'/V',
            value,
            handle_hidden(key, fields_hidden),
            b'',
            handle_readonly(key, fields_readonly),
            b'>>',
        ])


def handle_data_names(fdf_data_names, fields_hidden, fields_readonly):
    if isinstance(fdf_data_names, dict):
        fdf_data_names = fdf_data_names.items()

    for (key, value) in fdf_data_names:
        yield b''.join([b'<<\x0a/V /', smart_encode_str(value), b'\x0a/T (',
                        smart_encode_str(key), b')\x0a',
                        handle_hidden(key, fields_hidden), b'\x0a',
                        handle_readonly(key, fields_readonly), b'\x0a>>\x0a'])


def forge_fdf(pdf_form_url=None, fdf_data_strings=[], fdf_data_names=[],
              fields_hidden=[], fields_readonly=[],
              checkbox_checked_name=b"Yes"):
    """Generates fdf string from fields specified

    * pdf_form_url (default: None): just the url for the form.
      fdf_data_strings (default: []): array of (string, value) tuples for the
      form fields (or dicts). Value is passed as a UTF-16 encoded string,
      unless True/False, in which case it is assumed to be a checkbox
      (and passes names, '/Yes' (by default) or '/Off').
    * fdf_data_names (default: []): array of (string, value) tuples for the
      form fields (or dicts). Value is passed to FDF as a name, '/value'
    * fields_hidden (default: []): list of field names that should be set
      hidden.
    * fields_readonly (default: []): list of field names that should be set
      readonly.
    * checkbox_checked_value (default: "Yes"): By default means a checked
      checkboxes gets passed the value "/Yes". You may find that the default
      does not work with your PDF, in which case you might want to try "On".

    The result is a string suitable for writing to a .fdf file.

    """
    fdf = [b'%FDF-1.2\x0a%\xe2\xe3\xcf\xd3\x0d\x0a']
    fdf.append(b'1 0 obj\x0a<</FDF')
    fdf.append(b'<</Fields[')
    fdf.append(b''.join(handle_data_strings(fdf_data_strings,
                                            fields_hidden, fields_readonly,
                                            checkbox_checked_name)))
    fdf.append(b''.join(handle_data_names(fdf_data_names,
                                          fields_hidden, fields_readonly)))
    if pdf_form_url:
        fdf.append(b''.join(b'/F (', smart_encode_str(pdf_form_url), b')\x0a'))
    fdf.append(b']\x0a')
    fdf.append(b'>>\x0a')
    fdf.append(b'>>\x0aendobj\x0a')
    fdf.append(b'trailer\x0a\x0a<<\x0a/Root 1 0 R\x0a>>\x0a')
    fdf.append(b'%%EOF\x0a\x0a')
    return b''.join(fdf)


#==============================================================================
# if __name__ == "__main__":
#     # a simple example of using fdfgen
#     # this will create an FDF file suitable to fill in
#     # the vacation request forms we use at work.
# 
#     from datetime import datetime
#     fields = [('Name', 'Anders Pearson'),
#               ('Date', datetime.now().strftime("%x")),
#               ('Request_1', 'Next Monday through Friday'),
#               ('Request_2', ''),
#               ('Request_3', ''),
#               ('Total_days', 5),
#               ('emergency_phone', '857-6309')]
#     fdf = forge_fdf(fdf_data_strings=fields)
#     fdf_file = open("vacation.fdf", "wb")
#     fdf_file.write(fdf)
#     fdf_file.close()
# 
#     # Parse command-line arguments
#     import argparse
#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "--output", "-o",
#         help="FDF File to output to",
#         default='vacation.fdf',
#         type=argparse.FileType('wb'))
#     parser.add_argument(
#         "--fields", "-f",
#         help="Fields used in form; syntax is fieldname=fieldvalue",
#         default=fields,
#         nargs='*')
#     args = parser.parse_args()
#     if args.fields is not fields:
#         for e, x in enumerate(args. fields):
#             args.fields[e] = x.split('=')
#     fdf = forge_fdf(fdf_data_strings=args.fields)
#     args.output.write(fdf)
#     args.output.close()
# 
#==============================================================================

def concat(files, out_file=None):
    '''
        Merge multiples PDF files.
        Return temp file if no out_file provided.
    '''
    cleanOnFail = False
    if not out_file:
        cleanOnFail = True
        handle, out_file = tempfile.mkstemp()
        os.close(handle)
    if len(files) == 1:
        shutil.copyfile(files[0], out_file)
    args = ['pdftk']
    args += files
    args += ['cat', 'output', out_file]
    try:
        check_output_silent(args)
    except:
        if cleanOnFail:
            os.remove(out_file)
        raise
    return out_file

def shrink(file, fromPageNumber, toPageNumber, out_file = None):
    if not out_file:
        handle, out_file = tempfile.mkstemp()
        os.close(handle)
    call = ['pdftk', file, 'cat', str(fromPageNumber) + "-" + str(toPageNumber), 'output', out_file]
    check_output_silent(call)
    return out_file

def squeeze(file, out_file = None):
    if not out_file:
        handle, out_file = tempfile.mkstemp()
        os.close(handle)

    cpdfPath = os.path.join("Bin", platform.system(), "cpdf", "cpdf")
    call = [cpdfPath, "-squeeze", "-i", file, "-o", out_file]

    try:
        check_output_silent(call)
    except Exception as e:
        logging.error("Unable to squeeze pdf: " + str(e))

    return out_file

def addText(file, text, pos, posOffset, color = "black", font = "Times-Roman", fontsize = "12", out_file = None):
    if not out_file:
        handle, out_file = tempfile.mkstemp()
        os.close(handle)
    cpdfPath = os.path.join("Bin", platform.system(), "cpdf", "cpdf")
    call = [cpdfPath, "-add-text", text, "-" + pos, posOffset, "-color", color, "-font", font, "-font-size", fontsize, file, "-o", out_file]
    try:
        check_output_silent(call)
    except Exception as e:
        logging.error("Unable to add text to pdf: " + str(e))
    return out_file

def addBackground(file, background_file, out_file = None):
    if not out_file:
        handle, out_file = tempfile.mkstemp()
        os.close(handle)
    call = ['pdftk', file, 'background', background_file, 'output', out_file, 'need_appearances']
    check_output_silent(call)
    return out_file

def split(file, pagerange, out_file = None):
    if not out_file:
        handle, out_file = tempfile.mkstemp()
        os.close(handle)
    call = ['pdftk', file, "cat", pagerange, "output", out_file]
    check_output_silent(call)
    return out_file

def stamp(file, stamp_file, out_file = None):
    if not out_file:
        handle, out_file = tempfile.mkstemp()
        os.close(handle)
    call = ['pdftk', file, 'stamp', stamp_file, 'output', out_file, 'need_appearances']
    check_output_silent(call)
    return out_file

def multistamp(file, stamp_file, out_file = None):
    if not out_file:
        handle, out_file = tempfile.mkstemp()
        os.close(handle)
    call = ['pdftk', file, 'multistamp', stamp_file, 'output', out_file, 'need_appearances']
    check_output_silent(call)
    return out_file

def getNumPages(file):
    call = ['pdftk', file, 'dump_data_utf8']
    data = check_output_silent(call)
    data = data.decode('utf-8').split("\r\n")
    for d in data:
        if d.startswith("NumberOfPages: "):
            return int(d[len("NumberOfPages: "):])
    return 0

class PdfBookmark:
    def __init__(self, title, pageNumber, level=1):
        self.title = title
        self.pageNumber = pageNumber
        self.level = level

def addBookmarks(file, bookmarks, out_file = None):
    if not out_file:
        handle, out_file = tempfile.mkstemp()
        os.close(handle)

    handle, bookmarksFile = tempfile.mkstemp()
    os.close(handle)
    content = []
    for bm in bookmarks:
        content.append("BookmarkBegin")
        content.append("BookmarkTitle: " + bm.title)
        content.append("BookmarkLevel: " + str(bm.level))
        content.append("BookmarkPageNumber: " + str(bm.pageNumber))
    with open(bookmarksFile, 'wb') as f:
        f.write('\n'.join(content).encode())

    call = ['pdftk', file, 'update_info_utf8', bookmarksFile, 'output', out_file]
    check_output_silent(call)
    os.remove(bookmarksFile)
    return out_file

def createEmptyPage(pageLayout, backgroundColor = QtCore.Qt.transparent, out_file = None):
    if not out_file:
        handle, out_file = tempfile.mkstemp()
        os.close(handle)
        os.remove(out_file) # just using it to get a path
        out_file += ".pdf"
    
    return convertHtmlToPdf("", "", pageLayout, 0, backgroundColor, out_file)

def convertJpgToPdf(imageBytes, imageTargetSize, imageOffset, pageLayout, backgroundColor = QtCore.Qt.transparent, out_file = None):
    if not out_file:
        handle, out_file = tempfile.mkstemp()
        os.close(handle)
        os.remove(out_file) # just using it to get a path
        out_file += ".pdf"
    image = base64.b64encode(imageBytes).decode('ascii')
    html = f"<div style='background: white; margin-left: {imageOffset[0]}px; margin-top: {imageOffset[1]}px; width: {imageTargetSize[0]}px; height: {imageTargetSize[1]}px;'>\
    <img src='data:image/jpg;base64, {image}' style='width: 100%; height: 100%; object-fit: contain;'>\
    </div>"
    return convertHtmlToPdf(html, "", pageLayout, 0, backgroundColor, out_file)

def convertHtmlToPdf(html, htmlBaseUrl, pageLayout, pageloadDelayMs = 0, backgroundColor = QtCore.Qt.transparent, out_file = None, webEnginePage = None):
    if isinstance(htmlBaseUrl, str):
        htmlBaseUrl = QtCore.QUrl.fromLocalFile(QtCore.QFileInfo(htmlBaseUrl).absoluteFilePath())

    if not out_file:
        handle, out_file = tempfile.mkstemp()
        os.close(handle)
        os.remove(out_file) # just using it to get a path
        out_file += ".pdf"

    if webEnginePage is None:
         webEnginePage = QtWebEngineCore.QWebEnginePage()

    webEnginePage.setBackgroundColor(backgroundColor)
    with waitForSignal(webEnginePage.loadFinished):
        webEnginePage.setHtml(html, htmlBaseUrl)

    if pageloadDelayMs > 0:
        timer = QtCore.QTimer()
        with waitForSignal(timer.timeout):
            timer.start(pageloadDelayMs)

    with waitForSignal(webEnginePage.pdfPrintingFinished):
        webEnginePage.printToPdf(out_file, pageLayout)

    return out_file