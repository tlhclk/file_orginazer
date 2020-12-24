import xlrd, xlwt, os, re, datetime
from data_base import *


class FromExcel:
	def __init__(self,excel_path):
		fgroup="file_into.xls"
		self.fgroup_class_dict={"Other":File,"Image":Image,"Video":Video,"Music":Music,"Document":Document,"Folder":Path}
		excel_path=excel_path
		self.path_list=self.get_excel_data(excel_path)

	def get_header(self,sht,rown):
		header_list=[]
		attr_dict=self.fgroup_class_dict[sht.name]().get_attr_dict()
		for coln in range(sht.ncols):
			for key,value in attr_dict.items():
				if value["title"]==sht.cell(rown,coln).value:
					header_list.append(key)
		return header_list

	def get_excel_data(self,excel_path):
		wb0=xlrd.open_workbook(excel_path)
		all_sheet_names=wb0.sheet_names()
		path_list=[]
		for sheet_name in all_sheet_names:
			sht=wb0.sheet_by_name(sheet_name)
			sht_cls=self.fgroup_class_dict[sheet_name]
			header_list=self.get_header(sht,0)
			for rown in range(1,sht.nrows):
				cls=sht_cls()
				for coln,header in enumerate(header_list):
					value=sht.cell(rown,coln).value
					setattr(cls,header,value)
				path_list.append(cls)
		return path_list

	def start_file_flow(self):
		result=""
		for path in self.path_list:
			# Klasör değilse
			if not os.path.isdir(path.get_full_name()):
				if path.get_size()==0 or path.get_size()=="":
					#os.remove(path.get_full_name())
					result+="Silinecek Dosya: %s\n" % path.get_full_name()
				else:
					# Dosya Adı Değiştirme koşulları: 
					# yeni ad boş veya hiç olmıycak
					if path.new_name!=None and path.new_name!="":
						# new adı ve eski adı aynı olmıycak	
						if path.name!=path.get_name():
							# eski dosya bulunacak
							if os.path.isfile(path.get_full_name()):
								# yeni dosya bulunmayacak
								if not os.path.isfile(path.get_new_full_name()):
									# Dosya Adı Değiştirme
									os.rename(path.get_full_name(),path.get_new_full_name())
								else:
									result+="Yeni Dosyası Var: %s\n" % path.get_full_name()
							else:
								result+="Eski Dosyası Yok: %s\n" % path.get_full_name()
						else:
							result+="Eski Dosyası Adı ve Yeni Dosya Adı Aynı: %s\n" % path.get_full_name()
		result_file=open("result_file.txt","w+")
		result_file.write(str(result))
		result_file.close()

	def start_folder_flow(self):
		result = ""
		for path in self.path_list:
			# Klasör değilse
			if not os.path.isdir(path.get_full_name()):
				# Eski Klasör Varsa
				if os.path.isdir(path.parent_folder):
					# Yeni Klasör Varsa
					if os.path.isdir(path.new_parent_folder):
						# Eski Klasör ve Yeni Klasör Aynı Değilse
						if str(path.parent_folder)!=path.new_parent_folder:
							# Eski Dosya Varsa
							if os.path.isfile(path.get_full_name()):
								# Yen Dosya Yoksa
								if not os.path.isfile(path.get_new_full_name()):
									# Dosya Adı Değiştirme
									os.rename(path.get_full_name(), path.get_new_full_name())
								else:
									result+="Yeni Dosya Var: %s\n" % path.get_full_name()
							else:
								result+="Eski Dosya Yok: %s\n" % path.get_full_name()
						else:
							result+="Eski Klasör ve Yeni Klasör Aynı: %s\n" % path.get_full_name()
					else:
						result += "Yeni Klasör Yok: %s\n" % path.get_full_name()
				else:
					result += "Eski Klasör Yok: %s\n" % path.get_full_name()
		result_folder = open("result_file_folder.txt", "w+")
		result_folder.write(str(result))
		result_folder.close()

fe=FromExcel("D:\\Talha\\Masaüstü\\Masaüstü_file_structure_2020-09-26.xls")
fe.start_file_flow()