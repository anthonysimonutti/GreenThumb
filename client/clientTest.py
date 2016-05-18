import clientClass
import os.path
import json
import sys
import time

jsonTestData = []

if len(sys.argv) != 3:
    print "ERROR: Usage 'python clientTest.py <config.json> <testdataset.json>'"
    sys.exit(0)

jsonFileName = sys.argv[1]
jsonTestFileName = sys.argv[2]

if os.path.isfile(jsonFileName):
    print "The config file exists. Getting content..."
    config = json.load(open(jsonFileName, 'r'))
    configId = config["clientId"]
    configAddr = config["serverAddr"]
    configPort = config["serverPort"]
    configServerKey = config["serverKey"]
else:
    print "The config does not exist. Exiting."
    sys.exit(0)

if os.path.isfile(jsonTestFileName):
    print "The test data set exists. Getting content..."
    with open(jsonTestFileName) as f:
        for line in f:
            tempJson = json.loads(line)
            tempJson.update({'clientId': configId})
            jsonTestData.append(tempJson)

else:
    print "The testdataset does not exist. Exiting."
    sys.exit(0)


print "clientId:", configId
print "serverAddr:", configAddr
print "serverPort:", configPort

newconnection = clientClass.ipClient(configAddr, configPort, configServerKey)
newconnection.connect()

print len(jsonTestData)
i = 0
if newconnection.authenticate() != 1:
    for item in jsonTestData:
        try:
            newconnection.send(str(item))
            i += 1
            time.sleep(1)
        except:
            break
else:
    print "Authentication failed!"

print i

newconnection.close()
