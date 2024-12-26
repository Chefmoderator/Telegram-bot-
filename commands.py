import os

class commands:
    def __shutdown__(self):
        os.system("shurdown /s /t 0")
    def __download__(self,uri,name):
        os.system(f"powershell Invoke-WebReques -URI{uri} -OutFile{name}")
if __name__ == '__main__':
    command = commands()



