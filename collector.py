import xlrd,xlwt,os,re,datetime
from data_base import *


class DataCollector:
	file_list=[]
	folder_list=[]
	
	def __init__(self,main_path="D:\\Talha\\Masaüstü"):
		fgroup_path=os.getcwd()+"\\file_info.xls"
		self.main_path=main_path
		self.fgroup_dict=self.get_fgroup_dict(fgroup_path)
		self.fgroup_class_dict={"Other":Path,"Image":Image,"Video":Video,"Music":Music,"Document":Document,"Folder":Path}
		main_folder=self.build_main_folder()
		self.start_flow(main_folder)
		
		
	def get_fgroup_dict(self, fgroup_path):
		fgroup_dict = {}
		wb0 = xlrd.open_workbook(fgroup_path)
		sht1 = wb0.sheet_by_name("data")
		for y in range(1, sht1.nrows):
			ftype = sht1.cell(y, 0).value
			fgroup = sht1.cell(y, 1).value
			fgroup_dict[ftype] = fgroup
		return fgroup_dict
	
	def get_fgroup(self,ftype):
		if ftype in self.fgroup_dict:
			return self.fgroup_dict[ftype]
		else:
			return "Other"
		
	def build_main_folder(self):
		parsed_data=self.parse_path(self.main_path)
		main_folder=self.build_folder(parsed_data)
		self.folder_list.append(main_folder)
		return main_folder
		
	def parse_path(self,path):
		parsed_path = path.split("\\")
		parent_path="\\".join(parsed_path[:-1])
		path_name=parsed_path[-1]
		if os.path.isfile(path):
			parsed_name=path_name.split(".")
			if len(parsed_name)>1:
				name=".".join(parsed_name[:-1])
				ftype=parsed_name[-1]
				return False,parent_path,name,ftype
			else:
				return False, parent_path, path_name, ""
		else:
			return True,parent_path,path_name
		
	def get_children(self,folder):
		temp_file_list=[]
		temp_folder_list=[]
		try:
			children_list=os.listdir(folder.get_full_name())
			for path in children_list:
				full_path="%s\\%s" % (folder.get_full_name(),path.__str__())
				is_folder=os.path.isdir(full_path)
				if is_folder:
					parsed_data=self.parse_path(full_path)
					new_folder=self.build_folder(parsed_data)
					self.folder_list.append(new_folder)
					temp_folder_list.append(new_folder)
				else:
					parsed_data=self.parse_path(full_path)
					new_file=self.build_file(parsed_data)
					self.file_list.append(new_file)
					temp_file_list.append(new_file)
		except PermissionError:
			pass
		return temp_file_list,temp_folder_list

	def build_folder(self,parsed_data):
		folder=Path()
		folder.is_folder = parsed_data[0]
		folder.parent_folder = parsed_data[1]
		folder.name = parsed_data[2]
		folder.id=len(self.file_list)+len(self.folder_list)+1
		return folder
	
	def build_file(self,parsed_data):
		file_path="%s\\%s.%s" %(parsed_data[1],parsed_data[2],parsed_data[3])
		if not os.path.isdir(file_path):
			ftype=parsed_data[3].lower()
			fgroup=self.get_fgroup(ftype)
			file=self.fgroup_class_dict[fgroup]()
			file.is_folder=parsed_data[0]
			file.parent_folder=parsed_data[1]
			file.name=parsed_data[2]
			file.id=len(self.file_list)+len(self.folder_list)+1
			file.ftype=ftype
			file.fgroup=fgroup
			file.size=os.path.getsize(file_path)
			file_stats=os.stat(file_path)
			f_mode=file_stats.st_mode
			f_size=file_stats.st_size
			f_atime=file_stats.st_atime
			f_mtime=file_stats.st_mtime
			f_ctime=file_stats.st_ctime
			file.fmode=f_mode
			file.fsize=f_size
			file.fatime=datetime.datetime.utcfromtimestamp(f_atime).strftime("%d-%m-%Y %H:%M:%S")
			file.fmtime=datetime.datetime.utcfromtimestamp(f_mtime).strftime("%d-%m-%Y %H:%M:%S")
			file.fctime=datetime.datetime.utcfromtimestamp(f_ctime).strftime("%d-%m-%Y %H:%M:%S")
			return file
		else:
			return None

	def start_flow(self,folder):
		temp_file_list,temp_folder_list=self.get_children(folder)
		folder.file_list=temp_file_list
		folder.folder_list=temp_folder_list
		for next_folder in temp_folder_list:
			self.start_flow(next_folder)
		

