import json
from pprint import pprint


testDir = "/home/declan/Documents/code/slack expts/testdir"

testFile = "2016-12-03"

ext = ".json"

fname = testDir + "/" + testFile + ext

with open(fname, encoding='utf-8') as jsonfile:
    jsondata = json.loads(jsonfile.read())

#pprint(jsondata)

#print(jsondata[0])

[print(jd) for jd in jsondata]


testEntry = jsondata[0]
print()
print()
print(testEntry)

print(testEntry["type"])


testUser = "U1PPEPJTT"
print()
[print(jd) for jd in jsondata if jd["user"]==testUser]

print(len(jsondata))
