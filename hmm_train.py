#!/usr/bin/python

#Dilara Kekulluoglu 2014700171

import sys
import os
import re
import math
import codecs

fname = sys.argv[1]
tStyle = sys.argv[2]

def main(filename = fname,tagStyle = tStyle):
	if tagStyle =='--cpostag':
		format = 3
	else:
		format = 4
	
	result = {}
	words = []
	with codecs.open(filename,'r',encoding='utf8') as f:
		transition = {}
		emission = {}
		tagCount = {}
		tag = '<START>'
		for line in f:
			
			if line == '\n':
				newTag = '<END>'
				trans = tag+' '+newTag
				if trans not in transition:
					transition[trans] = 1
				else:
					transition[trans] = transition[trans] + 1
				tag = '<START>'
				continue
			else:
				word = line.split('\t')[1]
			
			if word == '_':
				continue
			
			
			newTag = line.split('\t')[format]
			trans = tag+' '+newTag
			emiss = tag+' '+word
			words.append(word)
			if trans not in transition:
				transition[trans] = 1
			else:
				transition[trans] = transition[trans] + 1
			
			if emiss not in emission:
				emission[emiss] = 1
			else:
				emission[emiss] = emission[emiss] + 1
			
			if newTag not in tagCount:
				tagCount[newTag] = 1
			else:
				tagCount[newTag] = tagCount[newTag] + 1
			
			tag = newTag
			
			
			
	
	result['tr'] = transition
	result['e'] = emission
	result['tag'] = tagCount
	
	create_tag_file(tagCount,tagStyle)
	create_dict(words)
	
	return result
			
		
	
def create_tag_file(tagCount,tagStyle):
	result_file = codecs.open('tags'+tagStyle+'.txt','a+',encoding='utf8')
	for tag in tagCount.keys():
		result_file.write(tag)
		result_file.write('\n')
	result_file.close()
	
def create_dict(words):
	dictionary = codecs.open('dictionary.txt','a+',encoding='utf8')
	for word in words:
		dictionary.write(word)
		dictionary.write('\n')
	dictionary.close()
	
	
	
	

if __name__ == '__main__':
  main()