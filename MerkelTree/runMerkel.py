__author__ = 'pramodkumar'
import sys
import MerkleTree as pr
import os
with open("Output.txt","w") as f:
    sys.stdout=f
    obj = pr.Diff(os.getcwd()+'/f1.txt', os.getcwd()+'/f3.txt')
    obj.make_trees()

