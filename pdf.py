# -*- coding: utf-8 -*-
"""
This file consists of the following merged together into one file for usability

    # FIRST #
Port of the PHP forge_fdf library by Sid Steward
(http://www.pdfhacks.com/forge_fdf/)

Anders Pearson <anders@columbia.edu> at Columbia Center For New Media Teaching
and Learning <http://ccnmtl.columbia.edu/>

    # SECOND # 
PDFFields - found at:
    https://github.com/evfredericksen/pdffields
"""

import codecs
import sys

if sys.version_info[0] < 3:
    bytes = str
    
from os import remove
from re import match
from tempfile import NamedTemporaryFile
from subprocess import check_output

def get_fields(pdf_file):
    '''
    Use pdftk to get a pdf's fields as a string, parse the string
    and return the fields as a dictionary, with field names as keys
    and field values as values.
    '''
    fields = {}
    call = ['pdftk', pdf_file, 'dump_data_fields']
    try:
        data_string = check_output(call).decode('utf8')
    except FileNotFoundError:
        raise PdftkNotInstalledError('Could not locate PDFtk installation')
    data_list = data_string.split('\r\n')
    if len(data_list) == 1:
        data_list = data_string.split('\n')
    for line in data_list:
        if line:
            re_object = match(r'(\w+): (.+)', line)
            if re_object is not None:
                if re_object.group(1) == 'FieldName':
                    key = re_object.group(2)
                    fields[key] = ''
                elif re_object.group(1) == 'FieldValue':
                    fields[key] = re_object.group(2)
    return fields

def write_pdf(source, fields, output, flatten=False):
    '''
    Take a source file path, list or dictionary of fdf fields, and
    output path, and create a filled-out pdf.
    '''
    fdf = forge_fdf(fdf_data_strings=fields)
    with NamedTemporaryFile(delete=False) as file:
        file.write(fdf)
    call = ['pdftk', source, 'fill_form', file.name, 'output', output]
    if flatten:
        call.append('flatten')
    try:
        check_output(call)
    except FileNotFoundError:
        raise PdftkNotInstalledError('Could not locate PDFtk installation')
    remove(file.name)
    
class PdftkNotInstalledError(Exception):
    pass


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
        check_output(args)
    except:
        if cleanOnFail:
            os.remove(out_file)
        raise
    return out_file