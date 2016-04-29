# hmm_pos_tagger
cmpe 561 hw #2

This code is written in Python 2.7

Download and put .py files in the same folder.

To use the program user need to call the hmm\_main.py with five arguments; path to train file, tagset name,path to blind test file, output file and path to gold test file. 

The output file created by the program is in the format "output"+tagset_name+".txt" so for the --cpostag it is output--cpostag.txt

Sample = 

python hmm\_main.py \\
.\metu\_sabanci\_cmpe\_561\train\turkish\_metu\_sabanci\_train.conll --cpostag \\
.\metu\_sabanci\_cmpe\_561\test\turkish\_metu\_sabanci\_test\_blind.conll output--cpostag.txt \\
.\metu\_sabanci\_cmpe\_561\test\turkish\_metu\_sabanci\_test\_gold.conll  \\



After the program ends we have  result files one for each run. You can find results of my run of the program on the validation dataset in the repository.

Refer to report of the assignment for the further info.
