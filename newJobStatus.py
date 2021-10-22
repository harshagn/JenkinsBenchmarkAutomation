import sys
from jenkinsapi.jenkins import Jenkins

myUser=sys.argv[1]
myPass=sys.argv[2]
jobName=sys.argv[3]
#sFile=sys.argv[4]
jenkins_url = 'http://10.2.128.101:8585/'
server = Jenkins(jenkins_url, username = myUser, password = myPass)
job_instance = server.get_job(jobName)
running = job_instance.is_queued_or_running()

#sUp = open(sFile,"rb")
if not running:
   latestBuild = job_instance.get_last_build()
   print(latestBuild.get_status())
   #sUp.write(result)
else:
   print("BUILDING")
   #sUp.write("BUILDING\n")
#sUp.close()
