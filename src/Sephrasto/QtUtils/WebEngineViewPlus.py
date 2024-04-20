from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEngineScript

# This class adds can add a js bridge that provides an init function that should be called in window.onload
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
    def __init__(self):
        super().__init__()

    def setWebEngineView(self, view):
        self.webEngineView = view

    @QtCore.Slot()
    def htmlLoaded(self):
        self.webEngineView.htmlLoaded.emit()

class WebEngineViewPlus(QWebEngineView):
    htmlLoaded = QtCore.Signal() #only fired if above bridge is used

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # when enabled, this setting will cause external links to be opened in the default browser
    # local file links will continue to be opened inside the view
    def setOpenLinksExternally(self, enable):
        if enable:
            class WebEnginePagePlus(QWebEnginePage):
                def acceptNavigationRequest(self, url,  _type, isMainFrame):
                    if not url.isLocalFile() and _type == QWebEnginePage.NavigationTypeLinkClicked:
                        QtGui.QDesktopServices.openUrl(url);
                        return False
                    return True
            self.setPage(WebEnginePagePlus(self))
        else:
            self.setPage(QWebEnginePage(self))

    def installJSBridge(self, bridge=JSBridge()):
        self.jsBridge = bridge
        self.jsBridge.setWebEngineView(self)
        self.channel = QWebChannel(self)
        self.channel.registerObject("Bridge", self.jsBridge)
        self.page().setWebChannel(self.channel)

    def insertStyleSheet(self, name, source, immediately = False):
        script = QWebEngineScript()
        s = f"""(function() {{
css = document.createElement('style');
css.type = 'text/css';
css.id = '{name}';
document.head.appendChild(css);
css.innerText = `{source}`;
}})()"""
        if immediately:
            self.page().runJavaScript(s, QWebEngineScript.ApplicationWorld)

        script.setName(name)
        script.setSourceCode(s)
        script.setInjectionPoint(QWebEngineScript.DocumentReady)
        script.setRunsOnSubFrames(True)
        script.setWorldId(QWebEngineScript.ApplicationWorld)
        self.page().scripts().insert(script)