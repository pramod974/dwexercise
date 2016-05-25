Author Pramodkumar

Merkle Tree Implementation

This program checks the difference in the 2 files by breaking them into blocks of size 1 MB each. So if to append some characters in the file(beginning or at the middle) then the characters going into the file blocks will change and all the blocks will differ from the original so the program will compute all the blocks as different. To get the correct implementation we should add and delete the same number of chracters in the file, so as to preserve the ordering of characters going into the file blocks.

File MerkleTree.py:
	* Contains basic implementation of Merkle Tree
	* Contain implementation of finding difference between the file blocks of the given input files

run using :
"python MerkleTree.py"

Suppose the files to be tested are f1.txt(original/correct file) and f2.txt (file to be checked for corruption in file blocks)
Type the follwing lines to execute the program as the command above

	obj = pr.Diff('file1.txt', 'file2.txt')

	obj.make_trees()


You can change the File Names in the above line to test a different file in "__main__" block.

**************************************************************************************************************

You alternatively can also use Runmerkel to get the Output.txt