import os

os.system("pyinstaller --onefile protector.py")

os.system("copy dist\protector.exe protector.exe")

os.system("del /q /f /s dist")

os.system("del /q /f /s build")

os.system("del protector.spec")