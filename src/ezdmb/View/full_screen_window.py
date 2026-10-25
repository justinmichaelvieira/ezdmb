# pylint: disable=no-name-in-module
import logging
import os.path

from PySide6.QtCore import QSize, Qt, QUrl, Slot
from PySide6.QtGui import QPixmap, QShortcut
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QLabel,
    QMainWindow,
    QSizePolicy,
    QStackedWidget,
    QWidget,
)

from ezdmb.Controller.configuration import configuration
from ezdmb.Utility.icon_utility import getWindowIcon
from ezdmb.Utility.shortcut_utility import setCloseOnEscKey, setOpenOnOKey
from ezdmb.View import menu_content_view


class full_screen_window(QMainWindow):
    def __init__(self, config: configuration, reopen_preview_window):
        super(self.__class__, self).__init__()
        self._config = config
        self._videoActive = False

        self.setObjectName("full_screen_window")
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setEnabled(True)

        self.setWindowIcon(getWindowIcon())

        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(200, 200))
        self.setAutoFillBackground(True)
        self.centralwidget = QWidget(self)
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setAutoFillBackground(True)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.contentStack = QStackedWidget(self.centralwidget)
        self.contentStack.setObjectName("contentStack")
        self.contentLbl = QLabel(self.contentStack)
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.contentLbl.setSizePolicy(sizePolicy)
        self.contentLbl.setFrameShape(QFrame.Shape.NoFrame)
        self.contentLbl.setLineWidth(0)
        self.contentLbl.setTextFormat(Qt.TextFormat.RichText)
        self.contentLbl.setScaledContents(True)
        self.contentLbl.setObjectName("contentLbl")
        self.contentStack.addWidget(self.contentLbl)
        self.videoWidget = QVideoWidget(self.contentStack)
        self.videoWidget.setObjectName("videoWidget")
        self.videoWidget.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        self.contentStack.addWidget(self.videoWidget)
        self.gridLayout_2.addWidget(self.contentStack, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.setWindowTitle("Menu")

        self.audioOutput = QAudioOutput(self)
        self.videoPlayer = QMediaPlayer(self)
        self.videoPlayer.setAudioOutput(self.audioOutput)
        self.videoPlayer.setVideoOutput(self.videoWidget)
        self.videoPlayer.setLoops(QMediaPlayer.Loops.Infinite)
        self.videoPlayer.errorOccurred.connect(self.onVideoError)

        self.contentViewUtil = menu_content_view.menu_content_view(
            self._config,
            self.contentLbl,
            "full_screen_window",
            self.onRefresh,
            self.onVideoRefresh,
        )
        app = QApplication.instance()
        if app is not None:
            app.aboutToQuit.connect(self.contentViewUtil.stop)
            app.aboutToQuit.connect(self.videoPlayer.stop)
        setCloseOnEscKey(self)
        self.openOnOShortcut: QShortcut = setOpenOnOKey(self, reopen_preview_window)

    @Slot(QPixmap)
    def onRefresh(self, value):
        self._videoActive = False
        self.videoPlayer.stop()
        self.contentStack.setCurrentWidget(self.contentLbl)
        self.contentLbl.clear()
        self.contentLbl.setPixmap(value)

    @Slot(str)
    def onVideoRefresh(self, value):
        self._videoActive = False
        self.videoPlayer.stop()
        self.contentLbl.clear()
        self.contentStack.setCurrentWidget(self.videoWidget)
        self._videoActive = True
        self.videoPlayer.setSource(QUrl.fromLocalFile(os.path.abspath(value)))
        self.videoPlayer.play()

    @Slot(QMediaPlayer.Error, str)
    def onVideoError(self, error, error_message):
        if not self._videoActive:
            return

        logging.getLogger(__name__).error(
            "Video playback failed (%s): %s",
            error,
            error_message,
        )
        self._videoActive = False
        self.videoPlayer.stop()
        self.contentLbl.setTextFormat(Qt.TextFormat.PlainText)
        self.contentLbl.setText("Unable to play video.")
        self.contentStack.setCurrentWidget(self.contentLbl)
