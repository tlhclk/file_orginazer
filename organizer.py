import xlrd, xlwt, os, datetime,re,shutil
from data_base import Image
from collector import DataCollector


class Organizer:
    def __init__(self, folder_path):
        fgroup_path = "file_info.xls"
        self.folder_path = folder_path
        self.fgroup_dict = self.get_fgroup_dict(fgroup_path)
        self.image_list = self.get_children()
        self.date_match_dict=self.get_date_match()
    
    def get_fgroup_dict(self, fgroup_path):
        fgroup_dict = {}
        wb0 = xlrd.open_workbook(fgroup_path)
        sht1 = wb0.sheet_by_name("data")
        for y in range(1, sht1.nrows):
            ftype = sht1.cell(y, 0).value
            fgroup = sht1.cell(y, 1).value
            fgroup_dict[ftype] = fgroup
        return fgroup_dict
    
    def get_fgroup(self, ftype):
        if ftype in self.fgroup_dict:
            return self.fgroup_dict[ftype]
        else:
            return "Other"
    
    def parse_path(self, path):
        pasrsed_path = path.split("\\")
        parent_path = "\\".join(pasrsed_path[:-1])
        path_name = pasrsed_path[-1]
        if not os.path.isdir(path):
            parsed_name = path_name.split(".")
            if len(parsed_name) > 1:
                name = ".".join(parsed_name[:-1])
                ftype = parsed_name[-1]
                return False, parent_path, name, ftype
            else:
                return False, parent_path, path_name, ""
        else:
            return True, parent_path, path_name
    
    def get_children(self):
        image_list = []
        if os.path.isdir(self.folder_path):
            children_list = os.listdir(self.folder_path)
            for child in children_list:
                child_path = "%sa\\%s" % (self.folder_path, child)
                if not os.path.isdir(child_path):
                    parsed_data = self.parse_path(child_path)
                    ftype = parsed_data[-1]
                    fgroup = self.get_fgroup(ftype)
                    if fgroup == "Video":
                        image_list.append(child)
                    else:
                        print("%s is not image" % child)
                else:
                    print("%s is not file" % child_path)
        else:
            print("Path is not Folder")
        return image_list
    
    def get_similarity(self, path1, path2):
        consecutive = 0
        inclusive = 0
        letter_difference = self.get_letter_difference(path1, path2)
        return letter_difference
    
    def get_letter_count(self, path):
        letter_dict = {}
        for letter in path:
            if letter not in letter_dict:
                letter_dict[letter] = 1
            else:
                letter_dict[letter] += 1
        return letter_dict
    
    def get_letter_difference(self, path1, path2):
        count1 = self.get_letter_count(path1)
        count2 = self.get_letter_count(path2)
        for letter2 in count2:
            if letter2 in count1:
                count1[letter2] = (count1[letter2], count2[letter2])
            else:
                count1[letter2] = (0, count2[letter2])
        for letter1 in count1:
            if type(count1[letter1]) == type(0):
                count1[letter1] = (count1[letter1], 0)
        different_letter_count = 0
        difference_count = 0
        for letter1 in count1:
            if count1[letter1][0] != count1[letter1][1]:
                different_letter_count += 1
                difference_count += abs(count1[letter1][0] - count1[letter1][1]) / 2.0
        return difference_count * different_letter_count
    
    def start_flow(self):
        for p1 in self.image_list:
            for p2 in self.image_list:
                sim = self.get_similarity(p1, p2)
                print(p1,p2,sim)
                
    def get_date_match(self):
        matched_files={}
        for p in self.image_list:
            qwe=re.search(r"IMG-(?P<date>\d{8})-\w+.\d+",p)
            asd=re.search(r"IMG_(?P<date>\d{8})_\d+",p)
            zxc=re.search(r"Screenshot_(?P<date>\d{8})-\d+",p)
            rty=re.search(r"PANO_(?P<date>\d{8})_\d+",p)
            fgh=re.search(r"VID_(?P<date>\d{8})_\d+",p)
            vbn=re.search(r"VID-(?P<date>\d{8})-\w+.\d+",p)
            if hasattr(qwe,"group"):
                date=qwe.group("date")
            elif hasattr(asd,"group"):
                date=asd.group("date")
            elif hasattr(zxc,"group"):
                date=zxc.group("date")
            elif hasattr(rty,"group"):
                date=rty.group("date")
            elif hasattr(fgh,"group"):
                date=fgh.group("date")
            elif hasattr(vbn,"group"):
                date=vbn.group("date")
            else:
                date="00000000"
            if date not in matched_files:
                matched_files[date]=[p]
            else:
                matched_files[date].append(p)
        return matched_files
    
    def group_files(self,target_path): # Group data based on date
        og=""
        if not os.path.isdir(target_path):
            os.mkdir(target_path)
        for key,value in self.date_match_dict.items():
            target_path_child="%s\\%s" % (target_path,key)
            if not os.path.isdir(target_path_child):
                os.mkdir(target_path_child)
            for file_name in value:
                target_path_file = "%s\\%s" % (target_path_child, file_name)
                if os.path.isfile(target_path_file):
                    og += "Dosya Mevcut: %s\n" % target_path_file
                else:
                    # os.rename("%s\\%s" % (self.folder_path,file_name),target_path_file)
                    shutil.copyfile("%s\\%s" % (self.folder_path, file_name), target_path_file)
        ogf=open("organizer-group_files.txt","w+")
        ogf.write(og)
        ogf.close()
        
        
        
        


main_path = "d:\\Talha\\Masaüstü\\Kişiler\\halil çelik (18.04.2020)\\Video"
target_path = "d:\\Talha\\Masaüstü\\Kişiler\\halil çelik (18.04.2020)\\Video2"
organizer = Organizer(main_path)
organizer.group_files(target_path)
#organizer.start_flow()
