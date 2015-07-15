__author__ = 'marc'

import os
from kmls_management.models import Kml



def transfer():
    filePath = "/static/kml/kmls.txt"
    serverPath = "/var/www/html"
    os.system("sshpass -p 'lqgalaxy' scp "+filePath+"lg@172.26.17.21:"+serverPath)


def a():
    ip_server=os.popen("ipconfig getifaddr en1")
    file = open("faed_management/static/kml/kmls.txt",'w')

    for i in Kml.objects.filter(visibility=True):
        file.write("http://172.16.116.32:8000/"+i.url+"\n")

