from PySide6 import QtWidgets, QtCore, QtGui, QtWebEngineCore
from Wolke import Wolke
import os.path
import json
import shutil
import Version
from PluginLoader import PluginLoader

class PluginRepo(QtCore.QObject):
    ready = QtCore.Signal()

    def __init__(self, name, apiLink):
        super().__init__()
        self.apiLink = QtCore.QUrl(apiLink)
        self.page = QtWebEngineCore.QWebEnginePage()
        self.page.profile().downloadRequested.connect(self.__onPluginDownloadRequested)
        self.page.loadFinished.connect(self.__onReleasesLoadFinished)
        self.isReady = False
        self.download = None
        self.dlDir = os.path.join(Wolke.Settings["Pfad-Plugins"], ".cache", name)
        self.pluginData = []
        self.sephrastoVersion = [0, 0, 0, 0]

    def __setReady(self):
        self.isReady = True
        self.ready.emit()

    def __onReleasesLoadFinished(self, ok):
        if ok:
            self.page.toPlainText(self.__onReleasesTextReceived)
        else:
            self.__setReady()

    def __onReleasesTextReceived(self, text):
        releases = json.loads(text)
        for r in releases:
            version = Version.disectVersionString(r["tag_name"])
            if not version:
                continue
            if Version.isClientLower(version):
                continue
            if len(r["assets"]) != 1:
                continue
            self.sephrastoVersion = version
            filename = os.path.basename(r["assets"][0]["browser_download_url"])
            targetPath = os.path.join(self.dlDir, r["tag_name"], filename)
            if os.path.isfile(targetPath):
                self.pluginData = PluginLoader.getPlugins(os.path.join(self.dlDir, r["tag_name"]))
                self.__setReady()
                return
            self.page.download(QtCore.QUrl(r["assets"][0]["browser_download_url"]), targetPath)
            return
        self.__setReady()
        
    def __onPluginDownloadRequested(self, download):
        self.download = download
        download.accept()
        download.isFinishedChanged.connect(self.__onPluginDownloaded)

    def __onPluginDownloaded(self):
        if self.download.state() == QtWebEngineCore.QWebEngineDownloadRequest.DownloadCompleted:
            self.download.isFinishedChanged.disconnect(self.__onPluginDownloaded)
            filename = self.download.suggestedFileName()
            dirname = os.path.dirname(filename)
            shutil.unpack_archive(filename, dirname)
            self.pluginData = PluginLoader.getPlugins(dirname)
            self.download = None
            self.__setReady()
        elif self.download.state() == QtWebEngineCore.QWebEngineDownloadRequest.DownloadCancelled or self.download.state() == QtWebEngineCore.QWebEngineDownloadRequest.DownloadInterrupted:
            self.download.isFinishedChanged.disconnect(self.__onPluginDownloaded)
            self.download = None
            self.__setReady()

    def update(self):
        self.page.load(self.apiLink)