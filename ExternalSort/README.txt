Author Pramodkumar

External Sort Implementation

* Used the following command to Generate text files containing strings:

ruby -e 'a=STDIN.readlines;10000000.times do;b=[];4.times do; b << a[rand(a.size)].chomp end; puts b.join(" "); end' < /usr/share/dict/words > file4.txt


The file
externalSort.py - Python has implementation of external sort


Put all the files you wanna sort to a input directory (say Input).
Suppose the input directory name in "Input" and you want to produce a sorted file by name "output.txt"

Example :
		import externalSort as es
		ob = es.sort('Input','out.txt')
		ob.external_sort()

* To rotate a sorted list type

		ob.rotate()


* To get the minimum element in the sorted rotated file type the command

		ob.find_min()
Example :
You can Invoke useSort.py to test it