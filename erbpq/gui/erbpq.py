from pathlib import Path

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QHBoxLayout
from qfluentwidgets import TextEdit

from ..gui.navigatedWindow import NavigatedWindow
from ..gui.tocWidget import TocWidget
from ..utils.epubParser import EpubParser


class Erbpq(NavigatedWindow):
    def __init__(self) -> None:
        super().__init__()

        self.epubParser = None

        self.setWindowTitle("Erbpq")
        self.__resizeWindow()
        self.__initLayout()
        self.show()

    def __resizeWindow(self) -> None:
        self.resize(1080, 784)
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def __initLayout(self) -> None:
        layout = QHBoxLayout(self.contentWidget)
        self.textEdit = TextEdit(self.contentWidget)
        layout.addWidget(self.textEdit)

        self.tocWidget = TocWidget(self)
        self.tocWidget.toLoadPage.connect(lambda x: self.loadPage(pagePath=x))

        self.addInterface("Toc", self.tocWidget)

    def loadEpub(self, epubPath: str) -> None:
        self.epubParser = EpubParser(epubPath)
        self.loadPage(0)
        self.tocWidget.load(self.epubParser.toc)

    def loadPage(self, pageIndex: int = None, pagePath: Path or str = None) -> None:
        if pagePath:
            pagePath = Path(pagePath)
            pageIndex = self.epubParser.pagesPath.index(pagePath)
        pageHtml = self.epubParser.getPageHtml(pageIndex)
        self.textEdit.setHtml(pageHtml)
        self.textEdit.document().setBaseUrl(QUrl.fromLocalFile(
            str(self.epubParser.pagesPath[pageIndex])))
