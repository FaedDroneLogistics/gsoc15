__author__ = 'marc'

import os
from kmls_management.models import Kml
import subprocess


def syncKmlsToGalaxy():
    filePath = "/tmp/kml/kmls.txt"
    serverPath = "/var/www/html"
    os.system("sshpass -p 'lqgalaxy' scp "+filePath+" lg@172.26.17.21:"+serverPath)



def a():
    p = subprocess.Popen("ifconfig getifaddr en5", shell=True, stdout=subprocess.PIPE)
    ip_server = p.communicate()[0]
    file = open("faed_management/static/kml/kmls.txt",'w')

    for i in Kml.objects.filter(visibility=True):
        file.write("http://172.26.17.230:8000"+i.url+"\n")


def syncKmlsFile():

    p = subprocess.Popen("ipconfig getifaddr en5", shell=True, stdout=subprocess.PIPE)
    ip_server = p.communicate()[0]

    os.system("rm /tmp/kml/kmls.txt")
    os.system("touch /tmp/kml/kmls.txt")
    file = open("/tmp/kml/kmls.txt",'w')

    for i in Kml.objects.filter(visibility=True):
        file.write("http://"+ str(ip_server)[0:(len(ip_server)-1)]+":8000/static/kml/"+i.name+"\n")
    print 'Write'
    file.write("http://172.26.17.230:8000/static/kml/ex_from_earth.kml\n")
    print 'Written'

    file.close()
