from PyQt5 import QtWidgets, QtGui, QtCore
import datetime

from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLabel

#import fbs_runtime.application_context.PyQt5
from fbs_runtime import FbsError
import fbs_runtime

import sys, os


def main():
    

    from MJOLNIRGui.MJOLNIR_GUI import MJOLNIRMainWindow,updateSplash
    #os.chdir(os.path.abspath(os.path.dirname(__file__)))
        
    
    
    
    from fbs_runtime.application_context.PyQt5 import ApplicationContext, \
        cached_property
    
    
    class AppContext(ApplicationContext):
        def __init__(self,*args,**kwargs):
            super().__init__(*args,**kwargs)
            self.splash = QtWidgets.QSplashScreen(QtGui.QPixmap(self.get_resource('splash.png')))                                    
            
            self.splash.show()
            
            self.timer = QtCore.QTimer() 
            
            updateInterval = 400 # ms
            originalTime = datetime.datetime.now()
            
            updater = lambda:updateSplash(self.splash,originalTime=originalTime,updateInterval=updateInterval)
            updater()
            
            
            self.timer.timeout.connect(updater) 
            self.timer.setInterval(updateInterval)
            self.timer.start()
            QtWidgets.QApplication.processEvents()
    
            
    
        def run(self):
            
            QtWidgets.QApplication.processEvents()
            self.splash.finish(self.main_window)
            self.main_window.show()
            
            return self.app.exec_()
    
        @cached_property
        def main_window(self):
            QtWidgets.QApplication.processEvents()
            res = MJOLNIRMainWindow(self)
            self.timer.stop()
            return res # Pass context to the window.
    try:
        run(appctxt = AppContext())
    except FbsError:
        renamingInFBS() 
        completionScreen()
    
    

def run(appctxt):
           # 1. Instantiate ApplicationContext
    exit_code = appctxt.run()
    sys.exit(exit_code)

def renamingInFBS():
    file = fbs_runtime.__file__.replace('__init__','_source')
    
    with open(file,'r') as f:
            lines = f.readlines()
    saveLines = []
    for line in lines:
        if line.find("if (result / 'src' / 'main' / 'python').is_dir()")>-1:
            line = "        if (result / 'src' / 'main' / 'python').is_dir() or (result / 'MJOLNIRGui').is_dir():\n"
        elif line.find("src/main/")>-1:
            line = line.replace("src/main/","MJOLNIRGui/")
        elif line.find("'src/build/settings/%s.json'")>-1:
            line = line.replace("src/build/settings","settings")
        saveLines.append(line)
            
    with open(file,'w') as f:
        f.write(''.join(saveLines))

def completionScreen():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle('MJOLNIRGui')
    window.resize(250, 150)
    label = QLabel('MJOLNIRGui has now set up FBS correctly.\nPlease rerun MJOLNIRGui')
    window.setCentralWidget(label)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
    
        