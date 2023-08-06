# +-------------------------------------------------------------------------------+
#
#      Program:    setup.py
#
#      Purpose:    setup for remote open control - key enabling technology (Rocket)
#
#      Target:     Maxwell SOC on isar
#
#      Author:     Martin Shishkov
#
#      License:    GPL 3
# +-------------------------------------------------------------------------------+
import os

class Init:
    def __init__(self):
        print('Installing rocket-daisy')
        
    def get_package(self):
        linkPyPi = "https://files.pythonhosted.org/packages/cd/12/96a4937906fd4dcb92c0672bd01cad8585433b10dd2e63ced0618596f6d2/rocket-daisy-0.1rc0.tar.gz"
        rocket = "rocket-daisy-0.1rc0"
        if not os.path.isdir(rocket):
            print('downloading rocket-daisy')
            os.system("wget " + linkPyPi)
            os.system(("tar xvzf %s.tar.gz" % (rocket)))
            os.chdir(rocket)
            os.system("sudo python3 setup.py bdist")
            
            
 
 
 
i = Init()
i.get_package()    
