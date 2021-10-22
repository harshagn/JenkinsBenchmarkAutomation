# Import Module
import requests, time
import sys
  
# URL to be called as argument to the program here
urlPath = sys.argv[1]

r = requests.post(urlPath, data={"ts":time.time()})
print(r.status_code)
print(r.content)

  
curl -X POST http://jenkins-url:8080/job/<job-name>/build --user <username>:<password> -H 'Jenkins-Crumb: 0db38413bd7ec9e98974f5213f7ead8b'

curl -v -X GET http://10.2.128.101:8080/crumbIssuer/api/json --user jadmin:113a50f588f73d4d8d30ec26445187a648 -H 'Jenkins-Crumb: ac15f33e85c027a23fa9f0d42e074fc79b268740c0ae16b861c54b1c7afb81ee'

http://10.2.128.101:8080/job/testDest/build?token=callCurl

soln:
