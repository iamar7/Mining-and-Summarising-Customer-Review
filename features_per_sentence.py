#! /usr/bin/python3
# -*- coding: utf-8 -*-

import nltk
import os, sys
from nltk.corpus import stopwords
import numpy as np
import collections

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



#############################################
'''TOKENIZATION AND NOUNS'''
review = "Great phone. Works like a 4gb phone. Great phone.Works like a 4gb phone.Turbo charging is just crazy."
pos_review = mult_token(review)
feature, featcnt = transaction(pos_review)
feature, featcnt = rem_stop_word(feature, featcnt)
feature = lemm(feature)
#############################################

#############################################
'''PROCESS FOR ADJECTIVES'''
adject, adjcnt = cntadj(pos_review)
adject, adjcnt = rem_stop_word(adject, adjcnt)
adject = lemm(adject)
#############################################

#############################################
'''APRIORI ALGO'''
transaction = feature
support = int((0.4)*len(feature))
tmp = convert1d(transaction)
lstunq = set(tmp)
frstfreq = freqone(lstunq, tmp)
dct, dct2 =  createdct(frstfreq)
scndfreq = freq2(transaction, dct, dct2)

opin = usefuladj(feature, featcnt, adject, adjcnt, frstfreq)

##############################################

#print(str(feature))			#obtaining the nouns for each sentence if it contains them
#print(str(featcnt))			#obtaining frequency of nouns for each sentence
#print(frstfreq)             #list of frequent features
#print(str(pos_review))		#par of speech(pos) tagging for the review for each word of each sentence
#print(str(adject))			#obtaining the nouns for each sentence if it contains them
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
