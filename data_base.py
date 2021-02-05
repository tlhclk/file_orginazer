
# For Path
class Path:
	id = None
	name = None
	parent_folder = None
	new_name=None
	new_parent_folder=None
	is_folder= None
	file_list = []
	folder_list = []
	attr_dict = {
		"id": {"index": 0, "title": "ID", "str": None,"type":"variable"},
		"name": {"index": 1, "title": "Adı", "str": "%s","type":"variable"},
		"parent_folder": {"index": 2, "title": "Klasör Adı", "str": None,"type":"variable"},
		"new_name": {"index": 3, "title": "Yeni Adı", "str": "%s","type":"variable"},
		"new_parent_folder": {"index": 4, "title": "Yeni Klasör Adı", "str": None,"type":"variable"},
		"is_folder": {"index": 5, "title": "Klasör Durumu", "str": None,"type":"boolean"},
		"file_list": {"index": 0, "title": "Dosya Listesi", "str": None,"type":"list"},
		"folder_list": {"index": 1, "title": "Klasör Listesi", "str": None,"type":"list"},
	}
	
	def __str__(self):
		return self.get_full_name()
		
	def get_name(self):
		if self.new_name!=None and self.new_name!="":
			return self.new_name
		else:
			return self.name
	
	def get_full_name(self):
		if self.parent_folder!=None and self.parent_folder!="":
			return "%s\\%s" % (self.parent_folder,self.get_name())
		else:
			return self.get_name()
		
	def get_new_full_name(self):
		if self.parent_folder!=None and self.parent_folder!="":
			if self.new_parent_folder!=None and self.new_parent_folder!="":
				return "%s\\%s" % (self.new_parent_folder, self.get_name())
			else:
				return "%s\\%s" % (self.parent_folder, self.get_name())
		else:
			return self.get_name()
	
	def get_file_count(self):
		return len(self.file_list)
	
	def get_folder_count(self):
		return len(self.folder_list)
	
	def get_size(self):
		size=0
		for file in self.file_list:
			size+=file.size
		for folder in self.folder_list:
			size+=folder.get_size()
		return size
	
	def add_path(self,path):# add folder and file paths that under the folder
		if path.is_folder:
			self.folder_list.append(path)
		else:
			self.file_list.append(path)
	
	def get_attr_dict(self):
		return self.attr_dict
		
# For File
class File(Path):
	ftype = None
	fgroup = None
	fmode = None
	fsize = None
	fatime = None
	fmtime = None
	fctime = None
	is_folder = False
	file_attr_dict = {
		"ftype": {"index": 6, "title": "Dosya Türü", "str": ".%s","type":"variable"},
		"fmode": {"index": 7, "title": "Dosya Kodu", "str": None,"type":"variable"},
		"fsize": {"index": 8, "title": "Dosya Boyutu2", "str": None,"type":"variable"},
		"fatime": {"index": 9, "title": "Dosyaya Erişim Zamanı", "str": None,"type":"variable"},
		"fmtime": {"index": 10, "title": "Dosya Değiştirme Zamanı", "str": None,"type":"variable"},
		"fctime": {"index": 11, "title": "Dosya Oluşturma Zamanı", "str": None,"type":"variable"},
	}
	
	def get_size(self):
		return self.fsize
	
	def get_attr_dict(self):
		return {**self.attr_dict,**self.file_attr_dict}
	
	def get_full_name(self):
		if self.ftype!=None or self.ftype!="":
			return "%s\\%s.%s" % (self.parent_folder,self.name,self.ftype)
		else:
			return "%s\\%s" % (self.parent_folder, self.name)
		
	def get_new_full_name(self):
		if self.ftype!=None or self.ftype!="":
			if self.new_parent_folder!=None and self.new_parent_folder!="":
				return "%s\\%s.%s" % (self.new_parent_folder,self.get_name(),self.ftype)
			else:
				return "%s\\%s.%s" % (self.parent_folder,self.get_name(),self.ftype)
		else:
			return "%s\\%s" % (self.parent_folder, self.get_name())
		
	
class Video(File):
	second_name=None
	season=None
	episode=None
	quality=None
	year=None
	desc=None
	video_attr_dict = {
		"second_name": {"index": 12, "title": "İkinci Ad", "str": None,"type":"variable"},
		"season": {"index": 13, "title": "Sezon", "str": None,"type":"variable"},
		"episode": {"index": 14, "title": "Bölüm", "str": None,"type":"variable"},
		"quality": {"index": 15, "title": "Kalite", "str": None,"type":"variable"},
		"year": {"index": 16, "title": "Yıl", "str": None,"type":"variable"},
		"desc": {"index": 17, "title": "Açıklama", "str": None,"type":"variable"},
	}

	def get_attr_dict(self):
		attr_dict=super(Video, self).get_attr_dict()
		return {**attr_dict,**self.video_attr_dict}
	
	def get_name(self):
		if self.new_name!=None and self.new_name!="":
			name= self.new_name
		else:
			name= self.name
		if self.second_name!=None and self.second_name!="":
			name+="-%s" % self.second_name
		if self.season!=None and self.season!="":
			name+=" (Season %s)" % str(int(self.season))
		if self.episode!=None and self.episode!="":
			name+=" (Episode %s)" % str(int(self.episode))
		if self.quality!=None and self.quality!="":
			name+=" [%s]" % self.quality
		if self.year!=None and self.year!="":
			name+=" [%s]" %str(int(self.year))
		if self.desc!=None and self.desc!="":
			name+=" (%s)" % self.desc
		return name
		
	
class Music(File):
	second_name=None
	singer=None
	album=None
	year=None
	desc=None
	music_attr_dict = {
		"second_name": {"index": 12, "title": "İkinci Ad", "str": None,"type":"variable"},
		"singer": {"index": 13, "title": "Şarkıcı", "str": None,"type":"variable"},
		"album": {"index": 14, "title": "Albüm", "str": None,"type":"variable"},
		"year": {"index": 15, "title": "Yıl", "str": None,"type":"variable"},
		"desc": {"index": 16, "title": "Açıklama", "str": None,"type":"variable"},
	}

	def get_attr_dict(self):
		attr_dict=super(Music, self).get_attr_dict()
		return {**attr_dict,**self.music_attr_dict}
	
	def get_name(self):
		if self.new_name!=None and self.new_name!="":
			name= self.new_name
		else:
			name= self.name
		if self.second_name != None and self.second_name!="":
			name += "-%s" % self.second_name
		if self.singer != None and self.singer!="":
			name += " [%s]" % self.singer
		if self.album != None and self.album!="":
			name += " [%s]" % self.album
		if self.year != None and self.year!="":
			name += " [%s]" % str(int(self.year))
		if self.desc != None and self.desc!="":
			name += " (%s)" % self.desc
		return name
	
class Image(File):
	second_name=None
	month=None
	year=None
	desc=None
	image_attr_dict = {
		"second_name": {"index": 12, "title": "İkinci Ad", "str": None, "type": "variable"},
		"month": {"index": 13, "title": "Ay", "str": None, "type": "variable"},
		"year": {"index": 14, "title": "Yıl", "str": None, "type": "variable"},
		"desc": {"index": 15, "title": "Açıklama", "str": None, "type": "variable"},
	}

	def get_attr_dict(self):
		attr_dict=super(Image, self).get_attr_dict()
		return {**attr_dict,**self.image_attr_dict}
	
	def get_name(self):
		if self.new_name!=None and self.new_name!="":
			name= self.new_name
		else:
			name= self.name
		if self.second_name != None and self.second_name!="":
			name += "-%s" % self.second_name
		if self.year != None and self.year!="":
			if self.month != None and self.month!="":
				name += " [%s/%s]" % (str(int(self.month)), str(int(self.year)))
			else:
				name += " [%s]" % str(int(self.year))
		if self.desc != None and self.desc!="":
			name += " (%s)" % self.desc
		return name
	
class Document(File):
	document_attr_dict = {
	}

	def get_attr_dict(self):
		#attr_dict=super(Document, self).get_attr_dict()
		#return {**attr_dict,**self.document_attr_dict}
		return {**self.attr_dict,**self.file_attr_dict,**self.document_attr_dict}
	
	def get_name(self):
		if self.new_name!=None and self.new_name!="":
			name= self.new_name
		else:
			name= self.name
		return name
	