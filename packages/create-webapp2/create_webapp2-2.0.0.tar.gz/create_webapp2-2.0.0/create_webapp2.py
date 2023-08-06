import os
import subprocess
import os.path
import sys
#global variables
Vscode_path="C://Program Files//Microsoft VS Code//Code.exe"
desktop="C:/Users/aksha/Desktop"
atom_path="C:/Users/aksha/AppData/Local/atom/atom.exe"
major_folders=["cgi-bin","data","backend","front-end","Template"]
data_folders=["images","text","table-data"]
front_end_folders=["HTML","CSS","Javascript"]
backend_folders=["Python","PHP","sql"]
#functions
filetypes = {
    ".py": "backend/Python",
    ".js":"front-end/Javascript",
    ".php": "backend/PHP",
    ".css":"front-end/CSS",
    ".html":"front-end/HTML",
    ".sql":"backend/sql",
}
def create_project(folder,name,file_format):
    file1=f"{name}{file_format}"
    os.chdir(desktop)
    def is_folder(folder):
        if os.path.isdir(folder)==False:
            os.mkdir(folder)
    def init_folder(list):
        for i in list:
            is_folder(i)
    is_folder(folder)
    os.chdir(f"{desktop}/{folder}")
    init_folder(major_folders)
    os.chdir("cgi-bin")
    webserver=open("simple_http.py","w")
    webserver.write(""" from http.server import HTTPServer, CGIHTTPRequestHandler
 port = 8080
 httpd = HTTPServer(('', port), CGIHTTPRequestHandler)
 print("Starting simple_httpd on port: " + str(httpd.server_port))
 httpd.serve_forever()""")
    webserver.close()
    os.chdir(f"{desktop}/{folder}/data")
    init_folder(data_folders)
    os.chdir("text")
    for i in range(1,3):
        subprocess.Popen([atom_path,f"data{i}.txt"])
    os.chdir(f"{desktop}/{folder}/front-end")
    init_folder(front_end_folders)
    os.chdir(f"{desktop}/{folder}/backend")
    init_folder(backend_folders)
    os.chdir("sql")
    is_folder("server_data")
    os.chdir(f"{desktop}/{folder}/Template")
    final_path=f"{desktop}/{folder}/cgi-bin/{file1}"
    subprocess.Popen([Vscode_path,final_path])

create_project(sys.argv[1],sys.argv[2],sys.argv[3])
    