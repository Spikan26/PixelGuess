import sys
import os
import random
from PIL import Image
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QGridLayout, QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap


def new_game():
    # Choisi une image dans le dossier 'img' et l'affiche dans la console
    rand_img = random.choice(os.listdir("img"))
    print(rand_img)
    # Charge l'image pour traitement
    img = Image.open("img/"+rand_img)

    # Redimensionne l'image et enregistre les 2 versions
    # source = image fixe de référence
    # result = image qui sera pixelisé et affiché
    fixed_height = 420
    height_percent = (fixed_height / float(img.size[1]))
    width_size = int((float(img.size[0]) * float(height_percent)))
    result = img.resize((width_size, fixed_height))
    result.save("img/source.png")
    result.save("img/result.png")


class WinForm(QWidget):
    def __init__(self, parent=None):
        super(WinForm, self).__init__(parent)
        self.setWindowTitle('PixelGuess')
        self.setFixedSize(480, 480)

        # Current resolution for the pixel image
        self.xc = 1
        self.yc = 1

        self.im = QPixmap("img/result.png")
        self.label = QLabel('Press Start to begin')
        self.startBtn = QPushButton('Start')
        self.endBtn = QPushButton('Stop')
        self.resetBtn = QPushButton('New')
        self.resultBtn = QPushButton('Result')

        layout = QGridLayout()

        # Initialise le Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.pixel)

        # Place les éléments sur la fenètre
        layout.addWidget(self.label, 0, 0, 1, 2)
        layout.addWidget(self.startBtn, 1, 0)
        layout.addWidget(self.endBtn, 1, 1)
        layout.addWidget(self.resetBtn, 2, 0)
        layout.addWidget(self.resultBtn, 2, 1)

        # Associe les fonctions aux boutons
        self.startBtn.clicked.connect(self.startTimer)
        self.endBtn.clicked.connect(self.endTimer)
        self.resetBtn.clicked.connect(self.resetGame)
        self.resultBtn.clicked.connect(self.resultTimer)

        self.setLayout(layout)

    # Démarre lentement le process
    def startTimer(self):
        self.timer.start(500)
        self.startBtn.setEnabled(False)
        self.endBtn.setEnabled(True)

    # Pause le process
    def endTimer(self):
        self.timer.stop()
        self.startBtn.setEnabled(True)
        self.endBtn.setEnabled(False)

    # Relance une nouvelle image
    def resetGame(self):
        self.timer.stop()
        self.startBtn.setEnabled(True)
        self.endBtn.setEnabled(False)
        self.label.setText("Press Start to begin")
        new_game()
        self.xc = 1
        self.yc = 1

    # Lance le process en accéléré pour afficher le résultat
    def resultTimer(self):
        self.timer.start(10)
        self.startBtn.setEnabled(False)
        self.endBtn.setEnabled(True)

    def pixel(self):
        # Charge l'image source
        img = Image.open("img/source.png")
        # Change la résolution de l'image
        imgSmall = img.resize((self.xc, self.yc),
                              resample=Image.Resampling.BILINEAR)
        # Ramène l'image à la bonne dimension
        result = imgSmall.resize(img.size, Image.Resampling.NEAREST)
        # Sauvegarde le résultat
        result.save('img/result.png')
        # Remplace l'image affiché
        self.im = QPixmap("img/result.png")
        self.label.setPixmap(self.im)
        # Augmente la résolution pour les prochaines images
        self.xc = self.xc + 1
        self.yc = self.yc + 1


if __name__ == '__main__':
    new_game()
    app = QApplication(sys.argv)
    form = WinForm()
    form.show()
    sys.exit(app.exec_())
