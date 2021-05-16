from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import os
from PIL import Image, ImageFilter




app = QApplication([])
window = QWidget()
window.setWindowTitle("Easy Editor")

btn_levo = QPushButton("Лево")
btn_pravo = QPushButton("Право")
btn_zerkal = QPushButton("Зеракло")
btn_rezko = QPushButton("Резкость")
btn_bw = QPushButton("Ч/Б")

pol = QListWidget()
btn_papka = QPushButton("Папка")
pickcha = QLabel("Картинка")


col_1 = QVBoxLayout()
col_1.addWidget(btn_papka)
col_1.addWidget(pol)


col_2 = QVBoxLayout()
col_2.addWidget(pickcha)


row_1 = QHBoxLayout()
row_1.addWidget(btn_levo)
row_1.addWidget(btn_pravo)

row_1.addWidget(btn_rezko)
row_1.addWidget(btn_zerkal)
row_1.addWidget(btn_bw)

col_2.addLayout(row_1)



row_2 = QHBoxLayout()
row_2.addLayout(col_1,20)
row_2.addLayout(col_2,80)


window.setLayout(row_2)




workdir = ''

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenameList():
    exceptions = ['jpg','jpeg','png','gif','bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), exceptions)
    pol.clear()
    for filename in filenames:
        pol.addItem(filename)



class ImageProcessor():

    def __init__(self ):
        self.filename=None
        self.original=None
        self.save_dir=("pap/")



    def LoadImage(self,Filename):
        self.filename = Filename
        way = os.path.join(workdir,self.filename)
        self.original=Image.open(way)


    def showImage(self,path):
        pickcha.hide()
        pixmapimage=QPixmap(path)    
        w, h = pickcha.width() , pickcha.height()
        pixmapimage = pixmapimage.scaled(w, h,  Qt.KeepAspectRatio)
        pickcha.setPixmap(pixmapimage)
        pickcha.show()

    def do_bw(self):
        self.original = self.original.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    
    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.original.save(image_path)

workimage= ImageProcessor()

def showClosenImage():
        if pol.currentRow() >=0: 
            filename = pol.currentItem().text()
            workimage.LoadImage(filename)
            image_path = os.path.join(workdir, workimage.filename)
            workimage.showImage(image_path)

pol.currentRowChanged.connect(showClosenImage)
btn_papka.clicked.connect(showFilenameList)
btn_bw.clicked.connect(workimage.do_bw)


window.show()
app.exec_()