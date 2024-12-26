import os , sys
os.system(f"attrib -h +s +r {sys.argv[0]}")

class explore:
    def __open_file__(self):
        self.path = "C:/"
        os.chdir(self.path)
    def __open_floder__(self, name_floder):
        try:
            os.chdir(name_floder)
        except:
            return False
    def __remove__(self, name):
        try:
            try:
                os.remove(name)
                return True
            except:
                os.rmdir(name)
                return False
        except:
            return False
    def __create_floder__(self, creat_floder):
        try:
            os.mkdir(creat_floder)
            return True
        except:
            return False
    def __show__(self):
        return os.listdir()
    def __search__(self, name):
        try:
            for root, dirs, files in os.walk("C:/"):
                if name in files:
                    return os.path.join(root, name)
                if name in dirs:
                    return os.path.join(root, name)
        except:
            return False
