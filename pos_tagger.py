#!/usr/bin/python

#Dilara Kekulluoglu 2014700171

import sys
import os
import re
import math
import codecs
import hmm_train

trainf = sys.argv[1]
ts = sys.argv[2]
testf = sys.argv[3]
#change here according to the answer mail
#for validation we need tagStyle
def main(train_file = trainf,tagStyle = ts,test_file = testf):
	
	
	
	#r'.\metu_sabanci_cmpe_561\train\turkish_metu_sabanci_train.conll'
	
	
	if tagStyle =='--cpostag':
		format = 3
	else:
		format = 4
	
	trained_hmm = hmm_train.main(train_file,tagStyle)
	transition = trained_hmm['tr']
	emission = trained_hmm['e']
	tags = trained_hmm['tag']
	print 'return from training'
	#test_file = r'.\metu_sabanci_cmpe_561\validation\turkish_metu_sabanci_val.conll'
	
	
	
	predicted_tags = []
	
	
	with codecs.open(test_file,'r',encoding='utf8') as f:
		sentence=[]
	
		for line in f:
			if line=='\n':
				pr = viterbi(sentence,transition,emission,tags)
				predicted_tags.extend(pr)
				output_file(sentence,pr,tagStyle)
				sentence = []				
				continue
			
			word = line.split('\t')[1]
			if word =='_':
				continue
			sentence.append(word)
			
		
		pr = viterbi(sentence,transition,emission,tags)
		predicted_tags.extend(pr)
		output_file(sentence,pr,tagStyle)
			
def output_file(sentence,pr,tagStyle):
	# process Unicode text
	
	filename = 'output'+tagStyle+'.txt'
	with codecs.open(filename,'a+',encoding='utf8') as outf:
		
		for w, t in zip(sentence, pr):
			line = w+'|'+t
			outf.write("%s\n" % line)
		outf.write("\n")




def viterbi(sentence,transition,emission,tags):
	encoding = sys.stdout.encoding
	
	v_m = [[-1 for x in range(len(sentence)+2)] for x in range(len(tags)+2)]
	v_m[0][0] = 0  #start case
	best_edge ={}
	total_word_count = 0
	for t,c in tags.iteritems():
		total_word_count = total_word_count + c
	
	for i in range(1,len(sentence)+1):
		j=1
		for current_tag,current_count in sorted(tags.items()):
			
			k=1
			maxPos = -20*len(sentence)
			maxTag = ''
			if i == 1:
				maxPos = 0
				maxTag = '<START>'
				
			else:
				for past_tag,past_count in sorted(tags.items()):
					trans = past_tag+' '+current_tag
					if trans not in transition:
						p_trans = -20 #minimum value
					else:
						p_trans = math.log(float(transition[trans])/past_count)
				
					pos = v_m[k][i-1] + p_trans
					if pos>maxPos:
						maxPos = pos
						maxTag = past_tag
				
									
					k = k + 1
			
			edge = str(i-1)+' '+current_tag
			best_edge[edge] = maxTag
			#the possibility of this tag for the word
			
			emiss = current_tag+' '+(sentence[i-1])
			
			if emiss not in emission:
				wordPos = float(1)/ (current_count+total_word_count)
			else:
				wordPos = float(emission[emiss]+1) / (current_count+total_word_count)
			#laplace smoothing
			v_m[j][i] = maxPos 	+ math.log(wordPos)		
			j = j + 1
	l = 1
	maxEndPos = -20*len(sentence)
	maxEndTag = ''
	for past_tag,past_count in sorted(tags.items()):
		trans = past_tag+' <END>'
		if trans not in transition:
			p_trans = -20 #minimum value
		else:
			p_trans = math.log(float(transition[trans])/past_count)
				
		pos = v_m[l][-2] + p_trans
		if pos>maxEndPos:
			maxEndPos = pos
			maxEndTag = past_tag
		l = l+1
						
	edge = '<END>'
	best_edge[edge] = maxEndTag
	predicted_tags = []
	predicted_tags.append(maxEndTag)
	
	i = -1
	while i > -1*(len(sentence)):
		new_edge = str(len(sentence)+i)+' '+predicted_tags[-1]
		
		predicted_tags.append(best_edge[new_edge])
		i = i-1
	
	predicted_tags.reverse()
	
	return predicted_tags



if __name__ == '__main__':
  main()