__author__ = 'marc'

import os

filePath = "/static/kml/kmls.txt"
serverPath = "/var/www/html"
os.system("sshpass -p 'lqgalaxy' scp "+filePath+"lg@172.26.17.21:"+serverPath)
