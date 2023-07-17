from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel

# These classes add a js bridge that provides an init function that should be called in window.onload
# The loadFinished function provided by Qt is executed too early which is bad for printing/screen grabbing
# Our PdfSerializer automatically uses this new htmlLoaded signal
# Use like following:
# <script type="text/javascript" src="qrc:///qtwebchannel/qwebchannel.js"></script>
# <script>
# window.onload = function(){                   
#     new QWebChannel(qt.webChannelTransport,
#         function(channel) {
#             Bridge = channel.objects.Bridge;
#             Bridge.init();
#         }
#     );  
# }
# </script>

class JSBridge(QtCore.QObject):
    def __init__(self, webEngineView):
        super().__init__()
        self.webEngineView = webEngineView

    @QtCore.Slot()
    def htmlLoaded(self):
        self.webEngineView.htmlLoaded.emit()

class WebEngineViewPlus(QWebEngineView):
    htmlLoaded = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jsBridge = JSBridge(self)
        self.channel = QWebChannel(self)
        self.channel.registerObject("Bridge", self.jsBridge)
        self.page().setWebChannel(self.channel)