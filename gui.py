from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from export_structure import ToExcel
from similarity import Similarity
from from_excel import FromExcel
import sys,os


class DesktopApp(QMainWindow):
	def __init__(self):
		super(DesktopApp, self).__init__()
		self.setWindowTitle('File Organizer')
		self.sx, self.sy, self.mx, self.my = 200, 100, 560, 640
		self.setGeometry(self.sx, self.sy, self.mx, self.my)
		self.setWindowIcon(QIcon("icon.png"))
		self.setToolTip("File Organizer")
		self.font1=QFont('Calibri', 14)
		self.font1.setBold(True)
		self.font2=QFont('Calibri', 11)
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
		self.btn1.setFont(self.font2)
		self.btn1.resize(140, 30)
		self.btn1.setStyleSheet("background-color: white; color: green")
		self.btn1.clicked.connect(self.get_folder)
		self.txt1 = QtWidgets.QLineEdit(self)
		self.txt1.resize(370, 30)
		
		self.lbl2 = QtWidgets.QLabel(self)
		self.lbl2.setText('  Organized Excel Data Path')
		self.lbl2.resize(370, 30)
		self.lbl2.setStyleSheet("background-color: green; color: white")
		self.lbl2.setFont(self.font1)
		self.btn2 = QtWidgets.QPushButton(self)
		self.btn2.setText("Select an Excel File")
		self.btn2.setFont(self.font2)
		self.btn2.resize(140, 30)
		self.btn2.setStyleSheet("background-color: white; color: green")
		self.btn2.clicked.connect(self.get_file)
		self.txt2 = QtWidgets.QLineEdit(self)
		self.txt2.resize(370, 30)
		
		self.btn3 = QtWidgets.QPushButton(self)
		self.btn3.setText("Rename Path Info")
		self.btn3.resize(140, 30)
		self.btn3.setFont(self.font2)
		self.btn3.setStyleSheet("background-color: white; color: green")
		self.btn3.clicked.connect(self.rename_path_info)
		
		self.btn4 = QtWidgets.QPushButton(self)
		self.btn4.setText("Organize The Paths")
		self.btn4.resize(140, 30)
		self.btn4.setFont(self.font2)
		self.btn4.setStyleSheet("background-color: white; color: green")
		self.btn4.clicked.connect(self.organize_the_paths)
		
		self.lbl5 = QtWidgets.QLabel(self)
		self.lbl5.resize(520, 400)
		self.lbl5.setStyleSheet("background-color: white")
		self.lbl5.setFont(self.font2)
		
		self.resize_widgets()
	
	def resize_widgets(self):
		self.lbl0.move(0,0)
		self.lbl1.move(170, 20)
		self.txt1.move(170, 60)
		self.btn1.move(20, 60)
		self.lbl2.move(170, 100)
		self.txt2.move(170, 140)
		self.btn2.move(20, 140)
		self.btn3.move(240,180)
		self.btn4.move(400,180)
		self.lbl5.move(20,220)
	
	def get_folder(self):# open and find a folder and get path and write to textbox
		fname = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select a Folder', os.getcwd(),
		                                                   QtWidgets.QFileDialog.ShowDirsOnly)
		te = ToExcel(main_path=fname, excel_path=fname.split("/")[-1]+"_organization_file.xls")
		te.start_flow()
		self.txt1.setText(fname)
		self.txt2.setText(os.path.basename(fname)+"_organization_file.xls")
	
	def get_file(self):# open and find a file and get path and write to textbox
		fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Select a File', os.getcwd(), "Excel files (*.xls *.xlsx)")
		#excel_path=self.txt1.text()+"/"+self.txt2.text()
		excel_path = fname
		fe = FromExcel(excel_path)
		self.db = fe.get_excel_data()
		self.txt2.setText(fname[0])
		self.txt1.setText(os.path.dirname(fname[0]))
		
	def rename_path_info(self):# gather all path infos and write to the excel (given path)
		# te=ToExcel(main_path=self.txt1.text(),excel_path=self.txt2.text())
		# te.start_flow()
		pass

	def organize_the_paths(self):
		sim=Similarity(self.db)
		sim.get_files_similarity()
	
def window():
	app = QApplication(sys.argv)
	win = DesktopApp()
	win.show()
	sys.exit(app.exec_())


window()
