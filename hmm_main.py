#!/usr/bin/python

#Dilara Kekulluoglu 2014700171

import sys
import os
import re
import math
import codecs
import pos_tagger
import evaluate

tr_f = sys.argv[1]
tg = sys.argv[2]
te_f = sys.argv[3]
output = sys.argv[4]
g_f = sys.argv[5]
def main(train_file = tr_f,tag=tg,test_file=te_f,out_file = output,gold_file = g_f):
	

	pos_tagger.main(train_file,tag,test_file)
	evaluate.main(out_file,tag,gold_file)
	
	
	
	

if __name__ == '__main__':
  main()