import os
import shutil
from os import path
search_path= os.path.dirname('\\python\\res\\')
i=0
src='D:\\Users\\Harsha\\JenkinsAutomation\\Input\\'
dst='D:\\Users\\Harsha\\JenkinsAutomation\\Input\\Res'
dst1="D:\\Users\\Harsha\\JenkinsAutomation\\completedFiles\\"
for root,dir, files in os.walk(dst):
        for name in files:
            if name.endswith('.dat'):
               os.remove(os.path.join(dst,name))
for file in os.listdir(src):
        if file.endswith('.dat'):
            shutil.copy(os.path.join(src,file),dst)
for x in os.listdir(dst):
    os.rename(dst + '\\' + x, dst + '\\'+"test"+str(i)+'.dat')
    i+=1
completedFiles=[i for i in os.listdir(search_path) if i.startswith("test") and path.isfile(path.join(dst,i))]
for f in files:
    shutil.move(path.join(dst,f), os.path.join(dst1,f))