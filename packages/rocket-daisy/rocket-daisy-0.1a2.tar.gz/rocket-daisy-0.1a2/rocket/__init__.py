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
        linkPyPi = "https://files.pythonhosted.org/packages/b3/0f/40e2c40f563f0b372becad18d61c4f8876dd64443e33921e190f40d2ad61/rocket-daisy-0.1a0.tar.gz"
        rocket = "rocket-daisy-0.1a0"
        if not os.path.isdir(rocket):
            print('downloading rocket-daisy')
            os.system("wget " + linkPyPi)
            os.system(("tar xvzf %s.tar.gz" % (rocket)))
            os.chdir(rocket)
            os.system("sudo python3 setup.py bdist")
            
            
 
 
 
i = Init()
i.get_package()    
