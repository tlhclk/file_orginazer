import xlrd, os, re
from data_base import *

class FromExcel:
	def __init__(self, excel_path):
		fgroup_path = os.getcwd() + "\\file_info.xls"
		self.fgroup_class_dict = {"Other": File, "Image": Image, "Video": Video, "Music": Music, "Document": Document,
		                          "Folder": Path}
		self.excel_path = excel_path
		self.fgroup_dict = self.get_fgroup_dict(fgroup_path)
	
	def get_excel_sheets(self, excel_path):
		wb0 = xlrd.open_workbook(excel_path)
		all_sheet_names = wb0.sheet_names()
		sheet_dict = {}
		for sht_name in all_sheet_names:
			sheet_dict[sht_name] = wb0.sheet_by_name(sht_name)
		return sheet_dict
	
	def get_fgroup_dict(self, fgroup_path):
		fgroup_dict = {}
		wb0 = xlrd.open_workbook(fgroup_path)
		sht1 = wb0.sheet_by_name("data")
		for y in range(1, sht1.nrows):
			ftype = sht1.cell(y, 0).value
			fgroup = sht1.cell(y, 1).value
			fgroup_dict[ftype] = fgroup
		return fgroup_dict
	
	def get_sheet_header(self, sheet):
		header_list = []
		for x in range(sheet.ncols):
			header_list.append(sheet.cell(0, x).value)
		return header_list
	
	def get_sheet_data(self, sheet):
		sheet_data = []
		rown = sheet.nrows
		for y in range(1, rown):
			cls = self.save_as_class(sheet, y)
			sheet_data.append(cls)
		return sheet_data
	
	def save_as_class(self, sheet, y):
		sname = sheet.name
		coln = sheet.ncols
		if sname in self.fgroup_class_dict:
			cls = self.fgroup_class_dict[sname]()
			attr_dict = cls.get_attr_dict()
			for x in range(coln):
				key = list(attr_dict.keys())[x]
				value = sheet.cell(y, x).value
				setattr(cls, key, value)
			return cls
		else:
			text = ""
			for x in range(coln):
				key = sheet.cell(0, x).value
				value = sheet.cell(y, x).value
				text += "%s:%s," % (key, value)
			return (None, text)
	
	def get_excel_data(self):
		database = []  # file_list
		excel_sheets = self.get_excel_sheets(self.excel_path)
		for sname in excel_sheets:
			sheet = excel_sheets[sname]
			sheet_data = self.get_sheet_data(sheet)
			database |= sheet_data
		return database
