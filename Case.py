import os
import pathlib as Path
import re
import shutil
import sys
import time
import xml.etree.ElementTree as et
import requests
from jenkinsapi.jenkins import Jenkins


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
    print ("Inside hdconf")
    print (root_path, ext)
    dir_list =[]
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.lower().endswith(ext.lower()):
                dir_list.append(os.path.join(root, file))
    return(dir_list)
                #return(yield os.path.join(root, file))

def buildStat(myUser,myPass,jobName,uri,wtime):
    myUser=sys.argv[1]
    myPass=sys.argv[2]
    jobName=sys.argv[3]
    jenkins_url = 'http://10.2.128.101:8585/'
    server = Jenkins(jenkins_url, username = myUser, password = myPass)

    job_instance = server.get_job(jobName)
    running = job_instance.is_queued_or_running()

    if not running:
       time.sleep(wtime)
       latestBuild = job_instance.get_last_build()
       print(latestBuild.get_status())
    else:
       print("BUILDING")

def getMetric(tfile):
    with open(tfile, "r") as file:
        rows = ( line.split('\=') for line in file)
        dict = { row[0]:row[1] for row in rows }
        for item in dict:
            if item=='Benchmark':
                return dict[item]


def main(arg1,arg2):
    #arg1 is the user launched the jenkins job and arg2 is the path of testcases folder path
    ucreds=""
    fileList=""
    QUEUE_POLL_INTERVAL =  1
    JOB_POLL_INTERVAL = 300
    OVERALL_TIMEOUT = 3600 # 1 hour

    # job specifics
    jenkins_uri = '10.2.128.101:8585'
    job_name = 'winsTransfer' # Jenkins job name to run
    build_token = 'callCurl'
    dst=arg2
    stFile="" #string to store path of individual user job status
    stPath="C:\\Users\\Harsha\\.jenkins\\users\\"
    credsMapper = {'Neetu':"11a9743d58ac07c23b75dbf8d77b7420a5",'Prateek':"11db69de90b55689babee473fbaedd885c",
                   'jadmin':"1131e40915212a5c5e273b2cb7d492a69e"}
    ucreds=userMap(credsMapper, arg1)
    #print(ucreds)
    fileList=hdconf(arg2,"_"+arg1+".dat")
    print (fileList)
    auth_creds=arg1+":"+ucreds
    metric=""
    print(auth_creds)
    #print(fileList)

    pat = os.path.join(dst, "Res")
    FILE=os.path.join(pat, "test.dat")
    for file in fileList:
        if os.path.exists(FILE):
            os.remove(os.path.join(pat, "test.dat"))
            os.remove(os.path.join(dst, "..\\run.xml"))
            os.remove('C:\\Users\\Harsha\\.jenkins\\workspace\\startPipeline\\Automation_Kit_Ver1.2-JenkinsAutomation\\benchmark-automation-master\\run.xml')
        else:
            # file does not exists
            pass
        shutil.copy(os.path.join(file),os.path.join(pat,"test.dat"))
        shutil.copy(os.path.join(dst,"..\\run-orig.xml"),os.path.join(dst,"..\\run.xml"))
        text_file_to_xml(os.path.join(dst,"..\\run.xml"), os.path.join(pat,"test.dat"))
        shutil.copy(os.path.join(dst,"..\\run.xml"),"C:\\Users\\Harsha\\.jenkins\\workspace\\startPipeline\\Automation_Kit_Ver1.2-JenkinsAutomation\\benchmark-automation-master\\run.xml")
        # print (file)
        # print (auth_creds,jenkins_uri,job_name,build_token)
        #call Jenkins job using requests url
        # start the build
        start_build_url = r'http://{}@{}/job/{}/build?token={}'.format(auth_creds,jenkins_uri,job_name,build_token)
        requests.post(start_build_url)
        
        #get the metric from test.dat and check job status in a for loop with appropriate wait times at each level
        metric=getMetric(os.path.join(pat,"test.dat"))

        #program to store files in separate folders depending on the job status - success/failure/aborted stage
       
        #files to store job status info in respective user folder
        stFile=os.path.join(stPath+arg1+"_*\\","statusJob.txt")
        sUp = open(stFile,"w")
         
        while True:
            #get the status of the job started
            status= buildStat(arg1,"cpu2017",metric+"Job",jenkins_uri,QUEUE_POLL_INTERVAL)
            sUp.write(status)
            sUp.close()
            sDn = open(stFile,"r")
            start_epoch = int(time.time())
            print("current job {} status is: {}".format(file,status))
           
            #program section to store files in separate folders depending on the job status - success/failure/aborted stage
            if "BUILDING"==sDn:
                time.sleep(JOB_POLL_INTERVAL)
                f="processedFiles"
                shutil.move(file, os.path.join(dst,f))
                #Move current file test_*.dat to processedFiles folder
                continue
            elif "SUCCESS"==sDn:
                f="completeFiles"
                shutil.move(os.path.join("processedFiles",file),os.path.join(dst,f))
                #Move current file test_*.dat to completeFiles folder
                print("Job {} is successfully completed \n".format(file))
                break
            elif "FAILURE"==sDn:
                f="failedFiles"
                shutil.move(os.path.join("processedFiles",file), os.path.join(dst,f))
                #Move current file test_*.dat to failedFiles folder
                print("Job {} has failed\n".format(file))
                break
            elif "ABORTED"==sDn:
                f="abortedFiles"
                shutil.move(os.path.join("processedFiles",file), os.path.join(dst,f))
                #Move current file test_*.dat to abortedFiles folder
                print("Job {} is Aborted\n".format(file))
                break
            else:
                print("No more jenkins job pending.....\n")
           
            cur_epoch = int(time.time())
            if (cur_epoch - start_epoch) > OVERALL_TIMEOUT:
       	        print("{}: No Job status before timeout of {} secs".format(OVERALL_TIMEOUT))
                sys.exit(1)
        sDn.close()

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])
