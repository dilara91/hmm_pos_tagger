#!/usr/bin/python

#Dilara Kekulluoglu 2014700171

import sys
import os
import re
import math
import codecs
import shutil

output_file = sys.argv[1]
tagStyle = sys.argv[2]
gold_st = sys.argv[3]

def main(output = output_file,tagS = tagStyle,gold = gold_st):

	if tagStyle =='--cpostag':
		format = 3
	else:
		format = 4

	dictionary =[]
	dictionary_file = codecs.open('dictionary.txt','r',encoding='utf8')
	for line in dictionary_file:
		dictionary.append(line.strip())
	dictionary_file.close()

	predictions = []
	knownpredictions = []
	unknownpredictions = []
	with codecs.open(output,'r',encoding='utf8') as my_file:
		for line in my_file:
			if line=='\n':
				continue
			word = line.strip().split('|')[0]
			if word in dictionary:
				knownpredictions.append(line.strip().split('|')[1])
			else:
				unknownpredictions.append(line.strip().split('|')[1])

			predictions.append(line.strip().split('|')[1])

	actual = []
	knownactual = []
	unknownactual = []
	with codecs.open(gold,'r',encoding='utf8') as gold_file:
		for line in gold_file:
			if line == '\n':
				continue
			word = line.split('\t')[1]
			if word == '_':
				continue

			if word in dictionary:
				knownactual.append(line.split('\t')[format])
			else:
				unknownactual.append(line.split('\t')[format])

			actual.append(line.split('\t')[format])


	tags = create_tags(tagS)

	contingency = [[0 for x in range(len(tags))] for x in range(len(tags))]

	hit = 0
	miss = 0
	for actual, predicted in zip(actual, predictions):
		if actual == predicted:
			hit = hit + 1
		else:
			miss = miss + 1
		actual_index = tags[actual]
		predicted_index = tags[predicted]
		contingency[actual_index][predicted_index] = contingency[actual_index][predicted_index] + 1

	knownhit = 0
	knownmiss = 0
	for actual, predicted in zip(knownactual, knownpredictions):
		if actual == predicted:
			knownhit = knownhit + 1
		else:
			knownmiss = knownmiss + 1

	unknownhit = 0
	unknownmiss = 0
	for actual, predicted in zip(unknownactual, unknownpredictions):
		if actual == predicted:
			unknownhit = unknownhit + 1
		else:
			unknownmiss = unknownmiss + 1

	result_file = codecs.open('result'+tagS+'.txt','w+',encoding='utf8')
	for i in range(len(tags)):
		result_file.write(str(contingency[i]))
		result_file.write('\n')



	macro_averaged_precision = 0
	macro_averaged_recall = 0

	total_tp = 0  #tp --> true positive
	total_fp = 0  #fp --> false positive
	total_fn = 0  #fn --> false negative

	for tag,index in tags.items():

		tp = contingency[index][index]
		fp = 0
		for i in range(len(tags)):
			fp = fp + contingency[i][index]
		fp = fp - tp

		fn = 0
		for i in range(len(tags)):
			fn = fn + contingency[index][i]
		fn = fn - tp

		total_tp = total_tp + tp
		total_fp = total_fp +fp
		total_fn = total_fn + fn
		if tp + fp != 0:
			precision = float(tp) / (tp + fp)
		else:					#when the classifier does not assign a class to
			precision = 1		#any file we have zero division so we take it as 1.
		if tp+fn != 0:
			recall = float(tp) / (tp + fn)
		else:
			recall = 0			#same with the case that there are no files in the train set for that class. This is not a problem we face with this dataset.
		result_file.write(tag+' precision : '+str(precision)+' recall : '+str(recall)+'\n')
		macro_averaged_precision =  macro_averaged_precision + precision
		macro_averaged_recall = macro_averaged_recall + recall

	result_file.write('\n')
	macro_averaged_precision = float(macro_averaged_precision) / len(tags)
	macro_averaged_recall = float(macro_averaged_recall) / len(tags)
	macro_f1_measure = 2*macro_averaged_precision*macro_averaged_recall / (macro_averaged_precision + macro_averaged_recall)
	result_file.write('macro averaged precision '+str(macro_averaged_precision)+'\n')
	result_file.write('macro averaged recall '+str(macro_averaged_recall)+'\n')
	result_file.write('macro f1 measure '+str(macro_f1_measure)+'\n\n')

	micro_averaged_precision = float(total_tp) / (total_tp + total_fp)
	micro_averaged_recall = float(total_tp) / (total_tp + total_fn)
	micro_f1_measure = 2*micro_averaged_precision*micro_averaged_recall / (micro_averaged_precision + micro_averaged_recall)
	result_file.write('micro averaged precision '+str(micro_averaged_precision)+'\n')
	result_file.write('micro averaged recall '+str(micro_averaged_recall)+'\n')
	result_file.write('micro f1 measure '+str(micro_f1_measure)+'\n')

	result_file.write('\n')
	result_file.write('accuracy : '+str((float(hit)/(hit+miss)))+'\n')
	result_file.write('accuracy known : '+str((float(knownhit)/(knownhit+knownmiss)))+'\n')
	result_file.write('accuracy unknown : '+str((float(unknownhit)/(unknownhit+unknownmiss)))+'\n')
	result_file.close()

	with codecs.open('result'+tagS+'.txt', "r") as f:
		shutil.copyfileobj(f, sys.stdout)

def unique(seq):

   seen = {}
   count = 0
   for item in seq:
       if item in seen:
       	   continue
       seen[item] = count
       count = count+1

   return seen

def create_tags(tagS):
	tags = {}
	count = 0
	with codecs.open('tags'+tagS+'.txt','r',encoding='utf8') as tag_file:
		for line in tag_file:
			if line=='\n':
				continue
			tags[line.strip()] = count
			count = count + 1

	return tags









if __name__ == '__main__':
  main()
