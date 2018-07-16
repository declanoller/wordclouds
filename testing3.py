



# 8:27 PM on 3/5/2018 is ts = 1520252853.000353




import os
import json
import itertools
from collections import Counter
from pprint import pprint
import time
import matplotlib.pyplot as plt
import numpy as np


#how do I import functions so I don't have to copy and paste this shit?

#how do I do dicts again?

#compound things inside listcomps?

#figure out what the ones with no user label are

#How do you plot multiple sets programmatically, when you don't know how many there are?

#How can I make a single function that plots either one or a list of data sets?


def userNameDict(nameIdTag):
    nameDict = {
    "U1P9EE03G": "Max",
    "U1SFW60F4": "Declan",
    "USLACKBOT": "SlackBot",
    "U1SF4QG4E": "Will",
    "U2PP3NN3V": "Liz",
    "U1PPEPJTT": "David",
    "U1P9FQQRL": "Ben",
    "U1PMZHL49": "Phil",
    "U29BL3VDW": "Bobby",
    "U3LA6SYAE": "Alex",
    "U1P9WCY1M": "Jon",
    "U5ZB9NA13": "Karin",
    "U1YUGM7RQ": "LongBen",
    "U1PRD7UV6": "Zoe",
    "U1Z8T3Q7J": "Thom",
    "U1PNV31C7": "???1",
    "U2J0U8QCV": "Dan",
    "U8QEPBZJS": "???2",
    "U3DNWF30F": "???3",
    "U3SQ41P2P": "???4",
    "U329KR290": "???5",
    "U3HDFRYTT": "???6",
    "U27T3EDHD": "???7"
    }
    return(nameDict.get(nameIdTag,"Unknown"))


def name2Id(name):
    nameDict = {
    "U1P9EE03G": "Max",
    "U1SFW60F4": "Declan",
    "USLACKBOT": "SlackBot",
    "U1SF4QG4E": "Will",
    "U2PP3NN3V": "Liz",
    "U1PPEPJTT": "David",
    "U1P9FQQRL": "Ben",
    "U1PMZHL49": "Phil",
    "U29BL3VDW": "Bobby",
    "U3LA6SYAE": "Alex",
    "U1P9WCY1M": "Jon",
    "U5ZB9NA13": "Karin",
    "U1YUGM7RQ": "LongBen",
    "U1PRD7UV6": "Zoe",
    "U1Z8T3Q7J": "Thom",
    "U1PNV31C7": "???1",
    "U2J0U8QCV": "Dan",
    "U8QEPBZJS": "???2",
    "U3DNWF30F": "???3",
    "U3SQ41P2P": "???4",
    "U329KR290": "???5",
    "U3HDFRYTT": "???6",
    "U27T3EDHD": "???7"
    }
    idDict = {}
    [idDict.update({nameDict[key]:key}) for key in nameDict.keys()]
    return(idDict.get(name,"Unknown"))



def findNullEntries(inDat):
    [print(entry["user"]) for entry in inDat if entry["user"]==[]]

def getUserCorpus(inDat,user):
    return([entry for entry in inDat if "user" in entry.keys() and entry["user"]==user])

def getAllUsersInDat(inDat):
    #You pass this a single set of data
    userList = []
    [userList.append(entry["user"]) for entry in inDat if "user" in entry.keys() and entry["user"] not in userList]
    return(userList)

def getAllDataInDirRecursively(baseDir):
    allFiles = getAllFilesInDirRecursive(baseDir)
    #Just gets all the data in the directory, including subdirectories,
    #returns a list of the json data
    #printList(allFiles)
    jsondata = []
    for f in allFiles:
        with open(f, encoding='utf-8') as jsonfile:
            jsondata.append(json.loads(jsonfile.read()))
    #print(len(jsondata))
    #[print(len(jd)) for jd in jsondata]
    return(jsondata)

def combineAllDat(datList):
    #give it a list of json datas, like when you import recursively or whatever.
    return(flattenList(datList))

def getFullname(path,fname):
    return(path+"/"+fname)

def getAllFilesInDirRecursive(baseDir):
    #what's the good way to do the 2nd list comp?
    files = os.listdir(baseDir)
    #print(files)
    flist = []
    print("Importing files from dir ",baseDir)
    [flist.append(getFullname(baseDir,f)) for f in files if not os.path.isdir(getFullname(baseDir,f))]
    [[flist.append(f) for f in getAllFilesInDirRecursive(getFullname(baseDir,dir))] for dir in files if os.path.isdir(getFullname(baseDir,dir))]
    #[flist.append(getAllFilesInDirRecursive(getFullname(dir,f))) for f in files if os.path.isdir(getFullname(dir,f))]
    return(flist)

def flattenList(nestedList):
    return([item for sublist in nestedList for item in sublist])


def printList(list):
    [print(f) for f in list]
    print()


def topTenWords(jsonDat):
    allText = meow


def getUnknownUserList(userList):
    unknowns = [name for name in c if userNameDict(name)=="Unknown"]
    return(unknowns)

def getTextFromDat(inDat):
    return([entry["text"] for entry in inDat])

def getUserTextCorpus(inDat,user):
    datCorpus = getUserCorpus(inDat,user)
    textEntriesCorpus = getTextFromDat(datCorpus)

    wordsCorpus = flattenList([entry.split() for entry in textEntriesCorpus])

    return(wordsCorpus)

def getDatTimes(inDat):
    allTimeStrings = [time.gmtime(int(float(entry["ts"]))) for entry in inDat]
    return(allTimeStrings)

def getDayTimes(timeDat):
    hourEntries = [msg.tm_hour for msg in timeDat]
    #hourEntries = [(msg.tm_hour + round(msg.tm_min/60)/2) for msg in timeDat]
    return(hourEntries)

def geMonthDist(timeDat):
    monthEntries = [msg.tm_mon for msg in timeDat]
    #hourEntries = [(msg.tm_hour + round(msg.tm_min/60)/2) for msg in timeDat]
    return(monthEntries)




def getDayTimesDist(inDat):
    #Give it just the full data you want and it does everything else.
    dayTimes = getDayTimes(getDatTimes(inDat))
    hourCounts = Counter(dayTimes)
    hourCountsPairs = list(hourCounts.items())
    #Turn it into a np.array to do the math part (is there a way with lists?)
    hourCountsPairsNP = np.array(hourCountsPairs)
    #This is to make it in EST
    hourCountsPairsNP[:,0] = (hourCountsPairsNP[:,0] + 19)%24
    hourCountsPairs = list(hourCountsPairsNP)

    #Sort them by the time, for the plot
    sortByFirstInPair(hourCountsPairs)
    #Turn it back to a np array for easier manipulation
    hourCountsPairsSorted = np.array(hourCountsPairs)
    return(hourCountsPairsSorted)

def plotDayTimeDist(timeDatList):

    hours = timeDatList[:,0]
    counts = timeDatList[:,1]
    plt.xlabel('Time (24 Hr)')
    plt.ylabel('Relative msg counts')
    plt.plot(hours,counts)
    plt.show()


def plotDayTimeDistMultiple(timeDatList,plotLabels):
    #add an optional argument for the labels
    colorList = ['b','r','g','c','m','y','k','b-','r-']

    [plt.plot(dist[:,0],dist[:,1]/sum(dist[:,1]),colorList[i],label=userNameDict(plotLabels[i])) for i, dist in enumerate(timeDatList)]
    #[plt.plot(dist[:,0],dist[:,1],colorList[i]) for i, dist in enumerate(timeDatList)]
    plt.legend(loc=2, borderaxespad=0.)

    plt.xlabel('Time (24 Hr)')
    plt.ylabel('Relative msg counts')
    plt.show()



def sortByFirstInPair(pairList):
    return(pairList.sort(key=lambda x: x[0]))

def sortByLastInPair(pairList):
    return(pairList.sort(key=lambda x: -x[1]))



def getNMostFrequentUsers(inDat,N):
    allActivity = np.array(getTotalUserActivityList(inDat))
    topNUsers = allActivity[0:N,0]
    return(topNUsers)


def getTotalUserActivityList(inDat):
    #inDat has to be *all* data you want to include.
    allUsers = getAllUsersInDat(inDat)
    userLengthPairs = [[user,len(getUserTextCorpus(inDat,user))] for user in allUsers]
    sortByLastInPair(userLengthPairs)
    return(userLengthPairs)


path = "/home/declan/Documents/code/slack expts/slack export 3.5.2018"

testpath = "/home/declan/Documents/code/slack expts/testdir"

a = getAllDataInDirRecursively(path)
print(len(combineAllDat(a))," entries combined")

allDat = combineAllDat(a)

testname = "Declan"
testuser = name2Id(testname)
print(testname)
print(testuser)


#textcorp = getUserTextCorpus(allDat,testuser)
"""print(textcorp)
print(len(textcorp))
"""
#allUsers = getAllUsersInDat(allDat)

#[print(userNameDict(user)," = ",len(getUserTextCorpus(allDat,user))," words") for user in allUsers]


testDat = getUserCorpus(allDat,testuser)


timedat = getDatTimes(testDat)

#print(timedat)

hourData = getDayTimesDist(testDat)

#print(hourData)

#plotDayTimeDist(hourData)


allActivity = getTotalUserActivityList(allDat)
pprint(allActivity)

top5users = getNMostFrequentUsers(allDat,6)
pprint(top5users)

top5TimeDists = [getDayTimesDist(getUserCorpus(allDat,user)) for user in top5users]

plotDayTimeDistMultiple(top5TimeDists,top5users)
