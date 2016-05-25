import math
import hashlib
#Class for Merkle Tree Implementation
class merkle(object):
    # constructor for the class merkle	
    def __init__(self,fpath):
	# List to store merkle tree 
        self.tree = []
	#List to store the blocks data
	self.treedata = []
	# Variable to store the filepath
	self.fpath = fpath
	# Variable to store the number of chunks the file is broken into 
	self.num_piece = 0
	# Variable to get n such that 2^n  > self.num_piece. The idea is to 
	# create a binary tree with leaf nodes linking to the chunks. Suppose
	# the chunk size is 12 so next number which is > 12 and also a power
	# of 2 is 16, giving us n = 4. So we create a biary tree with 16
	# leaves. So total number of nodes in the tree will be 2^(n+1) -1
	# for simplicity we will be storing "n+1" rather than "n"
	self.next_pow = 0
	# List to store chunks of the text file
	self.file_pieces = []
	# Dictionary to link file chunks to leaves
	self.link = {}

    # function to make chunks of the input file and store these chunks in 
    # "file_pieces" list
    def make_file_pieces(self):
	with open(self.fpath, 'rb') as fin:
	    # Make chunks of size 1MB each
            chunks = list(iter(lambda: fin.read(1000*1024), ''))
	
	self.num_piece = len(chunks)
	for item in chunks:
	    self.file_pieces.append(item)

    # function to initialize the merkle tree
    def make_tree(self):
	self.next_pow = math.ceil(math.log(self.num_piece,2)) + 1
	tree_range = int(math.pow(2,self.next_pow) -1)
        for i in xrange(0,tree_range):
	    self.tree.append(i)
	    self.treedata.append(i)

    # Function to link the file pieces to leaf nodes of merkle tree
    def link_piece_to_leaves(self):
        leaves = self.tree[len(self.tree)/2 : ]
	
	len_diff = len(self.tree) - len(self.file_pieces)
	for item in xrange(0,len_diff):
	    self.file_pieces.append(str(0))

	for a,b in zip(leaves, self.file_pieces):	
	    self.link[a] = b

    # Function to create hashes and build the complete merkle tree
    def make_hash(self):
	for key, val in self.link.items():
	    h = hashlib.sha1(val).hexdigest()
	    self.tree[key] = h
	    self.treedata[key] = val
	for i in xrange(len(self.tree)/2 -1, -1,-1):
	    l = self.left_child(i)
	    r = self.right_child(i)
	    new_str = self.tree[l] + self.tree[r]
	    h = hashlib.sha1(new_str).hexdigest()
	    self.tree[i] = h

	# return self.tree
	    
    # Function to find sibling of a node
    def find_sibling(self,i):
	if i%2 == 0:
	    return i - 1
	else:
	    return i + 1

    # Function to find uncle(parent's sibling) of a node
    def find_uncle(self,i):
	parent = self.find_parent(i)
	uncle = self.find_sibling(parent)
	return uncle

    # Function to find parent of a node
    def find_parent(self,i):
	return int(math.floor((i-1)/2));

    # Function to find left child of a parent node (non-leaf node)
    def left_child(self,i):
	return 2*i + 1

    # Function to find right child of a parent node (non-leaf node)
    def right_child(self,i):
	return 2*i + 2

    # Function to print the merkle tree
    def print_tree(self):
	print self.tree

    # Wrapper function to do all processing required in order to make 
    # merkle hash tree
    def execute(self):
	self.make_file_pieces()
	self.make_tree()
	self.link_piece_to_leaves()
	return self.make_hash()

# Class to find difference between 2 input files
class Diff(object):
    # Constructor for the class Diff
    def __init__(self,fpath1,fpath2):
        self.fpath1 = fpath1
	self.fpath2 = fpath2
	self.src = []
	self.dest = []
	self.valid=1
    # Make the merkel tree out of the given input files
    # and call "find_diff" method to find the difference
    # between the two given files
    def make_trees(self):
	ob1 = merkle(self.fpath1)
	ob2 = merkle(self.fpath2)
	self.src = ob1.execute()
	self.dest = ob2.execute()
	if ob1.num_piece>ob2.num_piece:
		self.find_diff(ob1,ob2)
	else:
		self.find_diff(ob2,ob1)

    # Function to check every file block of target file and see
    # if the block is similar to the source file or not
    def find_diff(self,ob1,ob2):
	start = len(ob2.tree)/2
	end = ob2.num_piece
	if ob1.num_piece!=ob2.num_piece:
		print "File size unequal Both are Different \n !"
	for i in xrange(start, start + end):
	    self.check_leaf(ob2,i,ob1)

    # Function implementing the algo to build the root hash from a given leaf node
    # The file block under inspection is first hashed. The hash of sibling block is
    # requested from the original file. The two hashes are concatenated and hashed again (1)
    # The block also ask for hash of its uncle node(parent's sibling) (2). (1) & (2) are hashed
    # and this process is repeated until the root is reached. Then we compare the root hash of the
    # target block with the root hash of the source file. If they are the same it means the target
    # file block is same as that of the original file block, else they are different.
    def check_leaf(self,ob2, index, ob1):
	tmpindex = index
	c1 = ob2.tree[index]
	c2 = ob1.tree[ob1.find_sibling(index)]
	c1data=ob2.treedata[index]
	c2data=ob1.treedata[ob1.find_sibling(index)]
	while int(tmpindex) != 0:
	    if tmpindex % 2 == 0:
	        new_str = c2 + c1
	    else:
		new_str = c1 + c2
	    h = hashlib.sha1(new_str).hexdigest()
	    c1 = h
	    c2 = ob1.tree[ob1.find_uncle(tmpindex)]
	    tmpindex = ob1.find_parent(tmpindex)

	if c1 != ob1.tree[0]:
	    print "Difference at block " + str(index -len(ob2.tree)/2) + "\n"
	    # print c1data
	    # print "***********************************"
	    # print c2data
	    # print "___________________________________"
	    self.valid=0
