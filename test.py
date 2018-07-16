from commonFunctions import SlackTools
from collections import Counter

st = SlackTools()


#users = ['Declan','Ben','Phil','David','Liz','Max','Will','Bobby']
users = ['David','Ben']

st.produceManyWordClouds(users)
