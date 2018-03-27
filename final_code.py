#! /usr/bin/python3
# -*- coding: utf-8 -*-

import nltk
import os, sys

from nltk.corpus import stopwords
import numpy as np
import collections
from pred_opinion import adjective
lemma = nltk.WordNetLemmatizer()
cachedstopwords = stopwords.words("english")



def mult_token(review):
	final = []
	sent_text = nltk.sent_tokenize(review)
	#print sent_text
	for sentence in sent_text:
		tokenized_text = nltk.word_tokenize(sentence)
		tagged = nltk.pos_tag(tokenized_text)
		#print(tagged)
		final.append(tagged)
		#print(final)
	return final

def transaction(arr):
	tmp = []
	bit = []
	h, w, n = 0, 0, len(arr)
	for i in range(0, n):
		bit.append(0)
		m, w = len(arr[i]), 0
		for j in range(0, m):
			if arr[i][j][1] == "NN" or arr[i][j][1] == "NNS" or arr[i][j][1] == "NNP" or arr[i][j][1] == "NNPS":
				if w == 0:
					tmp.append([])
				tmp[h].append(str(arr[i][j][0]))
				w += 1
				bit[i] += 1
		if w >= 1:
			h += 1
	return tmp, bit

def cntadj(arr):
	tmp = []
	bit = []
	h, w, n = 0, 0, len(arr)
	for i in range(0, n):
		bit.append(0)
		m, w = len(arr[i]), 0
		for j in range(0, m):
			if arr[i][j][1] == "JJ" or arr[i][j][1] == "JJS" or arr[i][j][1] == "JJR":
				if w == 0:
					tmp.append([])
				tmp[h].append(str(arr[i][j][0]))
				w += 1
				bit[i] += 1
		if w >= 1:
			h += 1
	return tmp, bit

def rem_stop_word(arr, bit):
	tmp = []
	h, w, fl, n = 0, 0, 0, len(arr)
	for i in range(0, n):
		while bit[fl] == 0:
			fl += 1
		m, w = len(arr[i]), 0
		for j in range(0, m):
			if arr[i][j] not in cachedstopwords:
				if w == 0:
					tmp.append([])
				tmp[h].append(str(arr[i][j]))
				w += 1
			else:
				bit[fl] -= 1
		if w >= 1:
			h += 1
		fl += 1
	return tmp, bit

def lemm(arr):
	n = len(arr)
	for i in range(0, n):
		m = len(arr[i])
		for j in range(0, m):
			arr[i][j] = lemma.lemmatize(arr[i][j])
	return arr

def convert1d(arr):
    ll = len(transaction)
    tmp = []
    for i in range(0, ll):
        rr = len(transaction[i])
        for j in range(0, rr):
            tmp.append(transaction[i][j])
    return tmp

def freqone(seed, arr):
    tmp = []
    for var in seed:
        if arr.count(var) >= support:
            tmp.append(var)
    return tmp

def createdct(arr):
    dct = {}
    dct2 = {}
    ll = len(arr)
    for i in range(ll):
        dct[arr[i]] = i+1
        dct2[i+1] = arr[i]
    return dct, dct2

def crtscndmat(i):
    mat = [[0 for x in range(i+1)] for y in range(i+1)]
    return mat

def freq2(rev, dct, dct2):
    tmp, ll = [], len(rev)
    ans = []
    ans.append([])
    pair = crtscndmat(len(dct))
    for i in range(ll):
        rr = len(rev[i])
        for j in range(rr):
            if rev[i][j] in dct:
                tmp.append(dct[rev[i][j]])
        tt = len(tmp)
        for y in range(tt-1):
            for z in range(y+1, tt):
                pair[tmp[y]][tmp[z]] += 1
                pair[tmp[z]][tmp[y]] += 1
        del tmp[:]
    ll, num = len(dct)+1, 0
    for i in range(1, ll):
        for j in range(i+1, ll):
            if pair[i][j] >= support:
                ans[num].append((dct2[i],dct2[j]))
                ans.append([])
                num += 1
    return ans

def usefuladj(feature, featcnt, adject, adjcnt, frstfreq):
    ll, rr, j = len(featcnt), len(feature), 0
    tmp = [0 for x in range(ll)]
    for i in range(rr):
        fl = 0
        for f in feature[i]:
            if f in frstfreq:
                fl = 1
                break
        if fl == 1:
            while featcnt[j] == 0:
                j += 1
            tmp[j] = fl
            j += 1
    for i in range(ll):
        tmp[i] = tmp[i]*adjcnt[i]
    #print(adjcnt)
    #print(tmp)
    return tmp

def foreachfeat(feature, featcnt, frstfreq):
    tmp = []
    tmp.append([])
    num, j = 0, 0
    rr = len(feature)
    for i in range(rr):
        fl = 0
        while featcnt[j] == 0:
            tmp.append([])
            num += 1
            j += 1
        for f in feature[i]:
            if f in frstfreq:
                tmp[num].append(f)
                fl = 1
        tmp.append([])
        num += 1
        if fl == 0:
            tmp.append([])
            num += 1
        j += 1
    if len(tmp[len(tmp)-1]) == 0:
        del tmp[len(tmp)-1]
    return tmp


#############################################
'''TOKENIZATION AND NOUNS'''
#review = "thiss a sent tokenize test. this is sent two. is this sent three? sent 4 is cool and picture is bad! Now its your turn."
#review = "Superb moto Builed Moto g5s plus which I loved before buying now too it's just like what I wanted, processing is gud no heating things gone up till now using it from 8 days."
review="If your are going to buy this laptop, think twice before buying it. I have been using this laptop for 2 years. these things i like about it and don't pros- U get good specs at this price. Keyboard back light is amazing. Your batter gonna perform awesome for a year may be ( depends on usage - i used to write code and graphic processing. Cons- Worst screen -- It feels like i'm looking at 1997 tv screens after 3-4 months later i can clearly see screen blinks red and white lines going up and down - twice i have changed screen - screen cost around 5k to 6k .Heating issues. The palm rest around touch pad catches durt so quickly so quickly that u have to keep a cloth with u all the time. Over all Build quality is sooo poor .. really buy acer or asus or macbook their build quality is just amazing."
review=review.lower()
pos_review = mult_token(review)

feature, featcnt = transaction(pos_review)
feature, featcnt = rem_stop_word(feature, featcnt)
#feature = lemm(feature)

#############################################

#############################################
'''PROCESS FOR ADJECTIVES'''
adject, adjcnt = cntadj(pos_review)
adject, adjcnt = rem_stop_word(adject, adjcnt)
#adject = lemm(adject)
# print "Adjectives : ",
# print adject, adjcnt

seed_file="seed_list.csv"

sentence_orient = []
adjective_dic = {}

for row in adject:
	cl=adjective(seed_file,row)
	cl.file_read()
	[pos,neg, adjmap]=cl.orientation()
	sentence_orient.append((pos, neg))
	cl.file_write()
	adjective_dic.update( adjmap )
#############################################

#############################################
'''APRIORI ALGO'''
transaction = feature
support = int((0.1)*len(feature))
tmp = convert1d(transaction)
lstunq = set(tmp)
frstfreq = freqone(lstunq, tmp)
dct, dct2 =  createdct(frstfreq)
scndfreq = freq2(transaction, dct, dct2)

# print "first frequent : ", frstfreq
# print "second frequent : ",scndfreq
# print scndfreq
opin = usefuladj(feature, featcnt, adject, adjcnt, frstfreq)
feature_list  = foreachfeat(feature, featcnt, frstfreq)
# print "frture list : ", feature_list
#print adjmap

##############################################
'''
print(str(review))			#review entered by user
print(str(pos_review))		#par of speech(pos) tagging for the review for each word of each sentence
print(str(feature))			#obtaining the nouns for each sentence if it contains them
print(str(featcnt))			#obtaining frequency of nouns for each sentence

print(str(adject))			#obtaining the nouns for each sentence if it contains them
print(str(adjcnt))			#obtaining frequency of adjectives for each sentence

print (transaction)   #nouns for aech sentence
print(dct)            #dictionary (frequentfeature:key(1,2,..))
print(dct2)           #dictionary (key(1,2,..):frequentfeature)
print(frstfreq)       #list of frequent features
print(scndfreq)       #list of frequent features (2 words)
'''
#Sentence Orientation

local_ft_orientaion = {}
backl = 2
frontl = 6
#print "adjective_dic : ",  adjective_dic
stopw = ['and', ',', '.', 'or', '?', 'but']



for sentence, features in zip(pos_review, feature_list):
	sentence = [i[0] for i in sentence]
	#print sentence
	#print features
	for feature in features:
		#print sentence

		ft_index = sentence.index(feature)

		#go backwards 2 units or stop at stopw
		for i in range(1,backl+1):

			ind = ft_index-i

			if(ind < 0):
				break


			word = sentence[ind]
			if word in stopw:
				break

			if word in adjective_dic.keys():
				local_ft_orientaion[ feature ] = adjective_dic[word]
				break


		if feature in local_ft_orientaion:
			continue

		local_ft_orientaion[feature] = 0
		#go forward 6 units , or stop at stopw

		for i in range(1, frontl+1):

			ind = ft_index+i

			if(ind >= len(sentence)):
				break

			word = sentence[ind]
			if word in stopw:
				break

			if word in adjective_dic.keys():
				local_ft_orientaion[ feature ] = adjective_dic[word]
				break


print "feature list : ", feature_list
for i in local_ft_orientaion.keys():
	if(local_ft_orientaion[i]!=0):
		print i, local_ft_orientaion[i]

# print "feature orientation : ", local_ft_orientaion

sentence_orientation = []

for index, op in enumerate(sentence_orient):
	net_orientation = (op[0]-op[1])
	if(net_orientation < 0):
		sentence_orientation.append(-1)
	elif(net_orientation > 0):
		sentence_orientation.append(1)
	else:
		for feature in feature_list[index]:
			# if feature in local_ft_orientaion:
			net_orientation += local_ft_orientaion[feature]
		if(net_orientation < 0):
			sentence_orientation.append(-1)
		elif(net_orientation > 0):
			sentence_orientation.append(1)
		else:
			sentence_orientation.append(0)


print "sentence_orientation : ", sentence_orientation

orientationSum = sum(sentence_orientation)
if orientationSum > 0:
	review_orientation = 1
elif orientationSum < 0:
	review_orientation = -1
else:
	review_orientation = 0

print "Review Orientation : ", review_orientation
