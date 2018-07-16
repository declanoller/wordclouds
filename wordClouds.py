from commonFunctions import SlackTools


st = SlackTools()

path = '/home/declan/Documents/code/data/slack export 3.5.2018'

a = st.getAllDataInDirRecursively(path)
#print(len(st.combineAllDat(a))," entries combined")
allDat = st.combineAllDat(a)

users = ['Declan','Ben','Phil','David','Liz','Max','Will','Bobby']
#users = ['David']
#users = ['David','Ben']

#st.produceManyWordClouds(users)

#[st.produceWordCloud(allDat,user) for user in users]

st.produceUniqueWordClouds(users)
















#
