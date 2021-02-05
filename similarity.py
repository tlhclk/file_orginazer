import os, re,difflib
import datetime as dt


class Similarity:
	threshold=17
	def __init__(self,database):
		self.db=database
		self.result_db={}
		self.master_files=[]
		
	def get_files_similarity(self):
		for file in self.db:
			self.master_files.append(file)
			sim_files=self.find_similar_files(file)
			print(file,sim_files)
			self.result_db[file]=sim_files
	
	def find_similar_files(self,f1):
		similar_files=[]
		for f2 in self.db:
			if f2!=f1:
				sim_score=self.sim_score(f1,f2)
				if sim_score>=self.threshold:
					similar_files.append(f2)
		return similar_files
	
	def sim_score(self,f1,f2):
		ns=self.get_name_score(f1,f2)
		ds=self.get_date_score(f1,f2)
		ss=self.get_size_score(f1,f2)
		total_score=ns+ds#+ss
		return total_score
	
	def get_letter_order(self,fn):
		lo_dict={}
		for i,letter in enumerate(fn):
			if letter not in lo_dict:
				lo_dict[letter]=[i]
			else:
				lo_dict[letter].append(i)
		return lo_dict
	
	def get_lc_score(self,key_list,lo1,lo2):
		lc_score=0
		for key in key_list:
			if key in lo1:
				if key in lo2:
					lc_score += abs(len(lo1[key]) - len(lo2[key]))
				else:
					lc_score += abs(len(lo1[key]) - 0)
			else:
				lc_score += abs(0 - len(lo2[key]))
		return (len(key_list) - lc_score)*10/len(key_list)
	
	def get_lo_score(self,key_list,fn1,fn2):
		lo_score=0
		difflib.SequenceMatcher(None,fn1,fn2).ratio()
		return lo_score
	
	def get_name_score(self,file1,file2):
		dsm=difflib.SequenceMatcher(None,file1.get_name(),file2.get_name())
		name_score=dsm.ratio()*10
		return name_score
	
	def get_date_score(self,file1,file2):
		#+-1 yıl %100 den %0a=10dan 0a
		d1=dt.datetime.strptime(file1.fmtime, '%d-%m-%Y %H:%M:%S')
		d2=dt.datetime.strptime(file2.fmtime, '%d-%m-%Y %H:%M:%S')
		day_diff=abs((d1-d2).total_seconds())/86400.0
		date_score=(365-day_diff)/36.5
		return date_score
	
	def get_size_score(self,file1,file2):
		# +-1 yıl file1 boyutundan 0a=10dan 0a
		s1=file1.fsize
		s2=file2.fsize
		size_diff=abs(s1-s2)
		size_score=(s1-size_diff)*10/float(s1)
		return size_score
	
	

#sim=Similarity(file_info())
#sim.get_files_similarity()