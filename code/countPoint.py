# -*- coding: utf-8 -*-

import json
from pprint import pprint
import re
from ArticutAPI import ArticutAPI
from requests import post

def articutLogIn(inforpath):
	userDICT = json2DictReader(inforpath)
	username = userDICT["username"]
	apikey = userDICT["apikey"]
	articut = ArticutAPI.Articut( username, apikey)
	return articut

def json2DictReader(jsonFilePath):
	with open(jsonFilePath, encoding = "utf-8-sig") as f :
		returnDICT = f.read()
	returnDICT = json.loads(returnDICT)
	return returnDICT

def txtReader(txtFilePath):
	with open(txtFilePath, encoding = "utf-8") as f :
		returnTXT = f.read()
	return returnTXT

def easy2LIST(inputSTR):
    inputLIST = inputSTR.split("\n")
    for i in inputLIST:
        if i == "":
            inputLIST.remove(i)
    return inputLIST

def talk2LIST(inputLIST):
    '''將時間,名字,內容切開'''
    for i in range(len(inputLIST)):
        if re.match(r"[0-9]+(:)+[0-9]", inputLIST[i]) or re.match(r"(下午)+[0-9]+(:)+[0-9]", inputLIST[i]) or re.match(r"(上午)+[0-9]+(:)+[0-9]", inputLIST[i]):
            inputLIST[i] = inputLIST[i].split("\t")
    #pprint(inputLIST)
    return inputLIST
    
def talk2LIST2(inputLIST):
    '''把沒有對話內容的項去掉,如果有內容被切開了就黏回去'''
    talkLIST = []
    
    for i in range(len(inputLIST)):
        if type(inputLIST[i]).__name__ == "list":
            if len(inputLIST[i]) > 2:
                thing = inputLIST[i][2:]
                thing = " ".join(thing)
                tempLIST = inputLIST[i][0:2]
                tempLIST.append(thing)
                talkLIST.append(tempLIST)
    #pprint(talkLIST)
    return talkLIST

def talk2CutList(inputLIST, nlptool):
    '''用 articut lv2 將內容斷詞'''
    talkLISTlv2 = []
        
    for i in range(len(inputLIST)):
        tempLIST = inputLIST[i]
        resultDICT = articut.parse(tempLIST[2], level = "lv2", userDefinedDictFILE = "define.json")
        tempLIST[2] = resultDICT["result_segmentation"]
        talkLISTlv2.append(tempLIST)
    return talkLISTlv2


def countPoint(talkLIST):
    p = 0
    talkListAll = []
    
    for i in range(len(talkLIST)):
        tempTalk = talkLIST[i][2]
        tempLIST = tempTalk.split("/")
        talkListAll += tempLIST
    
    boringDICT = json2DictReader("boring.json")
    
    for i in talkListAll:
        if boringDICT.get(i) == None:
            continue
        else:
            p += 1
    p = p / len(talkLISTlv2) * 100
    return p

def giveComment(point):
    commentLIST = ["好的開始是成功的一半！", 
                   "冷靜啊割", 
                   "想他ㄌ吧", 
                   "♪有情的人~別問她♪你還願意嗎♪", 
                   "他好多魚，你好多餘", 
                   "暈船中期，請盡速就醫", 
                   "庫拉皮卡是你", 
                   "您已超速了，請減速慢行", 
                   "在下去的邊緣試探，做好心理準備", 
                   "ㄛ不，他不愛泥，晚安ㄌ"]
    p = 0
    if point//10 > 9:
        p = 9
    else:
        p = point//10
    p = int(p)
    comment = commentLIST[p]
    return comment

#%%分數分成個人
def arrangeTalkLIST(talkLIST, memberLIST):
    '''把talkLIST以人為單位做整理'''
    resultLIST = []
    for i in range(len(memberLIST)):
        resultLIST.append([])
        for j in range(len(talkLIST)):
            if talkLIST[j][1] == memberLIST[i]:
                resultLIST[i].append(talkLIST[j])
    return resultLIST
    
def member2LIST(talkLIST):
    '''生成對話中所有人的list'''
    memberLIST = []
    memberLIST.append(talkLIST[0][1])
    for i in range(len(talkLIST)):
        if findMembers(talkLIST[i][1], memberLIST) == False:
            memberLIST.append(talkLIST[i][1])
    return memberLIST

def findMembers(member, memberLIST):
    try:
        memberLIST.index(member)
        return True
    except ValueError:
        return False
#%%
if __name__ == "__main__":
    
    inputSTR = txtReader("veryseasick.txt")
    print(inputSTR)
    
    inputLIST = easy2LIST(inputSTR)
    #pprint(inputLIST)
    
    inputLIST = talk2LIST(inputLIST)

    talkLIST = talk2LIST2(inputLIST)
    pprint(talkLIST)
    
    articut = articutLogIn("account.info")
    talkLISTlv2 = talk2CutList(talkLIST, articut)
    pprint(talkLISTlv2)
    
    '''全部人的分數'''
    point = countPoint(talkLISTlv2)
    print("all point:", point)
    comment = giveComment(point)
    print(comment)
    
    
    '''個人的分數'''
    memberLIST = member2LIST(talkLISTlv2)
    memberTalkLIST = arrangeTalkLIST(talkLISTlv2, memberLIST)
    for i in range(len(memberLIST)):
        point = countPoint(memberTalkLIST[i])
        comment = giveComment(point)
        print(memberLIST[i] + " point:", point)
        print(comment)
    
    

    