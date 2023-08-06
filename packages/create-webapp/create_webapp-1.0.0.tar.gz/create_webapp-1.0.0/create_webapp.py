import os
import subprocess
import os.path
import sys
#global variables
Vscode_path="C://Program Files//Microsoft VS Code//Code.exe"
desktop="C:/Users/aksha/Desktop"
atom_path="C:/Users/aksha/AppData/Local/atom/atom.exe"
#functions
filetypes = {
    ".py": "Python",
    ".js":"Javascript",
    ".php": "PHP",
    ".css":"CSS",
    ".html":"HTML"
}
def create_project(folder,name,file_format):
    file1=f"{name}{file_format}"
    os.chdir(desktop)
    def is_folder(folder):
        if os.path.isdir(folder)==False:
            os.mkdir(folder)
    is_folder(folder)
    os.chdir(f"{desktop}/{folder}")
    is_folder("cgi-bin")
    is_folder("data")
    os.chdir("data")
    is_folder("images")
    is_folder("text")
    os.chdir("text")
    for i in range(0,2):
        subprocess.Popen([atom_path,f"data{i}.txt"])
    is_folder("table_data")
    os.chdir(f"{desktop}/{folder}")
    is_folder("backend")
    os.chdir("backend")
    is_folder("HTML")
    is_folder("CSS")
    is_folder("Javascript")
    is_folder("PHP")
    is_folder("sql")
    is_folder("Python")
    os.chdir("PHP")
    is_folder("server_data")
    final_path=f"{desktop}/{folder}/backend/{filetypes.get(file_format)}/{file1}"
    subprocess.Popen([Vscode_path,final_path])

create_project("webapp1","test",".py")
    