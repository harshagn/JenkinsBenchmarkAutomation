import os
import sys
import shutil
import xml.etree.ElementTree as et
import re
import requests



def text_file_to_xml(xmlFile,dFile):
    # Please keep the left parameters of text file as same as tag of xml file i.e. case sensitive.
    d={}
    # test.dat is the text file from where the script will pick the values
    #dFile is the path with name of test.dat file under Res/ folder after test*.dat file copy
    with open(dFile) as f:
        lines=f.readlines()
        tree = et.parse(xmlFile)
        root=tree.getroot()
        res = []
        for y in lines:
            res.append(re.sub('\n', '', y))
        roots=["SUTInformation","BenchmarkInformation","TunableParameters","BIOSParameters"]
        for l in roots:
            for x in root.iter(l):
                for line in res:
                    (key,val) = line.split('\=')
                    d[key] = val
                    # run.xml is the output xml file where values will be overwritten
                    try:
                        x.find(key).text = val
                    except:
                        continue
    tree.write(xmlFile)

def userMap(dict,u):
    try:
        for item in dict:
            if u==item:
                return dict[item]
    except:
        print("Invalid user is entered.. Please check and try again")

def hdconf(root_path, ext):
    dir_list =[]
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.lower().endswith(ext):
                dir_list.append(os.path.join(root, file))
    return(dir_list)
                #return(yield os.path.join(root, file))

def buildJob(auth,uri,jobNm,buildToken):
    # start the build
    start_build_url = 'http://{}@{}/job/{}/build?token={}'.format(auth, uri, jobNm, buildToken)
    requests.post(start_build_url)

def main(arg1,arg2):
    #arg1 is the user launched the jenkins job and arg2 is the path of testcases folder path
    dst=arg2
    pat = os.path.join(dst, "Res")
    fileList=""  
    auth_creds=""
    fileList=hdconf(arg2,"_"+arg1+".dat")

    credsMapper = {'Neetu':"11a9743d58ac07c23b75dbf8d77b7420a5",'prateek':"11db69de90b55689babee473fbaedd885c",
                   'jadmin':"1131e40915212a5c5e273b2cb7d492a69e",'admin':"11cace5e4fb5872a562373b7c07ffd65a3"}
    ucreds=userMap(credsMapper, arg1)
    auth_creds=arg1+":"+ucreds
    print(auth_creds)

    # job specifics
    jenkins_uri = '10.2.128.101:8585'
    job_name = 'winsTransfer' # Jenkins job name to run
    build_token = 'callCurl'
    
    for file in fileList:
        os.remove(os.path.join(pat,"test.dat"))
        shutil.copy(os.path.join(file),os.path.join(pat,"test.dat"))
        shutil.copy(os.path.join(dst,"../run-orig.xml"),os.path.join(dst,"../run.xml"))
        text_file_to_xml(os.path.join(dst,"../run.xml"), os.path.join(pat,"test.dat"))
        buildJob(auth_creds,jenkins_uri,job_name,build_token)

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])

