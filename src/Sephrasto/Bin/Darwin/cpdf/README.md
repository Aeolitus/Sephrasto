cpdf-binaries
=============

PDF Command Line Tools binaries for Linux, Mac, Windows.

For non-commercial use only. See the file LICENSE for details. For commercial
use, a license must be purchased from
[http://www.coherentpdf.com](http://www.coherentpdf.com).

It prints a little message to stderr about the non-commercial license, and sets
the Producer to cpdf.


Functionality
---

* Quality Split and Merge, keeping bookmarks. Extract pages. Split on Bookmarks.
* Encrypt and Decrypt (including AES 128 and AES 256 encryption)
* Scale, rotate, crop and flip pages. Scale pages to fit.
* Copy, Remove and Add bookmarks
* Stamp logos, watermarks, page numbers and multiline text. Transparency.
* Supports Unicode UTF8 text input and output
* Make PDF-based presentations
* Put multiple pages on a single page
* List, copy, or remove annotations
* Read and set document information and metadata
* Add and remove file attachments to document or page.
* Thicken hairlines, blacken text, make draft documents
* Reconstruct malformed files
* Detect missing fonts, low resolution images
* Export and import PDF files in JSON format
* Build table of contents
* Convert text to PDF


Documentation
---

PDF Manual:

[http://www.coherentpdf.com/cpdfmanual.pdf](http://www.coherentpdf.com/cpdfmanual.pdf)

Examples:

[http://www.coherentpdf.com/usage-examples.html](http://www.coherentpdf.com/usage-examples.html)

Website:

[http://www.coherentpdf.com/](http://www.coherentpdf.com)


To Install
---

The program cpdf (or cpdf.exe for Windows) is a single executable with no
dependencies. Copy it to somewhere suitable on your platform.

The last version of cpdf compatible with Windows XP is v2.2.1.

MacOS: The executable is codesigned, but not notarized. If it refuses to run
the first time, go to System Preferences --> Security & Privacy --> General and
click "Allow anyway".


C/C++/Python API
----------------

C/C++/Python interfaces to cpdf are available, in source and binary form:

[https://github.com/johnwhitington/cpdflib-source](https://github.com/johnwhitington/cpdflib-source)

[https://github.com/coherentgraphics/cpdflib-binary](https://github.com/coherentgraphics/cpdflib-binary)


Support
---

Raise an issue in this github repository, or email
contact@coherentgraphics.co.uk
