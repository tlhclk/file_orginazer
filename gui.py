from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import sys


class DesktopApp(QMainWindow):
	def __init__(self):
		super(DesktopApp, self).__init__()
		self.setWindowTitle('File Organizer')
		self.sx, self.sy, self.mx, self.my = 200, 100, 540, 640
		self.setGeometry(self.sx, self.sy, self.mx, self.my)
		self.setWindowIcon(QIcon("icon.png"))
		self.setToolTip("File Organizer")
		self.font1=QFont('Calibri', 14)
		self.font1.setBold(True)
		self.font2=QFont('Calibri', 10)
		self.font2.setBold(True)
		self.initUI()
	
	def initUI(self):
		self.lbl0 = QtWidgets.QLabel(self)
		self.lbl0.resize(self.mx,self.my)
		self.lbl0.setStyleSheet("background-color: green")
		
		self.lbl1 = QtWidgets.QLabel(self)
		self.lbl1.setText('  To Organize')
		self.lbl1.resize(370, 30)
		self.lbl1.setStyleSheet("background-color: green; color: white")
		self.lbl1.setFont(self.font1)
		self.btn1 = QtWidgets.QPushButton(self)
		self.btn1.setText("Select a Folder")
		#self.btn1.clicked.connect(self.get_folder)
		self.txt1 = QtWidgets.QLineEdit(self)
		self.txt1.resize(370, 30)
		
		self.lbl2 = QtWidgets.QLabel(self)
		self.lbl2.setText('  Organized Excel Data Path')
		self.lbl2.resize(370, 30)
		self.lbl2.setStyleSheet("background-color: green; color: white")
		self.lbl2.setFont(self.font1)
		self.btn2 = QtWidgets.QPushButton(self)
		self.btn2.setText("Select an \nExcel File")
		#self.btn2.clicked.connect(self.get_file)
		self.txt2 = QtWidgets.QLineEdit(self)
		self.txt2.resize(370, 30)
		
		self.btn3 = QtWidgets.QPushButton(self)
		self.btn3.setText("Gather All Path Info")
		self.btn3.resize(120, 30)
		self.btn3.setStyleSheet("background-color: white; color: green")
		#self.btn3.clicked.connect(self.run_flow)
		
		self.btn4 = QtWidgets.QPushButton(self)
		self.btn4.setText("Organize The Paths")
		self.btn4.resize(120, 30)
		#self.btn4.clicked.connect(self.open_folder)
		
		self.lbl5 = QtWidgets.QLabel(self)
		self.lbl5.resize(500, 400)
		self.lbl5.setStyleSheet("background-color: white")
		self.lbl5.setFont(self.font2)
		
		self.resize_widgets()
	
	def resize_widgets(self):
		self.lbl0.move(0,0)
		self.lbl1.move(150, 20)
		self.txt1.move(150, 60)
		self.btn1.move(20, 60)
		self.lbl2.move(150, 100)
		self.txt2.move(150, 140)
		self.btn2.move(20, 140)
		self.btn3.move(260,180)
		self.btn4.move(400,180)
		self.lbl5.move(20,220)
	
def window():
	app = QApplication(sys.argv)
	win = DesktopApp()
	win.show()
	sys.exit(app.exec_())


window()
