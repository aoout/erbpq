from pathlib import Path

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTreeWidgetItem
from qfluentwidgets import TreeWidget


class TocWidget(TreeWidget):
    toLoadPage = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setHeaderHidden(True)
        self.itemClicked.connect(self.onItemClicked)

    def load(self, toc: list) -> None:
        self.clear()

        def add_item(item, parent=None):
            widgetItem = QTreeWidgetItem(parent)
            widgetItem.setText(0, item["text"])
            widgetItem.url = Path(item["url"].split("#")[0])
            if parent is None:
                self.addTopLevelItem(widgetItem)
            else:
                parent.addChild(widgetItem)
            for subitem in item.get("subitems", []):
                add_item(subitem, widgetItem)

        for item in toc:
            add_item(item)

    def onItemClicked(self, item, column) -> None:
        self.toLoadPage.emit(str(item.url))
