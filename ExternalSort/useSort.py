import os
import externalSort as pr
ob = pr.sort(os.getcwd()+'/Input',os.getcwd()+'/out.txt')
ob.external_sort()
ob.rotate()
ob.find_min()