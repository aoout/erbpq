import fire
from PyQt5.QtWidgets import QApplication
from .gui.erbpq import Erbpq
from typing import Optional

def run(epubPath:Optional[str]=None):
    app = QApplication([])
    erbpq = Erbpq()
    erbpq.loadEpub(epubPath)
    app.exec_()

def main():
    fire.Fire(run)