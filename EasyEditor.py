#подключение библиотек
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import os
from PIL import Image
from PIL import ImageFilter

#создание элементов интерфейса
app = QApplication([])
win = QWidget()
win.setWindowTitle("Easy Editor") 
win.resize(800,450)
folder = QPushButton("Выбрать папку")
gag = QLabel("Для начала использования выберите картинку")#Ты даун? Чё ты хочешь? Сначала картинку выбери!
left_btn = QPushButton("Повернуть влево")
right_btn = QPushButton("Повернуть вправо")
mirror_btn = QPushButton("Отзеркалить")
sharpness_btn = QPushButton("Резкость")
monochome_btn = QPushButton("Ч/б")
list123 = QListWidget()

#расстановка по линиям
layout_main = QHBoxLayout()
layout_list = QVBoxLayout()
layout_button = QHBoxLayout()
layout_img = QVBoxLayout()

layout_button.addWidget(left_btn)
layout_button.addWidget(right_btn)
layout_button.addWidget(mirror_btn)
layout_button.addWidget(sharpness_btn)
layout_button.addWidget(monochome_btn)


layout_list.addWidget(folder)
layout_list.addWidget(list123)

layout_img.addWidget(gag,95)
layout_img.addLayout(layout_button)

layout_main.addLayout(layout_list,20)
layout_main.addLayout(layout_img,80)

win.setLayout(layout_main)

workdir = ""

def filter(files,extensions):
    result = list()
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFileNamesList():
    extensions = [".jpg",".bmp",".jpeg", ".gif", ".png"]
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions) 
    list123.clear()
    for filename in filenames:
        list123.addItem(filename)

folder.clicked.connect(showFileNamesList)

#класс
class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.fullname2 = None
        self.saveDir = "Modifed/"
    
    def loadImage(self,filename):
        self.filename = filename
        fullname = os.path.join(workdir, filename)
        self.image = Image.open(fullname)
        
    def showImage(self, path):
        gag.hide()
        pixmapimage = QPixmap(path)
        w,h = gag.width(), gag.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        gag.setPixmap(pixmapimage)
        gag.show()

    def saveImage(self):
        path = os.path.join(workdir, self.saveDir)
        if not os.path.exists(path):
            os.mkdir(path)
        self.fullname2 = os.path.join(path, self.filename)
        self.image.save(self.fullname2)


    def monochome(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.saveDir, self.filename)
        self.showImage(image_path)


    def mirror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.saveDir, self.filename)
        self.showImage(image_path)

    def sharpness(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(workdir, self.saveDir, self.filename)
        self.showImage(image_path)

    def right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.saveDir, self.filename)
        self.showImage(image_path)

    def left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.saveDir, self.filename)
        self.showImage(image_path)


def showChosenImage():
    if list123.currentRow() >= 0:
        filename = list123.currentItem().text()
        workImage.loadImage(filename)
        workImage.showImage(os.path.join(workdir,workImage.filename))

workImage = ImageProcessor()
list123.currentRowChanged.connect(showChosenImage)

left_btn.clicked.connect(workImage.left)
right_btn.clicked.connect(workImage.right)
mirror_btn.clicked.connect(workImage.mirror)
sharpness_btn.clicked.connect(workImage.sharpness)
monochome_btn.clicked.connect(workImage.monochome)

#запуск приложения
win.show()
app.exec_()