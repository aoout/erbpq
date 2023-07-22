from PyQt5.QtCore import (QParallelAnimationGroup, QPoint, QPropertyAnimation,
                          QRect, QSize)
from PyQt5.QtWidgets import QHBoxLayout, QStackedWidget, QWidget
from qfluentwidgets import PushButton
from qframelesswindow import FramelessWindow, StandardTitleBar


class NavigatedWindow(FramelessWindow):
    def __init__(self):
        super().__init__()
        self.setTitleBar(StandardTitleBar(self))

        self.extended = False

        self.nonExtendedWidth = 100
        self.extendedWidth = 240

        self.interfaceButtons = []
        self.highlightedIndex = None

        self._initLayout()

    def _initLayout(self):

        self.sideBar = QWidget(self)
        self.contentWidget = QWidget(self)

        layout = QHBoxLayout(self.sideBar)
        self.stackedWidget = QStackedWidget(self.sideBar)
        layout.addWidget(self.stackedWidget)
        layout.setContentsMargins(self.nonExtendedWidth+12, 12, 0, 12)

    def __update(self):
        siderBarWidth = self.nonExtendedWidth if not self.extended else self.extendedWidth
        self.sideBar.move(0, 30)
        self.sideBar.resize(QSize(siderBarWidth, self.height()))
        self.contentWidget.move(siderBarWidth+12, 30)
        self.contentWidget.resize(
            QSize(self.width() - siderBarWidth - 12, self.height() - 12*2))

    def resizeEvent(self, e):
        self.__update()
        return super().resizeEvent(e)

    def interfaceButtonClicked(self, index):
        delta = self.extendedWidth - self.nonExtendedWidth
        if self.extended and self.highlightedIndex == index:

            animGroup = QParallelAnimationGroup(self)
            anim = QPropertyAnimation(self.sideBar, b'geometry', self)
            anim.setDuration(100)
            anim.setStartValue(self.sideBar.geometry())
            anim.setEndValue(QRect(self.sideBar.pos(), QSize(
                self.nonExtendedWidth, self.sideBar.height())))
            animGroup.addAnimation(anim)

            anim = QPropertyAnimation(self.contentWidget, b'geometry', self)
            anim.setDuration(100)
            anim.setStartValue(self.contentWidget.geometry())
            anim.setEndValue(QRect(QPoint(self.contentWidget.x() - delta, self.contentWidget.y()),
                             QSize(self.contentWidget.width() + delta, self.contentWidget.height())))
            animGroup.addAnimation(anim)

            animGroup.start()
            self.extended = not self.extended
            self.highlightedIndex = None
        elif not self.extended:

            animGroup = QParallelAnimationGroup(self)
            anim = QPropertyAnimation(self.sideBar, b'geometry', self)
            anim.setDuration(100)
            anim.setStartValue(self.sideBar.geometry())
            anim.setEndValue(QRect(self.sideBar.pos(), QSize(
                self.extendedWidth, self.sideBar.height())))
            animGroup.addAnimation(anim)

            anim = QPropertyAnimation(self.contentWidget, b'geometry', self)
            anim.setDuration(100)
            anim.setStartValue(self.contentWidget.geometry())
            anim.setEndValue(QRect(QPoint(self.contentWidget.x() + delta, self.contentWidget.y()),
                             QSize(self.contentWidget.width() - delta, self.contentWidget.height())))
            animGroup.addAnimation(anim)

            animGroup.start()

            self.stackedWidget.setCurrentIndex(index)
            self.extended = not self.extended
            self.highlightedIndex = index
        else:

            self.stackedWidget.setCurrentIndex(index)
            self.highlightedIndex = index

    def addInterface(self, text, widget):
        self.stackedWidget.addWidget(widget)
        self.interfaceButtons.append(PushButton(text, self.sideBar))

        num = len(self.interfaceButtons)
        height = 12+(num-1)*(self.interfaceButtons[-1].height()+6)
        self.interfaceButtons[-1].move(2, height)
        self.interfaceButtons[-1].clicked.connect(
            lambda: self.interfaceButtonClicked(num-1))
