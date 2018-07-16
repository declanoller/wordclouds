

exit(0)

path = '/home/declan/Documents/code/data/slack export 3.5.2018'

testpath = "/home/declan/Documents/code/slack expts/testdir"

a = getAllDataInDirRecursively(path)
print(len(combineAllDat(a))," entries combined")

allDat = combineAllDat(a)

"""
c = getAllUsersInDat(b)
print(c)

[print(name," = ",userNameDict(name)) for name in c]

unknownusers = getUnknownUserList(c)
"""

"""print(unknownusers)
print(unknownusers[0])

testUK = getUserCorpus(b,unknownusers[0])
pprint(getTextFromDat(testUK))
print()
print(unknownusers[0])"""

testuser = name2Id("Declan")
print("Declan")
print(testuser)


textcorp = getUserTextCorpus(allDat,testuser)
"""print(textcorp)
print(len(textcorp))
"""

#print(textcorp)

outfile = 'declan_corpus.txt'
f = open(outfile,'w')
f.close()
f = open(outfile,'a')
for word in textcorp:
    f.write(word)
    f.write('\n')

f.close()

exit(0)

allUsers = getAllUsersInDat(allDat)

[print(userNameDict(user)," = ",len(getUserTextCorpus(allDat,user))," words") for user in allUsers]

usersActivity = getUserActivityListForUserList(allDat,getNMostFrequentUsers(allDat,10))
activityPieChart(usersActivity)
