import os
import json
import itertools
from collections import Counter
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
from copy import copy
import string

class SlackTools:


    def produceManyWordClouds(self,userList):
        path = '/home/declan/Documents/code/data/slack_export_7.16.2018'

        a = self.getAllDataInDirRecursively(path)
        #print(len(self.combineAllDat(a))," entries combined")
        allDat = self.combineAllDat(a)

        #users = ['Declan','Ben','Phil','David','Liz','Max','Will','Bobby']
        #users = ['David']
        total_corpus = []
        for user in userList:
            total_corpus = total_corpus+self.getUserTextCorpus(allDat,self.name2Id(user))

        total_corpus = map(str.lower,total_corpus)

        counts = Counter(total_corpus).most_common(400)
        most_common_words = [item[0] for item in counts]
        #print(counts)

        [self.produceWordCloud(allDat,user,removeList=most_common_words) for user in userList]


    def produceUniqueWordClouds(self,users):

        path = '/home/declan/Documents/code/data/slack_export_7.16.2018'

        a = self.getAllDataInDirRecursively(path)
        #print(len(self.combineAllDat(a))," entries combined")
        allDat = self.combineAllDat(a)

        N_unique = 15

        users_word_rankings = {}
        users_corpuses = {}

        translator = str.maketrans('', '', string.punctuation)
        num_str = [str(i) for i in range(10)]


        #preparing all the corpuses
        for user in users:
            #get user ID and corpus
            testuser = self.name2Id(user)
            textcorp = self.getUserTextCorpus(allDat,testuser)

            #turn the whole corpus to lowercase
            textcorp = map(str.lower,textcorp)
            #get rid of punctuation
            textcorp = map(lambda str: str.translate(translator),textcorp)
            #get rid of bobby's weird punctuation
            textcorp = list(map(lambda str: str.replace('’',''),textcorp))
            #get rid of single digit numbers
            textcorp = [word for word in textcorp if word not in num_str]
            #get rid of user's own name
            textcorp = [word for word in textcorp if word!=testuser.lower()]

            #textcorp = self.removeListFromCorpus(textcorp,self.getNaughtyWords())
            textcorp = self.removeListFromCorpus(textcorp,['youve','hour','minutes','one','two','three','used'])

            #sort by most commonly used
            counts = Counter(textcorp).most_common(600)
            most_common_words = [item[0] for item in counts]
            #add to user:sorted corpus dict
            users_word_rankings[user] = most_common_words
            users_corpuses[user] = textcorp

            #print('\n{}\'s most common words:\n'.format(user))
            #[print(word) for word in most_common_words[:2*N_unique]]
            #print()



        #making the corpuses more personalized
        allowed_others = 0

        for user in users:
            print('\n\ngetting unique words for',user)

            other_users = copy(users)
            other_users.remove(user)
            #print('other users:',other_users)
            index = 0
            while index<=N_unique:
                others_with_word = 0
                cur_word = users_word_rankings[user][index]
                #print('\ncur word is \'{}\''.format(cur_word))

                for other_user in other_users:
                    if cur_word in users_word_rankings[other_user][:N_unique]:
                        #print('{} also has this word'.format(other_user))
                        others_with_word += 1

                if others_with_word>allowed_others:
                    #print('removing \'{}\' from all users'.format(cur_word))
                    for tempuser in users:
                        if cur_word in users_word_rankings[tempuser]:
                            #print('removing from ',tempuser)
                            users_word_rankings[tempuser].remove(cur_word)
                    index = 0
                else:
                    index += 1

            print('\n\nTop {} unique words for {} at this point'.format(N_unique,user))
            [print('{}. {}'.format(i,word)) for i,word in enumerate(users_word_rankings[user][:N_unique])]

        print('\n\n\n*****************************************************\n\n\n')


        #Get remaining words and remove other words
        for user in users:
            users_corpuses[user] = self.keepListInCorpus(users_corpuses[user],users_word_rankings[user])
            users_word_rankings[user] = self.keepListInCorpus(users_word_rankings[user],users_word_rankings[user])



        for user in users:
            print('\n\nTop {} unique words for {}'.format(N_unique,user))
            [print('{}. {}'.format(i,word)) for i,word in enumerate(users_word_rankings[user][:N_unique])]

            self.outputWordCloud(user,users_corpuses[user],'personalized_naughty')






    def getNaughtyWords(self):
        return(
        ['fuck','fucked','shit','shitty','shitted','shat',
        'cum','ass','jizz','cunt','suck','cuck','sex',
        'cock','penis','pussy','retard','dick',
        'balls','fart','asshole','butthole','rape',
        'shitting']
        )

    def outputWordCloud(self,user,corpus,other_label=''):

        outfile_stem = user+'_corpus_'+other_label
        outfile_text = outfile_stem+'.txt'
        outfile_img = outfile_stem+'.png'
        f = open(outfile_text,'w')
        f.close()
        f = open(outfile_text,'a')
        for word in corpus:
            f.write(word)
            f.write('\n')
        f.close()

        wordcloud_cmd = 'wordcloud_cli.py --text {} --image {} --height 500 --width 800'.format(outfile_text,outfile_img)
        os.system(wordcloud_cmd)

    def produceWordCloud(self,allDat,user,removeList=[]):
        testuser = self.name2Id(user)
        print(user)
        print(testuser)

        textcorp = self.getUserTextCorpus(allDat,testuser)
        textcorp = map(str.lower,textcorp)

        remove_words = []
        remove_words = ['yeah','one','uploaded','fpff.slack.com','http','think','thing','file','U1','U2','guy','look']+removeList

        remove_words = remove_words + self.getNaughtyWords()

        remove_words = map(str.lower,remove_words)

        for word in remove_words:
            textcorp = self.removeFromCorpus(textcorp,word)

        self.outputWordCloud(user,textcorp,'removedcommon')


    def removeListFromCorpus(self,corpus,remove_list):
        newlist = [word for word in corpus if word not in remove_list]
        return(newlist)

    def keepListInCorpus(self,corpus,keep_list):
        newlist = [word for word in corpus if word in keep_list]
        return(newlist)

    def removeFromCorpus(self,list,value):
        newlist = [word for word in list if value not in word]
        return(newlist)

    def userNameDict(self,nameIdTag):
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


    def name2Id(self,name):
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



    def findNullEntries(self,inDat):
        [print(entry["user"]) for entry in inDat if entry["user"]==[]]

    def getUserCorpus(self,inDat,user):
        return([entry for entry in inDat if "user" in entry.keys() and entry["user"]==user])

    def getAllUsersInDat(self,inDat):
        #You pass this a single set of data
        userList = []
        [userList.append(entry["user"]) for entry in inDat if "user" in entry.keys() and entry["user"] not in userList]
        return(userList)

    def getAllDataInDirRecursively(self,baseDir):
        allFiles = self.getAllFilesInDirRecursive(baseDir)
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

    def combineAllDat(self,datList):
        #give it a list of json datas, like when you import recursively or whatever.
        return(self.flattenList(datList))

    def getFullname(self,path,fname):
        return(path+"/"+fname)

    def getAllFilesInDirRecursive(self,baseDir):
        #what's the good way to do the 2nd list comp?
        files = os.listdir(baseDir)
        #print(files)
        flist = []
        #print("Importing files from dir ",baseDir)
        [flist.append(self.getFullname(baseDir,f)) for f in files if not os.path.isdir(self.getFullname(baseDir,f))]
        [[flist.append(f) for f in self.getAllFilesInDirRecursive(self.getFullname(baseDir,dir))] for dir in files if os.path.isdir(self.getFullname(baseDir,dir))]
        #[flist.append(getAllFilesInDirRecursive(getFullname(dir,f))) for f in files if os.path.isdir(getFullname(dir,f))]
        return(flist)

    def flattenList(self,nestedList):
        return([item for sublist in nestedList for item in sublist])


    def printList(self,list):
        [print(f) for f in list]
        print()


    def topTenWords(self,jsonDat):
        allText = meow


    def getUnknownUserList(self,userList):
        unknowns = [name for name in c if self.userNameDict(name)=="Unknown"]
        return(unknowns)

    def getTextFromDat(self,inDat):
        return([entry["text"] for entry in inDat])

    def getUserTextCorpus(self,inDat,user):
        datCorpus = self.getUserCorpus(inDat,user)
        textEntriesCorpus = self.getTextFromDat(datCorpus)

        wordsCorpus = self.flattenList([entry.split() for entry in textEntriesCorpus])

        return(wordsCorpus)


    def getTotalUserActivityList(self,inDat):
        #inDat has to be *all* data you want to include.
        allUsers = self.getAllUsersInDat(inDat)
        userLengthPairs = [[user,len(self.getUserTextCorpus(inDat,user))] for user in allUsers]
        self.sortByLastInPair(userLengthPairs)
        return(userLengthPairs)

    def getUserActivityListForUserList(self,inDat,userList):
        userLengthPairs = [[user,len(self.getUserTextCorpus(inDat,user))] for user in userList]
        self.sortByLastInPair(userLengthPairs)
        return(userLengthPairs)

    def activityBarPlot(self,userActivityPairList):
        print(userActivityPairList)
        objects = [self.userNameDict(id) for id in np.array(userActivityPairList)[:,0]]
        x_pos = list(np.arange(len(userActivityPairList)))
        performance = [int(n) for n in np.array(userActivityPairList)[:,1]]

        plt.bar(x_pos, performance, align='center', alpha=0.5)
        plt.xticks(x_pos, objects)
        plt.xlabel('User')
        plt.ylabel('# of messages')
        plt.title('User activity')
        plt.show()


    def activityPieChart(self,userActivityPairList):
        labels = [self.userNameDict(id) for id in np.array(userActivityPairList)[:,0]]
        sizes = [int(n) for n in np.array(userActivityPairList)[:,1]]
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
        explode = np.ones(len(sizes))  # explode 1st slice

        # Plot
        plt.pie(sizes, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=0)

        plt.axis('equal')
        plt.show()


    def sortByLastInPair(self,pairList):
        return(pairList.sort(key=lambda x: -x[1]))


    def getNMostFrequentUsers(self,inDat,N):
        allActivity = np.array(self.getTotalUserActivityList(inDat))
        topNUsers = allActivity[0:N,0]
        return(topNUsers)
