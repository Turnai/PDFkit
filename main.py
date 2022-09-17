import sys
from PyPDF2 import PdfReader, PdfMerger

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QFileDialog, qApp, QInputDialog

import PDFtools


class MyPDFtools(QMainWindow, PDFtools.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyPDFtools, self).__init__(parent)
        self.pdfpath = []
        self.setupUi(self)
        self.childUI()
        self.center()

    def childUI(self):
        self.actionExit.triggered.connect(qApp.quit)
        self.actionOpen.triggered.connect(self.GetPdfPath)
        self.actionClear.triggered.connect(self.ClearPdfPath)
        self.GetPdfPath()

        # self.show()

    def GetPdfPath(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if fname[0]:
            self.pdfpath.append(fname[0])
            self.statusBar.showMessage(str(self.pdfpath))
            self.PdfListtextBrowser.setText(str(self.pdfpath))

    def ClearPdfPath(self):
        self.pdfpath.clear()
        self.PdfListtextBrowser.setText(str(self.pdfpath))

    def GetMetadata(self):
        reader = PdfReader(self.pdfpath[-1])
        meta = reader.metadata
        print(meta.author)
        print(meta.creator)
        print(meta.producer)
        print(meta.subject)
        print(meta.title)
        self.MetadatatextBrowser.setText(meta.author + meta.creator + meta.producer)

    def ExtractText(self):
        reader = PdfReader(self.pdfpath[-1])
        page = reader.pages[0]
        self.ExtractTexttextBrowser.setText(page.extract_text())

    def MergingPdf(self):
        merger = PdfMerger()
        for pdf in self.pdfpath:
            merger.append(pdf)
        merger.write("merged-pdf.pdf")
        merger.close()
        self.statusBar.showMessage("Merge success!")

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    MainWindow = MyPDFtools()
    MainWindow.show()

    sys.exit(app.exec_())
