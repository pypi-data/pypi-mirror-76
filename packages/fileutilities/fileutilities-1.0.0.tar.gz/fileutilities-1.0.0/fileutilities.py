

import os
import subprocess
import os.path
#global variables
notion_path="C://Users//aksha//AppData//Local//Programs//Notion//Notion.exe"
atom_path="C:/Users/aksha/AppData/Local/atom/atom.exe"
Vscode_path="C://Program Files//Microsoft VS Code//Code.exe"
word_path="C://Program Files (x86)//Microsoft Office//root//Office16//WINWORD.EXE"
#functions
def file_maker(file_name,file_format):
    format_final=""
    format_list=[i for i in file_format]
    if '.' not in format_list:
        format_list.insert(0,'.')
        for a in format_list:
            format_final+=a
        final_file=f"{file_name.lower()}{format_final.lower()}"
        return final_file
def create_file(file_name,file_format=".txt",directory="",program=""):
     file1=file_maker(str(file_name),str(file_format))
     if os.path.isdir(str(directory)):
          os.chdir("C:/Users/aksha/Desktop")
          os.chdir(str(directory))
          if str(program).lower()=="vscode" or file_format==".py":
               subprocess.Popen([Vscode_path,file1])
          elif str(program).lower()=="atom":
               subprocess.Popen([atom_path,file1])
          elif str(program).lower()=="word":
               subprocess.Popen([word_path,file1])
          elif str(program).lower()=="notion":
               subprocess.Popen([notion_path,file1])
          else:
               os.startfile(file1)
     elif os.path.isdir(directory)==False:
          os.chdir("C:/Users/aksha/Desktop")
          os.mkdir(directory)
          os.chdir(directory)
          if program.lower()=="vscode":
               subprocess.Popen([Vscode_path,file1])
          elif program.lower()=="atom":
               subprocess.Popen([atom_path,file1])
          elif program.lower()=="word":
               subprocess.Popen([word_path,file1])
          elif program.lower()=="notion":
               subprocess.Popen([notion_path,file1])
def delete(name,file_format,folder=""):
     file2=file_maker(str(name),str(file_format))

     if str(folder)=="":
          os.remove(file2)
     else:
          os.chdir(str(folder))
          os.remove(file2)