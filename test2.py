import sys
from PyQt5 import *

app = QApplication(sys.argv)
   
label = QLabel()
pixmap = QPixmap(sys.argv[1])
label.setPixmap(pixmap)
label.show()

sys.exit(app.exec_())