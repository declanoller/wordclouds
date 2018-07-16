import json
from pprint import pprint
from collections import Counter


def removeCommonWords(counts):
    commonWords = ["the","is","not","a","an","to","it","of","too","I","at","/","in","it's","into"]
    for w in commonWords:
        del counts[w]
    #[del counts[w] for w in commonWords]
    return counts

testDir = "/home/declan/Documents/code/slack expts/testdir"

testFile = "2016-12-03"

ext = ".json"

fname = testDir + "/" + testFile + ext

with open(fname, encoding='utf-8') as jsonfile:
    jsondata = json.loads(jsonfile.read())

#pprint(jsondata)

#print(jsondata[0])

#[print(jd) for jd in jsondata]


testEntry = jsondata[0]
print()
print()
#print(testEntry)

#print(testEntry["type"])


testUser = "U1PPEPJTT"
print()
userText = [jd["text"].split() for jd in jsondata if jd["user"]==testUser and jd["type"]=="message"]
userText = [item for items in userText for item in items]

pprint(userText)

counts = Counter(userText)
print(counts)
counts = removeCommonWords(counts)
pprint(counts)
