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
        linkPyPi = "https://files.pythonhosted.org/packages/67/d8/81b4dea0c96461bb2ca8b7bfdc94f9d5eb364bac6b61cab023a2eacbd7a7/rocket-daisy-0.1b2.tar.gz"
        rocket = "rocket-daisy-0.1b2"
        if not os.path.isdir(rocket):
            print('downloading rocket-daisy')
            os.system("wget " + linkPyPi)
            os.system(("tar xvzf %s.tar.gz" % (rocket)))
            os.chdir(rocket)
            os.system("sudo python3 setup.py bdist")
            
            
 
 
 
i = Init()
i.get_package()    
