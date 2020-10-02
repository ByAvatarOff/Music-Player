from PyQt5 import QtWidgets
import sys
from myPlayer import Ui_Dialog


app = QtWidgets.QApplication(sys.argv)

Dialog = QtWidgets.QDialog()
ui = Ui_Dialog()
ui.setupUi(Dialog)
Dialog.show()

#Hook logic

sys.exit(app.exec_())
