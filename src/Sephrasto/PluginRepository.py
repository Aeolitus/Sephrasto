from PySide6 import QtWidgets, QtCore, QtGui, QtWebEngineCore
from PySide6.QtWebEngineCore import QWebEngineDownloadRequest
from Wolke import Wolke
import os.path
import json
import shutil
import Version
from PluginLoader import PluginLoader

class PluginRepo(QtCore.QObject):
    loadingProgress = QtCore.Signal()
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

        release = None
        for el in releases:
            if el["draft"]:
                continue
            if el["prerelease"] and not Wolke.CmdArgs.prerelease_plugins:
                continue
            version = Version.fromString(el["tag_name"])
            if not version:
                continue
            if Version.isClientLower(Version.stripPluginVersion(version)):
                continue
            if len(el["assets"]) < 1:
                continue
            if not el["assets"][0]["browser_download_url"].endswith(".zip"):
                continue

            if release is None or Version.isHigher(Version.fromString(release["tag_name"]), version):
                release = el

        if release is None:
            self.__setReady()
            return

        self.sephrastoVersion = Version.fromString(release["tag_name"])
        downloadUrl = release["assets"][0]["browser_download_url"]
        filename = os.path.basename(downloadUrl)
        tag = release["tag_name"]
        if release["prerelease"]:
            tag += "_prerelease"
        targetPath = os.path.join(self.dlDir, tag, filename)
        if os.path.isfile(targetPath):
            self.pluginData = PluginLoader.getPlugins(os.path.join(self.dlDir, tag))
            self.__setReady()
            return

        self.page.download(QtCore.QUrl(downloadUrl), targetPath)
            
        
    def __onPluginDownloadRequested(self, download):
        self.download = download
        download.accept()
        download.isFinishedChanged.connect(self.__onPluginDownloaded)
        download.receivedBytesChanged.connect(self.__onReceivedBytesChanged)

    def __onReceivedBytesChanged(self):
        self.loadingProgress.emit()

    def __onPluginDownloaded(self):
        state = self.download.state()
        if state == QWebEngineDownloadRequest.DownloadRequested or state == QWebEngineDownloadRequest.DownloadInProgress:
            return

        if state == QWebEngineDownloadRequest.DownloadCompleted:
            filename = self.download.suggestedFileName()
            dirname = os.path.dirname(filename)
            shutil.unpack_archive(filename, dirname)
            self.pluginData = PluginLoader.getPlugins(dirname)

        self.download.isFinishedChanged.disconnect(self.__onPluginDownloaded)
        self.download.receivedBytesChanged.disconnect(self.__onReceivedBytesChanged)
        self.download = None
        self.__setReady()

    def update(self):
        self.page.load(self.apiLink)

    @property
    def progress(self):
        if self.download is None:
            return 1.0
        return  self.download.receivedBytes() / self.download.totalBytes()
