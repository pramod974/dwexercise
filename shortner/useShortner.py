__author__ = 'pramodkumar'
from collections import Counter
import os
import shortner
#Example 1
originalURL,shortURL= shortner.shortenfile(os.getcwd()+"/urls.txt")
print "The shortened URL from files"
print "Total URL processed "
for k,v in zip(originalURL,shortURL):
    print k,"   ",v
print "Output Example 1 "
print "Total URL processed ",len(originalURL)


#Example 2
print "Output Example 2 "
print shortner.shorten("https://www.google.co.in/search?q=pyspark+external+sort&oq=pyspark+external+sort+&aqs=chrome..69i57.10233j0j7&sourceid=chrome&ie=UTF-8")


# Test for Uniqueness
# cs=Counter(shortURL)
# for k,v in cs.iteritems():
#     if v >1:
#         print k
