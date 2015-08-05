__author__ = 'marc'

import os
from kmls_management.models import Kml



def transfer():
    filePath = "/home/jbondia/Documentos/gsoc15/faed_management_tool/faed_management/static/kml/kmls.txt"
    serverPath = "/var/www/html"
    os.system("sshpass -p 'lqgalaxy' scp "+filePath+" lg@172.26.17.21:"+serverPath)


def a():
    # ip_server = os.popen("iFconfig getifaddr en1")
    file = open("faed_management/static/kml/kmls.txt",'w')

    for i in Kml.objects.filter(visibility=True):
        file.write("http://172.26.17.230:8000"+i.url+"\n")

