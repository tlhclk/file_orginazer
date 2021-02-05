import xlrd,xlwt,os,re,datetime
from data_base import *
from collector import DataCollector

class ToExcel:
	
	def __init__(self,main_path="D:\\Talha\\Masaüstü",excel_path=None):
		self.excel_path=excel_path
		dc=DataCollector(main_path)
		self.file_list=dc.file_list
		self.folder_list=dc.folder_list
		self.main_path=dc.main_path
		self.fgroup_dict=dc.fgroup_dict
		self.fgroup_class_dict=dc.fgroup_class_dict
		self.parse_path=dc.parse_path
		self.wb0 = xlwt.Workbook()
		self.excel_sheets=self.create_excel_sheets()
		
	def get_excel_path(self):
		if self.excel_path != None:
			return "%s\\%s" % (self.main_path,self.excel_path)
		else:
			if self.main_path[-1]==":":
				result= "%s\\%s_%s_%s.xls" % (self.main_path,self.parse_path(self.main_path)[2].replace(":",""),"file_structure",str(datetime.datetime.today())[:10])
				return result
			else:
				result= "%s\\%s_%s_%s.xls" % (self.main_path,self.parse_path(self.main_path)[2],"file_structure",str(datetime.datetime.today())[:10])
				return result
	
	def get_fgroup_list(self):
		temp_list=[]
		for value in self.fgroup_dict.values():
			if value not in temp_list:
				temp_list.append(value)
		return temp_list
	
	def create_excel_sheets(self):
		sheet_dict={}
		sheet_dict["folder_sht"]=self.wb0.add_sheet("Folder")
		sheet_dict["other_sht"]=self.wb0.add_sheet("Other")
		sheet_dict["children_sht"]=self.wb0.add_sheet("Children")
		for fgroup in self.get_fgroup_list():
			sheet_dict["%s_sht" % fgroup.lower()]=self.wb0.add_sheet(fgroup)
		return sheet_dict
	
	def filtered_list(self,object_list,filter_dict):
		result_list=[]
		if len(filter_dict)>0:
			filter_key,filter_value=list(filter_dict.items())[0]
		else:
			return object_list
		for object in object_list:
			if getattr(object,filter_key)==filter_value:
				result_list.append(object)
		return self.filtered_list(result_list,dict(list(filter_dict.items())[1:]))

	def write_folder(self):
		folder_sht=self.excel_sheets["folder_sht"]
		for attr_key,attr_value  in Path().get_attr_dict().items():
			if attr_value["type"]=="variable" or attr_value["type"] == "boolean":
				folder_sht.write(0,attr_value["index"],attr_value["title"])
		n=1
		for folder in self.folder_list:
			for attr_key,attr_value in folder.get_attr_dict().items():
				if attr_value["type"]=="variable" or attr_value["type"] == "boolean":
					folder_sht.write(n,attr_value["index"],getattr(folder,attr_key))
			n+=1
			
	def write_file(self):
		fgroup_list=self.get_fgroup_list()
		for fgroup in fgroup_list:
			sheet=self.excel_sheets["%s_sht" % fgroup.lower()]
			file_cls=self.fgroup_class_dict[fgroup]()
			for attr_key, attr_value in file_cls.get_attr_dict().items():
				if attr_value["type"] == "variable" or attr_value["type"] == "boolean":
					sheet.write(0, attr_value["index"], attr_value["title"])
			n=1
			for file in self.filtered_list(self.file_list,{"fgroup":fgroup}):
				for attr_key,attr_value in file.get_attr_dict().items():
					if attr_value["type"]=="variable" or attr_value["type"] == "boolean":
						sheet.write(n,attr_value["index"],getattr(file,attr_key))
				n+=1
	
	def write_children(self):
		sheet=self.excel_sheets["children_sht"]
		sheet.write(0, 0,"folder_id")
		sheet.write(0, 1,"file_id")
		sheet.write(0, 2,"is_folder")
		n=1
		for folder in self.folder_list:
			for file in folder.file_list:
				sheet.write(n,0,folder.id)
				sheet.write(n,1,file.id)
				sheet.write(n,2,True)
				n+=1
				
	def start_flow(self):
		self.write_folder()
		self.write_file()
		self.write_children()
		self.save_excel()
		
	def save_excel(self):
		self.wb0.save(self.get_excel_path())
